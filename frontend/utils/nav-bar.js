// Get Cookie

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

var login_button = document.getElementById("login_button");
var login_button_mobile = document.getElementById("login_button_mobile");

if(getCookie("LoggedIn")){
  if(login_button.className == "nav-btns"){
    login_button.innerHTML = "Profile";
  }
  else{
    login_button.innerHTML = "<Button>PROFILE</Button>";
  }
  if(login_button_mobile.className == "res-nav-btns"){
    login_button_mobile.innerHTML = "Profile";
  }
  else{
    login_button_mobile.innerHTML = "<Button>PROFILE</Button>";
  }
  login_button.href = "/frontend/user-profile/index.html";
  login_button_mobile.href = "/frontend/user-profile/index.html";
}