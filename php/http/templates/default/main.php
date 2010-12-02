<?php
///////////////////////////////////////////////////////////////////////////////
//GUS - Groups in a University Setting
//Author: Colby Blair
///////////////////////////////////////////////////////////////////////////////

function page_header($vt) {
return("
<html>
<head>
<title>GUS Default Visual Template</title>
<link rel=\"stylesheet\" type=\"text/css\" href=\"templates/" . $vt . "/main.css\" />
</head>
<body>

<h1 id=\"header_element\">GUS</h1>

<ul id=\"links\">
 <li><a href=\"index--old.php?page=home\">Home</a></li>
 <li><a href=\"index--old.php?page=about\">About</a></li>
 <li><a href=\"add-page.php?page=add-page.php\">Add A Page</a></li>
 <li><a href=\"add-user.php?page=add-user.php\">Add A User</a></li>
 <li><a href=\"add-group.php?page=add-group.php\">Add A Group</a></li>
 <li><a href=\"add-group-member.php?page=add-group-member.php\">Add A Group Member</a></li>
 <li>Login</li>
 <li>Register</li>
</ul>

<div id=\"content\">
");
}

function page_footer($extra_content) {
return("
$extra_content
</div>
</body>
</html>
");
}

?>
