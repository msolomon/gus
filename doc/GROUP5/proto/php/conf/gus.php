<?php

class gus {
	var $vt; //visual template

	public function gus() {
		if(!$this->set_visual_template()) 
			{$this->gus_error("Could not set visual template.");}
	}

	private function gus_error($msg) {
		die("GUS ERROR: " . $msg . "<br />\n");
	}

	private function set_visual_template() {
		if(empty($_GET["vt"])) { 
			$this->vt = "default";
			return("true");
		}
		else {$this->vt = $_GET["vt"]; return(true);}
	}
};

?>
