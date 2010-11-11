#include "gusConf.h"

//db *db1 = new db; //db1 has to be created here for bison. Working on a work around
extern db *db1;

int main() {

	cout << "GUS Testing Starting" << endl;
	db1->open();
	
	//demonstrating db functions
	db1->printRawData();
	cout << db1->select("cn", "user", "jcamel") << endl;
	cout << db1->select("sn", "user", "cblair") << endl;
	cout << db1->select("member", "group", "group1") << endl;

	//demonstrate group functions
	// before we can do any group stuff, we need it to be put
	// in respective files, i.e. group.h, group.cpp, etc.
	// see other classes like node.h, etc
	//group *g1 = new group("group1");
}
