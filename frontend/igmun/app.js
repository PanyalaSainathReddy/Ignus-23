// video animation on scroll 

  const intro = document.querySelector(".intro");
  const video = document.querySelector('video');
  const text = document.querySelector(".text-cont")
  


const controller = new ScrollMagic.Controller();
const scene = new ScrollMagic.Scene({
  duration: 4000,
  triggerElement: intro,
  triggerHook: 0
})
.setPin(intro)
.addTo(controller) 

// if(window.innerWidth < 900){
//   scene.removePin(true)
// }

    
let accelamt = 1;
let scrollpos = 0;
let delay = 0;
  

scene.on('update', e=>{
  scrollpos = e.scrollPos /1000;
})

setInterval(()=>{
  delay += (scrollpos - delay)*accelamt;
  video.currentTime = delay;
}, 33.3);




// countdown js 
var countDownDate = new Date("Feb 16, 2023 00:00:00").getTime();
const countdownTiles = document.querySelectorAll('.countdown-tile')
const days_cont = countdownTiles[0].children[0]
const hours_cont = countdownTiles[1].children[0]
const mins_cont = countdownTiles[2].children[0]
const secs_cont = countdownTiles[3].children[0]
var x = setInterval(function() {
  var now = new Date().getTime();
  var distance = countDownDate - now;

  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);
  days_cont.innerHTML = days;
  hours_cont.innerHTML = hours;
  mins_cont.innerHTML = minutes;
  secs_cont.innerHTML = seconds;
}, 1000);
