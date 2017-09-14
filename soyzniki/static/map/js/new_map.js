var map = L.map('map', {minZoom: 3});
var claster;
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
                saved_data[obj.name] = obj;
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
        this.servis.point = servis_point;
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
        this.points.data = false;
    }
};

var Interface = {
    /*
    элементы управления приложением
        transport - включение/выключения фильтра по транспорту, легковой и грузовой
        position - включение/выключения позицианорования
        regions - включение/выключение фильтра по региону
        search - включение/выключение поиска по содержимому
        servis - включение/выключение отображения точек по определенному сервису
    */
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
            this.set_points($('#'+Storage.get_servis().point).get(0))
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
        загрузка данных по точкам исходя из данных в хранилище
        */
        var request = {
            /*
            Данные запроса на сервер для поиска нужных точек
            */
            country: Storage.country,
            servis: Storage.get_servis().point,
            region: Storage.get_filters().region.id,
            transport: Storage.get_filters().transport,
            search: Storage.get_filters().search
        }
        if (Storage.get_points().data) {
            add_point(Storage.get_points().data);
        }
        else {
            $.ajax({
                url: '/map/find_point',
                type: 'POST',
                data: request
            }).done(function(data) {
                Storage.set_points(data);
                add_point(data);
            });
        }

        function add_point(point_data) {
            /*
            размещение полученных данных на карте
            */
            var all_data = JSON.parse(point_data);
            var points = all_data['points'];
            var marker = all_data['marker'];
            var elements = new Array();
            /*
            создание html разметки точек для добавления на карту
            */
            for (i=0; i<points.length; i++) {
                var lon = document.createElement('p');
                var lat = document.createElement('p');
                var link = document.createElement('a');
                var name = document.createElement('h2');
                var info = document.createElement('div');
                var address = document.createElement('p');
                var transport = document.createElement('p');
                var reclama = document.createElement('div');
                var time_work = document.createElement('div');
                var desc_point = document.createElement('div');
                var all_desc_point = document.createElement('div');
                lon.className = 'lon_point';
                lat.className = 'lat_point';
                link.innerHTML = 'Подробнее';
                link.className = 'link_point big_button';
                name.className = 'name_point';
                info.className = 'info_point';
                address.className = 'address_point';
                transport.className = 'transport_point';
                reclama.className = 'reclama_point';
                time_work.className = 'time_work_point';
                desc_point.className = 'desc_point_point';
                all_desc_point.className = 'all_desc_point';
                link.href = '/view/point/'+points[i]['id']+'/';
                lat.innerHTML = 'Широта: ' + points[i]['lat'];
                lon.innerHTML = 'Долгота: ' + points[i]['lon'];
                desc_point.id = points[i]['id'];
                info.appendChild(name);
                info.appendChild(time_work);
                all_desc_point.appendChild(lat);
                all_desc_point.appendChild(lon);
                all_desc_point.appendChild(transport)
                all_desc_point.appendChild(address);
                info.appendChild(all_desc_point);
                info.appendChild(link);
                desc_point.appendChild(info);
                desc_point.appendChild(reclama);
                elements[i] = {
                    'data': desc_point,
                    'lat': points[i]['lat'],
                    'lon': points[i]['lon'],
                };
            }
            /*
            иконка маркера
            */
            var icon = L.icon({
                iconUrl: '/media/' + marker,
                iconSize: [46, 46],
                iconAnchor: [23, 23],
                popupAnchor: [0, -23],
            });
            /*
            добавление точек в кластер и
            отображение кластера на крте
            */
            claster = new L.markerClusterGroup();
            var markers = new Array();  
            for (i=0; i<elements.length; i++) {
                markers[i] = L.marker(
                    [+elements[i]['lat'], +elements[i]['lon']],
                    {icon: icon}
                ).addTo(claster);
                markers[i].openPopup().bindPopup(
                    elements[i]['data'],
                    {
                        closeButton: false,
                        minWidth: 300,
                        maxWidth: 300
                    }
                )
            }
            claster.addTo(map);
            /*
            обработка кликов но дням недели на
            точках на карте
            */
            var popup = $('.leaflet-popup-pane').get(0);
            popup.onclick = function(event){
                var element = event.target;
                if ($(element).parent().hasClass('working_day')) {
                    if ($(element).hasClass('vis')) {
                        $(element).removeClass('vis');
                        $(element).siblings('.working_wripper').removeClass('visible');
                    }
                    else {
                        $('h3.vis').removeClass('vis');
                        $('div.working_wripper').removeClass('visible');
                        $(element).addClass('vis');
                        $(element).siblings('.working_wripper').addClass('visible')
                    }
                }
            }
        }
    },
    
    remove_point: function() {
        /*
        удаление данных по точкам из карты и хранилища
        */
        map.removeLayer(claster);
        Storage.clear_points();
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
    is_passenger: function() {
        /*
        если активен фильтр по пасажирскому трансрорту
        */
        if ($(this.transport.passenger).hasClass('icon_action')) {
            return true;
        }
        else {
            return false;
        }
    },
    is_freight: function() {
        /*
        если активен фильтр по грузовому транспорту
        */
        if ($(this.transport.freight).hasClass('icon_action')) {
            return true;
        }
        else {
            return false;
        }
    },
    set_region: function(val) {
        /*
        включение/выключение фильтра по региону
        принимает id выбранного региона или 0
        */
        function get_name_region(val) {
            /*
            получение английского развания региона
            */
            options = $('#region_filter option').get();
            result = false
            for (i=0; i<options.length; i++) {
                if ($(options[i]).attr('value') == val) {
                    result = $(options[i]).attr('name');
                    break
                }
            }
            return result
        }
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
        Storage.set_filters({
            region: {
                id: val,
                name: get_name_region(val)
            }
        });
    },
    is_region: function() {
        /*
        проверка на активность фильтра по региону
        */
        if ($(this.regions.button).hasClass('icon_action')) {
            return true;
        }
        else {
            return false;
        }
    },
    set_search: function(val) {
        /*
        включение/выключение фильтра по описанию,
        принимает значение поисковой строки
        */
        search = false
        if (val != '') {
            if (!$(this.search.button).hasClass('icon_action')) {
                $(this.search.button).addClass('icon_action');
            }
            search = val
        }
        else {
            if ($(this.search.button).hasClass('icon_action')) {
                $(this.search.button).removeClass('icon_action')
            }
        }
        Storage.set_filters({
            search: search
        });
    },
    is_search: function() {
        /*
        проверка на активность фильтра по поисковому запросу
        */
        if ($(this.search.button).hasClass('icon_action')) {
            return true;
        }
        else {
            return false;
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
    is_position: function() {
        /*
        проверка позиционирования на актиивность
        */
        if ($(this.position).hasClass('icon_action')) {
            return true;
        }
        else {
            return false;
        }
    },
    set_points: function(element) {
        var name = $(element).attr('id');
        if (this.is_active()) {
            if (this.get_active_point() == name) {
                /*
                если выбранный сервис является активным,
                выключить текущий сервис, удалить точки
                */
                for (i=0; i<this.servis.length; i++) {
                    if ($(this.servis[i]).hasClass('active')) {
                        $(this.servis[i]).toggleClass('active');
                        break;
                    }
                }
                Storage.clear_servis();
                this.remove_point();
            }
            else {
                /*
                если есть активный сеанс, выключить активный сервис,
                удалить точки, включить выбранный сервис, загрузить точки
                */
                for (i=0; i<this.servis.length; i++) {
                    if ($(this.servis[i]).hasClass('active')) {
                        $(this.servis[i]).toggleClass('active');
                        break;
                    }
                }
                Storage.clear_servis();
                this.remove_point();
                for (i=0;i<this.servis.length; i++) {
                    if ($(this.servis[i]).attr('id') == name) {
                        $(this.servis[i]).toggleClass('active');
                    }
                }
                Storage.set_servis(name);
                this.load_point();
            }
        }
        else {
            /*
            если нет активного сервиса, включить выбранный,
            загрузить точки
            */
            for (i=0;i<this.servis.length; i++) {
                if ($(this.servis[i]).attr('id') == name) {
                    $(this.servis[i]).toggleClass('active');
                }
            }
            Storage.set_servis(name);
            this.load_point();
        }
    },

    is_active: function() {
        /*
        проверка на наличие активного сервиса
        */

        var active = false;
        for (i=0; i<this.servis.length; i++) {
            if ($(this.servis[i]).hasClass('active')) {
                active = true;
                break;
            }
        }
        return active;
    },
    get_active_point: function() {
        /*
        возврат имени активного сервиса или false
        */
        var point = false;
        for (i=0; i<this.servis.length; i++) {
            if ($(this.servis[i]).hasClass('active')) {
                point = $(this.servis[i]).attr('id');
                break;
            }
        }
        return point;
    }
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
}

function set_url() {
    /*
    создание строки url согласно данным из хранилища
    */
    url = `/map/${Storage.country}/`;
    if (Storage.get_filters().region.name) {
        url = url + `${Storage.get_filters().region.name.replace(' ', '_')}/`;
    }
    if (Storage.get_servis().point) {
        url = url + `${Storage.get_servis().point}/`;
    }
    if (Storage.get_filters().search) {
        url = url + `${Storage.get_filters().search.replace(' ', '+')}/`;
    }
    history.pushState('', '', url);
}

$(document).ready(function() {
    initialaze();
});

$(window).unload(function() {
    Storage.set_map({
        coords: [map.getCenter().lat, map.getCenter().lng],
        zoom: map.getZoom(),
        scroll: $('#icons').scrollTop()
    });
    Storage.write_storage();
    console.log(window.localStorage)
});

$('#passenger_transport').click(function() {
    /*
    клик по кнопке фильтка пассажирского транспорта
    */
    if (Interface.is_passenger()) {
        /*
        если кнопка активна, выключить
        */
        Interface.set_transport({
            passenger: 0,
            freight: 0
        });
    }
    else {
        /*
        если кнопка не активна, включить
        */
        Interface.set_transport({
            passenger: 1,
            freight: 0
        });
    }
    if (Interface.is_active()) {
        Interface.remove_point();
        Interface.load_point();
    }
});

$('#freight_transport').click(function() {
    /*
    клик по кнопке фильтра грузового транспорта
    */
    if (Interface.is_freight()) {
        /*
        если кнопка активна, выключить
        */
        Interface.set_transport({
            passenger: 0,
            freight: 0,
        });
    }
    else {
        /*
        есди кнопка не активна, включить
        */
        Interface.set_transport({
            passenger: 0,
            freight: 1
        });
    }
    if (Interface.is_active()) {
        Interface.remove_point();
        Interface.load_point();
    }
});

$('#positon').click(function() {
    /*
    клик по кнопке позиционирования
    */
    if (Interface.is_position()) {
        /*
        если кнопка активна, выключить
        */
        Interface.set_position(0);
    }
    else {
        /*
        если кнопка не активна, включить
        */
        interface.set_position(1);
    }
});

$('#regions').click(function(event) {
    /*
    клик по кнопке выбора региона
    */
    if ((event.clientX) >= $(this).offset().left) {
        $(this).children('div').toggleClass('view_box');
    }
    if ($('#search').children('div').hasClass('view_box')) {
        $('#search').children('div').removeClass('view_box')
    }
    if (event.target.tagName == 'BUTTON') {
        if ($(Interface.regions.input).val() > 0) {
            /*
            если выбран регион (проверка по id пегиона)
            */
            Interface.set_region($(Interface.regions.input).val());
        }
        else {
            /*
            если установлено пустое значение
            */
            Interface.set_region(0)
        }
        $(this).children('div').toggleClass('view_box');
        set_url();
        if (Interface.is_active()) {
            Interface.remove_point();
            Interface.load_point();
        }
    }
});

$('#search').click(function(event) {
    /*
    клик по кнопке поиска по описанию
    */
    if ((event.clientX) >= $(this).offset().left) {
        $(this).children('div').toggleClass('view_box');
    }
    if ($('#regions').children('div').hasClass('view_box')) {
        $('#regions').children('div').removeClass('view_box')
    }
    if (event.target.tagName == 'BUTTON') {
        Interface.set_search($(Interface.search.input).val());
        $(this).children('div').toggleClass('view_box');
        set_url();
        if (Interface.is_active()) {
            Interface.remove_point();
            Interface.load_point();
        }
    }
    else {
        if (Storage.get_filters().search) {
            $(Interface.search.input).val(Storage.get_filters().search)
        }
    }
});


$('#icons').click(function(event) {
    /*
    клик по иконке сервиса
    */
    var action_point = $(event.target).parent('li').get(0);
    Interface.set_points(action_point);
    set_url();
});

/*
подгрузка данных при клике по иконке на карте
*/
map.on('popupopen', function(event){
    var content = event.popup._content;
    var id_point = content.id;
    $.ajax({
        url: `/map/get_info`,
        type: 'POST',
        data: {
            id_point: id_point
        }
    }).done(function(data){
        var point_data = JSON.parse(data);
        $('.name_point').html(point_data['name']);
        $('.time_work_point').html(point_data['time_work']);
        if (point_data['transport'] == 1) {
            $('.transport_point').html('Все виды транспорта')
        }
        if (point_data['transport'] == 2) {
            $('.transport_point').html('Только легковой транспорт')
        }
        if (point_data['transport'] == 3) {
            $('.transport_point').html('Только грузовой транспорт')
        }
        var address = point_data['region'] + ', ' +
        point_data['district'] + ', ' +
        point_data['city'];
        if (point_data['street'] != 'Нет информации'){
            address = address + ', ' +
            point_data['street'];
        }
        $('.address_point').html(address);
        var working_time = $('.working_time').get();
        var flag = false;
        for(i=0; i<working_time.length; i++){
            if($(working_time[i]).html() != 'Выходной'){
                flag = true;
                break;
            }
        }
        if (!flag){
            for(i=0; i<working_time.length; i++){
                $(working_time[i]).html('Нет данных');
            }
        }
    });
});