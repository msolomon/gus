#! /bin/sh

@echo "Building sphinx documentation in _build/html.../"
python makedoc.py
make html

@echo "Building epydoc documentation in epydoc/"
epydoc -n gus -o epydoc --html ../gus/

@echo "Running test suite to generate coverage documentation in covhtml/"
curr=`pwd`
cd ../gus
python manage.py test
cd $curr

