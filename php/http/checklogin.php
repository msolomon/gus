<!-- Abhay Patil - Check Login form -->
<?php
$host="localhost"; // Host name 
$username="root"; // Mysql username 
$password=""; // Mysql password 
$db_name="gus"; // Database name 
$tbl_name="guser"; // Table name

mysql_connect("$host", "$username", "$password")or die("cannot connect"); 
$db = mysql_select_db("$db_name")or die("cannot select DB");

$name=$_POST['name']; 
$description=$_POST['description'];

$name = stripslashes($name);
$description = stripslashes($description);
$name = mysql_real_escape_string($name);
$description = mysql_real_escape_string($description);

$sql="SELECT * FROM $tbl_name WHERE name='$name' and description='$description'";
$result=mysql_query($sql);

$count=mysql_num_rows($result);

echo "TS: count = $count<br />";


if($count>0){
//session_register(array("name",$name));
$_SESSION['name'] = $name;
//session_register(array("description",$description)); 
$_SESSION['description'] = $description;
print_r($_SESSION);
exit(1);
header("location:login_success.php");

}
else {
echo "Wrong Username or Password";
}
?>
