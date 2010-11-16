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

        struct GroupNode
        {
            char groupID[80];
            struct Advisor         //advisor is unique to each group
            {
                char name[30];
                char email[30];
                char phone[15];
            };
            User* userPtr;          //pointer to list of users in group
            GroupNode* leftPtr;     //pointers to other groups
            GroupNode* rigtPtr;
        };
        typedef struct GroupNode* GroupNodePtr;


    public:
        Group();                   //constructor
        {
            rootPtr = '\0';
        }


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
            cout << "\nAdvisor: " << treePtr->Advisor.name << endl;
            cout << "Email: " << treePtr->Advisor.email << endl;
            cout << "Phone: " << treePtr->Advisor.phone << "\n\n";
            return 1;
        }

                                                             //traverse tree to find group
        DisplayAdvisorInfo(treePtr->leftPtr, suppliedName);        
        DisplayAdvisorInfo(treePtr->rightPtr, suppliedName);
    }

    return 0;
}


/******************************************************************************************
*                     Print User Info of a given group and given user                     *
******************************************************************************************/
int BinarySearchTree::DisplayUserInfo(GroupNodePtr& treePtr, char* groupName, char* userName)
{
    if(treePtr != NULL)
    {
        if(! strcmp(treePtr->groupID, suppliedName) )             //if group is a match
        {
            UserNodePtr tmpPtr = treePtr->userPtr;      //point to first user of group
            while(tmpPtr != '\0')
            {
               if(! strcmp(tmpPtr->groupID, userName) )         //if user is a match
               {
                   cout << "\nUser: " << userName << endl;
                   cout << "Email: " << tmpPtr->email << endl;
                   cout << "Phone: " << tmpPtr->phone << "\n\n";
               }
            }
            return 1;                  
        }

                                                             //traverse tree to find group
        DisplayUserInfo(treePtr->leftPtr, suppliedName);        
        DisplayUserInfo(treePtr->rightPtr, suppliedName);
    }

    return 1;
}


#endif
