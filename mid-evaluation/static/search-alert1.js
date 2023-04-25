const form2 = document.getElementById('form2');
		const string_input = document.getElementById('product_alert1');
		form2.addEventListener('submit', (event)=>{
		event.preventDefault();
		const str = string_input.value.trim();
		if (str === '')
		{
			alert('Please Enter The Product Name');
			string_input.focus();
			return false;
		}
		form2.submit();
		});