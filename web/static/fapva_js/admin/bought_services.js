const socket = SOCKET('/ws/bought-services/');

socket.onopen = async function (e) {
    console.log('WebSocket connection established.');
};

socket.onmessage = async function (event) {
    let data = JSON.parse(event.data);

    $('#services-datatable').DataTable().ajax.reload(null, false);
};

socket.onclose = async function (e) {
    console.log('WebSocket connection closed.' + e);
};
socket.onerror = async function (e) {
    console.log(e);
};


BoughtServices = function (data) {
    this.services_datatable_url = data.services_datatable_url;
    this.order_url = data.order_url;
    this.services_datatable = null;
    var self = this;


    const services_datatable = $('#services-datatable');

    self.init_data_table(self.create_url())

    services_datatable.on("click", ".edit-service", function () {
        $("#services-form").trigger("reset");
        $("#exampleModal").modal('show');
        data = JSON.parse($(this).attr("data-pk"));
        let edit = $("#edit");
        edit.removeAttr("data-pk");
        $("#submit").addClass("d-none");
        edit.removeClass("d-none");
        edit.attr("data-pk", data);
    });


    $("#edit").on("click", function () {
        self.CreateServiceFormSubmit(self.order_url + $(this).attr("data-pk"), "PUT");
    })

};


BoughtServices.prototype.init_data_table = function (query_params) {
    const self = this;
    self.services_datatable = $('#services-datatable').DataTable({
        initComplete: function (resp) {
            $('#services-datatable thead th').removeClass('endtime');
            setInterval(function () {
                doCountdowns();
            }, 1000);
        },
        "processing": true,
        "serverSide": true,
        // "order": [[ 12, "asc" ]],
        "destroy": true,
        "ajax": {
            "url": self.services_datatable_url + query_params,
            "type": "GET",
            // dataSrc:"",
            // "dataSrc": "data.payload",
            dataFilter: function (responsce) {
                var json = jQuery.parseJSON(responsce);
                json = json.payload
                totalEntries = json.recordsTotal;
                return JSON.stringify(json); // return JSON string
            },
            // handle a non-successful response
            error: error_function

        },
        "columnDefs": [
            {className: "endtime", "targets": 7}
        ],
        "columns": [
            {
                "title": "ID",
                "data": "id",
                "mRender": function (data, type, full) {
                    if (data) {
                        return '<td>' + data + '</td>';
                    } else return '<td class="center"> - </td>'
                }
            },
            {
                "title": "Country",
                "data": "country_name",
                "mRender": function (data, type, full) {
                    if (data) {
                        return '<td>' + data + '</td>';
                    } else return '<td class="center"> - </td>'
                }
            },
            {
                "title": "Payment",
                "data": "payment_channel",
                "mRender": function (data, type, full) {
                    if (data) {
                        return '<td>' + data + '</td>';
                    } else return '<td class="center"> - </td>'
                }
            },
            {
                "title": "Service",
                "data": "service_name",
                "mRender": function (data, type, full) {
                    if (data) {
                        return '<td>' + data + '</td>';
                    } else return '<td class="center"> - </td>'
                }
            },
            {
                "title": "Number",
                "data": "number",
                "mRender": function (data, type, full) {
                    if (data) {
                        return '<td>' + data + '</td>';
                    } else return '<td class="center"> - </td>'
                }
            },
            {
                "title": "Price",
                "data": "price",
                "mRender": function (data, type, full) {
                    if (data) {
                        return '<td>$ ' + data + '</td>';
                    } else return '<td class="center"> - </td>'
                }
            },
            {
                "title": "Message",
                "data": "message",
                "mRender": function (data, type, full) {
                    if (data) {
                        return '<td>' + data + '</td>';
                    } else return '<td class="center"> - </td>'
                }
            },
            {
                "title": "Expire At",
                "data": "expire_at",
                "mRender": function (data, type, full) {
                    if (data) {
                        return '<td>' + get_or_convert_date_time_to_system_time_zone(data) + '</td>';
                    } else return '<td class="center"> - </td>'
                }
            },
            {
                "title": "Count Down",
                "data": "",
                "mRender": function (data, type, full) {
                    if (data) {
                        return '<td>' + data + '</td>';
                    } else return '<td class="center"> - </td>'
                }
            },
            {
                "title": "Actions",
                'data': 'id',
                "mRender": function (data, type, full) {

                    if (data) {
                        let operations = '';
                        operations += `<a title='Edit' data-pk='${full.id}' style='padding-right: 2px; cursor: pointer'  class='edit-service'><i class="fa fa-pencil-alt text-info"></i></a>`;
                        return operations;

                    }
                }

            }
        ],

    });
};


BoughtServices.prototype.CreateServiceFormSubmit = function (url, method) {
    let self = this;
    let message = $("#message").val();
    if (message === "") {
        genericSweetAlert("Error", "Please Enter a valid message.")
        return;
    }
    console.log(message);
    let sign_up_data = new FormData();
    sign_up_data.append('message', message);

    loadingSweetAlert(title = 'Please wait');
    $.ajax({
        url: url, // the endpoint
        type: method, // http method
        processData: false,
        contentType: false,
        data: sign_up_data,
        // data: $('#add-content-form').formSerialize(),
        dataType: "json",
        xhrFields: {
            withCredentials: true
        },

        success: function (json) {
            console.log(json);
            $("#exampleModal").modal('hide');
            genericSweetAlert(title = "Success", text = json.description, type = 'success');
            self.services_datatable.ajax.reload(null, false);
        },
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },

        // handle a non-successful response
        error: error_function
    });
}


BoughtServices.prototype.create_url = function (selection) {
    return '?type=' + selection;
}


function doCountdowns() {
    $('.endtime').each(function (index) {
        doCountdown(this); // a td node
    });
}


function doCountdown(node) {
    let endTime = Date.parse($(node).html()) / 1000;
    let now = (Date.parse(get_or_convert_date_time_to_system_time_zone()) / 1000);
    let timeLeft = endTime - now;
    let days = Math.floor(timeLeft / 86400);
    let hours = Math.floor((timeLeft - (days * 86400)) / 3600);
    let minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600)) / 60);
    let seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
    if (hours < "10") {
        hours = "0" + hours;
    }
    if (minutes < "10") {
        minutes = "0" + minutes;
    }
    if (seconds < "10") {
        seconds = "0" + seconds;
    }
    if (days < 0) {
    $(node).next("td").html(`0 : 0 : 0 : 0`);
    }else{
    $(node).next("td").html(`${days} : ${hours} : ${minutes} : ${seconds}`);

    }
}