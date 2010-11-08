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
" "		{}
"\n"		{return(yytext[0]);}
":"		{cout << "TS20\n"; return(yytext[0]);}
[^: \n]+	{yylval.sval = strdup(yytext);
		cout << "TS22:" << yytext << "\n"; 
		return(STRING);}
<<EOF>>		{return(EXIT);}
%%

