let CRYPTO_OFFSET = 0;
let CRYPTO_LIMIT = 2;
let CRYPTO_COUNT = 0;

PaypalPayment = function (data) {
    this.access_token = data.access_token;
    this.number_id = data.number_id;
    this.order_url = data.order_url;
    this.crypto_coin_image = data.crypto_coin_image;
    this.bitcoin_image = data.bitcoin_image;
    this.etherium_image = data.etherium_image;
    this.crypto_coin_image_2 = data.crypto_coin_image_2;


    let self = this;


    let CRYPTO_LIST = [
        {
            "image": self.crypto_coin_image
        },
        {
            "image": self.bitcoin_image,
        },
        {
            "image": self.etherium_image,
        },
        {
            "image": self.crypto_coin_image_2
        }
    ]

    CRYPTO_COUNT = CRYPTO_LIST.length;
    self.initiate_crypto_wallet(CRYPTO_LIST.slice(CRYPTO_OFFSET, CRYPTO_LIMIT + CRYPTO_OFFSET));
    $("#crypto-left").on("click", function () {
        console.log("left")
        CRYPTO_OFFSET = CRYPTO_OFFSET - CRYPTO_LIMIT;
        if (CRYPTO_OFFSET < 0) {
            CRYPTO_OFFSET = 0
        }
        self.initiate_crypto_wallet(CRYPTO_LIST.slice(CRYPTO_OFFSET, CRYPTO_LIMIT + CRYPTO_OFFSET));
    });

    $("#crypto-right").on("click", function () {
        console.log("right")
        if (CRYPTO_OFFSET + CRYPTO_LIMIT < CRYPTO_COUNT) {
            CRYPTO_OFFSET = CRYPTO_OFFSET + CRYPTO_LIMIT;
        }
        // if (CRYPTO_COUNT < CRYPTO_OFFSET){
        //     CRYPTO_OFFSET -= CRYPTO_LIMIT
        // }
        console.log(CRYPTO_OFFSET, CRYPTO_LIMIT + CRYPTO_OFFSET, CRYPTO_COUNT)
        self.initiate_crypto_wallet(CRYPTO_LIST.slice(CRYPTO_OFFSET, CRYPTO_LIMIT + CRYPTO_OFFSET));
    });


    self.init_transcation_ajax_call();
    if (self.number_id != 0 && self.number_id != "" && self.number_id != null){
         paypal
        .Buttons({
            // Sets up the transaction when a payment button is clicked
            createOrder: function (data, actions) {
                loadingSweetAlert("Please Wait");
                return fetch("/api/main/paypal/order", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        "token": `${self.access_token}`,
                        "number_id": `${self.number_id}`
                    })
                })
                    .then(function (response) {
                        return response.json();
                    })
                    .then(function (order) {
                        order_id = order.payload.id;
                        return order.payload.id;
                    });
            },
            // Finalize the transaction after payer approval
            onApprove: function (data, actions) {
                return fetch(`/api/main/paypal/orders/${data.orderID}/capture`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        "token": `${self.access_token}`
                    })
                })
                    .then((response) => response.json())
                    .then((orderData) => {
                        orderData = orderData.payload;
                        // Successful capture! For dev/demo purposes:
                        // console.log("Capture result", orderData, JSON.stringify(orderData, null, 2));
                        var transaction = orderData.capture_payload.purchase_units[0].payments.captures[0];
                        // When ready to go live, remove the alert and show a success message within this page. For example:
                        // var element = document.getElementById('paypal-button-container');
                        // element.innerHTML = '<h3>Thank you for your payment!</h3>';
                        // Or go to another URL:  actions.redirect('thank_you.html');
                        genericSweetAlert("Success", "Transaction Completed Successfully", "success").then(function () {
                            window.location.href = "/thank-you/"+orderData.order_id;
                        });
                    });
            },
        })
        .render("#paypal-button-container");

    if (paypal.HostedFields.isEligible()) {
        let orderId;
        // Renders card fields
        paypal.HostedFields.render({
            // Call your server to set up the transaction
            createOrder: () => {
                loadingSweetAlert("Please Wait");
                return fetch("/api/main/paypal/order", {
                    method: 'post',
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        "token": `${self.access_token}`,
                        "number_id": `${self.number_id}`
                    })
                })
                    .then((res) => res.json())
                    .then((orderData) => {
                        orderId = orderData.payload.id; // needed later to complete capture
                        return orderData.payload.id
                    })
            },
            styles: {
                '.valid': {
                    color: 'green'
                },
                '.invalid': {
                    color: 'red'
                }
            },
            fields: {
                number: {
                    selector: "#card-number",
                    placeholder: "4111 1111 1111 1111"
                },
                cvv: {
                    selector: "#cvv",
                    placeholder: "123"
                },
                expirationDate: {
                    selector: "#expiration-date",
                    placeholder: "MM/YY"
                }
            }
        }).then((cardFields) => {
            document.querySelector("#card-form").addEventListener("submit", (event) => {
                event.preventDefault();
                cardFields
                    .submit({
                        billingAddress: {
                            countryCodeAlpha2: document.getElementById(
                                "card-billing-address-country"
                            ).value,
                        },
                    })
                    .then((data) => {
                        console.log("Then", data.orderId);
                        fetch(`/api/main/paypal/orders/${data.orderId}/capture`, {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify({
                                "token": `${self.access_token}`,
                                "number_id": `${self.number_id}`
                            })
                        })
                            .then((res) => res.json())
                            .then((orderData) => {
                                orderData = orderData.payload;
                                console.log(orderData);
                                // Two cases to handle:
                                //   (1) Non-recoverable errors -> Show a failure message
                                //   (2) Successful transaction -> Show confirmation or thank you
                                // This example reads a v2/checkout/orders capture response, propagated from the server
                                // You could use a different API or structure for your 'orderData'
                                var errorDetail =
                                    Array.isArray(orderData.details) && orderData.details[0];
                                if (errorDetail) {
                                    var msg = "Sorry, your transaction could not be processed.";
                                    console.log("error", errorDetail.description);
                                    if (errorDetail.description)
                                        msg += "\n\n" + errorDetail.description;
                                    if (orderData.debug_id) msg += " (" + orderData.debug_id + ")";
                                    console.log("msg",msg);
                                    return alert(msg); // Show a failure message
                                }
                                // Show a success message or redirect
                                genericSweetAlert("Success", "Transaction completed!", 'success').then(function () {
                                    window.location.reload();
                                });
                            });
                    })
                    .catch((err) => {
                        console.log(err);
                        genericSweetAlert("Error", err.message, "error");
                    });
            });
        });
    } else {
        // Hides card fields if the merchant isn't eligible
        document.querySelector("#card-form").style = 'display: none';
    }
    }

}

