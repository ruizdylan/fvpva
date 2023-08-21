Countries = function (data) {
    this.countries_datatable_url = data.countries_datatable_url;
    this.countries_status_url = data.countries_status_url;
    this.countries_url = data.countries_url;
    this.countries_delete_url = data.countries_delete_url;
    this.countries_datatable = null;

    var self = this;
    const countries_datatable = $('#countries-datatable');
    self.init_data_table(self.create_url())


    $("#countries-datatable").on("click", ".on-default", function () {
        self.change_status($(this).data("pk"), self.countries_status_url);
    });

    $("#countries-datatable").on("click", ".delete-country", function () {
        self.change_status($(this).data("pk"), self.countries_delete_url);
    });


    $("#countries-datatable").on("click", ".edit-country", function () {
        $("#country-form").trigger("reset");
        $("#exampleModal").modal('show');
        data = JSON.parse($(this).attr("data-pk"));
        $("#name").val(data.name);
        $("#edit").removeAttr("data-pk");
        $("#dialling_code").val(data.dialling_code);
        $("#submit").addClass("d-none");
        $("#edit").removeClass("d-none");
        $("#edit").attr("data-pk",data.id);
    });



    $("#create-country").on('click',function(){
        $("#country-form").trigger("reset");
        $("#submit").removeClass("d-none");
        $("#edit").addClass("d-none");
        $("#exampleModal").modal('show');
    })

    $("#submit").on("click", function () {
        self.CreateCountryFormSubmit(self.countries_url, "POST");

    })

    $("#edit").on("click", function () {
        self.CreateCountryFormSubmit(self.countries_url+ "/"+ $(this).attr("data-pk"), "PUT");
    })
};


Countries.prototype.init_data_table = function (query_params) {
    const self = this;
    self.countries_datatable = $('#countries-datatable').DataTable({
        "processing": true,
        "serverSide": true,
        // "order": [[ 12, "asc" ]],
        "destroy": true,
        "ajax": {
            "url": self.countries_datatable_url + query_params,
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
                "title": "Dial Code",
                "data": "dialling_code",
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
                    if (data) {
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
                            operations += '<a title="Enable" data-pk="' + full.id + '" style="padding-right: 1px;  cursor: pointer"  class="on-default remove-row disapprove-country"><i class="fa fa-ban text-danger"></i> </a>';
                        } else {
                            operations += '<a title="Disable" data-pk="' + full.id + '" style="padding-right: 1px; cursor: pointer"  class="on-default remove-row approve-country"><i class="fa fa-check text-success"></i> </a>';
                        }
                        let stringify_data = JSON.stringify(full);
                        operations += '<a title="Delete" data-pk="' + full.id + '" style="padding-right: 1px; cursor: pointer"  class="delete-country"><i class="fa fa-trash text-danger"></i></a>';
                        operations += `<a title='Edit' data-pk='${stringify_data}' style='padding-right: 2px; cursor: pointer'  class='edit-country'><i class="fa fa-pencil-alt text-info"></i></a>`;
                        return operations;

                    }
                }

            }
        ],

    });
};

Countries.prototype.change_status = function (id, url) {
    const self = this;
    loadingSweetAlert(title = 'Please wait');
    $.ajax({
        url: url +"/" + id, // the endpoint
        type: "GET", // http method
        headers: {
        },
        success: function (json) {
            if (json['success']) {
                genericSweetAlert(title = 'Success', text = json['description'], type = 'success').then((function () {
                    self.countries_datatable.ajax.reload(null, false);
                }));
            }
        },
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        // handle a non-successful response
        error: error_function
    });
};

Countries.prototype.CreateCountryFormSubmit = function (url, method) {
    let self = this;
    let name = $("#name").val();
    let dialling_code = $("#dialling_code").val();
    let files = $('#file')[0].files;

    if (name.trim() === ""){
        genericSweetAlert("Error", "A Valid Name is Required")
        return;
    }
    if (dialling_code.trim() === ""){
        genericSweetAlert("Error", "A Valid Dialling Code is Required")
        return;
    }
    if ((files.length === 0 && method === "POST")){
        genericSweetAlert("Error", "Country Flag is Required")
        return;
    }
    let sign_up_data = new FormData();
    sign_up_data.append('name', name);
    sign_up_data.append('dialling_code', dialling_code);
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
            $("#exampleModal").modal('hide');
            genericSweetAlert(title = "Success", text = json.description, type = 'success');
            self.countries_datatable.ajax.reload(null, false);
        },
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        // handle a non-successful response
        error: error_function
    });
}

Countries.prototype.create_url = function (selection) {
    return '?type=' + selection;
}