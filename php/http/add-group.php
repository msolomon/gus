<?php
///////////////////////////////////////////////////////////////////////////////
//GUS - Groups in a University Setting
//Author: Colby Blair
///////////////////////////////////////////////////////////////////////////////

include("conf/gus.php");
include("conf/form.php");

$gus_main = new gus;
echo $gus_main->page_content();

$form1 = new form("add-group","add-group.php");
if($form1->input_data()) {
	$form1->process_input_data("ggroup",array("name")); //table_name, unique fields
}
else {
	$form1->add_textfield("Group Name:","name");
	$form1->add_textfield("Group Description:","description");
	$form1->add_submit("Submit");
	echo $form1->get_content();
}
?>
