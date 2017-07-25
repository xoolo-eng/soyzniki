
var element;
var hidden_element;
var latitude = document.getElementById('id_lat');
var longitude = document.getElementById('id_lon');
var map = L.map('map');
var popup = L.popup({'closeButton': false});
var zoom = {
    country: 5,
    region: 7,
    district: 9,
    city: 11
};
$(window).ready(function(){
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
});
$(document).ready(function(){
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);
    if ((latitude.value.length == 0) || (longitude.value.length == 0)){
        get_position('country', ACTIV_COUNTRY);
    }
    else {
        map.setView([latitude.value, longitude.value], zoom.city);
        popup.setLatLng([latitude.value, longitude.value])
        .setContent('Широта - '+latitude.value+'<br />Долгота - '+longitude.value)
        .openOn(map);
    }
    // latitude.readOnly = true;
    // longitude.readOnly = true;
});
$('.custom_input').blur( function(event){
    element = event.target.id;
    hidden_element = document.getElementById(element + '_id')
    setTimeout(function(){
        if(hidden_element.value.length > 0){
            get_position(element, hidden_element.value);
        }
    }, 150);
    
});
map.on('click', on_map_click);
function get_position(element, hidden_element){
    $.ajax({
        url: '/async/get_position',
        type: 'POST',
        data: {
            element: element,
            value: hidden_element
        }
    }).done(function(data){
        var position = JSON.parse(data)
        set_map(position[0], zoom[element])
    });
}
function set_map(positon, zoom){
    map.setView([positon['latitude'], positon['longitude']], zoom);
}
function on_map_click(e) {
    popup
    .setLatLng(e.latlng)
    .setContent('Широта - ' + e.latlng.lat +
        '<br />Долгота - ' + e.latlng.lng + '<br />'+
        '<button id="set_coord">Установить координаты</button>')
    .openOn(map);
    $('#set_coord').click(function(){
        latitude.value = e.latlng.lat;
        latitude.value = latitude.value.substr(0, 9);
        longitude.value = e.latlng.lng;
        longitude.value = longitude.value.substr(0, 9);
    });
}
