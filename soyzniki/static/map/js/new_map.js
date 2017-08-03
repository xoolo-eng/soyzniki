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
        var support = true;
        var country = ACTIV_COUNTRY;
        var map = {name: 'map', coords: false, zoom: 4, scroll: 0};
        var servis = {name: 'servis', point: false};
        var filters = {name: 'filters', transport: false, region: false};
        var points = {name: 'points', data: null};

        test_support: function() {
        /*
        проверка на поддержку локальноно хранилища, если поддержки
        нет, данные запишутся в куки
        */
        try {
            window.localStorage;
            suppotr = true;
        } catch (e) {
            suppotr false;
        }
    },
    update_storage: function(obj) {
        /*
        обнавление данных в хранилище браузера
        */
        if (support) {
            /*
                !!! написать проверку на переполнение
                локального хранилища
            */
            window.localStorage[obj.name] = obj;
        }
        else {
            $.cookie(obj.name, JSON.stringify(obj), {
                path: '/map/'
            });
        }
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
    read_storage: function() {
        /*
        запись данных хранилища из памяти
        */
        this.update_storage(map);
        this.update_storage(servis);
        this.update_storage(filters);
        this.update_storage(points);
    },
    get_map_data: function() {
        var map_data = map;
        delete map_data.name;
        return map_data;
    },
    set_map_data: function(obj) {
        if(obj.coords !== undefined) map.coords = obj.coords;
        if(obj.zoom !== undefined) map.zoom = obj.zoom;
        if(obj.scroll !== undefined) map.scroll = obj.scroll;
        this.update_storage(map);
    },
    get_servis_data: function() {
        var servis_data = servis;
        delete servis_data.name;
        return servis_data;
    },
    set_service_data: function(servis_point) {
        servis.poinst = servis_point;
        this.update_storage(servis)
    },
    get_filters_data: function() {
        var filters_data = filters;
        delete filters_data.name;
        return filters_data;
    }
    set_filters_data: function(obj) {

    },
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
}


$(document).ready(function() {

});

$(window).upload(function() {

});