package world;

import java.util.regex.*;

public class functions {
		
		//Grab a string and use regular expressions to make sure it is valid
		public static boolean isUserValid(String s, int debug){
			//variables
			String result = null;
			boolean output=false; //initiate to false, rather be wrong in a bad situation then right in a bad one
			//regular expression generation
			Pattern acceptable = Pattern.compile("^[a-zA-Z-']*"); //cannot have any symbols other than dashes and apostrophes
			
			//test for length. Must be <=20 and >5
			if(s.length()>20)
				result = "\"" + s.concat("\" is too long.");
			else if(s.length()<5)
				result = "\"" + s.concat("\" is too short.");
			//System.out.println(result);//
			//if it IS too long or too short change output
			if(result != null){
				System.out.println(result);
				output = false;
			}
			if(result == null){                              //Not too long or too short?
				//test to see if it is on the white-list
				Matcher in = acceptable.matcher(s);          //match our string
				if(!in.matches()){
					System.out.println("Illegal characters present in string.");
					output = false;
				}
				else {
					System.out.println("Input validation passed.");
					output = true;
				}
			}
			return output;
		}
		
		public static boolean isPassValid(String s, int debug){
			//variables
			String result = null;
			boolean output=false; //initiate to false, rather be wrong in a bad situation then right in a bad one
			//regular expression generation
			Pattern acceptable = Pattern.compile("[\\s]+"); //cannot have any symbols other than dashes and apostrophes
	
			//test for length. Must be <=20 and >5
			if(s.length()>20)
				result = "\"" + s.concat("\" is too long");
			else if(s.length()<5)
				result = "\"" + s.concat("\" is too short");
			if(result != null){
				System.out.println(result);
				output = false;
			}
			if(result == null){
				Matcher in = acceptable.matcher(s);
				if(in.find()){
					System.out.println("Illegal characters present in string");
					output = false;
				}
				else {
					System.out.println("Input validation passed.");
					output = true;
				}
			}
			return output;
		}
}
