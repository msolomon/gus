#define MAX_BUF_SIZE 256

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <iostream>

//flex / bison utilities
extern int yyparse();
extern "C" int yywrap(void);
extern FILE *yyin, *yyout;
extern int yylex (void);
extern void yyrestart (FILE *);
extern int nlin;

using namespace std;

#ifndef GUSCONFH
#define GUSCONFH

#define DBTYPE "MYSQL"

#endif
