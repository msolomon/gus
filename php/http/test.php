<?php
///////////////////////////////////////////////////////////////////////////////
//GUS - Groups in a University Setting
//Author: Colby Blair
///////////////////////////////////////////////////////////////////////////////

include("conf/gus.php");
$gus_main = new gus;

echo $gus_main->page_content();

/*
print_r($gus_main->ds->select("name,content", "page"));

echo $gus_main->ds->save("page", array(
				array("name" => "test",
					"content" => "Test content."
				)
			),
			array("name")
		);
*/
?>
