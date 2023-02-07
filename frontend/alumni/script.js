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

const params = new Proxy(new URLSearchParams(window.location.search), {
	get: (searchParams, prop) => searchParams.get(prop),
});

let stat = params.status;

if(stat == "success"){
  var x = document.getElementById("snackbar");
  x.innerHTML = "Thank you for your contribution!";
  x.className = "show";
  x.style.backgroundColor = "#4CAF50";
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
}
else if(stat == "failed"){
  var x = document.getElementById("snackbar");
  x.innerHTML = "Your Payment has been failed, try again!";
  x.className = "show";
  x.style.backgroundColor = "red";
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
}
else if(stat == "pending"){
	var x = document.getElementById("snackbar");
	x.innerHTML = "Your Payment is still Pending!";
	x.className = "show";
  x.style.backgroundColor = "red";
	setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
}

// froms tab funcitonality
const presence_btn = document.querySelector(".presence")
const contribution_btn = document.querySelector(".contribute")
const presence_form = document.getElementById("presence_form")
const contribution_form = document.getElementById("contribution_form")
var name_confirm = document.getElementById("name_confirm");
var email_confirm = document.getElementById("email_confirm");
var phone_confirm = document.getElementById("phone_confirm");
var year_confirm = document.getElementById("year_confirm");
var name_contribute = document.getElementById("name_contribute");
var email_contribute = document.getElementById("email_contribute");
var phone_contribute = document.getElementById("phone_contribute");
var year_contribute = document.getElementById("year_contribute");
var amount_contribute = document.getElementById("amount_contribute");
var remarks_contribute = document.getElementById("remarks_contribute");
var opinion_msg = document.getElementById("opinion_msg");
var confirmation_contribute = document.getElementById("confirmation_contribute");
var checkbox_confirmation_contribute = document.getElementById("checkbox_confirmation_contribute");

document.getElementById('presence_first_btn').addEventListener('click', function(){
  presence_btn.classList.add("active-btn")
  contribution_btn.classList.remove("active-btn")
  presence_form.style.display = "grid"
  contribution_form.style.display = "none"
});

document.getElementById('contribute_first_btn').addEventListener('click', function(){
  presence_btn.classList.remove("active-btn")
  contribution_btn.classList.add("active-btn")
  presence_form.style.display = "none"
  contribution_form.style.display = "grid"
});

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

presence_form.addEventListener("submit", (e)=>{
  e.preventDefault();
  var name = name_confirm.value;
  var email = email_confirm.value;
  var phone = phone_confirm.value;
  var year = year_confirm.value;

  body = {
    name: name,
    email: email,
    phone: phone,
    passing_year: year
  }

  fetch("https://api.ignus.co.in/api/payments/confirm-alumni-presence/", {
    method: "POST",
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json"
    }
  })
  .then(function(response){
    if(response.status == 201){
      var x = document.getElementById("snackbar");
      x.innerHTML = `Your presence has been confirmed!`;
      x.className = "show";
      x.style.backgroundColor = "#4CAF50";
      setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);

      presence_btn.classList.remove("active-btn");
      contribution_btn.classList.add("active-btn");
      presence_form.style.display = "none";
      contribution_form.style.display = "grid";
      presence_btn.disabled = true;

      name_contribute.value = name;
      email_contribute.value = email;
      phone_contribute.value = phone;
      year_contribute.value = year;
      name_contribute.disabled = true;
      email_contribute.disabled = true;
      phone_contribute.disabled = true;
      year_contribute.disabled = true;
      opinion_msg.style.display = "block";
      checkbox_confirmation_contribute.checked = false;
      confirmation_contribute.style.display = "none";
      document.getElementById('presence_first_btn').disabled = true;
    }
  })
  .catch(error => console.error('Error:', error));
});

contribution_form.addEventListener("submit", (e)=>{
  e.preventDefault();
  var name = name_contribute.value;
  var email = email_contribute.value;
  var phone = phone_contribute.value;
  var year = year_contribute.value;
  var amount = amount_contribute.value;
  var remarks = remarks_contribute.value;

  if(document.getElementById("checkbox_confirmation_contribute").checked == true){
    body = {
      name: name,
      email: email,
      phone: phone,
      passing_year: year
    }
  
    fetch("https://api.ignus.co.in/api/payments/confirm-alumni-presence/", {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json"
      }
    })
    .then(function(response){
      if(response.status == 201){
        body = {
          name: name,
          email: email,
          phone: phone,
          passing_year: year,
          amount: amount,
          remarks: remarks
        }
      
        fetch("https://api.ignus.co.in/api/payments/alumni-contribution/", {
          method: "POST",
          body: JSON.stringify(body),
          headers: {
            "Content-Type": "application/json"
          }
        })
        .then(function(response){
          if(response.status == 201){
            link = response.data.link;
            window.location.href = link;
          }
        })
        .catch(error => console.error('Error:', error));
      }
    })
    .catch(error => console.error('Error:', error));
  }
  else{
    body = {
      name: name,
      email: email,
      phone: phone,
      passing_year: year,
      amount: amount,
      remarks: remarks
    }
  
    fetch("https://api.ignus.co.in/api/payments/alumni-contribution/", {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json"
      }
    })
    .then(function(response){
      if(response.status == 201){
        link = response.data.link;
        window.location.href = link;
      }
    })
    .catch(error => console.error('Error:', error));
  }
});