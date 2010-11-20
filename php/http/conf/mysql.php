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

	public function error() {
		//optional message arg
		$msg = "";
		if(func_num_args() > 0) $msg = func_get_arg(0) . ",";
		die("$msg ERROR: " . mysql_error($this->ds));
	}

	public function save() {

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

	public function select_cond($who, $table, $cond) {
		$result = mysql_query("SELECT $who from $table where $cond");
		if(!$result) {
			echo "warning: " . mysql_error($this->ds) . "<br />\n";
			return($result);
		}
		$result = mysql_fetch_array($result);
		return($result); //returns the first value in case of > 1
	}

	public function create_table($table, $fields) {
		$query = "CREATE TABLE $table (\n";
		$nfields = 0;
		foreach($fields as $key =>$val) {
			if($nfields > 0) $query .= ",\n";
			$query .= "$key $val";
			$nfields++;
		}
		$query .= ")";
		return(mysql_query($query, $this->ds));
	}
}

?>
