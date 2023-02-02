const res_nav = document.querySelector(".res-nav");

$(document).ready(function(){
	$('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function(){
		$(this).toggleClass('open');
    $(".res-nav").toggleClass("opened");
	});
});

// document.getElementById("button2").addEventListener("click", function(){
// 	window.location.href = "#steps";
// });

// document.getElementById("pay_btn_1").addEventListener("click", function(){
// 	window.open("https://www.onlinesbi.sbi/sbicollect/icollecthome.htm", "_blank");
// });

// document.getElementById("pay_btn_2").addEventListener("click", function(){
// 	window.open("https://www.onlinesbi.sbi/sbicollect/icollecthome.htm", "_blank");
// });

if(sessionStorage.getItem("showmsg") != null){
	var x = document.getElementById("snackbar");
	x.innerHTML = sessionStorage.getItem("showmsg");
	x.className = "show";
	setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
	sessionStorage.removeItem("showmsg");
}

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

// API
const BASE_URL = "https://api.ignus.co.in/";
const URL_USER_AUTHENTICATE = "api/accounts/login/";
const URL_REFRESH_TOKEN = "api/accounts/refresh/";

const miAPI = axios.create({
	baseURL: BASE_URL,
	withCredentials: true
});
  
miAPI.interceptors.response.use(function (response) {
	return response;
}, function (error) {
	const originalReq = error.config;
  
	if (error.response.status == 401 && !originalReq._retry && error.response.config.url != URL_USER_AUTHENTICATE) {
	  originalReq._retry = true;
  
	  return axios.post(BASE_URL + URL_REFRESH_TOKEN, null, {
		withCredentials: true
	  }).then((res) => {
		if (res.status == 200) {
		  return axios(originalReq);
		}
	  }).catch((error) => { window.location.href = "/login.html" });
	}
	return Promise.reject(error);
});


function check(){
	if(getCookie("LoggedIn") == "True"){
		if(getCookie("isProfileComplete") == "True"){
			miAPI.get(BASE_URL + 'api/accounts/user-profile-details/', null, {
			headers: {
				'Content-type': 'application/json; charset=UTF-8',
			},
			withCredentials: true,
			}
			)
			.then(function (response) {
				change(response);
			})
			.catch(function (error) {
				console.log(error);
				// handle error
			})
			.finally(function () {
				// always executed
			});
		}
		else{
			window.location.href = "https://ignus.co.in/complete-profile/index.html";
		}
	}else{
		window.location.href = "https://ignus.co.in/login.html";
	}
}

function change(res){
	pass_btn_499 = document.getElementById("get_pass_499");
	pass_btn_2299 = document.getElementById("get_pass_2299");
	pass_btn_1499 = document.getElementById("get_pass_1499");
	pass_btn_1500 = document.getElementById("get_pass_1500");
	pass_btn_2500 = document.getElementById("get_pass_2500");
	pass_div_499 = document.getElementById("pass-tile-499");
	pass_div_2299 = document.getElementById("pass-tile-2299");
	pass_div_1499 = document.getElementById("pass-tile-1499");
	pass_div_1500 = document.getElementById("pass-tile-1500");
	pass_div_2500 = document.getElementById("pass-tile-2500");

	console.log(res);

	if(res.data.userprofile.amount_paid){
		if(res.data.userprofile.pronites){
			pass_btn_499.disabled = true;
			pass_btn_2299.disabled = true;
			pass_btn_1500.disabled = true;
			pass_btn_2500.disabled = true;
			pass_btn_499.style.backgroundColor = "grey";
			pass_btn_2299.style.backgroundColor = "grey";
			pass_btn_1500.style.backgroundColor = "grey";
			pass_btn_2500.style.backgroundColor = "grey";

			if(res.data.userprofile.flagship){
				pass_btn_1499.disabled = true;
				pass_btn_1499.style.backgroundColor = "green";
				pass_btn_1499.innerHTML = "PURCHASED";
			}
			else{
				pass_btn_1499.disabled = false;
				pass_btn_1499.style.backgroundColor = "#1d3557";
			}
			if(res.data.userprofile.igmun){
				if(res.data.userprofile.accomodation_2){
					pass_btn_2500.style.backgroundColor = "green";
					pass_btn_2500.innerHTML = "PURCHASED";
					pass_div_499.style.display = "none";
					pass_div_2299.style.display = "none";
					pass_div_1500.style.display = "none";
				}
				else{
					pass_btn_1500.style.backgroundColor = "green";
					pass_btn_1500.innerHTML = "PURCHASED";
					pass_div_499.style.display = "none";
					pass_div_2299.style.display = "none";
					pass_div_2500.style.display = "none";
				}
			}
			else{
				if(res.data.userprofile.accomodation_4){
					pass_btn_2299.style.backgroundColor = "green";
					pass_btn_2299.innerHTML = "PURCHASED";
					pass_div_499.style.display = "none";
					pass_div_1500.style.display = "none";
					pass_div_2500.style.display = "none";
				}
				else{
					pass_btn_499.style.backgroundColor = "green";
					pass_btn_499.innerHTML = "PURCHASED";
					pass_div_2299.style.display = "none";
					pass_div_1500.style.display = "none";
					pass_div_2500.style.display = "none";
				}
			}
		}
	}
	else{
		pass_btn_1499.disabled = true;
		pass_btn_1499.style.backgroundColor = "grey";
	}
}

let payButtonList = document.getElementsByClassName("pay-btn");
for(let i of payButtonList){
	i.addEventListener("click", function(e){
		console.log(e.target.value);
		pay(e.target.value);
	})
}

function pay(pay_amount){
	var body = {
		amount: pay_amount,
		pay_for: "pass-" + pay_amount,
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
		// handle error
	})
	.finally(function () {
		// always executed
	});
}