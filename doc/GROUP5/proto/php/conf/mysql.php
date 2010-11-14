<?php

class mysql {
	var $ds; //database connection

	public function __construct($hostname,$un,$pw) {
		return($this->ds = $this->connect($hostname,$un,$pw));
	}

	public function __destruct() {
		$this->disconnect();
	}

	private function connect($hostname, $un, $pw) {
		return(mysql_connect($hostname, $un, $pw));
	}

	private function disconnect() {
		mysql_disconnect($this->ds);
	}
}

?>
