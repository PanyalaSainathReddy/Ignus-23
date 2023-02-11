$(document).ready(function(){
	$('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function(){
		$(this).toggleClass('open');
    $(".res-nav").toggleClass("opened");
	});
});

const params = new Proxy(new URLSearchParams(window.location.search), {
	get: (searchParams, prop) => searchParams.get(prop),
});

let stat = params.status;

if(stat == "success"){
  var x = document.getElementById("snackbar");
  x.innerHTML = "Your Payment has been Successful!";
  x.className = "show";
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
}

const states = ['', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttarakhand', 'Uttar Pradesh', 'West Bengal', 'Andaman and Nicobar Islands', 'Delhi', 'Chandigarh', 'Dadra and Nagar Haveli', 'Daman and Diu', 'Lakshadweep', 'Puducherry'];

function getCookie(cname) {
	let name = cname + "=";
	let decodedCookie = decodeURIComponent(document.cookie);
	let ca = decodedCookie.split(';');
	for(let i = 0; i <ca.length; i++) {
	  let c = ca[i];
	  while (c.charAt(0) == ' ') {
		c = c.substring(1);
	  }
	  if (c.indexOf(name) == 0) {
		return c.substring(name.length, c.length);
	  }
	}
	return "";
}


// tooltip 
// const ques = document.querySelector(".ques")
// const tooltip = document.querySelector(".tooltip-text")
// ques.addEventListener("mouseover", (e)=>{
// 	tooltip.style.visibility = "visible"
// })
// ques.addEventListener("mouseout", (e)=>{
// 	tooltip.style.visibility = "hidden";
// })

var get_pass_btn = document.getElementById("get_pass");
get_pass_btn.addEventListener("click", function(){
	window.location.href = "../payment_steps/steps.html";
});

var logout_button = document.getElementById("logout_button");

// API
const BASE_URL = "https://api.ignus.co.in/"; 
const URL_USER_AUTHENTICATE= "api/accounts/login/";
const URL_REFRESH_TOKEN="api/accounts/refresh/";

const miAPI = axios.create({
    baseURL: BASE_URL,
    withCredentials:true
});

miAPI.interceptors.response.use(function(response) {
  return response;
},function(error) {
    const originalReq = error.config;

    if ( error.response.status == 401 && !originalReq._retry && error.response.config.url != URL_USER_AUTHENTICATE ) {
      originalReq._retry = true;

      return axios.post(BASE_URL+URL_REFRESH_TOKEN, null, {
        withCredentials:true
      }).then((res) =>{
          if ( res.status == 200) {
              return axios(originalReq);
          }
        }).catch((error) => {window.location.href="/login.html"});
    }
    return Promise.reject(error);
});

function getUserProfileDetails() {
  miAPI.get(BASE_URL + 'api/accounts/user-profile-details/', null, {
    withCredentials: true,
  }).then(function (response) {
    if(response.data.user.is_google){
      if(response.data.user.google_picture == ""){
        document.getElementById("profile_pic").src = "./../static/user-profile/blank-profile-picture-973460_1280.webp";
      }
      else{
        document.getElementById("profile_pic").src = response.data.user.google_picture;
      }
    }
    else{
      if(response.data.userprofile.profile_pic == null){
        document.getElementById("profile_pic").src = "./../static/user-profile/blank-profile-picture-973460_1280.webp";
      }
      else{
        document.getElementById("profile_pic").src = BASE_URL + response.data.userprofile.profile_pic;
      }
    }
    document.getElementById("user_name").innerHTML = response.data.user.first_name;
    if(response.data.userprofile.is_ca){
      document.getElementById("ca").style.display = "block";
    }
    document.getElementById("ignus_id").innerHTML = `Ignus Id: ` + response.data.userprofile.registration_code;
    if(response.data.userprofile.current_year == 1){
      document.getElementById("year_and_college").innerHTML = response.data.userprofile.current_year + "st year <br/>" + response.data.userprofile.college;
    }
    else if(response.data.userprofile.current_year == 2){
      document.getElementById("year_and_college").innerHTML = response.data.userprofile.current_year + "nd year <br/>" + response.data.userprofile.college;
    }
    else if(response.data.userprofile.current_year == 3){
      document.getElementById("year_and_college").innerHTML = response.data.userprofile.current_year + "rd year <br/>" + response.data.userprofile.college;
    }
    else if(response.data.userprofile.current_year == 4 || response.data.userprofile.current_year == 5){
      document.getElementById("year_and_college").innerHTML = response.data.userprofile.current_year + "th year <br/>" + response.data.userprofile.college;
    }
    else{
      document.getElementById("year_and_college").innerHTML = response.data.userprofile.college;
    }
    document.getElementById("state").innerHTML = states[response.data.userprofile.state];
    document.getElementById("email").innerHTML = "Email ID: " + response.data.user.email;
    document.getElementById("phone").innerHTML = "Contact No: " + response.data.userprofile.phone;
    if(response.data.userprofile.gender == "M"){
      document.getElementById("gender").innerHTML = "Gender: Male";
    }
    else if(response.data.userprofile.gender == "F"){
      document.getElementById("gender").innerHTML = "Gender: Female";
    }
    else{
      document.getElementById("gender").innerHTML = "Gender: Others";
    }
    if(response.data.user.iitj){
      document.getElementById("flagship_container").style.display = 'block';
      document.getElementById("payment_status_note").innerHTML = `You are a verified IITJ student, participation in all pronites and events is free for you (if everyone in your team is a verified IITJ student), you can register for the events you are interested in on the events page.`;
      get_pass_btn.style.display = 'none';
    }
    else if(response.data.userprofile.amount_paid){
      get_pass_btn.style.display = 'none';
      if(response.data.userprofile.pronites){
        document.getElementById("pronite_pass").style.display = 'flex';
        if(response.data.userprofile.igmun){
          document.getElementById("pass_name").innerHTML = 'IGMUN';
          document.getElementById("pass_sub_name").innerHTML = '+ All Pronites';
        }
        if(response.data.userprofile.accomodation_4){
          document.getElementById("acc_yes_text").innerHTML = 'Accomodation(4 days)';
          document.getElementById("acc_yes").style.display = 'flex';
          document.getElementById("acc_no").style.display = 'none';
        }
        else if(response.data.userprofile.accomodation_2){
          document.getElementById("acc_yes_text").innerHTML = 'Accomodation(2 days)';
          document.getElementById("acc_yes").style.display = 'flex';
          document.getElementById("acc_no").style.display = 'none';
        }
        else{
          document.getElementById("acc_yes").style.display = 'none';
          document.getElementById("acc_no").style.display = 'flex';
        }
        document.getElementById("pronites_qr").innerHTML = response.data.userprofile.pronites_qr;
        document.getElementById("pass_user_name_and_id").innerHTML = response.data.user.first_name + "<br/>" + response.data.userprofile.registration_code;
      }
      if(response.data.userprofile.flagship){
        document.getElementById("flagship_container").style.display = 'block';
        var flagship_note = `You are the team leader of `;
        var first_flagship_event = true;
        if(response.data.userprofile.aayaam){
          if(first_flagship_event){
            flagship_note += `Aayaam`;
            first_flagship_event = false;
          }
          else{
            flagship_note += `, Aayaam`;
          }
        }
        else if(response.data.userprofile.antarang){
          if(first_flagship_event){
            flagship_note += `Antarang`;
            first_flagship_event = false;
          }
          else{
            flagship_note += `, Antarang`;
          }
        }
        else if(response.data.userprofile.nrityansh){
          if(first_flagship_event){
            flagship_note += `Nrityansh`;
            first_flagship_event = false;
          }
          else{
            flagship_note += `, Nrityansh`;
          }
        }
        else if(response.data.userprofile.cob){
          if(first_flagship_event){
            flagship_note += `Clash of Bands`;
            first_flagship_event = false;
          }
          else{
            flagship_note += `, Clash of Bands`;
          }
        }
        flagship_note += `.`;
        document.getElementById("payment_status_note").innerHTML = flagship_note;
      }
    }
    else{
      document.getElementById("pronite_pass").style.display = 'none';
      get_pass_btn.style.display = 'block';
    }
  })
  .catch(function (error) {
    // handle error
    if(error.response.status == 500){
      window.location.href="/complete-profile/index.html";
    }
  })
  .finally(function () {
    // always executed
  })
}

logout_button.addEventListener('click', function(){
  miAPI.post(BASE_URL + 'api/accounts/logout/', null, {
      headers: {
        'Content-type': 'application/json; charset=UTF-8',
        // 'X-CSRFToken': getCookie('csrftoken'),
      },
      withCredentials: true,
    }
  )
  .then(function (response) {
    sessionStorage.setItem("showmsg", "Successfully logged-out!");
    window.location.replace("/index.html");
  })
  .catch(function (error) {
    // handle error
    // console.log(error);
  })
  .finally(function () {
    // always executed
  })
});