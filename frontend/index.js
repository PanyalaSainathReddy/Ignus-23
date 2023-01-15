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


// code for setting section (scene) backgrounds
for(let i=0; i<7; i++){
  sec[i].style.background = `url('./static/scenebg/bg${i+1}sh.png')`;
  sec[i].style.backgroundRepeat = "no-repeat";
  sec[i].style.backgroundPosition = "bottom";
  sec[i].style.backgroundSize = "100vw";
}




// animations for non touchscreen devices 
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



// animations for touchscreen devices 
container.addEventListener("touchstart", touchStart, false);
container.addEventListener("touchmove", touchMove, false);
var start = {x:0, y:0};
function touchStart(event) {
  start.x = event.touches[0].pageX;
  start.y = event.touches[0].pageY;
}

function touchMove(event) {
  offset = {};
  offset.x = start.x - event.touches[0].pageX;
  offset.y = start.y - event.touches[0].pageY;
  
  event.preventDefault();
  container.scrollBy({
    left: offset.y *0.1,
  })
  body.style.backgroundColor = clrs[Math.floor(container.scrollLeft / window.innerWidth)];
  sun.style.top = `${5 + window.outerHeight/(window.outerWidth*35)*container.scrollLeft}vh`;
  moon.style.top = `${60 + window.outerHeight - 1*(window.outerHeight/(window.outerWidth*2.5)*((container.scrollLeft)-3.5*window.outerWidth))}px`;

}




// audio functionality 
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




// responsive menu toggle 
$(document).ready(function(){
	$('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function(){
		$(this).toggleClass('open');
    $(".res-nav").toggleClass("opened");
	});
});




// countdown timer section 4 
var countDownDate = new Date("Feb 16, 2023 00:00:00").getTime();
var days_cont = document.querySelector(".days").children[0];
var hours_cont = document.querySelector(".hours").children[0];
var mins_cont = document.querySelector(".mins").children[0];
var secs_cont = document.querySelector(".seconds").children[0];
var x = setInterval(function() {
  var now = new Date().getTime();
  var distance = countDownDate - now;

  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);


  // document.getElementById("demo").innerHTML = days + "d " + hours + "h "
  // + minutes + "m " + seconds + "s ";  
  days_cont.innerHTML = days;
  hours_cont.innerHTML = hours;
  mins_cont.innerHTML = minutes;
  secs_cont.innerHTML = seconds;
}, 1000);

if(sessionStorage.getItem("showmsg")=='Successfully pre-registered' || sessionStorage.getItem("showmsg")=='Successfully logged-out!'){
  var x = document.getElementById("snackbar");
  x.className = "show";
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
  sessionStorage.removeItem("showmsg");
}


// lightBox functionality 
const lightBox = document.querySelector(".lightbox");
const lbCloseBtn = document.querySelector(".close");
const lbImg = document.getElementById("lbImg");

lbCloseBtn.addEventListener("click", ()=>{
  lightBox.style.display = "none";
})

lightBox.addEventListener("click", ()=>{
  if(lightBox.style.display != "none"){
    lightBox.style.display = "none";
  }
})

document.querySelector(".prakriti-btn").addEventListener("click", ()=>{
  // lightBox.style.display = "block"
  window.location.href = "prakriti/prakriti.html";
})

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

var reg_get_pass_btn = document.querySelector("#reg_get_pass_btn");

if(getCookie("LoggedIn")){
  reg_get_pass_btn.innerHTML = "<button> Get Passes </button>";
  reg_get_pass_btn.href = "payment_steps/steps.html";
}


// aftermovie js
// const amLightbox = document.querySelector(".am-lightbox");
// const amClose = amLightbox.children[0];
// const amBtns = document.querySelectorAll(".am-btn")
// amBtns.forEach((btn)=>{
//   btn.addEventListener("click", (e)=>{
//     let year = btn.innerHTML.substring(0, 4);
//     amLightbox.style.display = "block";
//   })
// })
// amClose.addEventListener("click", ()=>{
//   amLightbox.style.display = "none";
//   document.querySelectorAll("iframe").forEach((ifr)=>{
//     // ifr.contentWindow.postMessage(JSON.stringify({ event: 'command', func: 'stopVideo' }), '*');
//     const source= ifr.src;
//     ifr.src = "";
//     ifr.src = source;
//   })
// })
// amLightbox.addEventListener("click", ()=>{
//   amLightbox.style.display = "none";
//   document.querySelectorAll("iframe").forEach((ifr)=>{
//     // ifr.contentWindow.postMessage(JSON.stringify({ event: 'command', func: 'stopVideo' }), '*');
//     const source= ifr.src;
//     ifr.src = "";
//     ifr.src = source;
//   })
// })




// stats js 

// let ctr = 0;
// container.addEventListener("wheel", (e)=>{
//   if(Math.floor(container.scrollLeft / window.innerWidth) >= 4 && ctr == 0){
//     document.querySelectorAll(".stats-tile").forEach((tile)=>{
//       const stat = tile.children[1].children[0];
//       let final_val = stat.innerHTML;
//       stat.innerHTML = 0;
//       // console.log(tile);
//       setInterval(()=>{
//         if(stat.innerHTML != final_val){
//           stat.innerHTML = parseInt(stat.innerHTML) + 1;
//         }
//       }, 50)
//     })
//     ctr = 1;
//   }
// })
