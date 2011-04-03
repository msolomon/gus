# Copyright (c) 2011, Menno Smits
# Released subject to the New BSD License
# Please see http://en.wikipedia.org/wiki/BSD_licenses

'''
Unit tests for the FetchTokeniser and FetchParser classes
'''

from datetime import datetime
from textwrap import dedent
from imapclient.fixed_offset import FixedOffset
from imapclient.response_parser import parse_response, parse_fetch_response, ParseError
from imapclient.test.util import unittest

#TODO: tokenising tests
#TODO: test invalid dates and times


CRLF = '\r\n'

class TestParseResponse(unittest.TestCase):

    def test_unquoted(self):
        self._test('FOO', 'FOO')
        self._test('F.O:-O_0;', 'F.O:-O_0;')
        self._test(r'\Seen', r'\Seen')

    def test_string(self):
        self._test('"TEST"', 'TEST')

    def test_int(self):
        self._test('45', 45)

    def test_nil(self):
        self._test('NIL', None)

    def test_empty_tuple(self):
        self._test('()', ())

    def test_tuple(self):
        self._test('(123 "foo" GeE)', (123, 'foo', 'GeE'))

    def test_int_and_tuple(self):
        self._test('1 (123 "foo")', (1, (123, 'foo')), wrap=False)

    def test_nested_tuple(self):
        self._test('(123 "foo" ("more" NIL) 66)',
                   (123, "foo", ("more", None), 66))

    def test_deeper_nest_tuple(self):
        self._test('(123 "foo" ((0 1 2) "more" NIL) 66)',
                   (123, "foo", ((0, 1, 2), "more", None), 66))

    def test_juxtatposed_tuples(self):
        # Tuples with no whitespace between them should be returned as
        # a list of tuples
        self._test('(12 "foo")(34 NIL 0)',
                   [(12, "foo"), (34, None, 0)])
        self._test('(12 "foo")(34 NIL 0)(5 66)',
                   [(12, "foo"), (34, None, 0), (5, 66)])
        self._test('((12 "foo")(34 NIL 0) "foo")',
                   ([(12, "foo"), (34, None, 0)], "foo"))
        self._test('((12 "foo")(34 NIL 0)(4 55 6) "foo")',
                   ([(12, "foo"), (34, None, 0), (4, 55, 6)], "foo"))
        self._test('((12 "foo")(34 (NIL 1 2) 0)(4 55 6) "foo")',
                   ([(12, "foo"), (34, (None, 1, 2), 0), (4, 55, 6)], "foo"))
        self._test('(12 "foo")(34 NIL ("a" "b")("c" "d"))',
                   [(12, "foo"), (34, None, [('a', 'b'), ('c', 'd')])])

    def test_complex_mixed(self):
        self._test('((FOO "PLAIN" ("CHARSET" "US-ASCII") NIL NIL "7BIT" 1152 23) '
                   '("TEXT" "PLAIN" ("CHARSET" "US-ASCII" "NAME" "cc.diff") '
                   '"<hi.there>" "foo" "BASE64" 4554 73) "MIXED")',
                   (('FOO', 'PLAIN', ('CHARSET', 'US-ASCII'), None, None, '7BIT', 1152, 23),
                    ('TEXT', 'PLAIN', ('CHARSET', 'US-ASCII', 'NAME', 'cc.diff'),
                    '<hi.there>', 'foo', 'BASE64', 4554, 73), 'MIXED'))

    def test_envelopey(self):
        self._test('(UID 5 ENVELOPE ("internal_date" "subject" '
                   '(("name" NIL "address1" "domain1.com")) '
                   '((NIL NIL "address2" "domain2.com")) '
                   '(("name" NIL "address3" "domain3.com")) '
                   '((NIL NIL "address4" "domain4.com")) '
                   'NIL NIL "<reply-to-id>" "<msg_id>"))',
                   ('UID',
                    5,
                    'ENVELOPE',
                    ('internal_date',
                     'subject',
                     (('name', None, 'address1', 'domain1.com'),),
                     ((None, None, 'address2', 'domain2.com'),),
                     (('name', None, 'address3', 'domain3.com'),),
                     ((None, None, 'address4', 'domain4.com'),),
                     None,
                     None,
                     '<reply-to-id>',
                     '<msg_id>')))

    def test_envelopey_quoted(self):
        self._test('(UID 5 ENVELOPE ("internal_date" "subject with \\"quotes\\"" '
                   '(("name" NIL "address1" "domain1.com")) '
                   '((NIL NIL "address2" "domain2.com")) '
                   '(("name" NIL "address3" "domain3.com")) '
                   '((NIL NIL "address4" "domain4.com")) '
                   'NIL NIL "<reply-to-id>" "<msg_id>"))',
                   ('UID',
                    5,
                    'ENVELOPE',
                    ('internal_date',
                     'subject with "quotes"',
                     (('name', None, 'address1', 'domain1.com'),),
                     ((None, None, 'address2', 'domain2.com'),),
                     (('name', None, 'address3', 'domain3.com'),),
                     ((None, None, 'address4', 'domain4.com'),),
                     None,
                     None,
                     '<reply-to-id>',
                     '<msg_id>')))

    def test_literal(self):
        literal_text = add_crlf(dedent("""\
            012
            abc def XYZ
            """))
        self._test([('{18}', literal_text)], literal_text)


    def test_literal_with_more(self):
        literal_text = add_crlf(dedent("""\
            012
            abc def XYZ
            """))
        response = [('(12 "foo" {18}', literal_text), ")"]
        self._test(response, (12, 'foo', literal_text))


    def test_quoted_specials(self):
        self._test(r'"\"foo bar\""', '"foo bar"')
        self._test(r'"foo \"bar\""', 'foo "bar"')
        self._test(r'"foo\\bar"', r'foo\bar')

    def test_square_brackets(self):
        self._test('foo[bar rrr]', 'foo[bar rrr]')
        self._test('"foo[bar rrr]"', 'foo[bar rrr]')
        self._test('[foo bar]def', '[foo bar]def')
        self._test('(foo [bar rrr])', ('foo', '[bar rrr]'))
        self._test('(foo foo[bar rrr])', ('foo', 'foo[bar rrr]'))

    def test_incomplete_tuple(self):
        self._test_parse_error('abc (1 2', 'Tuple incomplete before "\(1 2"')

    def test_incomplete_juxtaposed_tuples(self):
        self._test_parse_error('(1 2)(3 4',
                               'Juxtaposed tuples incomplete before "\(1 2\)\(3 4"')

    def test_bad_literal(self):
        self._test_parse_error([('{99}', 'abc')],
                               'Expecting literal of size 99, got 3')


    def test_bad_quoting(self):
        self._test_parse_error('"abc next', """No closing '"'""")


    def _test(self, to_parse, expected, wrap=True):
        if wrap:
            # convenience - expected value should be wrapped in another tuple
            expected = (expected,)
        if not isinstance(to_parse, list):
            to_parse = [to_parse]
        output = parse_response(to_parse)
        self.assertSequenceEqual(output, expected)

    def _test_parse_error(self, to_parse, expected_msg):
        if not isinstance(to_parse, list):
            to_parse = [to_parse]
        self.assertRaisesRegexp(ParseError, expected_msg,
                                parse_response, to_parse)


