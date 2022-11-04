// toggle responsive navbar 
$(document).ready(function(){
	$('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function(){
    console.log("hye");
		$(this).toggleClass('open');
    $(".res-nav").toggleClass("opened");
	});
});

// blinking coming soon text 
var cstext = document.querySelector(".csimg");
let ct = 0;
setInterval(() => {
  if(ct == 0){
    cstext.src = "./../static/schedule/COMING SOON filled.png";
    ct = 1;
    
  }
  else if(ct == 1){
    cstext.src = "./../static/schedule/COMING SOON.png";
    ct = 0;
  }
}, 800);
