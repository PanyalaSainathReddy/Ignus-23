const res_nav = document.querySelector(".res-nav");

$(document).ready(function(){
	$('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function(){
		$(this).toggleClass('open');
    $(".res-nav").toggleClass("opened");
	});
});

document.getElementById("button2").addEventListener("click", function(){
	window.location.href = "#steps";
});

document.getElementById("pay_btn_1").addEventListener("click", function(){
	window.open("https://www.onlinesbi.sbi/sbicollect/icollecthome.htm", "_blank");
});

document.getElementById("pay_btn_2").addEventListener("click", function(){
	window.open("https://www.onlinesbi.sbi/sbicollect/icollecthome.htm", "_blank");
});