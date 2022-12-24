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

const BASE_URL = "http://127.0.0.1:8000/";
const URL_USER_AUTHENTICATE = "api/accounts/login/";
const URL_REFRESH_TOKEN = "api/accounts/refresh/";

const miAPI = axios.create({
    baseURL: BASE_URL,
    withCredentials: true
});

miAPI.interceptors.response.use(function (response) {
    return response;
}, function (error) {
    console.log("error :" + JSON.stringify(error));

    const originalReq = error.config;

    if (error.response.status == 401 && !originalReq._retry && error.response.config.url != URL_USER_AUTHENTICATE) {
        originalReq._retry = true;

        return axios.post(BASE_URL + URL_REFRESH_TOKEN, null, {
            withCredentials: true
        }).then((res) => {
            if (res.status == 200) {
                console.log("token refreshed");
                return axios(originalReq);
            }
        }).catch((error) => { window.location.href = "/frontend/login.html" });
    }
    console.log("Rest promise error");
    return Promise.reject(error);
});

// This function not always working
async function createOrder() {
    try {
        alert(document.cookie);
        const response = await miAPI.post("http://127.0.0.1:8000/payments/pay/", null, {
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            withCredentials: true,
        });
        alert(document.cookie);
        console.log(response);
        sessionStorage.setItem("msg", `Order ${getCookie("order_id")} Created Successfully`);
        alert(sessionStorage.getItem("msg"));
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
