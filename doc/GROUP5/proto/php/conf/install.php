<?php

include("main.php");

echo "GUS: Install starting...<br />\n";

switch(DBMODE) {
	case "mysql":
		#connect
		$ds = mysql_connect(DBHOST,DBADMIN,DBPW) or die(" MYSQL: Could not connect \
								to database.<br />\n");
		#create database
		mysql_query("CREATE DATABASE " . DBNAME , $ds) or 
			die(" MYSQL: Could not create database " . DBNAME);
		echo " MYSQL: Database " . DBNAME . " created.<br />\n";
		#use database
		mysql_select_db(DBNAME,$ds) or die( "MYSQL: could not select database "
							. DBNAME);
		#create and initialize gus attribute table
		mysql_query("CREATE TABLE attr (
				vt VARCHAR(100)
				)",$ds) 
			or die(" MYSQL: Could not create table attr, ERROR:<br />\n"
				. mysql_error($ds));
		echo " MYSQL: created table attr.<br />\n";
		mysql_query("CREATE TABLE page (
				name VARCHAR(100),
				content TEXT
				)",$ds) 
			or die(" MYSQL: Could not create table page, ERROR:<br />\n"
				. mysql_error($ds));
		echo " MYSQL: created table page.<br />\n";
		mysql_query("INSERT INTO attr (vt) VALUES ('default')") 
			or die(" MYSQL: Could not populate table $table, ERROR:<br />\n"
				. mysql_error($ds));
		echo " MYSQL: table attr populated.<br />\n";	
		mysql_query("INSERT INTO page (name,content) VALUES ('default','This is the default page')") 
			or die(" MYSQL: Could not populate table page, ERROR:<br />\n"
				. mysql_error($ds));
		echo " MYSQL: table page populated.<br />\n";	
		#mysql done
		echo " MYSQL: Install complete<br />\n";
		break;
	case "ldap":
		break;
	case "file":
		break;
}

echo "GUS: Install complete.<br />\n";

?>
