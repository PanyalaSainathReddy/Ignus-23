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
let stat = params.status;

if(stat == "success"){
	var x = document.getElementById("snackbar");
	x.innerHTML = 'Payment Successful!';
	x.style.backgroundColor = "#4CAF50";
	x.className = "show";
	setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
}

const BASE_URL = "https://api.ignus.co.in/";
const URL_USER_AUTHENTICATE= "api/accounts/login/";
const URL_REFRESH_TOKEN="api/accounts/refresh/";
const team_arr = new Array(10);

const miAPI = axios.create({
    baseURL: BASE_URL,
    withCredentials:true
});

miAPI.interceptors.response.use(function(response) {
  return response;
},function(error) {
    const originalReq = error.config;

    if ( error.response.status == 401 && !originalReq._retry && error.response.config.url != URL_USER_AUTHENTICATE ) {
      originalReq._retry = true;

      return axios.post(BASE_URL+URL_REFRESH_TOKEN, null, {
        withCredentials:true
      }).then((res) =>{
          if ( res.status == 200) {
              return axios(originalReq);
          }
        }).catch((error) => { window.location.href = "/login.html" });
    }
    return Promise.reject(error);
});

function getEventDetails(){
	if(getCookie("LoggedIn") == "True"){
		if(getCookie("isProfileComplete") == "True"){
			miAPI.get(BASE_URL + 'api/events/list/' + slug + '/', null, {
				withCredentials: true,
			}).then(function (response) {
				if(response.data.amount_paid){
					createCompleteEventDetails(response.data);
				}
				else{
					createEventDetails(response.data, 0);
				}
			})
			.catch(function (error) {
				// handle error
			})
			.finally(function () {
				// always executed
			})
		}
		else{
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
				createEventDetails(data, 1);
			})
			.catch(error => console.error('Error:', error));
		}
	}
	else{
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
			createEventDetails(data, 2);
		})
		.catch(error => console.error('Error:', error));
	}
}

