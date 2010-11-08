%{
#include <stdlib.h>
#include "db.tab.h"
#include "gusConf.h"
#include <string.h>

int nlin;

%}

%%
"#".*$	      { /*comment, no op*/ }
"EXIT"        { return(EXIT);}
"quit"        { return(EXIT);}
"bye"         { return(EXIT);}
"\n"          { ++nlin; return(yytext[0]);}
"user"		{return(USER);}
"group"		{return(GROUP);}
"%"		{return(yytext[0]);}
" "		{}
<<EOF>>      	{return(EXIT);}

%%

