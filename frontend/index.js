const container = document.querySelector("#container")
const clrs = ["#b5d5e0", "#c8e1e5", "#ffee7a", "#ffee7a", "#f89e9d", "#7f5690", "#7f5690"];
// "#d46e93"
const sec = document.getElementsByTagName("section");
const body = document.getElementById("body");
const moon = document.getElementById("moon");
const sun = document.getElementById("sun");
const aud_btn = document.getElementById("aud");
const footer = document.querySelector(".footer");

// for(let i=0; i<7; i++){
//     // sec[i].style.background = `url('./static/scenebg/bg${i+1}sh.png')`;
//     sec[i].style.backgroundRepeat = "no-repeat";
//     sec[i].style.backgroundSize = "100vw ";
//     sec[i].style.backgroundPosition = "bottom";
  
// }


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
audio.autoplay = true;
document.body.appendChild(audio);
audio.src = "./static/arabicmusi.mp4";
audio.loop = true;


let aud_ct = 0;
aud_btn.addEventListener("click", ()=>{
  if(aud_ct%2 == 0){
    audio.play();
    aud_ct++;
    aud_btn.children[0].src = "./static/speaker-off-icon.webp";
    
  }
  else{
    audio.pause();
    aud_ct++;
    aud_btn.children[0].src = "./static/Speaker_Icon.svg.png";
  }
})


