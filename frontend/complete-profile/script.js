$(document).ready(function(){
	$('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function(){
		$(this).toggleClass('open');
    $(".res-nav").toggleClass("opened");
	});
});

document.querySelector("#igmun-radio-btn").addEventListener("click", ()=>{
  document.querySelector(".expand_igmun").style.display = "block";
  document.querySelector(".expand").style.display = "none";
})

document.querySelector("#gold-radio-btn").addEventListener("click", ()=>{
  document.querySelector(".expand").style.display = "block";
  document.querySelector(".expand_igmun").style.display = "none";
})

document.querySelector("#silver-radio-btn").addEventListener("click", ()=>{
  document.querySelector(".expand").style.display = "block";
  document.querySelector(".expand_igmun").style.display = "none";
})

function getSelectedPass() {
  var ele = document.getElementsByName('pass');
    
  for(i = 0; i < ele.length; i++) {
      if(ele[i].checked){
        console.log(ele[i].value);
        return ele[i].value;
      }
  }
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

function check(){
  if(getCookie("LoggedIn") == ""){
    window.location.href = "/frontend/login.html";
  }
}

// API
const BASE_URL = "http://127.0.0.1:8000/"; 
const URL_USER_AUTHENTICATE= "api/accounts/login/";
const URL_REFRESH_TOKEN="api/accounts/refresh/";

const miAPI = axios.create({
    baseURL: BASE_URL,
    withCredentials:true
});

miAPI.interceptors.response.use(function(response) {
  return response;
},function(error) {
    console.log("error :" + JSON.stringify(error));

    const originalReq = error.config;

    if ( error.response.status == 401 && !originalReq._retry && error.response.config.url != URL_USER_AUTHENTICATE ) {
      originalReq._retry = true;

      return axios.post(BASE_URL+URL_REFRESH_TOKEN, null, {
        withCredentials:true
      }).then((res) =>{
          if ( res.status == 200) {
              console.log("token refreshed");
              return axios(originalReq);
          }
        }).catch((error) => {window.location.href="/frontend/login.html"});
    }
    console.log("Rest promise error");
    return Promise.reject(error);
});


var complete_profile_form=document.getElementById('complete_profile_form')

complete_profile_form.addEventListener('submit', function(e){
  e.preventDefault()
  var phone_number=document.getElementById('phone_number').value
  var college=document.getElementById('college').value
  var college_state=document.getElementById('college_state').value
  var current_year=document.getElementById('current_year').value
  var gender=document.getElementById('gender').value
  var pass=getSelectedPass()
  var referred_by=document.getElementById('referred_by').value
  var referred_by_igmun=document.getElementById('referred_by_igmun').value

  if(pass == "igmun-pass"){
    var body = {
      phone:phone_number,
      gender:gender,
      college:college,
      current_year:current_year,
      state:college_state,
      pass:pass,
      referred_by:'',
      referred_by_igmun:referred_by_igmun,
      igmun:true,
    }
  }
  else{
    var body = {
      phone:phone_number,
      gender:gender,
      college:college,
      current_year:current_year,
      state:college_state,
      pass:pass,
      referred_by:referred_by,
      referred_by_igmun:'',
      igmun:false,
    }
  }

  miAPI.post(BASE_URL + 'api/accounts/user-profile/', body, {
      headers: {
        'Content-type': 'application/json; charset=UTF-8',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      withCredentials: true,
    }
  )
  .then(function (response) {
    console.log(response);
    sessionStorage.setItem("showmsg", "Successfully registered");
    if(response.status == 201){
      window.location.replace("/frontend/index.html");
    }
  })
  .catch(function (error) {
    // handle error
    console.log(error);
  })
  .finally(function () {
    // always executed
  });
});