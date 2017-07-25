var map = L.map('map');
L.tileLayer('http://tile-{s}.openstreetmap.fr/hot/{z}/{x}/{y}.png', {attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);
map.setView([52.449986, 30.993617], 14);
var my_marker=L.icon({iconUrl:"/static/soyzniki/images/soyzniki.marker.svg",iconSize:[46,46],iconAnchor:[23,23],popupAnchor:[0,-23]});
var my_point = L.marker([52.449986, 30.993617], {icon: my_marker}).addTo(map);