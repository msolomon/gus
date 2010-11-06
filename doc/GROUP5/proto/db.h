#define MAX_BUF_SIZE 256

#include "gusConf.h"

#ifndef GUSDBH
#define GUSDBH

#include <mysql_driver.h>
#include <mysql_connector.h>

class db {
private:

public:
	db() {
		sql::mysql::MySQL_Driver *driver;
		sql::Connection	*con;
		driver = sql::mysql::MySQL_Driver::Instance();
		con = driver->connect("tcp://127.0.0.1:3306", "user", "password");
		delete con;
	};
	bool save();
};

#endif
