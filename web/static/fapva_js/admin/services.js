
Services = function (data) {
    this.services_datatable_url = data.services_datatable_url;
    this.services_status_url = data.services_status_url;
    this.services_url = data.services_url;
    this.services_delete_url = data.services_delete_url;
    this.services_datatable = null;

    var self = this;
    const services_datatable = $('#services-datatable');
    self.init_data_table(self.create_url())


    services_datatable.on("click", ".on-default", function () {
        self.change_status($(this).data("pk"), self.services_status_url);
    });

    services_datatable.on("click", ".delete-service", function () {
        self.change_status($(this).data("pk"), self.services_delete_url);
    });

    services_datatable.on("click", ".edit-service", function () {
        $("#services-form").trigger("reset");
        $("#exampleModal").modal('show');
        data = JSON.parse($(this).attr("data-pk"));
        $("#name").val(data.name);
        let edit = $("#edit");
        edit.removeAttr("data-pk");
        $("#submit").addClass("d-none");
        edit.removeClass("d-none");
        edit.attr("data-pk",data.id);
    });



    $("#create-service").on('click',function(){
        $("#services-form").trigger("reset");
        $("#submit").removeClass("d-none");
        $("#edit").addClass("d-none");
        $("#exampleModal").modal('show');
    })

    $("#submit").on("click", function () {
        self.CreateServiceFormSubmit(self.services_url, "POST");

    })

    $("#edit").on("click", function () {
        self.CreateServiceFormSubmit(self.services_url+ $(this).attr("data-pk"), "PUT");
    })
};


Services.prototype.init_data_table = function (query_params) {
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
                "title": "Flag",
                "data": "flag",
                "mRender": function (data, type, full) {
                    if (data) {
                        return '<td><img class="rounded-circle img img-responsive" width="15%" src="' + data + '"> </td>';
                    } else return '<td class="center"> - </td>'
                }
            },
            {
                "title": "Name",
                "data": "name",
                "mRender": function (data, type, full) {
                    if (data) {
                        return '<td>' + data + '</td>';
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
                        console.log(stringify_data);
                        operations += '<a title="Delete" data-pk="' + full.id + '" style="padding-right: 1px; cursor: pointer"  class="delete-service"><i class="fa fa-trash text-danger"></i></a>';
                        operations += `<a title='Edit' data-pk='${stringify_data}' style='padding-right: 2px; cursor: pointer'  class='edit-service'><i class="fa fa-pencil-alt text-info"></i></a>`;
                        return operations;

                    }
                }

            }
        ],

    });
};

Services.prototype.change_status = function (id, url) {
    const self = this;
    loadingSweetAlert(title = 'Please wait');
    $.ajax({
        url: url +"/" + id, // the endpoint
        type: "GET", // http method
        headers: {
        },
        success: function (json) {
            console.log(json['success'])
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

Services.prototype.CreateServiceFormSubmit = function (url, method) {
    let self = this;
    let name = $("#name").val();
    let files = $('#file')[0].files;

    if (name.trim() === ""){
        genericSweetAlert("Error", "A Valid Name is Required")
        return;
    }
    if ((files.length === 0 && method === "POST")){
        genericSweetAlert("Error", "Country Flag is Required")
        return;
    }
    let sign_up_data = new FormData();
    sign_up_data.append('name', name);
    if (files.length > 0){
        sign_up_data.append('flag', files[0]);
    }else{
        sign_up_data.append('flag', "");
    }

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
            console.log(json)
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

Services.prototype.create_url = function (selection) {
    return '?type=' + selection;
}