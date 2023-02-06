$(document).ready(function(){
	$('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function(){
		$(this).toggleClass('open');
    $(".res-nav").toggleClass("opened");
	});
});

function getCookie(cname) {
	let name = cname + "=";
	let decodedCookie = decodeURIComponent(document.cookie);
	let ca = decodedCookie.split(';');
	for(let i = 0; i <ca.length; i++) {
	  let c = ca[i];
	  while (c.charAt(0) == ' ') {
		c = c.substring(1);
	  }
	  if (c.indexOf(name) == 0) {
		return c.substring(name.length, c.length);
	  }
	}
	return "";
}

const params = new Proxy(new URLSearchParams(window.location.search), {
	get: (searchParams, prop) => searchParams.get(prop),
});

let slug = params.ref;

const BASE_URL = "https://api.ignus.co.in/";

function getEventDetails(){
	fetch(BASE_URL + 'api/events/list/' + slug + '/', {
		method: 'GET',
		credentials: 'include',
		headers: {
			'Content-type': 'application/json; charset=UTF-8',
		}
	})
	.then(function(response){
		return response.json()
	})
	.then(function(data){
		createEventDetails(data);
	})
	.catch(error => console.error('Error:', error));
}

function createEventDetails(data){
	desDiv = document.getElementById("desDiv");
	desDivMob = document.getElementById("desDivMob");
	evCount = data.events.length;
	desDivHtml = "";
	desDivMobHtml = "";
	for(i=0; i<evCount; i++){
		imgSrc = "./../static/event-details/dance.svg";
		if(data.events[i].cover != null){
			imgSrc = 'https://api.ignus.co.in' + data.events[i].cover;
		}
		desDivHtml += `
		<section class="details">
			<div class="content">
				<h1>${data.events[i].name}</h1>
		`;
		if(data.events[i].sub_title != ""){
			desDivHtml += `
				<span>${data.events[i].sub_title}</span><br>
			`;
		}
		if(data.events[i].start_time != null && data.events[i].end_time != null){
			desDivHtml += `
				<span> ${data.events[i].start_time.substr(8, 2)} - ${data.events[i].end_time.substr(8, 2)} Feb '23 </span><br>
			`;
		}
		if(data.events[i].team_event){
			if(data.events[i].min_team_size == data.events[i].max_team_size){
				desDivHtml += `
					<span> Team Size: ${data.events[i].min_team_size} </span>
				`;
			}
			else{
				desDivHtml += `
					<span> Team Size: ${data.events[i].min_team_size}-${data.events[i].max_team_size} </span>
				`;
			}
		}
		desDivHtml += data.events[i].about;
		if(getCookie("LoggedIn") == "True"){
			if(getCookie("isProfileComplete") == "True"){
				if(data.events[i].ol_live){
					desDivHtml += `<a href="${data.events[i].gform_link}" target='_blank'><button class="register-btn">REGISTER</button></a>`;
				}
				else{
					desDivHtml += `<a><button disabled class="register-btn">Registrations Not Open</button></a>`;
				}
			}
			else{
				desDivHtml += `<a href="../complete-profile/index.html"><button class="register-btn">REGISTER</button></a>`;
			}
		}else{
			desDivHtml += `<a href="../login.html"><button class="register-btn">REGISTER</button></a>`;
		}

		desDivHtml += `
			</div>
			<img src="${imgSrc}" alt="dance">
		</section>
		`;
		desDivMobHtml += `
		<section class="details">
			<img src="${imgSrc}" alt="dance">
			<div class="content">
				<h1>${data.events[i].name}</h1>
		`;
		if(data.events[i].sub_title != ""){
			desDivMobHtml += `
				<span>${data.events[i].sub_title}</span><br>
			`;
		}
		if(data.events[i].start_time != null && data.events[i].end_time != null){
			desDivMobHtml += `
				<span> ${data.events[i].start_time.substr(8, 2)} - ${data.events[i].end_time.substr(8, 2)} Feb '23 </span><br>
			`;
		}
		if(data.events[i].team_event){
			if(data.events[i].min_team_size == data.events[i].max_team_size){
				desDivMobHtml += `
					<span> Team Size: ${data.events[i].min_team_size} </span>
				`;
			}
			else{
				desDivMobHtml += `
					<span> Team Size: ${data.events[i].min_team_size}-${data.events[i].max_team_size} </span>
				`;
			}
		}
		desDivMobHtml += data.events[i].about;
		if(getCookie("LoggedIn") == "True"){
			if(getCookie("isProfileComplete") == "True"){
				if(data.events[i].ol_live){
					desDivMobHtml += `<a href="${data.events[i].gform_link}" target='_blank'><button class="register-btn">REGISTER</button></a>`;
				}
				else{
					desDivMobHtml += `<a><button disabled class="register-btn">REGISTER</button></a>`;
				}
			}
			else{
				desDivMobHtml += `<a href="../complete-profile/index.html"><button class="register-btn">REGISTER</button></a>`;
			}
		}else{
			desDivMobHtml += `<a href="../login.html"><button class="register-btn">REGISTER</button></a>`;
		}
		desDivMobHtml += `
			</div>
		</section>
		`;
	}
	desDiv.innerHTML = desDivHtml;
	desDivMob.innerHTML = desDivMobHtml;

	pdfEmbed = document.getElementById("pdfEmbed");
	pdfEmbed.setAttribute("src",  'https://api.ignus.co.in' + data.pdf);

	evOrg = document.getElementById("evOrg");
	orgCount = data.get_organizers.length;
	evOrgHtml = "<h1>Event Organisers</h1> <br>";
	for(i=0; i<orgCount; i++){
		evOrgHtml += `
        <h3>${data.get_organizers[i].name}</h3> 
        <span class="contact">${data.get_organizers[i].phone}</span> <br>
        <span class="contact"><a href="mailto:${data.get_organizers[i].email}" style="text-decoration: none; color: black;">${data.get_organizers[i].email}</a></span> <br><br>
		`;
	}
	evOrg.innerHTML = evOrgHtml;
	document.getElementById('download_rulebook').innerHTML = `<button style="margin-top: 15%;">Download Rulebook</button>`
}

if(sessionStorage.getItem("showmsg") != null){
	var x = document.getElementById("snackbar");
	x.innerHTML = sessionStorage.getItem("showmsg");
	x.className = "show";
	setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
	sessionStorage.removeItem("showmsg");
}