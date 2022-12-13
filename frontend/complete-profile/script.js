$(document).ready(function(){
	$('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function(){
    console.log("hye");
		$(this).toggleClass('open');
    $(".res-nav").toggleClass("opened");
	});
});

const radioBtns = document.querySelectorAll(".radio-btn");
console.log(radioBtns);
radioBtns.forEach((btn)=>{
	btn.addEventListener("click", ()=>{
		document.querySelector(".expand").style.height = "fit-content";
	})
})