class TestParseFetchResponse(unittest.TestCase):

    def test_basic(self):
        self.assertEquals(parse_fetch_response('4 ()'), {4: {'SEQ': 4}})


    def test_none_special_case(self):
        self.assertEquals(parse_fetch_response([None]), {})


    def test_bad_msgid(self):
        self.assertRaises(ParseError, parse_fetch_response, ['abc ()'])


    def test_bad_data(self):
        self.assertRaises(ParseError, parse_fetch_response, ['2 WHAT'])


    def test_missing_data(self):
        self.assertRaises(ParseError, parse_fetch_response, ['2'])


    def test_simple_pairs(self):
        self.assertEquals(parse_fetch_response(['23 (ABC 123 StUfF "hello")']),
                          {23: {'ABC': 123,
                                'STUFF': 'hello',
                                'SEQ': 23}})


    def test_odd_pairs(self):
        self.assertRaises(ParseError, parse_fetch_response, ['(ONE)'])
        self.assertRaises(ParseError, parse_fetch_response, ['(ONE TWO THREE)'])


    def test_UID(self):
        self.assertEquals(parse_fetch_response(['23 (UID 76)']),
                          {76: {'SEQ': 23}})
        self.assertEquals(parse_fetch_response(['23 (uiD 76)']),
                          {76: {'SEQ': 23}})


    def test_repeated_UID(self):
        self.assertEquals(parse_fetch_response(['23 (UID 76 FOO 123 UID 76 GOO 321)']),
                          {76: {'FOO': 123,
                                'GOO': 321,
                                'SEQ': 23}})
        self.assertEquals(parse_fetch_response(['23 (UID 76 FOO 123', 'UID 76 GOO 321)']),
                          {76: {'FOO': 123,
                                'GOO': 321,
                                'SEQ': 23}})


    def test_bad_UID(self):
        self.assertRaises(ParseError, parse_fetch_response, '(UID X)')
        

    def test_FLAGS(self):
        self.assertEquals(parse_fetch_response(['23 (FLAGS (\Seen Stuff))']),
                          {23: {'SEQ': 23, 'FLAGS': (r'\Seen', 'Stuff')}})


    def test_multiple_messages(self):
        self.assertEquals(parse_fetch_response(
                                    ["2 (FLAGS (Foo Bar)) ",
                                     "7 (FLAGS (Baz Sneeve))"]),
                         {
                            2: {'FLAGS': ('Foo', 'Bar'), 'SEQ': 2},
                            7: {'FLAGS': ('Baz', 'Sneeve'), 'SEQ': 7},
                         })


    def test_literals(self):
        self.assertEquals(parse_fetch_response([('1 (RFC822.TEXT {4}', 'body'),
                                                (' RFC822 {21}', 'Subject: test\r\n\r\nbody'),
                                                ')']),
                          {1: {'RFC822.TEXT': 'body',
                               'RFC822': 'Subject: test\r\n\r\nbody',
                               'SEQ': 1}})


    def test_literals_and_keys_with_square_brackets(self):
        self.assertEquals(parse_fetch_response([('1 (BODY[TEXT] {11}', 'Hi there.\r\n'), ')']),
                          { 1: {'BODY[TEXT]': 'Hi there.\r\n',
                                'SEQ': 1}})


    def test_BODY_HEADER_FIELDS(self):
        header_text = 'Subject: A subject\r\nFrom: Some one <someone@mail.com>\r\n\r\n'
        self.assertEquals(parse_fetch_response(
            [('123 (UID 31710 BODY[HEADER.FIELDS (from subject)] {57}', header_text), ')']),
            { 31710: {'BODY[HEADER.FIELDS (FROM SUBJECT)]': header_text,
                      'SEQ': 123}})


    def test_partial_fetch(self):
        body = '01234567890123456789'
        self.assertEquals(parse_fetch_response(
            [('123 (UID 367 BODY[]<0> {20}', body), ')']),
            { 367: {'BODY[]<0>': body,
                    'SEQ': 123}})
                    

    def test_INTERNALDATE(self):
        def check(date_str, expected_dt):
            output = parse_fetch_response(['3 (INTERNALDATE "%s")' % date_str])
            self.assertEquals(output.keys(), [3])
            self.assertEquals(set(output[3].keys()), set(['INTERNALDATE', 'SEQ']))
            actual_dt = output[3]['INTERNALDATE']
            self.assert_(actual_dt.tzinfo is None)   # Returned date should be in local timezone
            expected_dt = datetime_to_native(expected_dt)
            self.assert_(actual_dt == expected_dt, '%s != %s' % (actual_dt, expected_dt))

        check(' 9-Feb-2007 17:08:08 -0430',
              datetime(2007, 2, 9, 17, 8, 8, 0, FixedOffset(-4*60 - 30)))
 
        check('12-Feb-2007 17:08:08 +0200',
              datetime(2007, 2, 12, 17, 8, 8, 0, FixedOffset(2*60)))
 
        check(' 9-Dec-2007 17:08:08 +0000',
              datetime(2007, 12, 9, 17, 8, 8, 0, FixedOffset(0)))


    def test_mixed_types(self):
        self.assertEquals(parse_fetch_response([('1 (INTERNALDATE " 9-Feb-2007 17:08:08 +0100" RFC822 {21}',
                                                 'Subject: test\r\n\r\nbody'),
                                                ')']),
                          {1: {'INTERNALDATE': datetime_to_native(datetime(2007, 2, 9,
                                                                           17, 8, 8, 0,
                                                                           FixedOffset(60))),
                               'RFC822': 'Subject: test\r\n\r\nbody',
                               'SEQ': 1}})


def add_crlf(text):
    return CRLF.join(text.splitlines()) + CRLF


system_offset = FixedOffset.for_system()
def datetime_to_native(dt):
    return dt.astimezone(system_offset).replace(tzinfo=None)


