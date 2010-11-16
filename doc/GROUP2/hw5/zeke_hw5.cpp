/*************************************************************************
**************************************************************************
** Zeke Long                                                            **
** CS383 HW5                                                            **
**                                                                      **
**  Program to test advisor/user info to make sure GUS displays it      **
**  properly                                                            ** 
**                                                                      **
**************************************************************************
*************************************************************************/

#include <iostream>
#include <string.h>
#include "zeke_hw5.h"
using namespace std;

int main()
{
    int done=0, choice=0;
    BinarySearchTree groupTree;
    char groupName[100], userName[30], response; 

    while(done == 0)
    {
        cout << "Enter group name: ";
        cin >> groupName;
        cout << "\nEnter 1 for advisor info or 2 for user info: ";
        cin >> choice;   
        cout << endl;
        if(choice == 1)
            groupTree.DisplayAdvisorInfo(groupTree.rootPtr, groupName);
        else if(choice == 2)
        {
            cout << "Enter user name: ";
            cin >> userName;
            groupTree.DisplayUserInfo(groupTree.rootPtr, groupName, userName);
        }
        else
            cout << "Invalid Option\n";

        cout << "\nWould you like another listing? (y or n): ";
        cin >> response;
        if(response == 'n')
        {
            done = 1;
            cout << "\n\nBYE\n";
        }
    }
}
