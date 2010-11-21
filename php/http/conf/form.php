<?php

///////////////////////////////////////////////////////////////////////////////
//GUS - Groups in a University Setting
//Author: Colby Blair
///////////////////////////////////////////////////////////////////////////////

class form {
	private $content;

	public function __construct() {

	}

	public function __destroy(){

	}

	public function add_textfield($name) {
		$this->content .= "<input type=\"text\" name=\"$name\" />\n";
	}
}

?>
