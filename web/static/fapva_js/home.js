let COUNTRY_ID = 0;
let SERVICE_KEYWORD = "";
let COUNTRY_KEYWORD = "";

let SERVICE_COUNT = 0;

let SERVICE_LIMIT = 3;
let SERVICE_OFFSET = 0;

let COUNTRY_LIMIT = 4;
let COUNTRY_OFFSET = 0;

let COUNTRY_COUNT = 0;

let DOCUMENT_WIDTH = $(document).width();

Home = function (data) {
    this.countries_url = data.countries_url;
    this.services_url = data.services_url;
    this.services_data = [];
    this.countries_data = [];
    this.countries_select = "";
    this.services_select = "";
    let self = this;

    self.init_countries_ajax_call();

    $("#service-left").on("click", function () {
        SERVICE_OFFSET = SERVICE_OFFSET - SERVICE_LIMIT;
        if (SERVICE_OFFSET < 0) {
            SERVICE_OFFSET = 0
        }
        console.log(SERVICE_OFFSET, SERVICE_LIMIT);
        service_search()
    });

    $("#service-right").on("click", function () {
        if (SERVICE_OFFSET < SERVICE_COUNT) {
            SERVICE_OFFSET = SERVICE_OFFSET + SERVICE_LIMIT;
            console.log(SERVICE_OFFSET, SERVICE_LIMIT);
            service_search()
        }
    });

    $("#country-left").on("click", function () {
        COUNTRY_OFFSET = COUNTRY_OFFSET - COUNTRY_LIMIT;
        if (COUNTRY_OFFSET < 0) {
            COUNTRY_OFFSET = 0
        }
        console.log(COUNTRY_OFFSET, COUNTRY_OFFSET + COUNTRY_LIMIT);
        country_search()
    });

    $("#country-right").on("click", function () {
        if (COUNTRY_OFFSET < COUNTRY_COUNT) {
            COUNTRY_OFFSET = COUNTRY_OFFSET + COUNTRY_LIMIT;
            console.log(COUNTRY_OFFSET, COUNTRY_OFFSET + COUNTRY_LIMIT);
            country_search()
        }
    });

    $("#countries-data").on('click', '.card-body', function () {
        $(this).find("input[type=radio]").prop("checked", true);
        COUNTRY_ID = $(this).find("input[type=radio]").attr("data-pk");
        SERVICE_KEYWORD = $("#service-search").val();
        self.init_services_ajax_call(COUNTRY_ID);
    });

    $("#service-search").on('keyup', function () {
        SERVICE_KEYWORD = $(this).val();
        service_search()
    });

    function service_search() {
        let filteredData
        if (SERVICE_KEYWORD == null || SERVICE_KEYWORD === "") {
            filteredData = self.services_data.filter(function (obj) {
                if (COUNTRY_ID) {
                    console.log(parseInt(obj['country_id']), parseInt(COUNTRY_ID));
                    return parseInt(obj['country_id']) === parseInt(COUNTRY_ID)
                }
                return obj
            });
        } else {
            filteredData = self.services_data.filter(function (obj) {
                if (convertToSlug(obj['service_name']).indexOf(convertToSlug(SERVICE_KEYWORD)) != -1) {
                    if (COUNTRY_ID) {
                        return parseInt(obj['country_id']) === parseInt(COUNTRY_ID)
                    }
                    return obj
                }
            });
        }
        SERVICE_COUNT = filteredData.length;
        if (DOCUMENT_WIDTH <= 768) {
            if (SERVICE_COUNT >= SERVICE_OFFSET) {
                filteredData = filteredData.slice(SERVICE_OFFSET - SERVICE_LIMIT, SERVICE_LIMIT + SERVICE_OFFSET)
            } else {
                filteredData = filteredData.slice(SERVICE_OFFSET, SERVICE_LIMIT + SERVICE_OFFSET)
            }
        }
        self.init_services_select(filteredData);
    }

    $("#country-search").on('keyup', function () {
        COUNTRY_KEYWORD = $(this).val();
        country_search()
    });

    function country_search() {
        let filteredData = [];
        if (COUNTRY_KEYWORD == null || COUNTRY_KEYWORD === "") {
            filteredData = self.countries_data;
        } else {
            filteredData = self.countries_data.filter(function (obj) {
                if (convertToSlug(obj['name']).indexOf(convertToSlug(COUNTRY_KEYWORD)) != -1) {
                    return obj
                }
            });
        }
        COUNTRY_COUNT = filteredData.length;
        if (DOCUMENT_WIDTH <= 768) {
            if (COUNTRY_COUNT < COUNTRY_OFFSET) {
                filteredData = filteredData.slice(COUNTRY_OFFSET - COUNTRY_LIMIT, COUNTRY_LIMIT + COUNTRY_OFFSET)
            } else {
                filteredData = filteredData.slice(COUNTRY_OFFSET, COUNTRY_LIMIT + COUNTRY_OFFSET)
            }
        }
        // console.log(filteredData);
        self.init_countries_select(filteredData);
    }
};


