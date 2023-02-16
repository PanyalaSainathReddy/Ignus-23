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

  if (document.getElementById('mob_password_sign_up').value == document.getElementById('mob_confirm_password_sign_up').value) {
    document.getElementById('mob_message').style.color = 'green';
    document.getElementById('mob_message').innerHTML = 'password matching';
  } else {
    document.getElementById('mob_message').style.color = 'red';
    document.getElementById('mob_message').innerHTML = 'password not matching!';
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

const button_1 = document.getElementById('button_1');
const button_2 = document.getElementById('button_2');

document.getElementById('button_2').addEventListener(
	'click',
	(theFunction = () => {
    button_2.style.backgroundColor='#fff'
    button_1.style.backgroundColor='#eee'
		let x = document.getElementById('login_form')
		x.style.display="none"
	})
)

document.getElementById('button_1').addEventListener(
	'click',
	(theFunction = () => {
    button_2.style.backgroundColor='#eee'
    button_1.style.backgroundColor='#fff'
    let y = document.getElementById('login_form')
		y.style.display="block"
	})
)





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

// function checkLoggedIn() {
//   if(getCookie("LoggedIn")){
//     window.location.replace("index.html");
//   }
// }

const params = new Proxy(new URLSearchParams(window.location.search), {
	get: (searchParams, prop) => searchParams.get(prop),
});

let error = params.Error;

if(error){
  var x = document.getElementById("snackbar");
  x.innerHTML = error;
  x.className = "show";
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
}

// API
const BASE_URL = "https://api.ignus.co.in/";
var sign_up_form=document.getElementById('sign_up_form')

function checkLoggedIn() {
  if(getCookie("LoggedIn")){
    fetch(BASE_URL + 'api/accounts/clear-cookies/', {
      method: 'POST',
      body: null,
      headers: {
        'Content-type': 'application/json; charset=UTF-8',
      }
    })
    .then(function(response){
      console.log("Cleared all cookies");
    })
    .catch(function(error){
      console.log(error);
    })
  }
}

sign_up_form.addEventListener('submit', function(e){
  e.preventDefault()
  if(document.getElementById('email_sign_up').value.substring(document.getElementById('email_sign_up').value.length - 10) == "iitj.ac.in"){
    var x = document.getElementById("snackbar");
    x.innerHTML = `IITJ Users can only use Google Sign up`;
    x.className = "show";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
  }
  else{
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
        if(data.Error != undefined){
          var x = document.getElementById("snackbar");
          x.innerHTML = data.Error;
          x.className = "show";
          setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
        }
      })
      .catch(error => console.error('Error:', error));
    }
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
      if(getCookie("isProfileComplete") == "True"){
        window.location.replace("index.html");
      }
      else{
        window.location.replace("complete-profile/index.html");
      }
    }
    return response.json()
  })
  .then(function(data){
    if(data.Error != undefined){
      var x = document.getElementById("snackbar");
      x.innerHTML = data.Error;
      x.className = "show";
      setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
    }
  })
  .catch(error => console.error('Error:', error));
});

// Mobile Sign Up & Sign In

var mob_sign_up_form=document.getElementById('mob_sign_up_form')

mob_sign_up_form.addEventListener('submit', function(e){
  e.preventDefault()
  if(document.getElementById('mob_email_sign_up').value.substring(document.getElementById('mob_email_sign_up').value.length - 10) == "iitj.ac.in"){
    var x = document.getElementById("snackbar");
    x.innerHTML = `IITJ Users can only use Google Sign up`;
    x.className = "show";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
  }
  else{
    if(document.getElementById('mob_password_sign_up').value == document.getElementById('mob_confirm_password_sign_up').value){
      var first_name=document.getElementById('mob_first_name').value
      var last_name=document.getElementById('mob_last_name').value
      var email_sign_up=document.getElementById('mob_email_sign_up').value
      var password_sign_up=document.getElementById('mob_password_sign_up').value
  
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
        if(data.Error != undefined){
          var x = document.getElementById("snackbar");
          x.innerHTML = data.Error;
          x.className = "show";
          setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
        }
      })
      .catch(error => console.error('Error:', error));
    }
  }
});

var mob_sign_in_form=document.getElementById('mob_sign_in_form')

mob_sign_in_form.addEventListener('submit', function(e){
  e.preventDefault()
  var email_sign_in=document.getElementById('mob_email_sign_in').value
  var password_sign_in=document.getElementById('mob_password_sign_in').value

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
      if(getCookie("isProfileComplete") == "True"){
        window.location.replace("index.html");
      }
      else{
        window.location.replace("complete-profile/index.html");
      }
    }
    return response.json()
  })
  .then(function(data){
    if(data.Error != undefined){
      var x = document.getElementById("snackbar");
      x.innerHTML = data.Error;
      x.className = "show";
      setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
    }
  })
  .catch(error => console.error('Error:', error));
});

// Google Sign Up & Sign In

const CLIENT_ID = '37422384939-2d3r237achmdifp8hujd120h0bthbrr4.apps.googleusercontent.com';

var google_sign_up_button=document.getElementById('google_sign_up_button');
var mob_google_sign_up_button=document.getElementById('mob_google_sign_up_button');

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

mob_google_sign_up_button.addEventListener('click', function() {
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
var mob_google_sign_in_button=document.getElementById('mob_google_sign_in_button');

google_sign_in_button.addEventListener('click', function(){
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

mob_google_sign_in_button.addEventListener('click', function(){
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
