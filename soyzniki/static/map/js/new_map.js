var storage = {
    /*
    Объект хранилище. Держит в памяти значения последних 'действий':
        map - положение карты, зум, положение панели с сервисами;
        servic - название активированного сервиса;
        filters - актиированные пользователем филтры данных;
        points - данные последнего запроса точек по одному сервису;

    поле 'name' хранит название ключа для сохранения в локальном
        хранилище или куках
    */
    support: true,
    map: {name: 'map', coords: false, zoom: 4, scroll: 0},
    servis: {name: 'servis', point: false},
    filters: {name: 'filter', transport: false, region: false},
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
        j,yf
        */
        if (this.supprt) {
            window.localStorage[obj.name] = obj;
        }
        else {
            $.cookie(obj.name, JSON.stringify(obj), {
                path: '/map/'
            });
        }
    },
    get_map_data: function() {
        return this.map;
    },
    set_map_data: function(map_coords, map_zoom, map_scroll) {
        this.map.coords = map_coords;
        this.map.zoom = map_zoom;
        this.map.scroll = map_scroll;
        this.update_storage(this.map);
    }
};