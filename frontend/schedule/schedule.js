// toggle responsive navbar 
$(document).ready(function(){
	$('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function(){
		$(this).toggleClass('open');
    $(".res-nav").toggleClass("opened");
	});
});

function openPage(pageName,elmnt) {
	var i, tabcontent, tablinks;
	tabcontent = document.getElementsByClassName("tabcontent");
	for (i = 0; i < tabcontent.length; i++) {
	  tabcontent[i].style.display = "none";
	}
	tablinks = document.getElementsByClassName("tablink");
	for (i = 0; i < tablinks.length; i++) {
	  tablinks[i].style.backgroundColor = "";
	}
	document.getElementById(pageName).style.display = "block";
	elmnt.style.backgroundColor = '#1d3557';
};

// API
// const BASE_URL = "https://api.ignus.co.in/";

function loadSchedule(){
	document.getElementById("defaultOpen").click();

	// fetch(BASE_URL + 'api/events/schedule/', {
	// 	method: 'GET',
	// 	headers: {
	// 		'Content-type': 'application/json; charset=UTF-8',
	// 	}
	// })
	// .then(function(response){
	// 	return response.json()
	// })
	// .then(function(data){
	// 	// console.log(data);
	// 	updateSchedule(data);
	// })
	// .catch(error => console.error('Error:', error));
}

// var seventeen = document.getElementById("seventeen");
// var eighteen = document.getElementById("eighteen");
// var nineteen = document.getElementById("nineteen");

// var seventeenText = ``;
// var eighteenText = ``;
// var nineteenText = ``;

// function updateSchedule(data){
// 	for(let i = 0; i < data.length; i++){
// 		if(data[i].start_time != null){
// 			if(data[i].start_time.substring(8, 10) == "17"){
// 				seventeenText += `
// 					<tr class="event-row">
// 						<td>
// 							<p class="event-title">${data[i].name}</p>
// 							<p class="club-name">${data[i].sub_title}</p>
// 						</td>
// 						<td>${data[i].start_time.substring(11, 16)}</td>
// 				`
// 				if(data[i].get_venue != null){
// 					seventeenText += `
// 						<td style="min-width: 30px">${data[i].get_venue.name}</td>
// 					`
// 				}
// 				else{
// 					seventeenText += `
// 						<td style="min-width: 30px"> - </td>
// 					`
// 				}
// 				if(data[i].get_reference_name == "for-schedule"){
// 					seventeenText += `
// 						<td> </td>
// 					`
// 				}
// 				else{
// 					seventeenText += `
// 							<td>
// 								<a
// 								href="../event-details/index.html?ref=${data[i].get_reference_name}"
// 								style="text-decoration: none"
// 								>
// 								<button class="am-btn reg-btn">View More</button>
// 								</a>
// 							</td>
// 					`
// 				}
// 				seventeenText += `
// 					</tr>
// 				`;
// 			}
// 			else if(data[i].start_time.substring(8, 10) == "18"){
// 				eighteenText += `
// 					<tr class="event-row">
// 						<td>
// 							<p class="event-title">${data[i].name}</p>
// 							<p class="club-name">${data[i].sub_title}</p>
// 						</td>
// 						<td>${data[i].start_time.substring(11, 16)}</td>
// 				`
// 				if(data[i].get_venue != null){
// 					eighteenText += `
// 						<td style="min-width: 30px">${data[i].get_venue.name}</td>
// 					`
// 				}
// 				else{
// 					eighteenText += `
// 						<td style="min-width: 30px"> - </td>
// 					`
// 				}
// 				if(data[i].get_reference_name == "for-schedule"){
// 					eighteenText += `
// 						<td> </td>
// 					`
// 				}
// 				else{
// 					eighteenText += `
// 							<td>
// 								<a
// 								href="../event-details/index.html?ref=${data[i].get_reference_name}"
// 								style="text-decoration: none"
// 								>
// 								<button class="am-btn reg-btn">View More</button>
// 								</a>
// 							</td>
// 					`
// 				}
// 				eighteenText += `
// 					</tr>
// 				`;
// 			}
// 			else if(data[i].start_time.substring(8, 10) == "19"){
// 				nineteenText += `
// 					<tr class="event-row">
// 						<td>
// 							<p class="event-title">${data[i].name}</p>
// 							<p class="club-name">${data[i].sub_title}</p>
// 						</td>
// 						<td>${data[i].start_time.substring(11, 16)}</td>
// 				`
// 				if(data[i].get_venue != null){
// 					nineteenText += `
// 						<td style="min-width: 30px">${data[i].get_venue.name}</td>
// 					`
// 				}
// 				else{
// 					nineteenText += `
// 						<td style="min-width: 30px"> - </td>
// 					`
// 				}
// 				if(data[i].get_reference_name == "for-schedule"){
// 					nineteenText += `
// 						<td> </td>
// 					`
// 				}
// 				else{
// 					nineteenText += `
// 							<td>
// 								<a
// 								href="../event-details/index.html?ref=${data[i].get_reference_name}"
// 								style="text-decoration: none"
// 								>
// 								<button class="am-btn reg-btn">View More</button>
// 								</a>
// 							</td>
// 					`
// 				}
// 				nineteenText += `
// 					</tr>
// 				`;
// 			}
// 		}
// 	}

// 	seventeen.innerHTML = seventeenText;
// 	eighteen.innerHTML = eighteenText;
// 	nineteen.innerHTML = nineteenText;
// }