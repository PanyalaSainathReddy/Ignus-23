// API
var ca_register_form=document.getElementById('ca_register_form')

ca_register_form.addEventListener('submit', function(e){
  e.preventDefault()
  var full_name=document.getElementById('full_name').value
  var email=document.getElementById('email').value
  var phone_number=document.getElementById('phone_number').value
  var college=document.getElementById('college').value
  var city=document.getElementById('city').value
  var college_state=document.getElementById('college_state').value
  var current_year=document.getElementById('current_year').value

  fetch('https://api.ignus.co.in/api/accounts/ca-pre-register/', {
    method: 'POST',
    body: JSON.stringify({
        full_name:full_name,
        email:email,
        phone_number:phone_number,
        college:college,
        city:city,
        college_state:college_state,
        current_year:current_year,
    }),
    headers: {
      'Content-type': 'application/json; charset=UTF-8',
    }
    })
    .then(function(response){
        if(response.status==201){
            sessionStorage.setItem("showmsg", "Successfully Registered as CA");
            window.location.replace("ca.html");
        }
        else{
            alert("This Email has already been registered for CA!");
        }
    })
    .catch(error => console.error('Error:', error));
});