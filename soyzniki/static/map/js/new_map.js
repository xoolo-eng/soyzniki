/*
*
Объект хранилище, для сохранения настроек проиложения
*
*/
var map = L.map('map', {minZoom: 3});
var my_point;

var Storage = {
    /*
    Объект хранилище. Держит в памяти значения последних 'действий':
        map - положение карты, зум, положение панели с сервисами;
        servis - название активированного сервиса;
        filters - актиированные пользователем филтры данных, позиционирования;
        points - данные последнего запроса точек по одному сервису;

    поле 'name' хранит название ключа для сохранения в локальном
    хранилище или куках
    */
    test_support: function(){
        /*
        проверка на поддержку локальноно хранилища, если поддержки
        нет, данные запишутся в куки
        */
        try {
            window.localStorage;
            return true;
        }
        catch (e) {
            return false;
        }
    },

    support: false,
    country: ACTIV_COUNTRY,
    map: {name: 'map', coords: false, zoom: 4, scroll: 0},
    servis: {name: 'servis', point: false},
    filters: {name: 'filters', transport: false, region: {name: false, id: 0}, search: false, positon: false},
    points: {name: 'points', data: false},

    update_storage: function(obj) {
        /*
        обнавление данных в хранилище браузера
        */
        if (this.support) {
            if (window.localStorage.getItem(this.country) !== null) {
                var saved_data = JSON.parse(window.localStorage.getItem(this.country));
                saved_data[obg.name] = obj;
                window.localStorage.setItem(this.country, JSON.stringify(saved_data));
            }
        }
        else {
            $.cookie(this.country + '_' + obj.name, JSON.stringify(obj), {
                path: '/map/'
            });
        }
    },

    is_clear: function() {
        if((!this.filters.transport) && (!this.filters.region) && (!this.filters.search) && (!this.points.data) && (!this.servis.point))
            {return true;}
        else
            {return false;}
    },

    load_storage: function() {
        /*
        загрузка данных хранилища в память из хранилища
        */
        this.support = this.test_support();
        if (this.support) {
            if (window.localStorage.getItem(this.country) !== null) {
                var saved_data = JSON.parse(window.localStorage.getItem(this.country));
                this.map = saved_data.map;
                this.servis = saved_data.servis;
                this.filters = saved_data.filters;
                this.points = saved_data.points;
            }
        }
        else {
            if ($.cookie(this.country + '_map') !== undefined) {
                this.map = JSON.parse($.cookie(this.country + '_map'));
            }
            if ($.cookie(this.country + '_servis') !== undefined) {
                this.servis = JSON.parse($.cookie(this.country + '_servis'));
            }
            if ($.cookie(this.country + '_filters') !== undefined) {
                this.filters = JSON.parse($.cookie(this.country + '_filters'));
            }
        }
    },
    write_storage: function() {
        /*
        запись данных хранилища из памяти в хранилище
        */
        this.update_storage(this.map);
        this.update_storage(this.servis);
        this.update_storage(this.filters);
        this.update_storage(this.points);
    },
    get_map: function() {
        var map_data = this.map;
        delete map_data.name;
        return map_data;
    },
    set_map: function(obj) {
        if(obj.coords !== undefined) this.map.coords = obj.coords;
        if(obj.zoom !== undefined) this.map.zoom = obj.zoom;
        if(obj.scroll !== undefined) this.map.scroll = obj.scroll;
        this.update_storage(this.map);
    },
    clear_map: function() {
        this.map.coords = false;
        this.map.zoom = 4;
        this.map.scroll = 0;
    },
    get_servis: function() {
        var servis_data = this.servis;
        delete servis_data.name;
        return servis_data;
    },
    set_servis: function(servis_point) {
        this.servis.poinst = servis_point;
        this.update_storage(this.servis)
    },
    clear_servis: function() {
        this.servis.point = false;
    },
    get_filters: function() {
        var filters_data = this.filters;
        delete filters_data.name;
        return filters_data;
    },
    set_filters: function(obj) {
        if(obj.transport !== undefined) this.filters.transport = obj.transport;
        if(obj.region !== undefined) this.filters.region = obj.region;
        if(obj.search !== undefined) this.filters.search = obj.search;
        if(obj.positon !== undefined) this.filters.positon = obj.positon;
        this.update_storage(this.filters);
    },
    clear_filters: function() {
        this.filters.transport = false;
        this.filters.region = {name: false, id: 0};
        this.filters.search = false;
        this.filters.position = false;
    },
    get_points: function() {
        var points_data = this.points;
        delete points_data.name;
        return points_data;
    },
    set_points: function(points) {
        this.points.data = points;
        this.update_storage(this.points);
    },
    clear_points: function() {
        points.data = false;
    }
};

