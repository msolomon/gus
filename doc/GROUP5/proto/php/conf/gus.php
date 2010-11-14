<?php

include("main.php");
include(DBMODE . ".php");

class gus {
	var $vt; //visual template
	var $ds; //

	function __construct() {
		if(!$this->init_db()) {
			{$this->error("Could not initialize the ". DBMODE . " database.");}
		}
		if(!$this->set_visual_template()) 
			{$this->error("Could not set visual template.");}
	}

	function __destruct() {
	}

	private function error($msg) {
		die("GUS ERROR: " . $msg . "<br />\n");
	}

	private function init_db() {
		return($this->ds = new mysql(DBHOST,DBADMIN,DBPW));
	}
	
	private function set_visual_template() {
		//if there is an html vt arg, use that as the vt
		//otherwise, obtain the vt from the database
		if(empty($_GET["vt"])) { 
			$this->vt = "default";
			return("true");
		}
		else {$this->vt = $_GET["vt"]; return(true);}
	}
};

?>
