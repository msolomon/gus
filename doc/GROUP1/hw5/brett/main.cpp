#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

using namespace std;

int validate(string s){
  bool validchars = 0;
  for(int i = 0; i < s.length(); i++){
    if(s.at(i) == ' ' || s.at(i) == '_' || 
       ( s.at(i) >= 'A' && s.at(i) <= 'Z') ||
       ( s.at(i) >= 'a' && s.at(i) <= 'z') ||
       ( s.at(i) >= '0' && s.at(i) <= '9') ){
      //White list. Do nothing.
    }
    else{
      cout << s.at(i);
      validchars = 1;
    }
  }
  if(validchars == 1){
    cout << " are invalid characters." << endl;
    return 0;
  }
  if(s.length() < 1 ){
    cout << "ERROR: String is too short." << endl;
    return 0;
  }
  if(s.length() > 15 ){
    cout << "ERROR: String is too long." << endl;
    return 0;
  }
  cout << "SUCCESS!" << endl;
  return 1;
}

int test_usernames(string s){
  ifstream file;
  string line;
  string line2;
  file.open(s.c_str());
  if(!file.is_open()){
    cout << "File " << s << " does not exist." << endl;
    return 1;
  }
  getline (file,line);
  getline (file,line2);
  validate(line);
  validate(line2);
  while ( file.good() ){
    cout << endl;
    cout << "Username: " << line << endl;
    cout << "Password: " << line2 << endl;
    validate(line);
    validate(line2);
    getline (file,line);
    getline (file,line2);
  }
  return 0;
}

int test_usersettings(string s){
  ifstream file;
  string line;
  file.open(s.c_str());
  if(!file.is_open()){
    cout << "File " << s << " does not exist." << endl;
    return 1;
  }
  while(file.good() ){
    getline(file, line);
    if(line != ""){
      stringstream str(line); //Very easy parsing.
      str >> line;
      cout << "User symbol " << line << " has value ";
      str >> line;
      cout << line << endl;
    }
  }
  



  return 0;
}

int main(){
  
  test_usernames( "doesnotexist" );
  test_usernames( "test_user_pass" );
  
  test_usersettings( "doesnotexist" );
  test_usersettings( "test_user_settings" );

  
  




  return 0;
}
