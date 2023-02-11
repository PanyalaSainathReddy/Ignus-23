const res_nav = document.querySelector(".res-nav");

$(document).ready(function(){
	$('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function(){
		$(this).toggleClass('open');
    $(".res-nav").toggleClass("opened");
	});
});

const params = new Proxy(new URLSearchParams(window.location.search), {
	get: (searchParams, prop) => searchParams.get(prop),
});

let stat = params.status;
let paid = params.paid;

if(stat == "failed"){
  var x = document.getElementById("snackbar");
  x.innerHTML = "Your Payment has been failed, try again!";
  x.className = "show";
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
}
else if(stat == "pending"){
	var x = document.getElementById("snackbar");
	x.innerHTML = "Your Payment is still Pending!";
	x.className = "show";
	setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
}

if(paid == "false"){
	var x = document.getElementById("snackbar");
	x.innerHTML = "You first need to buy any pass to register for the event!";
	x.className = "show";
	x.style.backgroundColor = "red";
	setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
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
	pass_btn_1500 = document.getElementById("get_pass_1500");
	pass_btn_2500 = document.getElementById("get_pass_2500");
	pass_div_499 = document.getElementById("pass-tile-499");
	pass_div_2299 = document.getElementById("pass-tile-2299");
	pass_div_1500 = document.getElementById("pass-tile-1500");
	pass_div_2500 = document.getElementById("pass-tile-2500");
	add_accomodation_btn = document.getElementById("add_accomodation_btn");
	upper_btn_div = document.getElementById("upper_btn_div");

	console.log(res);

	if(res.data.userprofile.amount_paid){
		if(res.data.userprofile.pronites){
			pass_btn_499.disabled = true;
			pass_btn_2299.disabled = true;
			pass_btn_1500.disabled = true;
			pass_btn_2500.disabled = true;

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
					upper_btn_div.style.margin = "0px auto 20px";
					add_accomodation_btn.style.display = "block";
					add_accomodation_btn.addEventListener("click", function(){
						openModal('1000.00');
					});
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
					upper_btn_div.style.margin = "0px auto 20px";
					add_accomodation_btn.style.display = "block";
					add_accomodation_btn.addEventListener("click", function(){
						openModal('1800.00');
					});
				}
			}
		}
	}
}

let payButtonList = document.getElementsByClassName("pay-btn");
for(let i of payButtonList){
	i.addEventListener("click", function(e){
		openModal(e.target.value);
	})
}

var modal = document.getElementById("myModal");
var promoModal = document.getElementById("promoModal");
var span = document.getElementsByClassName("close")[0];
var close_promo = document.getElementsByClassName("close")[1];
var submit_button = document.getElementById("submit_button");

// When the user clicks the button, open the modal
function openModal(pay_amount){
	submit_button.disabled = false;
	submit_button.style.backgroundColor = "#1d3557";

	if(pay_amount == "499.00"){
		document.getElementById("modal_pass_amount").innerHTML = `<span>Amount: </span>Rs. 499.00`;
		document.getElementById("modal_pass_details").innerHTML = `<span>Details: </span> This pass includes access to all the events except flagship events, and includes silver lane pass for all pronites.`;
	}
	else if(pay_amount == "2299.00"){
		document.getElementById("modal_pass_amount").innerHTML = `<span>Amount: </span>Rs. 2299.00`;
		document.getElementById("modal_pass_details").innerHTML = `<span>Details: </span> This pass includes access to all the events except flagship events, includes silver lane pass to all pronites and an accomodation for 4 nights.`;
	}
	else if(pay_amount == "1500.00"){
		document.getElementById("modal_pass_amount").innerHTML = `<span>Amount: </span>Rs. 1500.00`;
		document.getElementById("modal_pass_details").innerHTML = `<span>Details: </span> This pass includes registration fee of IGMUN, and includes silver lane pass for last 2 pronites.`;
	}
	else if(pay_amount == "2500.00"){
		document.getElementById("modal_pass_amount").innerHTML = `<span>Amount: </span>Rs. 2500.00`;
		document.getElementById("modal_pass_details").innerHTML = `<span>Details: </span> This pass includes registration fee of IGMUN, includes silver lane pass for last 2 pronites and an accomodation for last 2 nights.`;
	}
	else if(pay_amount == "1000.00"){
		document.getElementById("modal_pass_amount").innerHTML = `<span>Amount: </span>Rs. 1000.00`;
		document.getElementById("modal_pass_details").innerHTML = `<span>Details: </span> This will add an accomodation for last 2 nights to your pass.`;
	}
	else if(pay_amount == "1800.00"){
		document.getElementById("modal_pass_amount").innerHTML = `<span>Amount: </span>Rs. 1800.00`;
		document.getElementById("modal_pass_details").innerHTML = `<span>Details: </span> This will add an accomodation for 4 nights to your pass.`;
	}

	modal.style.display = "block";
	document.getElementById("submit_button").value = pay_amount;
};


submit_button.addEventListener("click", function(e){
	var promo_code = document.getElementById("promo_code").value;
	var pay_amount = e.target.value;

	pay(pay_amount, promo_code);
});

// When the user clicks on (x), close the modal
span.onclick = function () {
	modal.style.display = "none";
	document.getElementById("promo_code").value = '';
};

close_promo.onclick = function () {
	promoModal.style.display = "none";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
	if (event.target == modal) {
		modal.style.display = "none";
		document.getElementById("promo_code").value = '';
	}
	else if(event.target == promoModal){
		promoModal.style.display = "none";
	}
};

function pay(pay_amount, promo_code){
	submit_button.disabled = true;
	submit_button.style.backgroundColor = "grey";

	var body = {
		amount: pay_amount,
		pay_for: "pass-" + pay_amount,
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