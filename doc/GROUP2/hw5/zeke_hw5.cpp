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
#include <string>
#include "zeke_hw5.h"
using namespace std;

int main()
{
    int done=0;
    BinarySearchTree groupTree;
    string choice, response;
    char groupName[100], userName[30]; 

    while(done == 0)
    {
        cout << "Enter group name: ";
        cin >> groupName;
        cout << "Enter 1 for advisor info or 2 for user info: ";
        cin >> choice;
        if(choice[0] == '1')
            groupTree.DisplayAdvisorInfo(groupTree.rootPtr, groupName);
        else if(choice[0] == '2')
        {
            cout << "Enter user name: ";
            cin >> userName;
            groupTree.DisplayUserInfo(groupTree.rootPtr, groupName, userName);
        }
        else
            cout << "Invalid Option\n";

        while(done == 0)
        {
            cout << "Would you like another listing? (y or n): ";
            cin >> response;
            if(response[0] == 'n')
            {
                done = 1;
                cout << "BYE\n";
            }
            else if(response[0] == 'y')
                break;
            else
                cout << "Invalid Option\n";
        }
    }
}
