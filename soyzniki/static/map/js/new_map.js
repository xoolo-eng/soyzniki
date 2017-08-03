/*
*
Объект хранилище, для сохранения настроек проиложения
*
*/

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
    var support = test_support();
    var country = ACTIV_COUNTRY;
    var map = {name: 'map', coords: false, zoom: 4, scroll: 0};
    var servis = {name: 'servis', point: false};
    var filters = {name: 'filters', transport: false, region: false, search: false};
    var points = {name: 'points', data: false};

    function() test_support{
        /*
        проверка на поддержку локальноно хранилища, если поддержки
        нет, данные запишутся в куки
        */
        try {
            window.localStorage;
            suppotr = true;
        }
        catch (e) {
            suppotr false;
        }
    };

    function update_storage(obj) {
        /*
        обнавление данных в хранилище браузера
        */
        if (support) {
            try {
                window.localStorage[obj.name] = obj;
            }
            catch (e) {
                if (e.number == 22) {
                    window.localStorage.clear();
                    try {
                        window.localStorage[obj.name] = obj;
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
    };

    is_clear: function() {
        if(!filters.transport and !filters.region and !filters.search and !points.data and !servis.point)
            {return true;}
        else
            {return false;}
    },

    load_storage: function() {
        /*
        загрузка данных хранилища в память
        */
        if (support) {
            if (window.localStorage[country]['map'] !== undefined){
                map = window.localStorage[country]['map'];
            }
            if (window.localStorage[country]['servis'] !== undefined){
                servis = window.localStorage[country]['servis'];
            }
            if (window.localStorage[country]['filters'] !== undefined){
                filters = window.localStorage[country]['filters'];
            }
            if (window.localStorage[country]['points'] !== undefined){
                points = window.localStorage[country]['points'];
            }
            window.localStorage.clear();
        }
        else {
            if ($.cookie(country + '_map') !== undefined) {
                map = JSON.parse($.cookie(country + '_map'));
            }
            if ($.cookie(country + '_servis') !== undefined) {
                servis = JSON.parse($.cookie(country + '_servis'));
            }
            if ($.cookie(country + '_filters') !== undefined) {
                filters = JSON.parse($.cookie(country + '_filters'));
            }
        }
    },
    write_storage: function() {
        /*
        запись данных хранилища из памяти
        */
        update_storage(map);
        update_storage(servis);
        update_storage(filters);
        update_storage(points);
    },
    get_map: function() {
        var map_data = map;
        delete map_data.name;
        return map_data;
    },
    set_map: function(obj) {
        if(obj.coords !== undefined) map.coords = obj.coords;
        if(obj.zoom !== undefined) map.zoom = obj.zoom;
        if(obj.scroll !== undefined) map.scroll = obj.scroll;
        update_storage(map);
    },
    clear_map: function() {
        map.coords = false;
        map.zoom = 4;
        map.scroll = 0;
    },
    get_servis: function() {
        var servis_data = servis;
        delete servis_data.name;
        return servis_data;
    },
    set_servis: function(servis_point) {
        servis.poinst = servis_point;
        update_storage(servis)
    },
    clear_servis: function() {
        servis.point = false;
    }
    get_filters: function() {
        var filters_data = filters;
        delete filters_data.name;
        return filters_data;
    }
    set_filters: function(obj) {
        if(obj.transport !== undefined) filters.transport = obj.transport;
        if(obj.region !== undefined) filters.region = obj.region;
        if(obj.search !== undefined) filters.search = obj.search;
        update_storage(filters);
    },
    clear_filters: function() {
        filters.transport = false;
        filter.region = false;
        filters.search = false;
    },
    get_points: function() {
        var points_data = points;
        delete points_data.name;
        return points_data;
    },
    set_points: function() {
        var points_data = points;
        delete points;
        return points_data;
    }
    clear_points: function() {
        points.data = false;
    }
};

/*
*
обработка url на предмет региона и/или активного сервиса
*
*/
function parse_url() {
    /*
    Разбор url на части. Возвращает массив из значений после первого слеша
    */
    var url = window.location.pathname;
    var url_list = url.split('/').slice(1, -2);
    return url_list;
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
    storage.load_storage();
    if(stroage.is_clear()) {
        /*
        разбор урл
        если значений больше двух
        проверка последних значений
        на предмет совпадения с регионами
        и названиями точек
        если есть совпадения, то заргрузка нужных данных
        */
    }
}

$(document).ready(function() {
    initialaze();
});

$(window).upload(function() {
    storage.write_storage();
});