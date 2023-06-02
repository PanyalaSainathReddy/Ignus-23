$(document).ready(function () {
  $('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function () {
    $(this).toggleClass('open');
    $(".res-nav").toggleClass("opened");
  });
});

// document.querySelector("#igmun-radio-btn").addEventListener("click", () => {
//   document.querySelector(".expand_igmun").style.display = "block";
//   document.querySelector(".expand").style.display = "none";
// })

// document.querySelector("#gold-radio-btn").addEventListener("click", () => {
//   document.querySelector(".expand").style.display = "block";
//   document.querySelector(".expand_igmun").style.display = "none";
// })

// document.querySelector("#silver-radio-btn").addEventListener("click", () => {
//   document.querySelector(".expand").style.display = "block";
//   document.querySelector(".expand_igmun").style.display = "none";
// })

var igmun_checkbox = document.querySelector("#igmun_checkbox");
var expand_igmun = document.querySelector(".expand_igmun");

igmun_checkbox.addEventListener("click", () => {
  if(expand_igmun.style.display == "block"){
    document.querySelector(".expand_igmun").style.display = "none";
  }
  else{
    document.querySelector(".expand_igmun").style.display = "block";
  }
})

// function getSelectedPass() {
//   var ele = document.getElementsByName('pass');

//   for (i = 0; i < ele.length; i++) {
//     if (ele[i].checked) {
//       console.log(ele[i].value);
//       return ele[i].value;
//     }
//   }
// }

// function getCookie(cname) {
//   let name = cname + "=";
//   let decodedCookie = decodeURIComponent(document.cookie);
//   let ca = decodedCookie.split(';');
//   for (let i = 0; i < ca.length; i++) {
//     let c = ca[i];
//     while (c.charAt(0) == ' ') {
//       c = c.substring(1);
//     }
//     if (c.indexOf(name) == 0) {
//       return c.substring(name.length, c.length);
//     }
//   }
//   return "";
// }

// function check() {
//   if (getCookie("LoggedIn") == "") {
//     window.location.replace("../login.html");
//   }
//   // else{
//   //   if(getCookie("isProfileComplete") == "True"){
//   //     window.location.replace("../user-profile/index.html");
//   //   }
//   // }
// }

// API
// const BASE_URL = "https://api.ignus.co.in/";
// const URL_USER_AUTHENTICATE = "api/accounts/login/";
// const URL_REFRESH_TOKEN = "api/accounts/refresh/";

// const miAPI = axios.create({
//   baseURL: BASE_URL,
//   withCredentials: true
// });

// miAPI.interceptors.response.use(function (response) {
//   return response;
// }, function (error) {
//   const originalReq = error.config;

//   if (error.response.status == 401 && !originalReq._retry && error.response.config.url != URL_USER_AUTHENTICATE) {
//     originalReq._retry = true;

//     return axios.post(BASE_URL + URL_REFRESH_TOKEN, null, {
//       withCredentials: true
//     }).then((res) => {
//       if (res.status == 200) {
//         return axios(originalReq);
//       }
//     }).catch((error) => { window.location.href = "/login.html" });
//   }
//   return Promise.reject(error);
// });


// var complete_profile_form = document.getElementById('complete_profile_form')

// complete_profile_form.addEventListener('submit', function (e) {
//   e.preventDefault()
//   var phone_number = document.getElementById('phone_number').value
//   var college = document.getElementById('college').value
//   var college_state = document.getElementById('college_state').value
//   var current_year = document.getElementById('current_year').value
//   var gender = document.getElementById('gender').value
//   // var pass = getSelectedPass()
//   var referral_code = document.getElementById('referral_code').value
//   var igmun_checkbox = document.getElementById('igmun_checkbox');
//   var igmun_pref = '';
//   var mun_exp = '';

//   if (igmun_checkbox.checked) {
//     var committee_1 = document.getElementById('committee_1').value;
//     var committee_2 = document.getElementById('committee_2').value;
//     if(committee_1 == 'DISEC'){
//       var pref_11 = document.getElementById('DISEC_11').value;
//       var pref_12 = document.getElementById('DISEC_12').value;
//       var pref_13 = document.getElementById('DISEC_13').value;
//     }
//     else if(committee_1 == 'UNHRC'){
//       var pref_11 = document.getElementById('UNHRC_11').value;
//       var pref_12 = document.getElementById('UNHRC_12').value;
//       var pref_13 = document.getElementById('UNHRC_13').value;
//     }
//     else if(committee_1 == 'ESS-UNGA'){
//       var pref_11 = document.getElementById('ESS_UNGA_11').value;
//       var pref_12 = document.getElementById('ESS_UNGA_12').value;
//       var pref_13 = document.getElementById('ESS_UNGA_13').value;
//     }
//     else if(committee_1 == 'LS'){
//       var pref_11 = document.getElementById('LS_11').value;
//       var pref_12 = document.getElementById('LS_12').value;
//       var pref_13 = document.getElementById('LS_13').value;
//     }
//     if(committee_2 == 'DISEC'){
//       var pref_21 = document.getElementById('DISEC_21').value;
//       var pref_22 = document.getElementById('DISEC_22').value;
//       var pref_23 = document.getElementById('DISEC_23').value;
//     }
//     else if(committee_2 == 'UNHRC'){
//       var pref_21 = document.getElementById('UNHRC_21').value;
//       var pref_22 = document.getElementById('UNHRC_22').value;
//       var pref_23 = document.getElementById('UNHRC_23').value;
//     }
//     else if(committee_2 == 'ESS-UNGA'){
//       var pref_21 = document.getElementById('ESS_UNGA_21').value;
//       var pref_22 = document.getElementById('ESS_UNGA_22').value;
//       var pref_23 = document.getElementById('ESS_UNGA_23').value;
//     }
//     else if(committee_2 == 'LS'){
//       var pref_21 = document.getElementById('LS_21').value;
//       var pref_22 = document.getElementById('LS_22').value;
//       var pref_23 = document.getElementById('LS_23').value;
//     }
//     igmun_pref = '{(1) ' + committee_1 + ' || (1a) ' + pref_11 + ' || (1b) ' + pref_12 + ' || (1c) ' + pref_13 + '}, {(2) ' + committee_2 + ' || (2a) ' + pref_21 + ' || (2b) ' + pref_22 + ' || (2c) ' + pref_23 + ' }';
//     mun_exp = document.getElementById('mun_exp').value;
//   }
  
//   var body = {
//     phone: phone_number,
//     gender: gender,
//     college: college,
//     current_year: current_year,
//     state: college_state,
//     referral_code: referral_code,
//     igmun: igmun_checkbox.checked,
//     igmun_pref: igmun_pref,
//     mun_exp: mun_exp,
//   }

//   miAPI.post(BASE_URL + 'api/accounts/user-profile/', body, {
//     headers: {
//       'Content-type': 'application/json; charset=UTF-8',
//       // 'X-CSRFToken': getCookie('csrftoken'),
//     },
//     withCredentials: true,
//   }
//   )
//     .then(function (response) {
//       if (response.status == 201) {
//         if(complete_profile_form.submitted == 'goToProfile'){
//           window.location.replace("../user-profile/index.html");
//         }
//         else if(complete_profile_form.submitted == 'goToPass'){
//           window.location.replace("../payment_steps/steps.html");
//         }
//       }
//     })
//     .catch(function (error) {
//       // handle error
//     })
//     .finally(function () {
//       // always executed
//     });
// });
