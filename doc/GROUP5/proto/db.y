%{ 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "gusConf.h"
#include <typeinfo>

// better error reporting
#define YYERROR_VERBOSE

// bison requires that you supply this function
bool yyerror(const char *msg)
{
  	printf("ERROR(PARSER): %s at line %d.\n", msg, nlin + 1);
	return(false);
}

%}

%union {
	double dval;
	int varindex;
        int ival;
        char *sval;
}

%token EXIT 
%token USER GROUP STRING

%type <sval> STRING

%%

database: ts;

ts: USER EXIT;

lines: 	line | line lines;

line: 	expr "\n";

expr: 	USER STRING
	| GROUP STRING
	;

attrs:	attr
	| attr attrs;

attr:	STRING "=" STRING;

%%

