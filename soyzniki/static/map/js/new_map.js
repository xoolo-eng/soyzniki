/*
*
Объект хранилище, для сохранения настроек проиложения
*
*/
var map = L.map('map', {minZoom: 3});

var storage = {
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
    storage.load_storage();
    L.tileLayer('https://tile-{s}.openstreetmap.fr/hot/{z}/{x}/{y}.png', {attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);
    if (storage.get_map().coords) {
        map.setView(storage.get_map().coords, storage.get_map().zoom);
    }
    else {
        $.ajax({
            url: '/map/get_lat_lng',
            type: 'POST',
            data: {
                'country': ACTIV_COUNTRY
            },
            dataType: 'json'
        }).done(function(data){
            map.setView(data['lat_lng'], 8)
        });
    }

    if (storage.get_filters().transport) {
        $('#' + storage.get_filters().transport).addClass('icon_action');
    }
    if (storage.get_filters().position) {
        $('#positon').addClass('icon_action');
        // установка позиционирования
    }
    if (storage.get_filters().search) {
        $('#search').addClass('icon_action');
        $('#search_filter').val(storage.get_filters().search);
    }
    if (storage.get_filters().region.name) {
        $('#regions').addClass('icon_action');
        var option = $('#region_filter').children('option').get()
        $(option[0]).removeAttr('selected');
        for (i=1;i<option.length; i++) {
            if ($(option[i]).val() == storage.get_filters().region.id) {
                $(option[i]).attr('selected', '');
                break;
            }
        }
    }
    if (storage.get_map().scroll) {
        $('#icons').scrollTop(storage.get_map().scroll);
    }
    if (storage.get_servis().point) {
        $('#' + storage.get_servis().point).addClass('active');
        // загрузка точек
    }
}

$(document).ready(function() {
    initialaze();
});

$(window).unload(function() {
    storage.write_storage();
});