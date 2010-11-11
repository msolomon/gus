#include "node.h"
#include "string.h"
#include <stdio.h>

void node::reinitNode() {
 	this->name = NULL;
	this->val = NULL;
	this->next = NULL;
}

void node::addNode(char *name, char *val) {
	//if head values are not null, add to last next in list
	if(this->name != NULL && this->val != NULL) {
	        node *pTemp = this;
		while(pTemp->next != NULL) {
			pTemp = pTemp->next;
		}
		node *newNode = new node;
		newNode->name = strdup(name);
		newNode->val = strdup(val);
		newNode->next = NULL;
		pTemp->next = newNode;
	}
	else {
	//else, initialze and add to head
		this->name = strdup(name);
		this->val = strdup(val);
		this->next = NULL;
	}
	//printf("Added node %s : %s\n", pTemp->name, pTemp->val); 
}

char *node::getVal(char *name) { 
        for(node *pTemp = this; ; pTemp = pTemp->next) {
                if(pTemp == NULL) {
                        cout << "NODE_WARNING: list element with name " << name << " is not in the list." << endl;
                        return("");
                }
                else if(strcmp(name, pTemp->name) == 0) {
                        return(pTemp->val);
                }
        }
}

bool node::isEmpty() {
	if(this->name == NULL && this->val == NULL) return(true);
	return(false);
}

//testing methods
void node::print(int i ) {
        node *pTemp = this;
        for(int x = 0; x <= i; x++, pTemp = pTemp->next) {
                if(pTemp == NULL) {
                        cout << "NODE_WARNING: index of " << i << " is beyond the size of the list." << endl;
                        return;
                }
		else if(x == i) {			
		        cout << "node element[" << x << "] - " << pTemp->name << " : " << pTemp->val << endl;
			return;
		}	
        }
}

void node::printAll() {
        node *pTemp = this;
        if(pTemp == NULL) {
                cout << "node list is empty" << endl;
                return;
        }
        for(; pTemp != NULL; pTemp = pTemp->next) {
                cout << "node list name = val : " << pTemp->name << " = " << pTemp->val << endl;
        }

}
