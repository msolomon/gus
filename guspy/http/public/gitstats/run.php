<?php
	exec("gitstats/gitstats /home/joran0420/git_gus/gus .");
	exec("cat index.html|sed 's/Period/Period <a href=\"run.php\">update<\/a>/' > index1.html;mv index1.html index.html");
	header("location:index.html");	
?>
