%{ 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "gusConf.h"
#include <typeinfo>

extern int yylex();
extern int nlin;

//gus data structures
extern db *db1;
node *ntemp = new node; //node temp

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
%token USER GROUP STRING SPACE

%type <sval> USER STRING

%%

database: lines EXIT			{return(0);}
	;

lines: line | line '\n' | line '\n' lines;

line: 	USER STRING attrs		{db1->pushNode(ntemp);
					 db1->insertHeadNode("user", $2); 
					 ntemp = new node;
					}
	| GROUP STRING attrs		{db1->pushNode(ntemp);
					 db1->insertHeadNode("group", $2); 
					 ntemp = new node;
					}

	;

attrs:	attr
	| attr attrs;

attr:	STRING '=' STRING		{ntemp->addNode($1, $3);}
	;

%%

