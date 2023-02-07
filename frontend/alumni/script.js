$(document).ready(function(){
	$('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function(){
    // console.log("hye");
		$(this).toggleClass('open');
    $(".res-nav").toggleClass("opened");
	});
});

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
      e.preventDefault();

      document.querySelector(this.getAttribute('href')).scrollIntoView({
          behavior: 'smooth'
      });
  });
});




// froms tab funcitonality
const presence_btn = document.querySelector(".presence")
const contribution_btn = document.querySelector(".contribute")
const presence_form = document.querySelector(".presence-form")
const contribution_form = document.querySelector(".contribution-form")
const submit_btn = document.querySelector(".submit-btn")


presence_btn.addEventListener("click", ()=>{
  presence_btn.classList.add("active-btn")
  contribution_btn.classList.remove("active-btn")
  presence_form.style.display = "grid"
  contribution_form.style.display = "none"
  
})
contribution_btn.addEventListener("click", ()=>{
  presence_btn.classList.remove("active-btn")
  contribution_btn.classList.add("active-btn")
  presence_form.style.display = "none"
  contribution_form.style.display = "grid"

})