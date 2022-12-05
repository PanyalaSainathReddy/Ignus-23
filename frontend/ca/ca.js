ScrollReveal({ reset: true });

ScrollReveal().reveal(".left", ".right", ".image", ".image2", ".passes", ".prizes", {
  reset: false
});

ScrollReveal().reveal(".title", {
  duration: 3000,
  origin: "top",
  distance: "400px",
  easing: "cubic-bezier(0.5, 0, 0, 1)",
  rotate: {
    x: 20,
    z: -10
  }
});

ScrollReveal().reveal(".left", {
  duration: 2000,
  move: 0
});

ScrollReveal().reveal(".right", {
    duration: 2000,
    move: 0
  });

  ScrollReveal().reveal(".image", {
    duration: 3000,
    move: 0
  });

  ScrollReveal().reveal(".image2", {
    duration: 3000,
    move: 0
  });

  ScrollReveal().reveal(".passes", {
    duration: 500,
    move: 0,
    delay: 500,
  });

  ScrollReveal().reveal(".prizes", {
    duration: 500,
    move: 0,
    delay: 500,
  });

  ScrollReveal().reveal(".certificate", {
    duration: 500,
    move: 0,
    delay: 500,
  });

  ScrollReveal().reveal(".merchandise", {
    duration: 500,
    move: 0,
    delay: 500,
  });

  ScrollReveal().reveal(".workshop", {
    duration: 500,
    move: 0,
    delay: 500,
  });

  ScrollReveal().reveal(".celebrities", {
    duration: 500,
    move: 0,
    delay: 500,
  });






ScrollReveal().reveal("", {
  duration: 2000,
  origin: "right",
  distance: "300px",
  easing: "ease-in-out"
});

const res_nav = document.querySelector(".res-nav");

$(document).ready(function(){
	$('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function(){
		$(this).toggleClass('open');
    $(".res-nav").toggleClass("opened");
	});
});



