<?php
///////////////////////////////////////////////////////////////////////////////
//GUS - Groups in a University Setting
//Author: Colby Blair
///////////////////////////////////////////////////////////////////////////////

include("conf/gus.php");
include("conf/form.php");

$gus_main = new gus;
echo $gus_main->page_content();

$form1 = new form("add-group-member","add-group-member.php");
if($form1->input_data()) {
	$_POST['uid'] = $gus_main->get_uid($_POST["uname"]);
	$_POST['gid'] = $gus_main->get_gid($_POST["gname"]);
	unset($_POST["uname"]);
	unset($_POST["gname"]);
	$form1->process_input_data("ggroup_member",array("uid","gid")); //table_name, unique fields
}
else {
	$form1->add_textfield("User Name:","uname");
	$form1->add_textfield("Group Name:","gname");
	$form1->add_submit("Submit");
	echo $form1->get_content();
}
?>