Home.prototype.init_countries_select = function (data_list) {
    let self = this;
    if (data_list.length === 0){
        $("#countries-data").html('<div class="m-auto text-white">No Countries Found</div>');
        return
    }
    this.countries_select = ""
    // $(this).find("input[type=radio]").prop("checked", true);
    // COUNTRY_ID = $(this).find("input[type=radio]").attr("data-pk");
    data_list.map(i => {
        let checked = false;
        if (COUNTRY_ID === i.id) {
            checked = true
        }
        this.countries_select += `<div class="card-body d-flex justify-content-start my-2" href="#">
                                    <div class="w-10 mx-3 show my-auto">
                                        <img class="rounded-circle img img-responsive"
                                             src="${i.flag}" width="37px">
                                    </div>
                                    <div class="w-70 flex-grow-1 show m-auto">
                                        <div><b>${i.name}</b></div>
                                    </div>
                                    <div class="w-10 m-auto show container-input">
                                        <input type="radio" ${checked? "checked": ""} data-pk="${i.id}" id="country" name="county" class="country-id"/>
                                    </div>
                                </div>`;
    });
    $("#countries-data").html(this.countries_select);
}


Home.prototype.init_services_select = function (data_list) {
    let self = this;
    if (data_list.length === 0) {
        $("#services-data").html('<div class="m-auto text-white">No Services Found</div>');
        return
    }
    this.services_select = "";
    data_list.map(i => {
        this.services_select += `<a class="card-body d-flex justify-content-start my-2" href="/payment-method?number_id=${i.id}" data-pk="${i.id}" data-price="${i.price}">
                                    <div class="flex-fill m-auto hide text-center justify-content-center text-white text-uppercase my-2">
                                        Buy Now
                                    </div>
                                    <div class="w-10 mx-3 show my-auto">
                                        <img src="${i.flag}" width="37px">
                                    </div>
                                    <div class="w-70 flex-grow-1 show">
                                        <div><b>${i.service_name}</b></div>
                                        <div class="title-text">${i.number}</div>
                                    </div>
                                    <div class="w-10 m-auto show">
                                        <span class="bg-dark text-white border px-3 py-1 border-round">${i.price} USD</span>
                                    </div>
                                </a>`;
    });
    $("#services-data").html(this.services_select);
}


Home.prototype.init_countries_ajax_call = function () {
    let self = this;
    $.ajax({
        url: this.countries_url, // the endpoint
        type: "GET", // http method
        success: function (json) {
            self.countries_data = json.payload;
            COUNTRY_COUNT = self.countries_data.length;
            if (COUNTRY_COUNT > 0) {
                COUNTRY_ID = self.countries_data[0].id;
            }
            self.init_services_ajax_call();
            if (DOCUMENT_WIDTH <= 768) {
                let data = self.countries_data
                self.init_countries_select(data.slice(COUNTRY_OFFSET, COUNTRY_OFFSET + COUNTRY_LIMIT));
                return
            }
            self.init_countries_select(self.countries_data);

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


Home.prototype.init_services_ajax_call = function () {
    let self = this;
    $.ajax({
        url: this.services_url + "?is_paid=true&country_id=" + COUNTRY_ID, // the endpoint
        type: "GET", // http method
        success: function (json) {
            self.services_data = json.payload;
            SERVICE_COUNT = self.services_data.length;
            if (DOCUMENT_WIDTH <= 768) {
                let data = self.services_data
                self.init_services_select(data.slice(SERVICE_OFFSET, SERVICE_OFFSET + SERVICE_LIMIT));
                return
            }
            self.init_services_select(self.services_data)
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

