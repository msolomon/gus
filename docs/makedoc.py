#! python
import os
prefix = '../dev/src/src/'
line_prefix = '.. automodule:: '
line_postfix = '\t:members:\n\t:undoc-members:'

dic = {}

for dirpath, dirnames, filenames in os.walk(prefix):
    for f in filenames:
        if dirpath == prefix + 'gus2': continue
        if f[-3:] == '.py':
            p = dirpath[len(prefix)+5:]
            if p not in dic:
                dic[p] = []
            dic[p].append((dirpath,f))

def get_line(dirt):
    dirpath, f = dirt
    return ''.join([
        line_prefix,
        dirpath[len(prefix):].replace('/', '.'),
        '.',
        f[:-3],
        '\n',
        line_postfix,
        '\n'])

default = \
'''
.. Do not edit this document!
.. It is auto-generated from makedoc.py

Welcome to gus's documentation!
===============================

Contents:

.. toctree::
   :maxdepth: 5
%s

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
'''

def ensure(d):
    if not os.path.exists(d):
        os.makedirs(d)

ensure('_modules')
ensure('_build')
ensure('_static')
ensure('_templates')

for p in dic.keys():
    out = []
    out.append(p)
    out.append('\n')
    out.append((len(p)+2)*'=')
    out.append('\n')
    l = sorted(dic[p])
    for line in l:
        out.append('\n')
        out.append(line[1][:-3])
        out.append('\n')
        out.append((len(out[-2])+2)*'-')
        out.append('\n')
        out.append(get_line(line))
    f = open('_modules/%s.rst' % p, 'w')        
    f.write(''.join(out))
    f.close()
mods = sorted(dic.keys())
out = ''.join(['\n   _modules/' + m for m in mods])
f = open('index.rst', 'w')
f.write(default % out)
f.close()


print "Done. Run 'make' to build Sphinx documentation."
