ScrollReveal({ reset: true });

ScrollReveal().reveal(".left", ".right", ".image", ".image2", ".passes", ".prizes", {
  reset: false
});

ScrollReveal().reveal(".title", {
  duration: 3000,
  origin: "top",
  distance: "400px",
  easing: "cubic-bezier(0.5, 0, 0, 1)",
  rotate: {
    x: 20,
    z: -10
  }
});

ScrollReveal().reveal(".left", {
  duration: 2000,
  move: 0
});

ScrollReveal().reveal(".right", {
    duration: 2000,
    move: 0
  });

  ScrollReveal().reveal(".image", {
    duration: 3000,
    move: 0
  });

  ScrollReveal().reveal(".image2", {
    duration: 3000,
    move: 0
  });

  ScrollReveal().reveal(".passes", {
    duration: 500,
    move: 0,
    delay: 500,
  });

  ScrollReveal().reveal(".prizes", {
    duration: 500,
    move: 0,
    delay: 500,
  });

  ScrollReveal().reveal(".certificate", {
    duration: 500,
    move: 0,
    delay: 500,
  });

  ScrollReveal().reveal(".merchandise", {
    duration: 500,
    move: 0,
    delay: 500,
  });

  ScrollReveal().reveal(".workshop", {
    duration: 500,
    move: 0,
    delay: 500,
  });

  ScrollReveal().reveal(".celebrities", {
    duration: 500,
    move: 0,
    delay: 500,
  });

ScrollReveal().reveal("", {
  duration: 2000,
  origin: "right",
  distance: "300px",
  easing: "ease-in-out"
});

const res_nav = document.querySelector(".res-nav");

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

var ca_register_btn = document.getElementById("ca_register_btn");
var referral_code = document.getElementById("referral_code");

if(getCookie("LoggedIn") == "True"){
  if(getCookie("isProfileComplete") == "True"){
    if(getCookie("isCA") == "True"){
      ca_register_btn.innerHTML = "<a>Registered!</a>";
      referral_code.innerHTML = `Referral Code: <b style="font-size: larger;">${getCookie("ignusID")}</b>`
    }
  }
  else{
    ca_register_btn.innerHTML = "<a href='../complete-profile/index.html'>CA Register</a>";
  }
}
else{
  ca_register_btn.innerHTML = "<a href='../login.html'>CA Register</a>";
}

// API
const BASE_URL = "https://api.ignus.co.in/"; 
const URL_USER_AUTHENTICATE= "api/accounts/login/";
const URL_REFRESH_TOKEN="api/accounts/refresh/";

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
        }).catch((error) => {window.location.href="/login.html"});
    }
    return Promise.reject(error);
});

ca_register_btn.addEventListener("click", function(){
  if(getCookie("LoggedIn") == "True"){
    if(getCookie("isProfileComplete") == "True"){
      if(getCookie("isCA") == "False"){
        miAPI.post("api/accounts/ca-register/", null, {
          headers: {
            'Content-type': 'application/json; charset=UTF-8',
            // 'X-CSRFToken': getCookie('csrftoken'),
          },
          withCredentials: true,
        }
        ).then(function(response){
          // ca_register_btn.innerHTML = "<a>Registered!</a>";
          window.location.replace("../ca/ca.html");
          sessionStorage.setItem("showmsg", "Successfully Registered as CA");
        }).catch(function(error){
          if(error.response.status == 403){
            sessionStorage.setItem("showmsg", error.response.data.error);
            window.location.replace("../ca/ca.html");
          }
          else if(error.response.status == 402){
            sessionStorage.setItem("showmsg", error.response.data.error);
            window.location.replace("../payment_steps/steps.html");
          }
        });
      }
    }
  }
});

if(sessionStorage.getItem("showmsg")=='Successfully Registered as CA'){
  var x = document.getElementById("snackbar");
  x.className = "show";
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
  sessionStorage.removeItem("showmsg");
}
