<?php

include("main.php");
include(DBMODE . ".php");

class gus {
	var $vt; //visual template
	var $ds; //database connection

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
		$this->vt = $this->ds->select("vt","attr");
		$this->vt = $this->vt[0]; //set to fir val in result, ignores multi matches
		if(!empty($_GET["vt"])) {$this->vt = $_GET["vt"];} //override if html arg
		return($this->vt);
	}

	public function page_content() {
		require_once(TMPLDIR . "/" . $this->vt . "/main.php");
		if(empty($_GET['page'])) $_GET['page'] = 'home';
		$content = $this->ds->select_cond('content', 'page', "name='" . $_GET['page'] . "'");
		$content = $content[0]; //take the first with multi matches
		return(page_header() . $content . page_footer());
	}
};

?>
