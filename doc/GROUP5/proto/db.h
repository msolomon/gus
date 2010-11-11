#define MAX_BUF_SIZE 256

#include "gusConf.h"

#ifndef GUSDBH
#define GUSDBH

#include <driver.h>
#include <connection.h>

class db {
private:
	node *data[MAX_BUF_SIZE]; //database data
	int dataI; //index for data array

public:
	db() {
		dataI = 0;
		//sql::mysql::MySQL_Driver *driver;
		//sql::Connection	*con;
		//driver = sql::mysql::MySQL_Driver::Instance();
		//con = driver->connect("tcp://127.0.0.1:3306", "user", "password");
		//delete con;
	
	};

	bool pushNode(node *); //pushes a node onto the end of this->data
	bool insertHeadNode(char*, char*);
	bool open();
	bool save();

	//troubleshooting / debug methods
	int entries(); //returns how many entries
	void printRawData();

};

#endif
