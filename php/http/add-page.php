<?php
///////////////////////////////////////////////////////////////////////////////
//GUS - Groups in a University Setting
//Author: Colby Blair
///////////////////////////////////////////////////////////////////////////////

include("conf/gus.php");
include("conf/form.php");

$gus_main = new gus;
echo $gus_main->page_content();

$form1 = new form("add-page","add-page.php");
if($form1->input_data()) {
	$form1->process_input_data("page",array("name")); //table_name, unique fields
}
else {
	$form1->add_textfield("Page Name:","name");
	$form1->add_textfield("Initial Page Content:","content");
	$form1->add_submit("Submit");
	echo $form1->get_content();
}
?>
