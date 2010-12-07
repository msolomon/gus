<!-- Abhay Patil - Login Success -->

<? 
session_start();
if(!session_is_registered(name)){
header("location:login.php");
}
?>

<html>
<body>
Login Successful
</body>
</html>
