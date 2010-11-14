#include "db.h"

bool db::pushNode(node *ntemp){
	data[this->dataI] = (node*)malloc(sizeof(ntemp));
	data[this->dataI] = ntemp;
	this->dataI++;
	return(true); //no cases for failure yet
}

bool db::insertHeadNode(char *name, char* val) {
	node *ntemp = this->data[this->dataI - 1];
	this->data[this->dataI - 1] = new node;
	this->data[this->dataI - 1]->addNode(name, val);
	this->data[this->dataI - 1]->next = ntemp;
	return(true); //should return a test that all are not NULL	
}

bool db::open() {
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
}

char *db::select(char *field, char *key, char *val) {
	//returns matches, comma delimited if more than one
	//ex. select cn (field) where user (key) equals (val)
	for(int i = 0; i < this->dataI; i++) {
		if(strcmp(this->data[i]->getVal(key), val) == 0
		) {
				return(this->data[i]->getVal(field));
		}
	}
	return("");
}

bool db::save() {
	return(false);
}


//troubleshooting / debug methods
int db::entries() {
	return(this->dataI);
}

void db::printRawData() {
	for(int i = 0; i < this->entries(); i++) {
		cout << i << ":\n";
		this->data[i]->printAll();
	}
}


