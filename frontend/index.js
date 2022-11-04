const container = document.querySelector("#container")
const clrs = ["#b5d5e0", "#c8e1e5", "#ffee7a", "#ffee7a", "#f89e9d", "#7f5690", "#7f5690"];
// "#d46e93"
const sec = document.getElementsByTagName("section");
const body = document.getElementById("body");
const moon = document.getElementById("moon");
const sun = document.getElementById("sun");
const aud_btn = document.getElementById("aud");
const footer = document.querySelector(".footer");
const res_nav = document.querySelector(".res-nav");
var ca_or_login_button = document.getElementById("ca_or_login_button");
// var logout_button = document.getElementById("logout_button");

if(window.localStorage.getItem("token") != null){
  ca_or_login_button.innerHTML = "<button>LOGOUT</button>";
  ca_or_login_button.removeAttribute("href");
  // logout_button.style.display = "block";
}

ca_or_login_button.addEventListener("click", function(){
  if(window.localStorage.getItem("token") != null){
    window.localStorage.removeItem("token");
    window.location.href = "http://127.0.0.1:5500/frontend/index.html";
  }
});

for(let i=0; i<7; i++){
  sec[i].style.background = `url('./static/scenebg/bg${i+1}sh.png')`;
  sec[i].style.backgroundRepeat = "no-repeat";
  sec[i].style.backgroundPosition = "bottom";
  sec[i].style.backgroundSize = "100vw";
}

container.addEventListener("wheel", (e)=>{
  e.preventDefault();
  container.scrollBy({
    left: e.deltaY,
  })
  body.style.backgroundColor = clrs[Math.floor(container.scrollLeft / window.innerWidth)];
  sun.style.top = `${5 + window.outerHeight/(window.outerWidth*35)*container.scrollLeft}vh`;
  moon.style.top = `${60 + window.outerHeight - 1*(window.outerHeight/(window.outerWidth*2.5)*((container.scrollLeft)-3.5*window.outerWidth))}px`;
  if(Math.floor(container.scrollLeft / window.innerWidth) >= 5){
    footer.style.animation = "fadeUp 4s ease-in-out";
  }
});

var audio = document.createElement("audio");
audio.autoplay = false;
document.body.appendChild(audio);
audio.src = "./static/arabicmusi.mp4";
audio.loop = true;


let aud_ct = 0;
aud_btn.addEventListener("click", ()=>{
  if(aud_ct%2 == 0){
    audio.play();
    aud_ct++;
    aud_btn.children[0].src = "./static/Speaker_Icon.svg.png";
    
  }
  else{
    audio.pause();
    aud_ct++;
    aud_btn.children[0].src = "./static/speaker-off-icon.webp";
  }
})


$(document).ready(function(){
	$('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function(){
		$(this).toggleClass('open');
    $(".res-nav").toggleClass("opened");
	});
});



var countDownDate = new Date("Feb 16, 2023 00:00:00").getTime();
var days_cont = document.querySelector(".days").children[0];
var hours_cont = document.querySelector(".hours").children[0];
var mins_cont = document.querySelector(".mins").children[0];
var x = setInterval(function() {
  var now = new Date().getTime();
  var distance = countDownDate - now;

  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));

  // document.getElementById("demo").innerHTML = days + "d " + hours + "h "
  // + minutes + "m " + seconds + "s ";  
  days_cont.innerHTML = days;
  hours_cont.innerHTML = hours;
  mins_cont.innerHTML = minutes;

  
}, 1000);

if(sessionStorage.getItem("showmsg")=='Successfully pre-registered'){
  var x = document.getElementById("snackbar");
  x.className = "show";
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
  sessionStorage.removeItem("showmsg");
}