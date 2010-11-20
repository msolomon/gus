<?php

include("conf/gus.php");
$gus_main = new gus;

echo $gus_main->page_content();
print_r($gus_main->ds->select("name,content", "page"));

?>
