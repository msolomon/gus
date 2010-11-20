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

	public function save($table, $names, $values) {
		//need conditional for if values already exist
		/*$nfields = 0;
		$names = "";
		$values = "";
		foreach($names as $key) {
			if($nfields > 0) {$names .= ", ";
			$names .= "$key";
			$nfields++;
		}
		foreach($values as $key =>) {
			if($nfields > 0) {$names .= ", ";
			$names .= "$key";
			$nfields++;
		}

		$query = "INSERT INTO $table ($names) VALUES ($values)";
		echo $query;
		exit(1);
		*/
	}

	public function select($who, $table) {
		$result_arr = array();
		$result = mysql_query("SELECT $who from $table");
		if(!$result) $this->error("mysql->select");
		while($row = mysql_fetch_array($result)) {
			array_push($result_arr, $row);
		}
		return($result_arr);
	}

	public function select_cond($who, $table, $cond) {
		$result_arr = array();
		$result = mysql_query("SELECT $who from $table where $cond");
		if(!$result) $this->error("mysql->select_cond");
		while($row = mysql_fetch_array($result)) {
			array_push($result_arr, $row);
		}
		return($result_arr);
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
