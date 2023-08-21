let COUNTRY_ID = 0;
let COUNTRY_KEYWORD = "";

let COUNTRY_LIMIT = 4;
let COUNTRY_OFFSET = 0;

let COUNTRY_COUNT = 0;

let DOCUMENT_WIDTH = $(document).width();

$(document).ready(function () {
    let url = `ws://${window.location.host}/ws/socket-server/`;
    const chatSocket = new WebSocket(url);
    chatSocket.onmessage = function (e) {
        let data = JSON.parse(e.data);
        console.log("Data", data)
    }
});

FreeNumbers = function (data) {
    this.countries_url = data.countries_url;
    this.countries_data = [];
    this.countries_select = "";
    let self = this;

    self.init_countries_ajax_call();

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
    });


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
        console.log(filteredData);
        self.init_countries_select(filteredData);
    }
};


FreeNumbers.prototype.init_countries_select = function (data_list) {
    let self = this;
    if (data_list.length === 0){
        $("#countries-data").html('<div class="m-auto text-white">No Countries Found</div>');
        return
    }
    this.countries_select = ""
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
                                        <input type="radio" ${checked? "checked" : ""} data-pk="${i.id}" id="country" name="county" class="country-id"/>
                                    </div>
                                </div>`;
    });
    $("#countries-data").html(this.countries_select);
}


FreeNumbers.prototype.init_countries_ajax_call = function () {
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


