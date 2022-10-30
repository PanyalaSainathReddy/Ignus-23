let colors = ["#F1C270", "#32AFA5", "#7F5690", "#97A19C", "#F66C40"];
const sec = document.querySelectorAll(".sec");
const btmNavBtns = document.querySelector(".bottom-nav").children;
for(let i=0; i<5; i++){
  sec[i].style.backgroundColor = colors[i];
  btmNavBtns[i].style.backgroundColor = colors[i];
}

$(document).ready(function(){
	$('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function(){
		$(this).toggleClass('open');
    $(".res-nav").toggleClass("opened");
	});
});