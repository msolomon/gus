<?php

function page_header() {
return("
<html>
<title>GUS Default Visual Template</title>
<body>

<ul>
 <li><a href=\"index.php?page=home\">Home</a></li>
 <li><a href=\"index.php?page=about\">About</a></li>
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
