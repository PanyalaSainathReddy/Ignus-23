// API
var pre_register_form=document.getElementById('pre_register_form')

pre_register_form.addEventListener('submit', function(e){
  e.preventDefault()
  var full_name=document.getElementById('full_name').value
  var email=document.getElementById('email').value
  var phone_number=document.getElementById('phone_number').value
  var college=document.getElementById('college').value
  var college_state=document.getElementById('college_state').value
  var current_year=document.getElementById('current_year').value
  var por=document.getElementById('por').value
  var por_holder_contact=document.getElementById('por_holder_contact').value

  fetch('https://api.ignus.co.in/api/accounts/pre-register/', {
    method: 'POST',
    body: JSON.stringify({
        full_name:full_name,
        email:email,
        phone_number:phone_number,
        college:college,
        college_state:college_state,
        current_year:current_year,
        por:por,
        por_holder_contact:por_holder_contact,
    }),
    headers: {
      'Content-type': 'application/json; charset=UTF-8',
    }
    })
    .then(function(response){
        if(response.status==201){
            sessionStorage.setItem("showmsg", "Successfully pre-registered");
            window.location.replace("/index.html");
        }
        else{
            alert("This Email has already been pre-registered");
        }
    })
    .catch(error => console.error('Error:', error));
});