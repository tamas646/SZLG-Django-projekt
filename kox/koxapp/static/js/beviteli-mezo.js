function tápanyag_átváltás(){

    var kaloria,zsir,feherje,szenhidrat;

    kaloria = document.getElementById("kcal");
    zsir = document.getElementById("fat");
    feherje = document.getElementById("prot");
    szenhidrat = document.getElementById("carb");

    kaloria.value = ((zsir.value*9)+(feherje.value*4)+(szenhidrat.value*4));
    return kaloria;
}

function get_food_details(select)
{
	if(select.value != 0)
	{
		let fd = new FormData();
		fd.append('csrfmiddlewaretoken', csrf);
		fd.append('id', select.value);
		fetch('backend/get_food_details',
		{
			'method': 'POST',
			'body': fd,
			'credentials': 'same-origin',
		}).then(request =>
		{
			request.text().then(json_text =>
			{
				try
				{
					var response = JSON.parse(json_text);
				}
				catch(e)
				{
					console.log(json_text);
					alert('Szerveroldali hiba');
					location.reload(true);
					return;
				}
				if(!response['success'])
				{
					alert(response['message']);
					location.reload(true);
					return;
				}
				document.getElementById('fat').value = response['data']['zsir'];
				document.getElementById('prot').value = response['data']['feherje'];
				document.getElementById('carb').value = response['data']['szenhidrat'];
				tápanyag_átváltás();
			});
		});
	}
}
