#define MAX_BUF_SIZE 256

#include "gusConf.h"

#ifndef GUSDBH
#define GUSDBH

#include <driver.h>
#include <connection.h>

class db {
private:
	node *data; //database data

public:
	db() {
		//sql::mysql::MySQL_Driver *driver;
		//sql::Connection	*con;
		//driver = sql::mysql::MySQL_Driver::Instance();
		//con = driver->connect("tcp://127.0.0.1:3306", "user", "password");
		//delete con;
	
		FILE *dbfp = fopen(DBFNAME,"r"); //database file pointer
		//yyrestart for multiple file parsing
		yyrestart(dbfp); nlin = 0;
		//instead of - yyin = fopen(yyfilename,"r");
		if (yyin == NULL) {
        		cout << "Note: gus db file '" << DBFNAME << "' is not "
				<< "\nreadable, assuming it doesn't exist.\n";
		}
		else if(yyparse() == 1) {
                	//yyparse will report its own error
			exit(1);
		}
		
	};

	bool save();
};

#endif
