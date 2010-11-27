<?php
///////////////////////////////////////////////////////////////////////////////
//GUS - Groups in a University Setting
//Author: Colby Blair
///////////////////////////////////////////////////////////////////////////////

class mysql {
	private $ds; //database connection

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
		//need to find out why ds is no longer a valid mysql conn
		@mysql_close($this->ds); 
	}

	private function names_and_values($table, $data, &$names, &$values) {
		$nfields = 0;
		$names = $values = "";
		foreach($data as $key => $val) {
			if($nfields > 0) {$names .= ", "; $values .= ", ";}
			#set names
			$names .= $key;
			#set values
			if(gettype($val) == "string") {$values .= "'$val'";}
			else {$values .= $val;}
			$nfields++;
		}
	}

	private function where($table,$data,&$where,$use_fields) {
		$nfields = 0;
		$where = "";
		foreach($data as $key => $val) {
			if(in_array($key,$use_fields)) {
				if($nfields > 0) {$where .= " AND ";}
				#set where
				$where .= "$key=";
				if(gettype($val) == "string") {$where .= "'$val'";}
				else {$where .= $val;}
				$nfields++;
			}
		}
	}

	private function set($table, $data, &$set) {
		$nfields = 0;
		$set = "";
		foreach($data as $key => $val) {
			if($nfields > 0) {$set .= ", ";}
			#set set
			$set .= "$key=";
			if(gettype($val) == "string") {$set .= "'$val'";}
			else {$set .= $val;}
			$nfields++;
		}
	}

	private function exists($table,$data,$use_field) {
		$names = $values = $where = "";
		$this->names_and_values($table, $data, $names, $values);
		$this->where($table,$data,$where,$use_field);
		$test_arr = $this->select_cond($names, $table, $where);
		return(!empty($test_arr));
	}

	public function error() {
		//optional message arg
		$msg = "";
		if(func_num_args() > 0) $msg = func_get_arg(0) . ",";
		die("$msg ERROR: " . mysql_error($this->ds));
	}

	public function save($table, $data,$use_fields) {
		foreach($data as $row) {
			$names = $values = $where = $set = "";
			$this->names_and_values($table, $row, $names, $values);
			$this->where($table,$row,$where,$use_fields);
			$this->set($table,$row,$set);
			if($this->exists($table,$row,$use_fields)) {
				$query = "UPDATE $table SET $set WHERE $where";
			}
			else {
				$query = "INSERT INTO $table ($names) VALUES ($values)";
			}
			$result = mysql_query($query, $this->ds);
			if(!$result) $this->error("mysql->save query: $query");
		}
		return(true);
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
		$query = "SELECT $who from $table where $cond";
		$result = mysql_query($query);
		if(!$result) $this->error("mysql->select_cond query: $query");
		while($row = mysql_fetch_array($result)) {
			array_push($result_arr, $row);
		}
		return($result_arr);
	}

	public function create_table($table, $fields) {
		#opt args
		$tattrs = ""; //table attributes
		if(func_num_args() === 3) $tattrs = func_get_arg(2);
		$query = "CREATE TABLE $table (\n";
		$nfields = 0;
		foreach($fields as $key =>$val) {
			if($nfields > 0) $query .= ",\n";
			$query .= "$key $val";
			$nfields++;
		}
		$query .= ") $tattrs";
		$result = mysql_query($query, $this->ds);
		if(!$result) $this->error("mysql->create_table query: $query");
		return(true);
	}
}

?>
