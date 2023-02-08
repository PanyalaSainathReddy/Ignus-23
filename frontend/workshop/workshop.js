// let colors = ["#F1C270", "#32AFA5", "#7F5690", "#97A19C", "#F66C40"];
// const sec = document.querySelectorAll(".sec");
// const btmNavBtns = document.querySelector(".bottom-nav").children;
const events_btns = document.getElementsByClassName("evBtn");

const lightBox = document.querySelector(".lightbox");
const lbCloseBtn = document.querySelector(".close");
const lbImg = document.getElementById("lbImg");

const res_nav = document.querySelector(".res-nav");

for(let i=0; i<events_btns.length; i++){
  events_btns[i].addEventListener("click", ()=>{
    let key = events_btns[i].innerHTML.toLowerCase();
    key = key.split(" ").join("");
    if(key == "pottery" || key == "phadpainting"){
      window.location.href = `../workshop-details/index.html?ref=${key}`;
    }
  })
}

$(document).ready(function(){
	$('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function(){
		$(this).toggleClass('open');
    $(".res-nav").toggleClass("opened");
	});
});
