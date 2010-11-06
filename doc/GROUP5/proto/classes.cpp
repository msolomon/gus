/* Functions begin with capital letters, variables begin with lower case letters */

#include <string>
#include <iostream>
#include <stdio.h>
#include <fstream>

using namespace std;
class userl;                 // a member of a user list
class groupl;
class user;

class group
{
int number;                   //Reference number for the group
char* name;                   //Name of the group
userl* leader;                //pointer to the head of the group leader list
userl* mod;                   //pointer to the head of the moderator list
userl* member;                //pointer to the head of the member list
groupl* subgroup;             //pointer to the head of the subgroup list
char* webpage;                //linke to the webpage

public:
void PrintAllUsers();
userl* Leader();
userl* Mod();
userl* Member();

char* Webpage();
bool IsInGroup(string who);
bool IsSubGroup(string who);
groupl* SubGroups();
void AddUser(user who);
void AddMod(user who);
void AddLead(user who);
};

class groupl              //a member of a group list
{
groupl* next;
group* Group;
};

class user
{
char* name;                 //the user's name... might like this to be in its own class later
char* password;             //the user's password. need a better mechanism for this
int userID;                 //for referenc purposes
groupl* groups;             //the list of groups the user is in

public:
char* Name();
};

class userl                 // a member of a user list
{
userl* next;
user* who;

public:
userl* Next();
user* Who();
};


//////////////////////////////////////////////////////////////
//////////This is the start of the functions from/////////////
//////////////////////the group class...//////////////////////
//////////////////////////////////////////////////////////////
userl* group::Leader()
{
   return leader;
}

userl* group::Mod()
{
   return mod;
}

userl* group::Member()
{
   return member;
}

void group::PrintAllUsers()
{
   userl* listptr = leader;
   user* who = NULL;
   char* name = NULL;
   cout << "Leaders: " << '\n';
   while(listptr != NULL)
   {
      who = (*listptr).Who();
      name = (*who).Name();
      printf("%s\n", name);
//      cout << name << '\n';
      listptr = (*listptr).Next();
   };
/*
   listptr = mod;
   cout << '\n' << "Moderators: " << '\n';
   while(listptr != '\0')
   {
      cout << (*listptr->who->name) << '\n';
      listptr = listptr->next;
   };

   listptr = member;
   cout << '\n' << "Members: " << '\n';
   while(listptr != '\0')
   {
      cout << (*listptr->who->name) << '\n';
      listptr = listptr->next;
   };
*/
}
userl* userl::Next()
{
   return next;
}

user* userl::Who()
{
   return who;
}

char* user::Name()
{
   return name;
}

/*
char* Leader()
{
}

char* Webpage()
{
}

bool IsInGroup(char* who)
{
}

bool IsSubGroup(char* who)
{
}

groupl* SubGroups()
{
}

void AddUser(user who)
{
}

void AddMod(user who)
{
}

void AddLead(user who)
{
}
*/
/////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////






int main()
{

}
