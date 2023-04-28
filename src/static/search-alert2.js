const form3 = document.getElementById('form3');
const string_input1 = document.getElementById('compare1');
const string_input2 = document.getElementById('compare2');
form3.addEventListener('submit', (event)=>{
event.preventDefault();
const str1 = string_input1.value.trim();
const str2 = string_input2.value.trim();
if (str1 === '' || str2==='')
{
    alert('Please enter two valid stores');
    string_input.focus();
    return false;
}
form3.submit();
});