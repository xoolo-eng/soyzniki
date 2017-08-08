/*
*
Объект хранилище, для сохранения настроек проиложения
*
*/

function test_support(){
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
    }


var storage = {
    /*
    Объект хранилище. Держит в памяти значения последних 'действий':
        map - положение карты, зум, положение панели с сервисами;
        servis - название активированного сервиса;
        filters - актиированные пользователем филтры данных;
        points - данные последнего запроса точек по одному сервису;

    поле 'name' хранит название ключа для сохранения в локальном
    хранилище или куках
    */
    
    support: test_support(),
    country: ACTIV_COUNTRY,
    map: {name: 'map', coords: false, zoom: 4, scroll: 0},
    servis: {name: 'servis', point: false},
    filters: {name: 'filters', transport: false, region: {name: false, id: 0}, search: false},
    points: {name: 'points', data: false},

    update_storage: function(obj) {
        /*
        обнавление данных в хранилище браузера
        */
        if (this.support) {
            try {
                window.localStorage[country][obj.name] = obj;
            }
            catch (e) {
                if (e.number == 22) {
                    window.localStorage.clear();
                    try {
                        window.localStorage[country][obj.name] = obj;
                    }
                    catch (e) {
                        if (e.number == 22) {
                            console.log('Переполнение хранилища')
                        }
                    }
                }
            }
        }
        else {
            $.cookie(obj.name, JSON.stringify(obj), {
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
        загрузка данных хранилища в память
        */
        if (this.support) {
            if (window.localStorage[this.country]['map'] !== undefined){
                this.map = window.localStorage[this.country]['map'];
            }
            if (window.localStorage[this.country]['servis'] !== undefined){
                this.servis = window.localStorage[this.country]['servis'];
            }
            if (window.localStorage[this.country]['filters'] !== undefined){
                this.filters = window.localStorage[this.country]['filters'];
            }
            if (window.localStorage[this.country]['points'] !== undefined){
                this.points = window.localStorage[this.country]['points'];
            }
            window.localStorage.clear();
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
        запись данных хранилища из памяти
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
        this.update_storage(this.filters);
    },
    clear_filters: function() {
        this.filters.transport = false;
        this.filters.region = {name: false, id: 0};
        this.filters.search = false;
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

// /*
// *
// обработка url на предмет региона и/или активного сервиса
// *
// */
// function parse_url() {
    
//     Разбор url на части. Возвращает массив из значений после первого слеша
    
//     var url = window.location.pathname;
//     var url_list = url.split('/').slice(1, -2);
//     return url_list;
// }

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
    if (storage.is_clear()) {
        console.log
    }
    console.log(storage);
}

$(document).ready(function() {
    initialaze();
});

$(window).unload(function() {
    storage.write_storage();
});