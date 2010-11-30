#!/bin/sh

#add more files here, no extensions! space delimited
LFILES="usecase_master"

for file in $LFILES; do
	latex $file.tex
	dvips $file.dvi
	ps2pdf $file.ps
done