PaypalPayment.prototype.initiate_crypto_wallet = function(data_list){
    let self = this;
    if (data_list.length === 0) {
        $("#crypto-list").html('<li class="m-auto text-white">No Services Found</li>');
        return
    }
    let services_select = "";
    data_list.map(i => {
        let checked = false;
        services_select += `<li class="">
                    <div>
                        <img src="${i.image}"/>
                    </div>
                    <input type="radio" name="crypto" />
                </li>`;
    });
    $("#crypto-list").html(services_select);
}

PaypalPayment.prototype.init_transcation_ajax_call = function () {
    let self = this;
    $.ajax({
        url: this.order_url, // the endpoint
        type: "GET", // http method
        headers: {
        },
        success: function (json) {
            if (json.payload.length === 0){
                $("#data-body").html(`<tr><td colspan="4" align="center">No Data Found</td></tr>`)
                return
            }
            data = ``;
            json.payload.map(i => {
                data += `<tr>
                            <td>${i.id}</td>
                            <td>${i.price} USD</td>
                            <td>${get_or_convert_date_time_to_system_time_zone(i.date_time).split(",")[0]}</td>
                            <td>${get_or_convert_date_time_to_system_time_zone(i.date_time).split(",")[1]}</td>
                       
                        </tr>`;
            });

            $("#data-body").html(data);
        },
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}


function formatDate(date) {
  var d = new Date("2023-05-24 " +date);
  var hh = d.getHours();
  var m = d.getMinutes();
  var s = d.getSeconds();
  var dd = "AM";
  var h = hh;
  if (h >= 12) {
    h = hh - 12;
    dd = "PM";
  }
  if (h == 0) {
    h = 12;
  }
  m = m < 10 ? "0" + m : m;

  s = s < 10 ? "0" + s : s;

  /* if you want 2 digit hours:
  h = h<10?"0"+h:h; */

  var pattern = new RegExp("0?" + hh + ":" + m + ":" + s);

  var replacement = h + ":" + m;
  /* if you want to add seconds
  replacement += ":"+s;  */
  replacement += " " + dd;

  return date.replace(pattern, replacement);
}