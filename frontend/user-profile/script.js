$(document).ready(function(){
	$('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function(){
    console.log("hye");
		$(this).toggleClass('open');
    $(".res-nav").toggleClass("opened");
	});
});

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

var logout_button = document.getElementById("logout_button");


// tooltip 
const ques = document.querySelector(".ques")
const tooltip = document.querySelector(".tooltip-text")
ques.addEventListener("mouseover", (e)=>{
	tooltip.style.visibility = "visible"
})
ques.addEventListener("mouseout", (e)=>{
	tooltip.style.visibility = "hidden";
})



// API
// const BASE_URL = "http://127.0.0.1:8000/"; 
// const URL_USER_AUTHENTICATE= "api/accounts/login/";
// const URL_REFRESH_TOKEN="api/accounts/refresh/";

// const miAPI = axios.create({
//     baseURL: BASE_URL,
//     withCredentials:true
// });

// miAPI.interceptors.response.use(function(response) {
//   return response;
// },function(error) {
//     console.log("error :" + JSON.stringify(error));

//     const originalReq = error.config;

//     if ( error.response.status == 401 && !originalReq._retry && error.response.config.url != URL_USER_AUTHENTICATE ) {
//       originalReq._retry = true;

//       return axios.post(BASE_URL+URL_REFRESH_TOKEN, null, {
//         withCredentials:true
//       }).then((res) =>{
//           if ( res.status == 200) {
//               console.log("token refreshed");
//               return axios(originalReq);
//           }
//         }).catch((error) => {window.location.href="/frontend/login.html"});
//     }
//     console.log("Rest promise error");
//     return Promise.reject(error);
// });

// function getUserProfileDetails() {
//   miAPI.get(BASE_URL + 'api/accounts/user-profile-details/', null, {
//     withCredentials: true,
//   }).then(function (response) {
//     console.log(response);
//     document.getElementById("user_name").innerHTML = response.data.user.first_name;
//     document.getElementById("ignus_id").innerHTML = response.data.userprofile.registration_code;
//     if(response.data.userprofile.current_year == 1){
//       document.getElementById("year_and_college").innerHTML = response.data.userprofile.current_year + "st year <br/>" + response.data.userprofile.college;
//     }
//     else if(response.data.userprofile.current_year == 2){
//       document.getElementById("year_and_college").innerHTML = response.data.userprofile.current_year + "nd year <br/>" + response.data.userprofile.college;
//     }
//     else if(response.data.userprofile.current_year == 3){
//       document.getElementById("year_and_college").innerHTML = response.data.userprofile.current_year + "rd year <br/>" + response.data.userprofile.college;
//     }
//     else if(response.data.userprofile.current_year == 4 || response.data.userprofile.current_year == 5){
//       document.getElementById("year_and_college").innerHTML = response.data.userprofile.current_year + "th year <br/>" + response.data.userprofile.college;
//     }
//     else{
//       document.getElementById("year_and_college").innerHTML = response.data.userprofile.college;
//     }
//     document.getElementById("state").innerHTML = states[response.data.userprofile.state];
//     document.getElementById("email").innerHTML = "Email ID: " + response.data.user.email;
//     document.getElementById("phone").innerHTML = "Contact No: " + response.data.userprofile.phone;
//     if(response.data.userprofile.gender == "M"){
//       document.getElementById("gender").innerHTML = "Gender: Male";
//     }
//     else if(response.data.userprofile.gender == "F"){
//       document.getElementById("gender").innerHTML = "Gender: Female";
//     }
//     else{
//       document.getElementById("gender").innerHTML = "Gender: Others";
//     }
//     document.getElementById("qr_code").innerHTML = response.data.userprofile.qr_code;
//     document.getElementById("pass_user_name_and_id").innerHTML = response.data.user.first_name + "<br/>" + response.data.userprofile.registration_code;
//   })
//   .catch(function (error) {
//     // handle error
//     console.log(error);
//     if(error.response.status == 500){
//       window.location.href="/frontend/complete-profile/index.html";
//     }
//   })
//   .finally(function () {
//     // always executed
//   })
// }

// logout_button.addEventListener('click', function(){
// 	console.log("logout");
//   miAPI.post(BASE_URL + 'api/accounts/logout/', null, {
//       headers: {
//         'Content-type': 'application/json; charset=UTF-8',
//         'X-CSRFToken': getCookie('csrftoken'),
//       },
//       withCredentials: true,
//     }
//   )
//   .then(function (response) {
//     console.log(response);
//     sessionStorage.setItem("showmsg", "Successfully registered");
//     window.location.replace("/frontend/index.html");
//   })
//   .catch(function (error) {
//     // handle error
//     console.log(error);
//   })
//   .finally(function () {
//     // always executed
//   })
// });