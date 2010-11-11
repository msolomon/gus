#include "gusConf.h"

db *db1 = new db; //db1 has to be created here for bison. Working on a work around

int main() {

	cout << "GUS Testing Starting" << endl;
	db1->open();
	
	//demonstrating db functions
	db1->printRawData();
	cout << db1->select("cn", "user", "jcamel") << endl;
	cout << db1->select("sn", "user", "cblair") << endl;
	cout << db1->select("member", "group", "group1") << endl;
}
