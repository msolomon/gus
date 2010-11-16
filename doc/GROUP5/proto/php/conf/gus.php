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
		if(!$this->init_data()) 
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
	
	private function init_data() {
		$this->vt = $this->ds->select("vt","attrs");
		$this->vt = $this->vt[0]; //set to fir val in result, ignores multi matches
		if(!empty($_GET["vt"])) {$this->vt = $_GET["vt"];} //override if html arg
		return($this->vt);
	}
};

?>
