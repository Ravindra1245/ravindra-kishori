const form2 = document.getElementById('form2');
const string_input = document.getElementById('forgot');
form2.addEventListener('submit', (event)=>{
event.preventDefault();
const str = string_input.value.trim();
if (str === '')
{
    alert('Please Enter an Email Id');
    string_input.focus();
    return false;
}
alert("Email has been sent to you please reset the password");
form2.submit();
});