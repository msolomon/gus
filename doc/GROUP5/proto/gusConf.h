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

//#define DBTYPE "MYSQL"
//#define DBTYPE "LDAP"
#define DBTYPE "FILE"
#define DBFNAME "db/main.gusdb"
#define MAX_BUF_SIZE 256

#include "node.h"
#include "db.h"

#endif
