const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');
const homeButton = document.getElementById('home');

var matchPassword = function() {
  if (document.getElementById('password_sign_up').value == document.getElementById('confirm_password_sign_up').value) {
    document.getElementById('message').style.color = 'green';
    document.getElementById('message').innerHTML = 'password matching';
  } else {
    document.getElementById('message').style.color = 'red';
    document.getElementById('message').innerHTML = 'password not matching!';
  }
}

homeButton.addEventListener('click', () => {
  window.location.replace("/index.html");
});

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});

const login = document.getElementById("login");
const register = document.getElementById("register");
const button = document.getElementById("btn");

function moveRegister() {
  login.style.left = "-400px";
  register.style.left = "50px";
  button.style.left = "110px";
}

function moveLogin() {
  login.style.left = "50px";
  register.style.left = "450px";
  button.style.left = "0";
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

function checkLoggedIn() {
  if(getCookie("LoggedIn")){
    window.location.replace("index.html");
  }
}

// API
const BASE_URL = "http://127.0.0.1:8000/";
var sign_up_form=document.getElementById('sign_up_form')

sign_up_form.addEventListener('submit', function(e){
  e.preventDefault()
  if(document.getElementById('password_sign_up').value == document.getElementById('confirm_password_sign_up').value){
    var first_name=document.getElementById('first_name').value
    var last_name=document.getElementById('last_name').value
    var email_sign_up=document.getElementById('email_sign_up').value
    var password_sign_up=document.getElementById('password_sign_up').value

    fetch(BASE_URL + 'api/accounts/register/', {
      method: 'POST',
      body: JSON.stringify({
        first_name:first_name,
        last_name:last_name,
        email:email_sign_up,
        password:password_sign_up,
      }),
      credentials: 'include',
      headers: {
        'Content-type': 'application/json; charset=UTF-8',
      }
    })
    .then(function(response){
      if(response.status == 200){
        window.location.replace("complete-profile/index.html");
      }
      return response.json()
    })
    .then(function(data){
      console.log(data);
    })
    .catch(error => console.error('Error:', error));
  }
});

var sign_in_form=document.getElementById('sign_in_form')

sign_in_form.addEventListener('submit', function(e){
  e.preventDefault()
  var email_sign_in=document.getElementById('email_sign_in').value
  var password_sign_in=document.getElementById('password_sign_in').value

  fetch(BASE_URL + 'api/accounts/login/', {
    method: 'POST',
    body: JSON.stringify({
      username:email_sign_in,
      password:password_sign_in,
    }),
    credentials: 'include',
    headers: {
      'Content-type': 'application/json; charset=UTF-8',
    }
  })
  .then(function(response){
    if(response.status == 200){
      window.location.replace("index.html");
    }
    return response.json()
  })
  .then(function(data){
      console.log(data);
  })
  .catch(error => console.error('Error:', error));
});

const CLIENT_ID = '590434107360-00fhk8vg36d7nsru0oo9n1rpbh9ot6k9.apps.googleusercontent.com';

var google_sign_up_button=document.getElementById('google_sign_up_button');

google_sign_up_button.addEventListener('click', function() {
  const googleAuthUrl = 'https://accounts.google.com/o/oauth2/v2/auth';
  const redirectUri = 'api/accounts/register/google/';

  const scope = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
  ].join(' ');

  const params = {
    response_type: 'code',
    client_id: CLIENT_ID,
    redirect_uri: BASE_URL + redirectUri,
    prompt: 'select_account',
    access_type: 'online',
    scope
  };

  const urlParams = new URLSearchParams(params).toString();

  window.location = `${googleAuthUrl}?${urlParams}`;
});


var google_sign_in_button=document.getElementById('google_sign_in_button');

google_sign_in_button.addEventListener('click', function() {
  const googleAuthUrl = 'https://accounts.google.com/o/oauth2/v2/auth';
  const redirectUri = 'api/accounts/login/google/';

  const scope = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
  ].join(' ');

  const params = {
    response_type: 'code',
    client_id: CLIENT_ID,
    redirect_uri: BASE_URL + redirectUri,
    prompt: 'select_account',
    access_type: 'online',
    scope
  };

  const urlParams = new URLSearchParams(params).toString();

  window.location = `${googleAuthUrl}?${urlParams}`;
});