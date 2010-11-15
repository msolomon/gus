<?php

class mysql {
	var $ds; //database connection

	public function __construct($hostname,$un,$pw) {
		return( ($this->ds = $this->connect($hostname,$un,$pw)) 
			&& mysql_select_db(DBNAME,$this->ds)
			);
	}

	public function __destruct() {
		$this->disconnect();
	}

	private function connect($hostname, $un, $pw) {
		return(mysql_connect($hostname, $un, $pw));
	}

	private function disconnect() {
		mysql_close($this->ds);
	}

	public function select($who, $table) {
		$result = mysql_query("SELECT $who from $table");
		if(!$result) {
			echo "warning: " . mysql_error($this->ds) . "<br />\n";
			return($result);
		}
		$result = mysql_fetch_array($result);
		return($result); //returns the first value in case of > 1
	}
}

?>
