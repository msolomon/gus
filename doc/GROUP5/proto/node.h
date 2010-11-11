#include "gusConf.h"
#include <stdio.h>

using namespace std;

#ifndef NODEH
#define NODEH

class node {
public:
	char *name;
	char *val;
	struct node *next;
 
	node() {
		this->name = NULL;
	        this->val = NULL;
        	this->next = NULL;
	}
 
	//General Node_ methods
	void reinitNode();
	void addNode(char *name, char *val);
	char *getVal(char *name);
	bool isEmpty();

  	//testing methods
  	void print(int i);
  	void printAll();  
};

#endif
