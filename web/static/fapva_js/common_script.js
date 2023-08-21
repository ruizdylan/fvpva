function simpleToastNotification(type="success", message=""){
        $.simplyToast(type,message,{
        offset:
        {
          from: "bottom",
          amount: 10
        },
        align: "right",
        width: 300,
        delay: 2500,
        allow_dismiss: false,
        stackup_spacing: 10
    });
}

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

function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

const error_function = function (xhr, errmsg, err) {
    if (xhr.status === 403 || xhr.status === 401) {
        data = xhr.responseJSON;
        message = "detail" in data? data.detail : data.description
        genericSweetAlert(title = "Error", text = message, type = 'error').then(function () {
            window.location.href = "/";
        });
        return
    }
    else if (xhr.status === 500){
        genericSweetAlert(title = "Error", text = xhr.statusText, type = 'error');
        return
    }else if (xhr.status === 404){
        genericSweetAlert(title = "Error", text = xhr.statusText, type = 'error');
        return
    }else if (xhr.status === 422){
        genericSweetAlert(title = "Error", text = xhr.responseJSON.description, type = 'error');
        return
    }
}

$("#logout").on("click",function(){
    $.ajax({
        url: "/api/users/logout", // the endpoint
        type: "GET", // http method
        headers: {
        },
        success: function (json) {
            if (json['success'] == true) {
                setCookie("u-at","")
                saveToLocalStorage("u-at","")
                simpleToastNotification("success", json['description'])
                window.location.href = "/"
            }
        },
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            if (xhr.status == 403) {
                genericSweetAlert(title = "Error", type = 'error');
            }
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
})


function convertToSlug(Text) {
  return Text.toLowerCase()
             .replace(/ /g, '-')
             .replace(/[^\w-]+/g, '');
}

function get_or_convert_date_time_to_system_time_zone(date=""){
    let time_zone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    if (date){
        return new Date(date).toLocaleString("en-US", {timeZone: time_zone})
    }
    return new Date().toLocaleString("en-US", {timeZone: time_zone})
}


function SOCKET(path) {
    // let port = ":8001";
    let port = "";
    let wsStart = "";
    if (window.location.protocol == 'https:') {
        wsStart = 'wss://';
    } else if (window.location.protocol == 'http:') {
        wsStart = 'ws://';
    }
    let endpoint = wsStart + window.location.host + port + path;
    let socket = new WebSocket(endpoint)

    return socket;
}
