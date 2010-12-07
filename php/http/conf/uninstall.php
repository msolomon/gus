<?php
///////////////////////////////////////////////////////////////////////////////
//GUS - Groups in a University Setting
//Author: Colby Blair
///////////////////////////////////////////////////////////////////////////////

include("main.php");

switch(DBMODE) {
	case "mysql":
		$ds = mysql_connect(DBHOST,DBADMIN,DBPW) or die(" MYSQL: Could not connect to database.<br />\n");
		mysql_query("DROP DATABASE " . DBNAME , $ds) or die(" MYSQL: Could not drop database " . DBNAME . "<br />\n");
		echo " MYSQL: Database " . DBNAME . " dropped.<br />\n";
		mysql_close($ds);
		break;
	case "ldap":
		break;
	case "file":
		break;
}

?>
