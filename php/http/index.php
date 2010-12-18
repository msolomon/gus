<?php
///////////////////////////////////////////////////////////////////////////////
//GUS - Groups in a University Setting
//Author: Colby Blair
///////////////////////////////////////////////////////////////////////////////

include("conf/gus.php");
$gus_main = new gus;

echo $gus_main->page_content("
<!-- Abhay Patil - login, copied by Cindy -->

<table width=\"300\" border=\"0\" align=\"center\" cellpadding=\"0\" cellspacing=\"1\" bgcolor=\"#CCCCCC\">
<tr>
<form name=\"form1\" method=\"post\" action=\"checklogin.php\">
<td>
<table width=\"100%\" border=\"0\" cellpadding=\"3\" cellspacing=\"1\" bgcolor=\"#FFFFFF\">
<tr>
<td colspan=\"3\"><strong>Member Login </strong></td>
</tr>
<tr>
<td width=\"78\">Username</td>
<td width=\"6\">:</td>
<td width=\"294\"><input name=\"name\" type=\"text\" id=\"name\"></td>
</tr>
<tr>
<td>Password</td>
<td>:</td>
<td><input name=\"description\" type=\"text\" id=\"description\"></td>
</tr>
<tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td><input type=\"submit\" name=\"Submit\" value=\"Login\"></td>
</tr>
</table>
</td>
</form>
</tr>
</table>

");
?>
