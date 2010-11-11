package world;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class test {
	
	public static void main(String[] args) throws IOException {
		//variables
	    String str;
		int lineNum = 1;
		//
		//in any other instance this must be just "test.dat"; not "src/test.dat". (Eclipse is finicky)
		BufferedReader in = new BufferedReader(new FileReader("test.dat")); //get our input file read
		while ((str = in.readLine()) != null) {
			if(lineNum%2==0){												//Check password
				if(functions.isPassValid(str,lineNum))System.out.println("\tSuccess");
				else System.out.println("\tFailure");
			}
			else{
				if(functions.isUserValid(str,lineNum))System.out.println("\tSuccess"); //Check userName
				else System.out.println("\tFailure");							
			}
			if(lineNum%2==0)System.out.println("End Test Case. \n");
			lineNum++;
		}
		in.close();
	}
}
