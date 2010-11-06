/*
  Copyright (c) 2008, 2010, Oracle and/or its affiliates. All rights reserved.

  The MySQL Connector/C++ is licensed under the terms of the GPLv2
  <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>, like most
  MySQL Connectors. There are special exceptions to the terms and
  conditions of the GPLv2 as it is applied to this software, see the
  FLOSS License Exception
  <http://www.mysql.com/about/legal/licensing/foss-exception.html>.

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published
  by the Free Software Foundation; version 2 of the License.

  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
  or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
  for more details.

  You should have received a copy of the GNU General Public License along
  with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA
*/

#ifndef __TEST_OUTPUTTER_H_
#define __TEST_OUTPUTTER_H_

#include "../common/ccppTypes.h"

namespace testsuite
{
// TODO: Add listener state passing - verbose/trace/streams
// TODO: Add failed tests list passing

_ABSTRACT class TestOutputter
{
public:

  virtual ~TestOutputter()
  {
  }

  virtual void Header     (const String & text= "") _PURE;

  virtual void SuiteHeader(const String & name
                           , unsigned     first
                           , int          testsInSuite) _PURE;

  virtual void TestPassed(unsigned ordNum
                          , const String & name
                          , const String & comment= "") _PURE;

  virtual void TestFailed(unsigned ordNum
                          , const String & name
                          , const String & comment= "") _PURE;

  virtual void Comment(const String & comment) _PURE;

  virtual void Summary(unsigned testsRun
                       , unsigned testsFailed
                       // a bit TAP-bound... However listener can complete
                       // needed info
                       , std::vector<int> & failedTestsNum) _PURE;

  virtual void SuiteSummary(const String & suiteName
                            , unsigned testsRun
                            , unsigned testsFailed) _PURE;


  // Make string from anything shouldn't be a problem
  virtual void Assert(const String & expected
                      , const String & result
                      , const String & file
                      , int line) _PURE;

  virtual std::ostream & messagesLog()  _PURE;
  virtual std::ostream & errorsLog()    _PURE;
};
}

#endif
