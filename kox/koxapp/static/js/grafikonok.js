window.addEventListener('load', function()
{
	for(element of document.getElementsByClassName('myPieChart_bevitel'))
	{
		let labels = [
			element.parentNode.previousElementSibling.firstElementChild.children[1].firstElementChild.firstChild.nodeValue,
			element.parentNode.previousElementSibling.firstElementChild.children[2].firstElementChild.firstChild.nodeValue,
			element.parentNode.previousElementSibling.firstElementChild.children[3].firstElementChild.firstChild.nodeValue,
		];
		let data = [
			element.parentNode.previousElementSibling.firstElementChild.children[1].lastElementChild.firstChild.nodeValue,
			element.parentNode.previousElementSibling.firstElementChild.children[2].lastElementChild.firstChild.nodeValue,
			element.parentNode.previousElementSibling.firstElementChild.children[3].lastElementChild.firstChild.nodeValue,
		];
		let chart = new Chart(element.getContext('2d'), {
			type: 'pie',
			data: {
				labels: labels,
				datasets: [{
					backgroundColor: 'rgb(255, 99, 132)',
					data: data,
					backgroundColor: ['red', 'green', 'blue'],
				}]
			},
			options: { responsive: true, legend: { display: false } }
		});
	}
	for(element of document.getElementsByClassName('myPieChart_mozgas'))
	{
		let labels = [];
		let data = [];
		for(tr of element.parentNode.previousElementSibling.firstElementChild.children)
		{
			labels.push(tr.firstElementChild.firstChild.nodeValue);
			data.push(parseInt(tr.lastElementChild.firstChild.nodeValue));
		}
		let chart = new Chart(element.getContext('2d'), {
			type: 'pie',
			data: {
				labels: labels,
				datasets: [{
					backgroundColor: 'rgb(255, 99, 132)',
					data: data,
					backgroundColor: ['gray', 'yellow', 'blue', 'red', 'green', 'black', 'white'],
				}]
			},
			options: { responsive: true, legend: { display: false } }
		});
	}
});
