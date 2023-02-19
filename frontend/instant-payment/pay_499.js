// API
const BASE_URL = "https://api.ignus.co.in/";

document.getElementById("pay_499_form").addEventListener("submit", function(event) {
    event.preventDefault();

    var name = document.getElementById("name").value;
    var pass_type = document.getElementById("pass_type").value;
    var remarks = document.getElementById("remarks").value;
    var amount = "799.00";
    if(pass_type == "silver"){
      amount = "499.00";
    }

    fetch(BASE_URL + 'api/payments/payment-500/', {
        method: 'POST',
        body: JSON.stringify({
          name: name,
          amount: amount,
          remarks: remarks,
        }),
        headers: {
          'Content-type': 'application/json; charset=UTF-8',
        }
      })
      .then(function(response){
        return response.json()
      })
      .then(function(data){
        console.log(data);
        link = data.link;
        window.location.href = link;
      })
      .catch(error => console.error('Error:', error));
});