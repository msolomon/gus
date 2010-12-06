<!-- Abhay Patil - Registration form -->
<!-- CSS done by Scott Bedall, linked by Cynthia Rempel -->
<LINK REL=StyleSheet HREF="templates/default/template.css" TYPE="text/css" MEDIA=screen>
<h2 align="center">User Registration Form</h2>

<form name="registration_form" method="post" action="register.php" onsubmit="return Validate();">
    <table width="53%" border="0" align="center" cellpadding="5" cellspacing="0">
    <tr>
        <td width="49%">Name</td>
        <td colspan="2">
          <div align="left"
           <input type="text" name="name" size="45" maxlength="30">
         </div>
        </td>
      </tr>
      <tr>
        <td width="49%">&nbsp;</td>
        <td height="2" colspan="2">&nbsp;</td>
      </tr>

    <tr>
        <td width="49%">Email</td>
        <td colspan="2">
          <div align="left"
           <input type="text" name="email" size="45" maxlength="30">
         </div>
        </td>
      </tr>
      <tr>
        <td width="49%">&nbsp;</td>
        <td height="2" colspan="2">&nbsp;</td>
      </tr>
    </form>

    <tr>
        <td width="49%">Student ID</td>
        <td colspan="2">
          <div align="left"
           <input type="text" name="username" size="45" maxlength="30">
         </div>
        </td>
      </tr>
      <tr>
        <td width="49%">&nbsp;</td>
        <td height="2" colspan="2">&nbsp;</td>
      </tr>
        </form>

    <tr>
        <td width="49%">Password</td>
        <td colspan="2">
          <div align="left"
           <input type="password" name="password" size="45" maxlength="30">
         </div>
        </td>
      </tr>
      <tr>
        <td width="49%">&nbsp;</td>
        <td height="2" colspan="2">&nbsp;</td>
      </tr>
        </form>

    <tr>
        <td width="49%">Confirm Password</td>
        <td colspan="2">
          <div align="left"
           <input type="password" name="repassword" size="45" maxlength="30">
         </div>
        </td>
      </tr>
      <tr>
        <td width="49%">&nbsp;</td>
        <td height="2" colspan="2">&nbsp;</td>
      </tr>
        </form>

    <tr>
        <td width="49%">Phone</td>
        <td colspan="2">
          <div align="left"
           <input type="text" name="phone" size="45" maxlength="30">
         </div>
        </td>
      </tr>
      <tr>
        <td width="49%">&nbsp;</td>
        <td height="2" colspan="2">&nbsp;</td>
      </tr>

    <tr>
        <td colspan="3">
          <div align="left">
            <input type="submit" name="Submit" value="Submit">
          </div>
        </td>
      </tr>
    </table>
        </form>



<script language = "Javascript">
  
function Validate()
{

var regex = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
var regex1 = /^([0-9]{3})+\-([0-9]{5})+$/;
var regex2 = /^([a-zA-Z0-9_\.\-])+$/;
var regex3 = /^([0-9]{3})+\-([0-9]{3})+\-([0-9]{4})+$/;
    if (document.registration_form.name.value == '') 
    {
        alert('Please fill in your name!');
        return false;
    }
    else if (document.registration_form.email.value == '') 
    {
       alert('Please fill in your email address!');
       return false;
    }

else if(!regex.test(document.registration_form.email.value))
         {
             alert("Invalid email address format");
             return false;
         }

   else if (document.registration_form.username.value == '') 
    {
        alert('Please fill in your student ID(xxx-xxxxx)!');
        return false;
    }

else if(!regex1.test(document.registration_form.username.value))
         {
             alert("Invalid student id format");
             return false;
         }


    else if (document.registration_form.password.value == '') 
    {
       alert('Please fill in your desired password!');
      return false;
    }

else if(!regex2.test(document.registration_form.password.value))
         {
             alert("Invalid password format");
             return false;
         }


    else if (document.registration_form.repassword.value == '') 
    {
       alert('Please fill in your password again for confirmation!');
      return false;
    }

    else if (document.registration_form.password.value != 
    document.registration_form.repassword.value) 
    {
        alert("The two passwords are not identical! "+
        "Please enter the same password again for confirmation");
        return false;
    }
    else if (document.registration_form.phone.value == '') 
    {
        alert('Please fill in your phone number!');
        return false;
    }

else if(!regex3.test(document.registration_form.phone.value))
         {
             alert("Invalid phone format");
             return false;
         }


    else
    return true;
}

</script>
