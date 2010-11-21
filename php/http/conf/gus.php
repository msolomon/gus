<?php
///////////////////////////////////////////////////////////////////////////////
//GUS - Groups in a University Setting
//Author: Colby Blair
///////////////////////////////////////////////////////////////////////////////

include("main.php");
include(DBMODE . ".php");

class gus {
	private $vt; //visual template
	private $ds; //database connection

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
		$this->vt = $this->ds->select_cond("name,content","attr","name='vt'");
		$this->vt = $this->vt[0]['content']; //set to first val in result, ignores multi matches
		if(!empty($_GET["vt"])) {$this->vt = $_GET["vt"];} //override if html arg
		return($this->vt);
	}

	public function page_content() {
		require_once(TMPLDIR . "/" . $this->vt . "/main.php");
		if(empty($_GET['page'])) $_GET['page'] = 'home';
		$content = $this->ds->select_cond('content', 'page', "name='" . $_GET['page'] . "'");
		if(empty($content)) $content = "This page does not exist<br />";
		else $content = $content[0]['content']; //takes the first if multi matches
		return(page_header() . $content . page_footer());
	}
}

?>
