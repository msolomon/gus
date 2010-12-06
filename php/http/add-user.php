<?php
///////////////////////////////////////////////////////////////////////////////
//GUS - Groups in a University Setting
//Author: Colby Blair
///////////////////////////////////////////////////////////////////////////////

include("conf/gus.php");
include("conf/form.php");

$gus_main = new gus;

$content = "";
$form1 = new form("add-user","add-user.php");
if($form1->input_data()) {
	$form1->process_input_data("guser",array("name")); //table_name, unique fields
}
else {
	$form1->add_textfield("User Name:","name");
	$form1->add_textfield("User Description:","description");
	$form1->add_submit("Submit");
	$content = $form1->get_content();
}

echo $gus_main->page_content($content);
?>
