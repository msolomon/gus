<?php
///////////////////////////////////////////////////////////////////////////////
//GUS - Groups in a University Setting
//Author: Colby Blair
///////////////////////////////////////////////////////////////////////////////

require_once("conf/main.php");

class form {
	private $content;
	private $ds; //database connection
	private $required; //required fields

	public function __construct($name,$action) {
		require_once("conf/" . DBMODE . ".php");
		if(DBMODE === 'mysql') $this->ds = new mysql(DBHOST,DBUN,DBPW);
		$this->content = "
<form name=\"$name\" action=\"$action\" method=\"post\">
 <table>
";
	}

	public function __destroy(){

	}

	public function set_required($fields) {
		$this->required = $fields;
	}

	public function input_data() {
		foreach($this->required as $key) {
			if(!in_array($key,$_POST)) return(false);
		}
		return(!empty($_POST));
	}

	public function process_input_data($table,$use_fields) {
		$this->ds->save($table,array($_POST),$use_fields);
		//no need to check if successful, db class should handle errors
		echo "Form data submission successful<br />\n";
	}

	public function add_textfield($text,$name) {
		$this->content .= "
  <tr>
   <td>$text <input type=\"text\" name=\"$name\" /></td>
  </tr>
";
	}

	public function add_submit($text) {
		$this->content .= "
  <tr>
   <td><input type=\"submit\" value=\"$text\" /></td>
  </tr>
";
	}

	public function get_content() {
		return($this->content . "
 </table>
</form>"
		);
	}	
}

?>
