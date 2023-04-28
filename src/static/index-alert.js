const form=document.querySelector('form');
const string_input=document.getElementById('product_alert');
form.addEventListener('submit', (event)=>{
    event.preventDefault();
    const str = string_input.value.trim();
    if (str === '')
    {
        alert('Please Enter The Product Name');
        string_input.focus();
        return false;
    }
    form.submit();
});