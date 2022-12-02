const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');
const homeButton = document.getElementById('home');

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

// API
var sign_up_form=document.getElementById('sign_up_form')

sign_up_form.addEventListener('submit', function(e){
  e.preventDefault()
  var first_name=document.getElementById('first_name').value
  var last_name=document.getElementById('last_name').value
  var email_sign_up=document.getElementById('email_sign_up').value
  var password_sign_up=document.getElementById('password_sign_up').value

  fetch('https://api.ignus.co.in/api/accounts/register/', {
    method: 'POST',
    body: JSON.stringify({
      first_name:first_name,
      last_name:last_name,
      email:email_sign_up,
      password:password_sign_up,
    }),
    headers: {
      'Content-type': 'application/json; charset=UTF-8',
    }
    })
    .then(function(response){
    return response.json()})
    .then(function(data){
      console.log(data);
      localStorage.setItem('token', data.token);
      window.location.replace("/index.html");
  })
  .catch(error => console.error('Error:', error));
});

var sign_in_form=document.getElementById('sign_in_form')

sign_in_form.addEventListener('submit', function(e){
  e.preventDefault()
  var email_sign_in=document.getElementById('email_sign_in').value
  var password_sign_in=document.getElementById('password_sign_in').value

  fetch('https://api.ignus.co.in/api/api-token-auth/', {
    method: 'POST',
    body: JSON.stringify({
      username:email_sign_in,
      password:password_sign_in,
    }),
    headers: {
      'Content-type': 'application/json; charset=UTF-8',
    }
    })
    .then(function(response){
    return response.json()})
    .then(function(data){
      console.log(data);
      localStorage.setItem('token', data.token);
      window.location.replace("/index.html");
  })
  .catch(error => console.error('Error:', error));
});