/*
элементы управления приложением
    transport - включение/выключения фильтра по транспорту, легковой и грузовой
    position - включение/выключения позицианорования
    regions - включение/выключение фильтра по региону
    search - включение/выключение поиска по содержимому
    servis - включение/выключение отображения точек по определенному сервису
*/
var Interface = {
    transport: {
        passenger: $('#passenger_transport').get(0),
        freight: $('#freight_transport').get(0)
    },
    position: $('#position').get(0),
    regions: {
        button: $('#regions').get(0),
        input: $('#region_filter').get(0)
    },
    search: {
        button: $('#search').get(0),
        input: $('#search_filter').get(0)
    },
    servis: $('#icons > ul > li').get(),

    interval: 0,

    load_interface: function() {
        /*
        загрузка интерфейса, установка значений для элементов управления
        */
        if (Storage.get_filters().transport) {
            switch(Storage.get_filters().transport) {
                case 'passenger': {
                    $(this.transport.passenger).addClass('icon_action');
                    break;
                }
                case 'freight': {
                    $(this.transport.freight).addClass('icon_action');
                    break;
                }
            }
        }
        if (Storage.get_filters().position) {
            $(this.positon).addClass('icon_action');
            this.start_position();
        }
        if (Storage.get_filters().search) {
            $(this.search.button).addClass('icon_action');
            $(this.search.input).val(Storage.get_filters().search);
        }
        if (Storage.get_filters().region.name) {
            $(this.regions.button).addClass('icon_action');
            var option = $(this.regions.input).children('option').get()
            $(option[0]).removeAttr('selected');
            for (i=1;i<option.length; i++) {
                if ($(option[i]).val() == Storage.get_filters().region.id) {
                    $(option[i]).attr('selected', '');
                    break;
                }
            }
        }
        if (Storage.get_servis().point) {
            for (i=0;i<this.servis;i++) {
                if ($(this.servis[i]).attr('id') == Storage.get_servis().point) {
                    $(this.servis[i]).addClass('active');
                    break;
                }
            }
            this.load_point();
        }
    },

    start_position: function() {
        /*
        запуск отслеживания местоположения 
        */
        var my_marker;
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(function(position) {
                my_marker=L.icon({iconUrl:"/static/map/images/position.svg",iconSize:[46,46],iconAnchor:[23,23],popupAnchor:[0,-23]});
                map.setView([position.coords.latitude, position.coords.longitude]);
                my_point = L.marker([position.coords.latitude, position.coords.longitude], {icon: my_marker}).addTo(map);
            });
            interval = setInterval(function() {
                navigator.geolocation.getCurrentPosition(function(position) {
                    map.removeLayer(my_point);
                    map.setView([position.coords.latitude, position.coords.longitude]);
                    my_point = L.marker([position.coords.latitude, position.coords.longitude], {icon: marker}).addTo(map);
                });
            }, 5000);
        }
    },

    stop_position: function() {
        /*
        прекращение отслеживания местоположения
        */
        clearInterval(this.interval);
        map.removeLayer(my_point);
    },

    load_point: function() {
        /*
        загрузка данных по точкам исхобя из данных в хранилище
        */
    },
    set_transport: function(obj) {
        /* 
        включение/выключение фильтров по транспорту
        принимается объект с полями типов транспорта,
        в занчениях передается 1 или 0 (вкл/выкл)
        */
        if (obj.passenger) {
            if (!$(this.transport.passenger).hasClass('icon_action')) {
                $(this.transport.passenger).addClass('icon_action');
                Storage.set_filters({transport: 'passenger'});
            }
        }
        else {
            if ($(this.transport.passenger).hasClass('icon_action')) {
                $(this.transport.passenger).removeClass('icon_action');
                Storage.set_filters({transport: false});
            }
        }
        if (obj.freight) {
            if (!$(this.transport.freight).hasClass('icon_action')) {
                $(this.transport.freight).addClass('icon_action');
                Storage.set_filters({transport: 'freight'});
            }
        }
        else {
            if ($(this.transport.freight).hasClass('icon_action')) {
                $(this.transport.freight).removeClass('icon_action');
                Storage.set_filters({transport: false});
            }
        }
    },
    set_region: function(val) {
        /*
        включение/выключение фильтра по региону
        принимает id выбранного региона или 0
        */
        if (val > 0) {
            if (!$(this.regions.button).hasClass('icon_action')) {
                $(this.regions.button).addClass('icon_action');
            }
        }
        else {
            if ($(this.regions.button).hasClass('icon_action')) {
                $(this.regions.button).removeClass('icon_action');
            }
        }
    },
    set_search: function(val) {
        /*
        включение/выключение фильтра по описанию,
        принимает значение поисковой строки
        */
        if (val > 0) {
            if (!$(this.search.button).hasClass('icon_action')) {
                $(this.search.button).addClss('icon_action');
            }
        }
        else {
            if ($(this.search.button).hasClass('icon_action')) {
                $(this.search.button).removeClass('icon_action')
            }
        }
    },
    set_position: function(val) {
        /*
        включение/выключение определения позиционирии,
        принимает 1 - включение / 0 - выключение.
        */
        if (val == 1) {
            if (!$(this.position).hasClass('icon_action')) {
                $(this.position).addClass('icon_action');
                this.start_position();
            }
        }
        if (val == 0) {
            if ($(this.position).hasClass('icon_action')) {
                $(this.position).removeClass('icon_action');
                this.stop_position();
            }
        }
    },
}

