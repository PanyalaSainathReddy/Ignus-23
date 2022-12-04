// API
var pre_register_form=document.getElementById('pre_register_form')

pre_register_form.addEventListener('submit', function(e){
  e.preventDefault()
  var full_name=document.getElementById('full_name').value
  var email=document.getElementById('email').value
  var phone_number=document.getElementById('phone_number').value
  var college=document.getElementById('college').value
  var city=document.getElementById('city').value
  var exp_delegate=document.getElementById('exp_delegate').value
  var committee=document.getElementById('committee').value

  fetch('https://api.ignus.co.in/api/igmun/preregform/', {
    method: 'POST',
    body: JSON.stringify({
        full_name:full_name,
        email:email,
        phone_number:phone_number,
        org:college,
        city:city,
        exp_delegate:exp_delegate,
        preferred_comm:committee,
    }),
    headers: {
      'Content-type': 'application/json; charset=UTF-8',
    }
    })
    .then(function(response){
        if(response.status==201){
            sessionStorage.setItem("showmsg", "Successfully pre-registered for IGMUN");
            window.location.replace("/igmun/index.html");
        }
        else{
            alert("This Email has already been pre-registered for igmun");
        }
    })
    .catch(error => console.error('Error:', error));
});