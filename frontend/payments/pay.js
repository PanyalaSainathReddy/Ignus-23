function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
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

// This function not always working
async function createOrder() {
    try {
        const response = await axios.post("http://127.0.0.1:8000/payments/pay/", null, { withCredentials: true });
        alert(document.cookie);

        // Doesn't redirect
        window.location.replace("pay.html");
    } catch (error) {
        console.error(error);
        alert(error);
    }
}

function pay() {
    let order_id = getCookie("order_id");
    alert(order_id);
    let amount_due = getCookie("amount_due");
    let currency = getCookie("currency");

    var options = {
        key: "rzp_test_Ur7QOvBoxgfjC4",
        amount: parseInt(amount_due),
        currency: currency,
        name: "IGNUS '23 IIT Jodhpur",
        description: "Test Transaction",
        image: "../static/ignus icon.png",
        order_id: order_id,
        callback_url: "http://127.0.0.1:8000/payments/callback/",
        prefill: {
            name: "SAAHIL BHAVSAR",
            email: "saahil.1609.bhavsar@gmail.com",
            contact: "9325220982",
        },
        theme: {
            color: "#3399cc",
        },
        redirect: true
    };

    var razorpayGateway = new Razorpay(options);
    razorpayGateway.open();
}
