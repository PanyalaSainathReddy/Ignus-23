$(document).ready(function(){
	$('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function(){
    // console.log("hye");
		$(this).toggleClass('open');
    $(".res-nav").toggleClass("opened");
	});
});

// API
const BASE_URL = "https://api.ignus.co.in/";

function loadSponsors(){
	fetch(BASE_URL + 'api/sponsors/list/', {
		method: 'GET',
		headers: {
			'Content-type': 'application/json; charset=UTF-8',
		}
	})
	.then(function(response){
		return response.json()
	})
	.then(function(data){
		// console.log(data);
		updateSponsors(data);
	})
	.catch(error => console.error('Error:', error));
}

var sponsors_main_div = document.getElementById("sponsors_main_div");

var sponsors_main_div_text = ``;

function updateSponsors(data){
  for(let i = 0; i < data.length; i++){
    sponsors_main_div_text += `
      <section>
        <h2 style="text-align: center">${data[i].sponsor_type}</h2>
        <div class="sponsors-container">
    `;
    for(let j = 0; j < data[i].sponsors.length; j++){
      sponsors_main_div_text += `
        <div class="sponsors-tile">
      `;
      if(data[i].sponsors[j].sponsor_link == ""){
        sponsors_main_div_text += `
            <img src="${BASE_URL + data[i].sponsors[j].image.substring(20)}" alt="${data[i].sponsors[j].name}">
        `;
      }
      else{
        sponsors_main_div_text += `
            <a href="${data[i].sponsors[j].sponsor_link}" target="_blank">
              <img src="${BASE_URL + data[i].sponsors[j].image.substring(20)}" alt="${data[i].sponsors[j].name}">
            </a>
        `;
      }
      sponsors_main_div_text += `
        </div>
      `;
    }
    sponsors_main_div_text += `
        </div>
      </section>
    `;
  }
  sponsors_main_div.innerHTML = sponsors_main_div_text;
}