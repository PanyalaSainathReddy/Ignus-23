// API
var eb_register_form=document.getElementById('eb_register_form')

eb_register_form.addEventListener('submit', function(e){
  e.preventDefault()
  var full_name=document.getElementById('full_name').value
  var email=document.getElementById('email').value
  var phone_number=document.getElementById('phone_number').value
  var college=document.getElementById('college').value
  var address=document.getElementById('address').value
  var exp_eb=document.getElementById('exp_eb').value
  var exp_delegate=document.getElementById('exp_delegate').value
  var committee=document.getElementById('committee').value

  fetch('https://api.ignus.co.in/api/igmun/ebform/', {
    method: 'POST',
    body: JSON.stringify({
        full_name:full_name,
        email:email,
        phone_number:phone_number,
        org:college,
        permanent_address:address,
        exp_eb:exp_eb,
        exp_delegate:exp_delegate,
        preferred_comm:committee,
    }),
    headers: {
      'Content-type': 'application/json; charset=UTF-8',
    }
    })
    .then(function(response){
        if(response.status==201){
            sessionStorage.setItem("showmsg", "Successfully eb-registered");
            window.location.replace("/igmun/index.html");
        }
        else{
            alert("This Email has already been registered");
        }
    })
    .catch(error => console.error('Error:', error));
});