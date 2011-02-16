#! /bin/sh

@echo "Building sphinx documentation in _build/html.../"
python makedoc.py
make html

@echo "Building epydoc documentation in epydoc/"
epydoc -n gus -o epydoc --html ../gus/