/*
Функция обновления элементов управления приложением
*/
function render_app() {

}

/*
*
Функция инициализации приложения
*
*/
function initialaze() {
    /*
    Настройка ajax для корректной отправки post запросов
    с учетом защиты от csrf
    */
    var csrftoken = $.cookie('csrftoken');
    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    /* загрузка хранилища */
    Storage.load_storage();
    Interface.load_interface();
    L.tileLayer('https://tile-{s}.openstreetmap.fr/hot/{z}/{x}/{y}.png', {attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);
    if (Storage.get_map().coords) {
        map.setView(Storage.get_map().coords, Storage.get_map().zoom);
    }
    else {
        $.ajax({
            url: '/map/get_lat_lng',
            type: 'POST',
            data: {
                'country': Storage.country
            },
            dataType: 'json'
        }).done(function(data){
            map.setView(data['lat_lng'], 8)
        });
    }
    // if (Storage.get_map().scroll) {
    //     $('#icons').scrollTop(Storage.get_map().scroll);
    // }
    // Interface.set_region(Storage.filters.region.id);
    // if (Storage.filters.transport) {
    //     type_transport = `${Storage.filters.transport}`;
    //     Interface.set_transport({type_transport: 1});
    // }
    // if (Storage.filters.position) {
    //     Interface.set_position();
    // }
}

$(document).ready(function() {
    initialaze();
});

$(window).unload(function() {
    Storage.write_storage();
});