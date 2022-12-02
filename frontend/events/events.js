let colors = ["#F1C270", "#32AFA5", "#7F5690", "#97A19C", "#F66C40"];
const sec = document.querySelectorAll(".sec");
const btmNavBtns = document.querySelector(".bottom-nav").children;
const events_btns = document.getElementsByClassName("evBtn");

const lightBox = document.querySelector(".lightbox");
const lbCloseBtn = document.querySelector(".close");
const lbImg = document.getElementById("lbImg");


for(let i=0; i<events_btns.length; i++){
  events_btns[i].addEventListener("click", ()=>{
    lightBox.style.display = "block";
    let key = events_btns[i].innerHTML.toLowerCase();
    key = key.split(" ").join("");
    lbImg.src = `../static/events/${key}.jpeg`
  })
}

lbCloseBtn.addEventListener("click", ()=>{
  lightBox.style.display = "none";
})

lightBox.addEventListener("click", ()=>{
  if(lightBox.style.display != "none"){
    lightBox.style.display = "none";
  }
})

for(let i=0; i<5; i++){
  sec[i].style.backgroundColor = colors[i];
  btmNavBtns[i].style.backgroundColor = colors[i];
  btmNavBtns[i].addEventListener("click", ()=>{
    window.scrollTo(0, window.innerHeight*i);
  })
}

window.addEventListener("scroll", (e)=>{
  let idx = Math.ceil(window.scrollY/window.innerHeight);
  btmNavBtns[idx].style.fontWeight = "800";
  for(let j=0; j<5; j++){
    if(j!=idx){
      btmNavBtns[j].style.fontWeight = "400";
    }
  }
})



$(document).ready(function(){
	$('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function(){
		$(this).toggleClass('open');
    $(".res-nav").toggleClass("opened");
	});
});


