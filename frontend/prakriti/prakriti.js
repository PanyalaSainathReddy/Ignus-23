

const res_nav = document.querySelector(".res-nav");

$(document).ready(function(){
	$('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function(){
		$(this).toggleClass('open');
    $(".res-nav").toggleClass("opened");
	});
});

// for heading

(window).scroll(function() {
    const 
      a = (this).scrollTop(),
      b = 800;
    $("h1").css({
      backgroundPosition: "center " + a / 2 + "px" 
    });
    $(".parallax").css({ 
      top: a / 1.6 + "px", 
      opacity: 1 - a / b 
    });
  });
  
  // parallax scrolling
  
  document.addEventListener("scroll", () => {
    const 
      top = window.pageYOffset,
      one = document.querySelector(".one"),
      two = document.querySelector(".two"),
      three = document.querySelector(".three"),
      four = document.querySelector(".four"),
      five = document.querySelector(".five");
  
    one.style.bottom = -(top * 0.1) + "px";
    two.style.bottom = -(top * 0.2) + "px";
    three.style.bottom = -(top * 0.3) + "px";
    four.style.bottom = -(top * 0.4) + "px";
    five.style.bottom = -(top * 0.5) + "px";
  });
  
  /*
  // mouse dependency
  
  const currentX = '';
  const currentY = '';
  const movementConstant = 0.015;
  $(document).mousemove(function(e) {
    if (currentX == '') currentX = e.pageX;
    const xdiff = e.pageX - currentX;
    currentX = e.pageX;
    if (currentY == '') currentY = e.pageY;
    const ydiff = e.pageY - currentY;
    currentY = e.pageY;
  $('.parallax div').each(function(i, el) {
      const movement = (i + 1) * (xdiff * movementConstant);
      const movementy = (i + 1) * (ydiff * movementConstant);
      const newX = $(el).position().left + movement;
      const newY = $(el).position().top + movementy;
      $(el).css('left', newX + 'px');
      $(el).css('top', newY + 'px');
    });
  });
  */

  var index = 0;
  var slides = document.querySelectorAll(".slides");
  var dot = document.querySelectorAll(".dot");
  
  function changeSlide(){
  
    if(index<0){
      index = slides.length-1;
    }
  
    if(index>slides.length-1){
      index = 0;
    }
  
    for(let i=0;i<slides.length;i++){
      slides[i].style.display = "none";
      dot[i].classList.remove("active");
    }
  
    slides[index].style.display= "block";
    dot[index].classList.add("active");
  
    index++;
  
    setTimeout(changeSlide,2000);
  
  }
  
  changeSlide();

  function inVisible(element) {
    //Checking if the element is
    //visible in the viewport
    var WindowTop = $(window).scrollTop();
    var WindowBottom = WindowTop + $(window).height();
    var ElementTop = element.offset().top;
    var ElementBottom = ElementTop + element.height();
    //animating the element if it is
    //visible in the viewport
    if ((ElementBottom <= WindowBottom) && ElementTop >= WindowTop)
      animate(element);
  }
  
  function animate(element) {
    //Animating the element if not animated before
    if (!element.hasClass('ms-animated')) {
      var maxval = element.data('max');
      var html = element.html();
      element.addClass("ms-animated");
      $({
        countNum: element.html()
      }).animate({
        countNum: maxval
      }, {
        //duration 5 seconds
        duration: 1000,
        easing: 'linear',
        step: function() {
          element.html(Math.floor(this.countNum) + html);
        },
        complete: function() {
          element.html(this.countNum + html);
        }
      });
    }
  
  }
  
  //When the document is ready
  $(function() {
    //This is triggered when the
    //user scrolls the page
    $(window).scroll(function() {
      //Checking if each items to animate are 
      //visible in the viewport
      $("h2[data-max]").each(function() {
        inVisible($(this));
      });
    })
  });
  
  