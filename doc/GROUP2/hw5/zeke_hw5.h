/**********************************************************************
***********************************************************************
** Zeke Long                                                         **
** CS383 HW5                                                         **
**                                                                   **
**              Header file for zeke_hw5.cpp                         **
***********************************************************************
**********************************************************************/

#ifndef _ZekeHW5_H_
#define _ZekeHW5_H_

#include <iostream>
using namespace std;

class BinarySearchTree
{
    private:
        struct User           
        {
            char name[30];
            char email[30];
            char phone[15];
            User * next;          /* there is a list of users attached 
                                     to each GroupNode */
        };
        typedef struct User* UserNodePtr;

        struct Advisor         //advisor is unique to each group
        {
            char name[30];
            char email[30];
            char phone[15];
        };
        typedef struct Advisor* AdvisorNodePtr;

        struct GroupNode
        {
            char groupID[80];
            AdvisorNodePtr AdvisorPtr;    //points to advisor
            UserNodePtr userPtr;          //pointer to list of users in group
            GroupNode* leftPtr;           //pointers to other groups
            GroupNode* rightPtr;
        };
        typedef struct GroupNode* GroupNodePtr;

    public:
        BinarySearchTree()                   //constructor
        {
            rootPtr = '\0';
        }


        GroupNode* rootPtr;

                             //function prototypes
        int DisplayAdvisorInfo(GroupNodePtr& treePtr, char* suppliedName);       
        int DisplayUserInfo(GroupNodePtr& treePtr, char* suppliedName, char* userName);
};


/******************************************************************************************
*                      Print Advisor Info of a given group                                *
******************************************************************************************/
int BinarySearchTree::DisplayAdvisorInfo(GroupNodePtr& treePtr, char* suppliedName)
{
    if(treePtr != NULL)
    {
        if(! strcmp(treePtr->groupID, suppliedName) )             //if group is a match
        {
            cout << "\nAdvisor: " << treePtr->AdvisorPtr->name << endl;
            cout << "Email: " << treePtr->AdvisorPtr->email << endl;
            cout << "Phone: " << treePtr->AdvisorPtr->phone << "\n\n";
            return 1;
        }

                                                             //traverse tree to find group
        DisplayAdvisorInfo(treePtr->leftPtr, suppliedName);        
        DisplayAdvisorInfo(treePtr->rightPtr, suppliedName);
    }

    cout << "GROUP NOT FOUND\n";
    return 0;
}


/******************************************************************************************
*                     Print User Info of a given group and given user                     *
******************************************************************************************/
int BinarySearchTree::DisplayUserInfo(GroupNodePtr& treePtr, char* suppliedName, 
                                                                            char* userName)
{
    if(treePtr != NULL)
    {
        if(! strcmp(treePtr->groupID, suppliedName) )             //if group is a match
        {
            UserNodePtr tmpPtr = treePtr->userPtr;      //point to first user of group
            while(tmpPtr != '\0')
            {
               if(! strcmp(tmpPtr->name, userName) )         //if user is a match
               {
                   cout << "\nUser: " << userName << endl;
                   cout << "Email: " << tmpPtr->email << endl;
                   cout << "Phone: " << tmpPtr->phone << "\n\n";
                   return 1;
               }
            }
            cout << "USER NOT FOUND\n";
            return 0;                  
        }

                                                             //traverse tree to find group
        DisplayUserInfo(treePtr->leftPtr, suppliedName, userName);        
        DisplayUserInfo(treePtr->rightPtr, suppliedName, userName);
    }

    cout << "GROUP NOT FOUND\n";
    return 0;
}


#endif
