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
    support: true,
    map: {name: 'map', coords: false, zoom: 4, scroll: 0},
    servis: {name: 'servis', point: false},
    filters: {name: 'filters', transport: false, region: false},
    points: {name: 'points', data: null},

    test_support: function() {
        /*
        проверка на поддержку локальноно хранилища, если поддержки
        нет, данные запишутся в куки
        */
        try {
            window.localStorage;
            this.suppotr = true;
        } catch (e) {
            this.suppotr false;
        }
    },
    update_storage: function(obj) {
        /*
        обнавление данных в хранилище браузера
        */
        if (this.support) {
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
        if (this.support) {
            if (window.localStorage['map'] !== undefined){
                this.map = window.localStorage['map'];
            }
            if (window.localStorage['servis'] !== undefined){
                this.servis = window.localStorage['servis'];
            }
            if (window.localStorage['filters'] !== undefined){
                this.filters = window.localStorage['filters'];
            }
            if (window.localStorage['points'] !== undefined){
                this.points = window.localStorage['points'];
            }
        }
        else {
            if ($.cookie('map') !== undefined) {
                this.map = JSON.parse($.cookie('map'));
            }
            if ($.cookie('servis') !== undefined) {
                this.servis = JSON.parse($.cookie('servis'));
            }
            if ($.cookie('filters') !== undefined) {
                this.filters = JSON.parse($.cookie('filters'));
            }
            if ($.cookie('points') !== undefined) {
                this.points = JSON.parse($.cookie('points'));
            }
        }
    },
    read_storage: function() {
        /*
        запись данных хранилища из памяти
        */
        this.update_storage(this.map);
        this.update_storage(this.servis);
        this.update_storage(this.filters);
        this.update_storage(this.points);
    },
    get_map_data: function() {
        var map_data = this.map;
        delete map_data.name;
        return map_data;
    },
    set_map_data: function(map_coords, map_zoom, map_scroll) {
        this.map.coords = map_coords;
        this.map.zoom = map_zoom;
        this.map.scroll = map_scroll;
        this.update_storage(this.map);
    },
    get_servis_data: function() {
        var servis_data = this.servis;
        delete servis_data.name;
        return servis_data
    }
};