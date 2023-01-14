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
