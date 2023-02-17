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

function getWorkshopDetails(){
	if(getCookie("LoggedIn") == "True"){
		if(getCookie("isProfileComplete") == "True"){
			miAPI.get(BASE_URL + 'api/events/list/' + slug + '/', null, {
				withCredentials: true,
			}).then(function (response) {
				if(response.data.iitj){
					createCompleteEventDetails(response.data, 0);
				}
				else if(response.data.amount_paid){
					createCompleteEventDetails(response.data, 1);
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
}

function createCompleteEventDetails(data, x){
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
		desDivHtml += data.events[i].about;
		if(data.events[i].is_registered){
			desDivHtml += `<button class="register-btn">REGISTERED!</button>`;
		}
		else{
			if(x==0){
				if(data.reference_name == "dance-workshop"){
					desDivHtml += `<button class="register-btn" onClick="pay('100.00', 'pass-200.00-dance-workshop')">REGISTER</button>`;
				}
				else if(data.reference_name == "resinart-workshop"){
					desDivHtml += `<button class="register-btn" onClick="pay('100.00', 'pass-129.00-resinart-workshop')">REGISTER</button>`;
				}
				else{
					desDivHtml += `<button class="register-btn" onClick="registerEvent('${data.events[i].name}')">REGISTER</button>`;
				}
			}
			else if(x==1){
				if(data.reference_name == "dance-workshop"){
					desDivHtml += `<button class="register-btn" onClick="pay('200.00', 'pass-200.00-dance-workshop')">REGISTER</button>`;
				}
				else if(data.reference_name == "resinart-workshop"){
					desDivHtml += `<button class="register-btn" onClick="pay('129.00', 'pass-129.00-resinart-workshop')">REGISTER</button>`;
				}
				else if(data.reference_name == "music-workshop"){
					desDivHtml += `<button class="register-btn" onClick="pay('100.00', 'pass-100.00-music-workshop')">REGISTER</button>`;
				}
				else if(data.reference_name == "filmmaking-workshop"){
					desDivHtml += `<button class="register-btn" onClick="pay('100.00', 'pass-100.00-filmmaking-workshop')">REGISTER</button>`;
				}
				else{
					desDivHtml += `<button class="register-btn" onClick="registerEvent('${data.events[i].name}')">REGISTER</button>`;
				}
			}
		}
		desDivHtml +=`		
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
		if(data.events[i].start_time != null){
			desDivMobHtml += `
				<span> ${data.events[i].start_time.substr(8, 2)} Feb '23, ${data.events[i].start_time.substr(11, 5)} onwards </span><br>
			`;
		}
		desDivMobHtml += data.events[i].about;
		if(data.events[i].is_registered){
			desDivMobHtml += `<button class="register-btn">REGISTERED!</button>`;
		}
		else{
			if(x==0){
				if(data.reference_name == "dance-workshop"){
					desDivMobHtml += `<button class="register-btn" onClick="pay('100.00', 'pass-200.00-dance-workshop')">REGISTER</button>`;
				}
				else if(data.reference_name == "resinart-workshop"){
					desDivMobHtml += `<button class="register-btn" onClick="pay('100.00', 'pass-129.00-resinart-workshop')">REGISTER</button>`;
				}
				else{
					desDivMobHtml += `<button class="register-btn" onClick="registerEvent('${data.events[i].name}')">REGISTER</button>`;
				}
			}
			else if(x==1){
				if(data.reference_name == "dance-workshop"){
					desDivMobHtml += `<button class="register-btn" onClick="pay('200.00', 'pass-200.00-dance-workshop')">REGISTER</button>`;
				}
				else if(data.reference_name == "resinart-workshop"){
					desDivMobHtml += `<button class="register-btn" onClick="pay('129.00', 'pass-129.00-resinart-workshop')">REGISTER</button>`;
				}
				else if(data.reference_name == "music-workshop"){
					desDivMobHtml += `<button class="register-btn" onClick="pay('100.00', 'pass-100.00-music-workshop')">REGISTER</button>`;
				}
				else if(data.reference_name == "filmmaking-workshop"){
					desDivMobHtml += `<button class="register-btn" onClick="pay('100.00', 'pass-100.00-filmmaking-workshop')">REGISTER</button>`;
				}
				else{
					desDivMobHtml += `<button class="register-btn" onClick="registerEvent('${data.events[i].name}')">REGISTER</button>`;
				}
			}
		}
		desDivMobHtml +=`		
			</div>
		</section>
		`;
	}
	desDiv.innerHTML = desDivHtml;
	desDivMob.innerHTML = desDivMobHtml;
}

if(sessionStorage.getItem("showmsg") != null){
	var x = document.getElementById("snackbar");
	x.innerHTML = sessionStorage.getItem("showmsg");
	x.className = "show";
	setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
	sessionStorage.removeItem("showmsg");
}

function registerEvent(event_name){
	var body = {
		event_name: event_name,
	}
	miAPI.post(BASE_URL + 'api/events/register/', body, {
		headers: {
			'Content-type': 'application/json; charset=UTF-8',
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

function pay(amount, pay_for){
	var body = {
		amount: amount,
		pay_for: pay_for,
		promo_code: "",
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
			setTimeout(function(){x.className = x.className.replace("show", "");}, 5000);
		}
	})
	.finally(function () {
		// always executed
	});
}