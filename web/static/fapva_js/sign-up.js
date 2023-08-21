/**
 * Created by Ashar on 7/1/2020.
 */

SignUp = function (data) {
    this.sign_up_url = data.sign_up_url;
    this.login_url = data.login_url;
    this.home_url = data.home_url;
    this.next = data.next;
    const self = this;


    $("#signupForm").on('submit', function (e) {
        e.preventDefault();
        self.SignUpFormSubmit();
    })
    $("#loginForm").on('submit', function (e) {
        e.preventDefault();
        self.LoginUpFormSubmit();
    })
};


SignUp.prototype.SignUpFormSubmit = function () {
    var self = this;
    var sign_up_data = new FormData();
    // console.log(data);
    // return false;
    sign_up_data.append('first_name', $("#first_name").val());
    sign_up_data.append('last_name', $("#last_name").val());
    sign_up_data.append('email', $("#email").val());
    sign_up_data.append('password', $("#password").val());

    loadingSweetAlert(title = 'Please wait');
    $.ajax({
        url: this.sign_up_url, // the endpoint
        type: "POST", // http method
        processData: false,
        contentType: false,
        data: sign_up_data,
        // data: $('#add-content-form').formSerialize(),
        dataType: "json",
        xhrFields: {
            withCredentials: true
        },

        success: function (json) {
            console.log(json)
            setCookie("u-at", json.payload.access_token, 100);
            saveToLocalStorage("u-at", json.payload.access_token)
            simpleToastNotification("success", json.description)
            if (self.next){
                window.location.href = self.next;
            }else{
            window.location.href = self.home_url;

            }
        },
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("Authorization", "Token " + getCookie('u-at'));
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            data = xhr.responseJSON;
            genericSweetAlert(title = "Error", text=data.description, type = 'error');
        }
    });
}


SignUp.prototype.LoginUpFormSubmit = function () {
    var self = this;
    var login_up_data = new FormData();
    login_up_data.append('email', $("#email").val());
    login_up_data.append('password', $("#password").val());

    loadingSweetAlert(title = 'Please wait');
    $.ajax({
        url: this.login_url, // the endpoint
        type: "POST", // http method
        processData: false,
        contentType: false,
        data: login_up_data,
        // data: $('#add-content-form').formSerialize(),
        dataType: "json",
        xhrFields: {
            withCredentials: true
        },

        success: function (json) {
            console.log(json)
            setCookie("u-at", json.payload.access_token, 100);
            saveToLocalStorage("u-at", json.payload.access_token)
            simpleToastNotification("success", json.description)
                        if (self.next){
                window.location.href = self.next;
            }else{
            window.location.href = self.home_url;

            }
        },
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("Authorization", "Token " + getCookie('u-at'));
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            data = xhr.responseJSON;
            genericSweetAlert(title = "Error", text=data.description, type = 'error');
        }
    });
}