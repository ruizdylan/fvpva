ServicesNumber = function (data) {
    this.services_datatable_url = data.services_datatable_url;
    this.services_status_url = data.services_status_url;
    this.services_url = data.services_url;
    this.services_delete_url = data.services_delete_url;
    this.services_data = data.services_data;
    this.countries_data = data.countries_data;
    this.countries_select = [];
    this.services_select = [];
    this.services_datatable = null;
    var self = this;

    this.countries_select = [{
        "id": "",
        "text": "Select a state",
        "selected": true
    }];
    this.countries_data.map(i => {
        this.countries_select.push({
            "id": i.id,
            "text": i.name,
            "selected": false
        })
    })

    this.services_select = [{
        "id": "",
        "text": "Select a Service",
        "selected": true
    }];
    this.services_data.map(i => {
        this.services_select.push({
            "id": i.id,
            "text": i.name,
            "selected": false
        })
    })
    const services_datatable = $('#services-datatable');

    self.init_data_table(self.create_url())

    services_datatable.on("click", ".on-default", function () {
        self.change_status($(this).data("pk"), self.services_status_url);
    });

    services_datatable.on("click", ".delete-service", function () {
        self.change_status($(this).data("pk"), self.services_delete_url);
    });


    self.init_select_state();
    self.init_select_service();

    services_datatable.on("click", ".edit-service", function () {
        $("#price").removeAttr("disabled");
        $("#services-form").trigger("reset");
        $("#exampleModal").modal('show');
        data = JSON.parse($(this).attr("data-pk"));
        $("#price").val(data.price);
        $("#number").val(data.number);
        $("#is_paid").val(JSON.stringify(data.is_paid));
        console.log(data.is_paid)
        if (!data.is_paid){
            $("#price").attr("disabled","true")
        }
        self.init_select_state(data.country_id);
        self.init_select_service(data.service_id);


        let edit = $("#edit");
        edit.removeAttr("data-pk");
        $("#submit").addClass("d-none");
        edit.removeClass("d-none");
        edit.attr("data-pk", data.id);
    });

    $("#is_paid").on('change',function(){
        if($(this).val() === 'false'){
        $("#price").val(0);
        $("#price").attr("disabled", "true");
        }else{
        $("#price").val(0);
        $("#price").removeAttr("disabled");
        }
    })

    $("#create-service").on('click', function () {
                $("#price").removeAttr("disabled");

        $("#services-form").trigger("reset");
        $("#submit").removeClass("d-none");
        $("#edit").addClass("d-none");
        $("#exampleModal").modal('show');
        self.init_select_state();
        self.init_select_service();
    })

    $("#submit").on("click", function () {
        self.CreateServiceFormSubmit(self.services_url, "POST");

    })

    $("#edit").on("click", function () {
        self.CreateServiceFormSubmit(self.services_url + "/" + $(this).attr("data-pk"), "PUT");
    })
};


ServicesNumber.prototype.init_data_table = function (query_params) {
    const self = this;
    self.services_datatable = $('#services-datatable').DataTable({
        "processing": true,
        "serverSide": true,
        // "order": [[ 12, "asc" ]],
        "destroy": true,
        "ajax": {
            "url": self.services_datatable_url + query_params,
            "type": "GET",
            // dataSrc:"",
            // "dataSrc": "data.payload",

            headers: {
            },
            dataFilter: function (responsce) {
                var json = jQuery.parseJSON(responsce);
                json = json.payload
                totalEntries = json.recordsTotal;
                return JSON.stringify(json); // return JSON string
            },
            // handle a non-successful response
            error: error_function

        },
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
                "title": "Number Type",
                "data": "is_paid",
                "mRender": function (data, type, full) {
                    if (data) {
                        return '<td>Paid</td>';
                    } else return '<td class="center"> Free </td>'
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
                "title": "Active",
                "data": "is_active",
                "mRender": function (data, type, full) {
                    var status = ''
                    if (data == true) {
                        return '<td><span class="text-success">Yes</span></td>';
                    } else {
                        return '<td><span class="text-danger">No</span> </td>';
                    }
                }
            },

            {
                "title": "Actions",
                'data': 'id',
                "mRender": function (data, type, full) {

                    if (data) {
                        let operations = '';
                        if (full.is_active) {
                            operations += '<a title="Enable" data-pk="' + full.id + '" style="padding-right: 1px;  cursor: pointer"  class="on-default remove-row disapprove-service"><i class="fa fa-ban text-danger"></i> </a>';
                        } else {
                            operations += '<a title="Disable" data-pk="' + full.id + '" style="padding-right: 1px; cursor: pointer"  class="on-default remove-row approve-service"><i class="fa fa-check text-success"></i> </a>';
                        }
                        let stringify_data = JSON.stringify(full);
                        operations += '<a title="Delete" data-pk="' + full.id + '" style="padding-right: 1px; cursor: pointer"  class="delete-service"><i class="fa fa-trash text-danger"></i></a>';
                        operations += `<a title='Edit' data-pk='${stringify_data}' style='padding-right: 2px; cursor: pointer'  class='edit-service'><i class="fa fa-pencil-alt text-info"></i></a>`;
                        return operations;

                    }
                }

            }
        ],

    });
};

ServicesNumber.prototype.change_status = function (id, url) {
    const self = this;
    loadingSweetAlert(title = 'Please wait');
    $.ajax({
        url: url + "/" + id, // the endpoint
        type: "GET", // http method
        headers: {
        },
        success: function (json) {
            if (json['success'] == true) {
                genericSweetAlert(title = 'Success', text = json['description'], type = 'success').then((function () {
                    self.services_datatable.ajax.reload(null, false);
                }));
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
};

ServicesNumber.prototype.CreateServiceFormSubmit = function (url, method) {
    let self = this;
    let price = $("#price").val();
    let number = $("#number").val();
    let is_paid = $("#is_paid").val();
    let country_id = $("#select-state").select2('data')[0].id;
    let service_id = $("#select-service").select2('data')[0].id;
    if (country_id === "") {
        genericSweetAlert("Error", "Please select a country")
        return;
    }
    if (service_id === "") {
        genericSweetAlert("Error", "Please select a service")
        return;
    }
    if ((price === "" || price <= 0) && is_paid === 'true') {
        genericSweetAlert("Error", "A Valid Price is Required")
        return;
    }
    if (number === "" || number <= 0) {
        genericSweetAlert("Error", "A Valid Number is Required")
        return;
    }


    let sign_up_data = new FormData();
    sign_up_data.append('price', price);
    sign_up_data.append('number', number);
    sign_up_data.append('country_id', country_id);
    sign_up_data.append('service_id', service_id);
    sign_up_data.append('is_paid', is_paid);

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

ServicesNumber.prototype.create_url = function (selection) {
    return '?type=' + selection;
}

ServicesNumber.prototype.init_select_state = function (id = null) {
    let self = this;
    $("#select-state").select2({
        width: '100%',
        data: this.countries_select,
    });
    $('#select-state').val(id).trigger('change')
}

ServicesNumber.prototype.init_select_service = function (id = null) {

    let self = this;
    $("#select-service").select2({
        width: '100%',
        data: this.services_select
    });
    $('#select-service').val(id).trigger('change')
}