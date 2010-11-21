<?php
///////////////////////////////////////////////////////////////////////////////
//GUS - Groups in a University Setting
//Author: Colby Blair
///////////////////////////////////////////////////////////////////////////////

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
				);
		$ds->create_table("ggroup", array("name" =>"VARCHAR(100)",
						"description" => "TEXT"
						)
				);
		$ds->save("attr", array(array("name" => 'vt','content' => 'default')
					), 
			array("name")
			);
		echo " MYSQL: table attr populated.<br />\n";	
		$ds->save("page", array(array("name" => 'home',
						"content" => "This is the default page."
						)
					),
			array("name")
			);
		echo " MYSQL: table page populated.<br />\n";	
		$ds->save("ggroup", array(array("name" => 'default',
						"description" => "This is the default gus group."
						)
					),
			array("name")
			);
		echo " MYSQL: table group populated.<br />\n";	
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
