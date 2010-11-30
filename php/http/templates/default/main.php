<?php
///////////////////////////////////////////////////////////////////////////////
//GUS - Groups in a University Setting
//Author: Colby Blair
///////////////////////////////////////////////////////////////////////////////

function page_header() {
return("
<html>
<title>GUS Default Visual Template</title>
<body>

<ul>
 <li><a href=\"index.php?page=home\">Home</a></li>
 <li><a href=\"index.php?page=about\">About</a></li>
 <li><a href=\"add-page.php?page=add-page.php\">Add A Page</a></li>
 <li><a href=\"add-user.php?page=add-user.php\">Add A User</a></li>
 <li><a href=\"add-group.php?page=add-group.php\">Add A Group</a></li>
 <li><a href=\"add-group-member.php?page=add-group-member.php\">Add A Group Member</a></li>
 <li>Login</li>
 <li>Register</li>
</ul>

");
}

function page_footer() {
return("
</body>
</html>
");
}

?>
