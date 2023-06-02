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