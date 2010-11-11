#include "gusConf.h"

db *db1 = new db;;

int main() {

	cout << "GUS Testing Starting" << endl;
	db1->open();
	db1->printRawData();
}
