%{
#include <stdlib.h>
#include "db.tab.h"
#include "gusConf.h"
#include <string.h>

int nlin;

%}

%%
"#".*$	      	{ /*comment, no op*/ }
"EXIT"        	{return(EXIT);}
"quit"        	{return(EXIT);}
"bye"         	{return(EXIT);}
"user"		{return(USER);}
"group"		{return(GROUP);}
"\n"		{nlin++; return(yytext[0]);}
"="		{return(yytext[0]);}
" "		{ }
[^= \n]+	{yylval.sval = strdup(yytext);
		return(STRING);}
<<EOF>>		{return(EXIT);}
%%