function createEventDetails(data, x){
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
		if(i%2 == 0){
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
			if(data.events[i].start_time != null){
				desDivHtml += `
					<span> ${data.events[i].start_time.substr(8, 2)} Feb '23, ${data.events[i].start_time.substr(11, 5)} onwards </span><br>
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
			if(x == 0){
				desDivHtml += `<a href="../payment_steps/steps.html?paid=false"><button class="register-btn">REGISTER</button></a>`
			}else if(x == 1){
				desDivHtml += `<a href="../complete-profile/index.html"><button class="register-btn">REGISTER</button></a>`
			}else if(x == 2){
				desDivHtml += `<a href="../login.html"><button class="register-btn">REGISTER</button></a>`
			}

			desDivHtml += `
				</div>
				<img src="${imgSrc}" alt="dance">
			</section>
			`;
		}
		else{
			desDivHtml += `
			<section class="details">
				<img src="${imgSrc}" alt="dance">
				<div class="content">
					<h1>${data.events[i].name}</h1>
			`;
			if(data.events[i].sub_title != ""){
				desDivHtml += `
					<span>${data.events[i].sub_title}</span><br>
				`;
			}
			if(data.events[i].start_time != null){
				desDivHtml += `
					<span> ${data.events[i].start_time.substr(8, 2)} Feb '23, ${data.events[i].start_time.substr(11, 5)} onwards </span><br>
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
			if(x == 0){
				desDivHtml += `<a href="../payment_steps/steps.html?paid=false"><button class="register-btn">REGISTER</button></a>`
			}else if(x == 1){
				desDivHtml += `<a href="../complete-profile/index.html"><button class="register-btn">REGISTER</button></a>`
			}else if(x == 2){
				desDivHtml += `<a href="../login.html"><button class="register-btn">REGISTER</button></a>`
			}

			desDivHtml += `
				</div>
			</section>
			`;
		}
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
		if(data.events[i].start_time != null){
			desDivMobHtml += `
				<span> ${data.events[i].start_time.substr(8, 2)} Feb '23, ${data.events[i].start_time.substr(11, 5)} onwards </span><br>
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
		if(x == 0){
			desDivMobHtml += `<a href="../payment_steps/steps.html?paid=false"><button class="register-btn">REGISTER</button></a>`
		}else if(x == 1){
			desDivMobHtml += `<a href="../complete-profile/index.html"><button class="register-btn">REGISTER</button></a>`
		}else if(x == 2){
			desDivMobHtml += `<a href="../login.html"><button class="register-btn">REGISTER</button></a>`
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

function createCompleteEventDetails(data){
	desDiv = document.getElementById("desDiv");
	desDivMob = document.getElementById("desDivMob");
	evCount = data.events.length;
	desDivHtml = "";
	desDivMobHtml = "";
	for(i=0; i<evCount; i++){
		imgSrc = "./../static/event-details/dance.svg";
		if(data.events[i].cover != null){
			imgSrc =  'https://api.ignus.co.in' + data.events[i].cover;
		}
		if(i%2 == 0){
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
			if(data.events[i].start_time != null){
				desDivHtml += `
					<span> ${data.events[i].start_time.substr(8, 2)} Feb '23, ${data.events[i].start_time.substr(11, 5)} onwards </span><br>
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
			if(data.events[i].team_event){
				if(data.events[i].is_registered){
					team_arr[i] = JSON.stringify(data.events[i].team);
					desDivHtml += `<button class="register-btn" onClick="openModal(team_arr[${i}], ${data.events[i].max_team_size})">Your Team</button>`;
				}
				else{
					if(data.name == "Flagship Event"){
						desDivHtml += `<button class="register-btn" onClick="openModal2('1499.00', '${data.reference_name}')">PAY & REGISTER</button>`
					}
					else{
						desDivHtml += `<button class="register-btn" onClick="registerEvent('${data.events[i].name}')">REGISTER</button>`;
					}
				}
			}
			else{
				if(data.events[i].is_registered){
					desDivHtml += `<button class="register-btn">REGISTERED!</button>`;
				}
				else{
					desDivHtml += `<button class="register-btn" onClick="registerEvent('${data.events[i].name}')">REGISTER</button>`;
				}
			}
			desDivHtml +=`		
				</div>
				<img src="${imgSrc}" alt="dance">
			</section>
			`;
		}
		else{
			desDivHtml += `
			<section class="details">
				<img src="${imgSrc}" alt="dance">
				<div class="content">
					<h1>${data.events[i].name}</h1>
			`;
			if(data.events[i].sub_title != ""){
				desDivHtml += `
					<span>${data.events[i].sub_title}</span><br>
				`;
			}
			if(data.events[i].start_time != null){
				desDivHtml += `
					<span> ${data.events[i].start_time.substr(8, 2)} Feb '23, ${data.events[i].start_time.substr(11, 5)} onwards </span><br>
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
			if(data.events[i].team_event){
				if(data.events[i].is_registered){
					team_arr[i] = JSON.stringify(data.events[i].team);
					desDivHtml += `<button class="register-btn" onClick="openModal(team_arr[${i}], ${data.events[i].max_team_size})">Your Team</button>`;
				}
				else{
					if(data.name == "Flagship Event"){
						desDivHtml += `<button class="register-btn" onClick="openModal2('1499.00', '${data.reference_name}')">PAY & REGISTER</button>`
					}
					else{
						desDivHtml += `<button class="register-btn" onClick="registerEvent('${data.events[i].name}')">REGISTER</button>`;
					}
				}
			}
			else{
				if(data.events[i].is_registered){
					desDivHtml += `<button class="register-btn">REGISTERED!</button>`;
				}
				else{
					desDivHtml += `<button class="register-btn" onClick="registerEvent('${data.events[i].name}')">REGISTER</button>`;
				}
			}
			desDivHtml +=`		
				</div>
			</section>
			`;
		}
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
		if(data.events[i].start_time != null){
			desDivMobHtml += `
				<span> ${data.events[i].start_time.substr(8, 2)} Feb '23, ${data.events[i].start_time.substr(11, 5)} onwards </span><br>
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
		if(data.events[i].team_event){
			if(data.events[i].is_registered){
				team_arr[i] = JSON.stringify(data.events[i].team);
				desDivMobHtml += `<button class="register-btn" onClick="openModal(team_arr[${i}], ${data.events[i].max_team_size})">Your Team</button>`;
			}
			else{
				if(data.name == "Flagship Event"){
					desDivMobHtml += `<button class="register-btn" onClick="openModal2('1499.00', '${data.reference_name}')">PAY & REGISTER</button>`
				}
				else{
					desDivMobHtml += `<button class="register-btn" onClick="registerEvent('${data.events[i].name}')">REGISTER</button>`;
				}
			}
		}
		else{
			if(data.events[i].is_registered){
				desDivMobHtml += `<button class="register-btn">REGISTERED!</button>`;
			}
			else{
				desDivMobHtml += `<button class="register-btn" onClick="registerEvent('${data.events[i].name}')">REGISTER</button>`;
			}
		}
		desDivMobHtml +=`		
			</div>
		</section>
		`;
	}
	desDiv.innerHTML = desDivHtml;
	desDivMob.innerHTML = desDivMobHtml;

	pdfEmbed = document.getElementById("pdfEmbed");
	pdfEmbed.setAttribute("src", 'https://api.ignus.co.in' + data.pdf);

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

function registerEvent(event_name){
	var body = {
		event_name: event_name,
	}
	miAPI.post(BASE_URL + 'api/events/register/', body, {
		headers: {
			'Content-type': 'application/json; charset=UTF-8',
			// 'X-CSRFToken': getCookie('csrftoken'),
		},
		withCredentials: true,
	}).then(function (response) {
		if(response.status == 200 || response.status == 201){
			sessionStorage.setItem("showmsg", response.data.message);
			window.location.reload();
		}
	})
	.catch(function (error) {
		// handle error
		if(error.response.status == 402){
			// Complete payment for Flagship Event
			var x = document.getElementById("snackbar");
			x.innerHTML = error.response.data.message;
			x.className = "show";
			setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
		}
	})
	.finally(function () {
		// always executed
	})
}

document.getElementById('close_btn').addEventListener('click', function(){
	document.getElementById('modal').style.display = 'none';
	document.getElementById('overlay').style.display = 'none';
	document.body.style.position = 'static';
});

function openModal(team, max_team_size){
	team = JSON.parse(team);
	document.getElementById('modal_heading').innerHTML = `Team ID: ` + team.id;
	document.getElementById('modal_team_leader').innerHTML = team.leader.name + " (" + team.leader.id + ")";
	var team_mem_details = "";
	for(i=0; i<team.members.length; i++){
		team_mem_details += team.members[i].name + " (" + team.members[i].id + ")";
		if(i != team.members.length-1){
			team_mem_details += ", ";
		}
	}
	if(team_mem_details == ""){
		team_mem_details = "You haven't added anyone to your team yet!";
	}
	document.getElementById('modal_team_members').innerHTML = team_mem_details;
	document.getElementById('modal_team_members').value = team_mem_details;
	if(team.leader.id == getCookie('ignusID')){
		if(team.members.length+1 < max_team_size){
			document.getElementById('add_mem_form').style.display = 'block';
		}
		else{
			document.getElementById('add_mem_form').style.display = 'none';
		}
		document.getElementById('del_team_btn').style.display = 'block';
	}
	else{
		document.getElementById('add_mem_form').style.display = 'none';
		document.getElementById('del_team_btn').style.display = 'none';
	}
	document.getElementById('add_mem_btn').value = team.id;

	document.getElementById('modal').style.display = 'block';
	document.getElementById('overlay').style.display = 'block';
	document.body.style.position = 'fixed';
}

document.getElementById('add_mem_form').addEventListener('submit', function(e){
	e.preventDefault();
	var body = {
		team_id: document.getElementById('add_mem_btn').value,
		member: document.getElementById('add_mem_id').value,
	}
	miAPI.put(BASE_URL + 'api/events/update-team/', body, {
		headers: {
			'Content-type': 'application/json; charset=UTF-8',
			// 'X-CSRFToken': getCookie('csrftoken'),
		},
		withCredentials: true,
	}).then(function (response) {
		if(response.status == 200){
			var team_members = "";
			document.getElementById('add_mem_id').value = '';
			team_arr[response.data.event_rank-1] = JSON.stringify(response.data.team);
			for(i=0; i<response.data.team.members.length; i++){
				team_members += response.data.team.members[i].name + " (" + response.data.team.members[i].id + ")";
				if(i != response.data.team.members.length-1){
					team_members += ", ";
				}
			}
			if(team_members == ""){
				team_members = "You haven't added anyone to your team yet!";
			}
			document.getElementById('modal_team_members').innerHTML = team_members;
			if(response.data.team.members.length+1 < response.data.max_team_size){
				document.getElementById('add_mem_form').style.display = 'block';
			}
			else{
				document.getElementById('add_mem_form').style.display = 'none';
			}
		}
	})
	.catch(function (error) {
		// handle error
		if(error.response.status == 402){
			// The user has not completed their payment.
			var x = document.getElementById("snackbar");
			x.innerHTML = error.response.data.message;
			x.className = "show";
			setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
		}
		else if(error.response.status == 406){
			// The user has already registered for the event or Team is full.
			var x = document.getElementById("snackbar");
			x.innerHTML = error.response.data.message;
			x.className = "show";
			setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
		}
		else if(error.response.status == 404){
			// User Ignus ID Invalid.
			var x = document.getElementById("snackbar");
			x.innerHTML = error.response.data.message;
			x.className = "show";
			setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
		}
		else if(error.response.status == 403){
			// You are not a team leader.
			var x = document.getElementById("snackbar");
			x.innerHTML = error.response.data.message;
			x.className = "show";
			setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
		}
	})
	.finally(function () {
		// always executed
	})
});

document.getElementById('del_team_btn').addEventListener('click', function(){
	var result = confirm("Are you sure you want to delete your team?");
	if(result){
		var body = {
			team_id: document.getElementById('add_mem_btn').value,
		}
		miAPI.delete(BASE_URL + 'api/events/delete-team/', {
			headers: {
				'Content-type': 'application/json; charset=UTF-8',
				// 'X-CSRFToken': getCookie('csrftoken'),
			},
			data: body,
			withCredentials: true,
		}).then(function (response) {
			if(response.status == 200){
				sessionStorage.setItem("showmsg", response.data.message);
				window.location.reload();
			}
		})
		.catch(function (error) {
			// handle error
			if(error.response.status == 403){
				// You are not a team leader.
				var x = document.getElementById("snackbar");
				x.innerHTML = error.response.data.message;
				x.className = "show";
				setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
			}
		})
		.finally(function () {
			// always executed
		})
	}
});

if(sessionStorage.getItem("showmsg") != null){
	var x = document.getElementById("snackbar");
	x.innerHTML = sessionStorage.getItem("showmsg");
	x.className = "show";
	setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
	sessionStorage.removeItem("showmsg");
}

var modal2 = document.getElementById("myModal");
var modal_span = document.getElementsByClassName("close")[0];
var submit_button = document.getElementById("submit_button");

// When the user clicks the button, open the modal2
function openModal2(pay_amount, ref_name){
	submit_button.disabled = false;
	submit_button.style.backgroundColor = "#1d3557";
	document.getElementById("modal_pass_amount").innerHTML = `<span>Amount: </span>Rs. 1499.00`;
	
	if(ref_name == "antarang"){
		document.getElementById("modal_pass_details").innerHTML = `<span>Details: </span> This payment of Rs. 1499 will make you a team leader for Antarang. This payment is for whole team, you will be able to add members to your team after the payment.`;
	}
	else if(ref_name == "nrityansh"){
		document.getElementById("modal_pass_details").innerHTML = `<span>Details: </span> This payment of Rs. 1499 will make you a team leader for Nrityansh. This payment is for whole team, you will be able to add members to your team after the payment.`;
	}
	else if(ref_name == "aayaam"){
		document.getElementById("modal_pass_details").innerHTML = `<span>Details: </span> This payment of Rs. 1499 will make you a team leader for Aayaam. This payment is for whole team, you will be able to add members to your team after the payment.`;
	}
	else if(ref_name == "clashofbands"){
		document.getElementById("modal_pass_details").innerHTML = `<span>Details: </span> This payment of Rs. 1499 will make you a team leader for Thunder Beats. This payment is for whole team, you will be able to add members to your team after the payment.`;
	}

	modal2.style.display = "block";
	document.getElementById("submit_button").value = pay_amount + "-" + ref_name;
};


submit_button.addEventListener("click", function(e){
	var promo_code = document.getElementById("promo_code").value;
	var pay_amount_ref_name = e.target.value;

	pay(pay_amount_ref_name, promo_code);
});

// When the user clicks on (x), close the modal2
modal_span.onclick = function () {
	modal2.style.display = "none";
	document.getElementById("promo_code").value = '';
};

// When the user clicks anywhere outside of the modal2, close it
window.onclick = function (event) {
	if (event.target == modal2) {
		modal2.style.display = "none";
		document.getElementById("promo_code").value = '';
	}
};

function pay(pay_amount_ref_name, promo_code){
	submit_button.disabled = true;
	submit_button.style.backgroundColor = "grey";

	var body = {
		amount: '1499.00',
		pay_for: "pass-" + pay_amount_ref_name,
		promo_code: promo_code,
	}

	miAPI.post(BASE_URL + 'api/payments/init-payment/', body, {
	headers: {
		'Content-type': 'application/json; charset=UTF-8',
	},
	withCredentials: true,
	}
	)
	.then(function (response) {
		console.log(response);
		var mid = response.data.mid;
		var orderId = response.data.orderId;
		var txnToken = response.data.txnToken;
		window.location.href = "https://ignus.co.in/payments/pay.html?mid=" + mid + "&orderId=" + orderId + "&txnToken=" + txnToken;
	})
	.catch(function (error) {
		console.log(error);
		if(error.response.status == 400){
			var x = document.getElementById("snackbar");
			x.innerHTML = error.response.data.message;
			x.style.backgroundColor = "red";
			x.className = "show";
			setTimeout(function(){
				x.className = x.className.replace("show", "");
				submit_button.disabled = false;
				submit_button.style.backgroundColor = "#1d3557";
			}, 5000);
		}
	})
	.finally(function () {
		// always executed
	});
}