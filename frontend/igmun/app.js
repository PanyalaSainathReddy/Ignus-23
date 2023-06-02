// countdown js 
// var countDownDate = new Date("Feb 18, 2023 00:00:00").getTime();
// const countdownTiles = document.querySelectorAll('.countdown-tile')
// const days_cont = countdownTiles[0].children[0]
// const hours_cont = countdownTiles[1].children[0]
// const mins_cont = countdownTiles[2].children[0]
// const secs_cont = countdownTiles[3].children[0]
// var x = setInterval(function() {
//   var now = new Date().getTime();
//   var distance = countDownDate - now;

//   var days = Math.floor(distance / (1000 * 60 * 60 * 24));
//   var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
//   var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
//   var seconds = Math.floor((distance % (1000 * 60)) / 1000);
//   days_cont.innerHTML = days;
//   hours_cont.innerHTML = hours;
//   mins_cont.innerHTML = minutes;
//   secs_cont.innerHTML = seconds;
// }, 1000);

// responsive menu js 
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
      e.preventDefault();

      document.querySelector(this.getAttribute('href')).scrollIntoView({
          behavior: 'smooth'
      });
  });
});

const menuIcon = document.getElementById("menu-icon")

const resNav = document.querySelector(".res-nav")
let isOpen = false
menuIcon.addEventListener("click", (e)=>{
  if(!isOpen){
    isOpen = true;
    resNav.style.height = '100vh'; 
    menuIcon.src = './../static/igmun/close.png' 
  } else {
    isOpen = false;
    resNav.style.height = '0';
    menuIcon.src = './../static/igmun/menu.png'
  }
})
const resNavBtns = document.querySelectorAll(".res-nav-btns")
resNavBtns.forEach((btn)=>{
  btn.addEventListener("click", (e)=>{
    isOpen = false;
    resNav.style.height = '0'
    menuIcon.src = './../static/igmun/menu.png'
  })
})

// for(let i=0; i<4; i++){
//   resNavBtns[i].addEventListener("click", (e)=>{
//     isOpen = false;
//     resNav.style.height = '0';
//     menuIcon.src = './../static/igmun/menu.png'
//   })
// }

if(sessionStorage.getItem("showmsg")=='Successfully EB-Registered' || sessionStorage.getItem("showmsg")=='Successfully Pre-Registered for IGMUN' || sessionStorage.getItem("showmsg")=='Successfully Registered as Igmun CA!'){
  var x = document.getElementById("snackbar");
  x.innerHTML = sessionStorage.getItem("showmsg");
  x.className = "show";
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
  sessionStorage.removeItem("showmsg");
}
const nav_btns = document.querySelectorAll(".nav-btns")

window.addEventListener("scroll", (e)=>{
  if(window.scrollY > window.innerHeight*2){
    nav_btns.forEach((btn) => {
      btn.style.color = "grey";
      menuIcon.style.mixBlendMode = "difference";
    }) 
  } else {
    nav_btns.forEach((btn) => {
      btn.style.color = "#fff";
      menuIcon.style.mixBlendMode = "normal";
    })
  }
})

const cards = document.querySelectorAll(".card")
cards.forEach((card)=>{
  card.addEventListener("click", ()=>{
    document.querySelector(".person-details").style.display = "flex";
  })
})

// Get Cookie

// function getCookie(cname) {
// 	let name = cname + "=";
// 	let decodedCookie = decodeURIComponent(document.cookie);
// 	let ca = decodedCookie.split(';');
// 	for(let i = 0; i <ca.length; i++) {
// 	  let c = ca[i];
// 	  while (c.charAt(0) == ' ') {
// 		c = c.substring(1);
// 	  }
// 	  if (c.indexOf(name) == 0) {
// 		return c.substring(name.length, c.length);
// 	  }
// 	}
// 	return "";
// }

// var res_nav_get_pass_btn = document.getElementById("res_nav_get_pass_btn");
// var nav_get_pass_btn = document.getElementById("nav_get_pass_btn");

// if(getCookie("LoggedIn")){
//   res_nav_get_pass_btn.style.display = "block";
//   nav_get_pass_btn.style.display = "block";
// }