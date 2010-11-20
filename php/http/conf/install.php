<?php

include("main.php");
include("mysql.php");

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
		$ds = new mysql(DBHOST,DBADMIN,DBPW);
		$ds->create_table("attr", array("name" => "VARCHAR(100)",
						"content" => "VARCHAR(100)"
						)
				);
		$ds->create_table("page", array("name" =>"VARCHAR(100)",
						"content" => "TEXT"
						)
				) or $ds->error(" MYSQL: Could not create page table.\n<br />");
		//$ds->save("attr", array("vt" => 'default'));
		//$ds->save("page", array("name",'content'), ?);
		//
		mysql_query("INSERT INTO attr (name,content) VALUES ('vt','default')") 
			or die(" MYSQL: Could not populate table attr, ERROR:<br />\n"
				. mysql_error($ds));
		echo " MYSQL: table attr populated.<br />\n";	
		mysql_query("INSERT INTO page (name,content) VALUES ('home','This is the default page')") 
			or die(" MYSQL: Could not populate table page, ERROR:<br />\n"
				. mysql_error($ds));
		//
		print_r($ds->select("name,content", "page"));
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
