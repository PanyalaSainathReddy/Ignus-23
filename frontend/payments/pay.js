function createOrder() {
    axios.post("http://127.0.0.1:8000/payments/pay/")
        .then((response) => response.data)
        .then((data) => {
            // if (localStorage.getItem("order_id")) {
            //     localStorage.removeItem("order_id");
            //     localStorage.removeItem("amount_due");
            //     localStorage.removeItem("currency");
            // }
            
            // This does not run everytime
            // Make sure it runs every fucking time
            if (confirm("Order created successfully! Proceed to payment?")) {
                localStorage.setItem("amount_due", data["amount_due"]);
                localStorage.setItem("currency", data["currency"]);
                localStorage.setItem("order_id", data["id"]);
                // window.location = "http://127.0.0.1:5500/frontend/payments/pay.html";
            } else { }
        });
}

function pay() {
    let order_id = localStorage.getItem("order_id");
    let amount_due = localStorage.getItem("amount_due");
    let currency = localStorage.getItem("currency");

    var options = {
        key: "rzp_test_Ur7QOvBoxgfjC4",
        amount: amount_due,
        currency: currency,
        name: "IGNUS '23 IIT Jodhpur",
        description: "Test Transaction",
        image: "../static/ignus icon.png",
        order_id: order_id,
        handler: successHandler,
        prefill: {
            name: "SAAHIL BHAVSAR",
            email: "saahil.1609.bhavsar@gmail.com",
            contact: "9325220982",
        },
        theme: {
            color: "#3399cc",
        },
        redirect: false
    };

    var razorpayGateway = new Razorpay(options);
    razorpayGateway.open();

    razorpayGateway.on('payment.failed', failureHandler);
}

function successHandler(response) {
    axios.post("http://127.0.0.1:8000/payments/callback/", {
        razorpay_payment_id: response.razorpay_payment_id,
        razorpay_order_id: response.razorpay_order_id,
        razorpay_signature: response.razorpay_signature
    })
        .then(res => {
            // This alert not working
            alert("Payment Successful!");
        });
}

function failureHandler(response) {
    axios.post("http://127.0.0.1:8000/payments/callback/", {
        error: {
            code: response.error.code,
            description: response.error.description,
            source: response.error.source,
            step: response.error.step,
            reason: response.error.reason,
            metadata: {
                order_id: response.error.metadata.order_id,
                payment_id: response.error.metadata.payment_id
            }
        }
    })
        .then(res => {
            // This alert not working
            alert("Payment Failed!");
        });
}
