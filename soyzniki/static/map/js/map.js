var servis;
var start_position;
var clasters = {
	all_transport: undefined,
	passenger_transport: undefined,
	freight_transport: undefined
};
var marker;
var my_point;
var end_position;
var map = L.map('map', {minZoom: 3});
var country = ACTIV_COUNTRY;
L.tileLayer('https://tile-{s}.openstreetmap.fr/hot/{z}/{x}/{y}.png', {attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);
$(document).ready(function(){
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
	initialize();
});
$(window).resize(function() {

});

$(window).unload(function(){
	var active = $('#icons li.active').get(0);
	var active_point;
	if (active !== undefined) {
		active_point = $(active).attr('id');
	}
	else {
		active_point = ''
	}
	var map_cookie = {
		center: map.getCenter(),
		zoom: map.getZoom(),
		scroll: $('#icons').scrollTop(),
		activate: active_point
	}
	var cookie_name = `map_${country}`;
	$.cookie(cookie_name, JSON.stringify(map_cookie),
	{
		path: '/map/'
	});
});
function initialize(){
	// if ($.cookie('saveresult') === undefined) {
	// 	localStorage.clear();
	// }
	var map_cookie;
	var cookie_name = `map_${country}`;
	if($.cookie(cookie_name) !== undefined)
	{
		map_cookie = JSON.parse($.cookie(cookie_name));
		map.setView(map_cookie.center, map_cookie.zoom);
		$('#icons').scrollTop(map_cookie.scroll);
		if (map_cookie.activate !== '') {
			var icon = $('#' + map_cookie.activate).get(0);
			if (icon !== undefined) {
				$(icon).addClass('active');
				get_point(map_cookie.activate, country);
			}
		}
		else {
			var url = window.location.pathname;
			var url_list = url.split('/').slice(0, -1);
			var type_servis = url_list[url_list.length - 1]
			var servic = $('#' + type_servis).get(0);
			if (servic !== undefined) {
				$(servic).addClass('active');
				get_point(map_cookie.activate, country);
			}
		}
		
	}
	else
	{
		$.ajax({
			url: '/map/get_lat_lng',
			type: 'POST',
			data: {
				'country': country
			},
			dataType: 'json'
		}).done(function(data){
			map.setView(data['lat_lng'], 8)
		});
	}

}
icons.onclick = function(event){
	var active = this.getElementsByClassName('active')[0]
	var icon = event.target.parentElement;
	var url_page;
	var url_list;
	var url = window.location.pathname;
	if(active === undefined)
	{
		icon.className = 'active';
		servis = icon.id;
		url_page = `${url}${servis}/`;
		console.log(url_page);
		history.pushState('', '', url_page);
		get_point(servis, country)
	}
	else
	{
		if(icon.className == 'active')
		{
			icon.className = '';
			remove_point()
			url_list = url.split('/').slice(0, -2)
			url_page = url_list.join('/') + '/';
			console.log(url_page);
			history.pushState('', '', url_page);
		}
		else
		{
			active.className = '';
			remove_point()
			url_list = url.split('/').slice(0, -2)
			url_page = url_list.join('/') + '/';
			console.log(url_page);
			history.pushState('', '', url_page);
			icon.className = 'active';
			servis = icon.id;
			url_page = `${url_page}${servis}/`;
			console.log(url_page)
			history.pushState('', '', url_page);
			get_point(servis, country)
		}
	}
	$('#open_button').removeClass('open');
	$('#open_button').addClass('close');
	$('#leftBar').removeClass('open');
	$('#leftBar').addClass('close');
	if ($('#passenger_transport').hasClass('icon_action')) {
		$('#passenger_transport').removeClass('icon_action');
	}
	if ($('#freight_transport').hasClass('icon_action')) {
		$('#freight_transport').removeClass('icon_action');
	}
}
$('#search').click(function() {
	$(this).children('div').toggleClass('view_box');
	if ($(this).find('#search_filter').val() == '') {
		$(this).toggleClass('icon_action');
	}
});
$('#regions').click(function() {
	$(this).children('div').toggleClass('view_box');
	if ($(this).find('#region_filter').val() == '') {
		$(this).toggleClass('icon_action');
	}
});

$('#passenger_transport').click(function(){
	var open_servis = $('.active').get(0);
	if (open_servis !== undefined){
		if($(this).hasClass('icon_action')){
			$(this).removeClass('icon_action');
		}
		else {
			if($('#freight_transport').hasClass('icon_action')){
				$('#freight_transport').removeClass('icon_action');
				$(this).addClass('icon_action');
			}
			else{
				$(this).addClass('icon_action');
			}
		}
	}
});
$('#freight_transport').click(function(){
	var open_servis = $('.active').get(0);
	if (open_servis !== undefined){
		if($(this).hasClass('icon_action')){
			$(this).removeClass('icon_action');
		}
		else {
			if($('#passenger_transport').hasClass('icon_action')){
				$('#passenger_transport').removeClass('icon_action');
				$(this).addClass('icon_action');
			}
			else{
				$(this).addClass('icon_action');
			}
		}
	}
});
$('#position').click(function(){
	var watchID;
	var interval;
	if ($(this).hasClass('icon_action')){
		$(this).removeClass('icon_action');
		clearInterval(interval)
		map.removeLayer(my_point);
	}
	else{
		var my_marker;
		if ("geolocation" in navigator) {
			navigator.geolocation.getCurrentPosition(function(position) {
				my_marker=L.icon({iconUrl:"/static/map/images/position.svg",iconSize:[46,46],iconAnchor:[23,23],popupAnchor:[0,-23]});
				map.setView([position.coords.latitude, position.coords.longitude]);
				my_point = L.marker([position.coords.latitude, position.coords.longitude], {icon: my_marker}).addTo(map);
			});
			interval = setInterval(function() {
				set_my_pos(my_marker);
			}, 5000);
			$(this).addClass('icon_action');
		}
		else {
			alert('Ваш браузер не поодерживает получение текущего местополжения')
		}
	}
});
function set_my_pos(marker){
	navigator.geolocation.getCurrentPosition(function(position) {
		map.removeLayer(my_point);
		map.setView([position.coords.latitude, position.coords.longitude]);
		my_point = L.marker([position.coords.latitude, position.coords.longitude], {icon: marker}).addTo(map);
	});
}
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
function get_point(servis, country){
	start_animate();
	if(window.localStorage[`${servis}_point`] !== undefined){
		var points = JSON.parse(window.localStorage[`${servis}_point`]);
		stop_animate();
		add_points(points['points'], points['marker']);
	}
	else {
		$.ajax({
			url: '/map/find_point',
			type: 'POST',
			data: {
				country: country,
				servis: servis
			}
		}).done(function(data){
			try {
				window.localStorage[`${servis}_point`] = data;
			} catch (e) {
				if (e == QUOTA_EXCEEDED_ERR) {
					window.localStorage.clear();
				}
			}
			// window.localStorage.clear();
			window.localStorage[`${servis}_point`] = data;
			var points = JSON.parse(window.localStorage[`${servis}_point`]);
			stop_animate();
			add_points(points['points'], points['marker']);
		});
	}
}
function add_points(points, marker){
	if ($.cookie('saveresult') === undefined) {
		$.cookie('saveresult', 1, {path: '/map/'});
	}
	var elements = new Array();
	for (i=0; i<points.length; i++) {
		// var id = document.createElement('p');
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
		// id.className = 'id_point';
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
		// id.innerHTML = points[i]['id'];
		lat.innerHTML = 'Широта: ' + points[i]['lat'];
		lon.innerHTML = 'Долгота: ' + points[i]['lon'];
		desc_point.id = points[i]['id'];
		info.appendChild(name);
		// info.appendChild(id);
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
	add_claster(elements, marker);

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
function add_claster(elements, marker_icon)
{
	clasters.all_transport = new L.markerClusterGroup();
	var icon = L.icon({
		iconUrl: '/media/' + marker_icon,
		iconSize: [46, 46],
		iconAnchor: [23, 23],
		popupAnchor: [0, -23],
	});
	marker = new Array();
	for(i=0;i<elements.length;i++) {
		marker[i] = L.marker([+elements[i]['lat'], +elements[i]['lon']], {icon: icon}).addTo(clasters.all_transport);
		marker[i].openPopup().bindPopup(elements[i]['data'], {closeButton: false, minWidth: 300, maxWidth: 300});
	}
	clasters.all_transport.addTo(map);
/*
	clasters.all_transport = new L.markerClusterGroup();
	clasters.passenger_transport = new L.markerClusterGroup();
	clasters.freight_transport = new L.markerClusterGroup();
	marker = new Array();
	for(i=0;i<elements.length;i++)
	{
		var icon = L.icon({
			iconUrl: '/media/' + icon,
			iconSize: [46, 46],
			iconAnchor: [23, 23],
			popupAnchor: [0, -23],
		});
		if(elements[i]['transport'] == 1){
			marker[i] = L.marker([+elements[i]['lat'], +elements[i]['lon']], {icon: icon}).addTo(clasters.all_transport);
		}
		if(elements[i]['transport'] == 2){
			marker[i] = L.marker([+elements[i]['lat'], +elements[i]['lon']], {icon: icon}).addTo(clasters.passenger_transport);
		}
		if(elements[i]['transport'] == 3){
			marker[i] = L.marker([+elements[i]['lat'], +elements[i]['lon']], {icon: icon}).addTo(clasters.freight_transport);
		}
		marker[i].openPopup().bindPopup(elements[i]['data']);
	}
	clasters.all_transport.addTo(map);
	clasters.passenger_transport.addTo(map);
	clasters.freight_transport.addTo(map);
*/}
function remove_point()
{
	map.removeLayer(clasters.all_transport);
	/*
	map.removeLayer(clasters.all_transport);
	map.removeLayer(clasters.passenger_transport);
	map.removeLayer(clasters.freight_transport);*/
}

$('#open_button').click(function() {
	if ($(this).hasClass('close')) {
		$(this).removeClass('close');
		$(this).addClass('open');
		$('#leftBar').removeClass('close');
		$('#leftBar').addClass('open');
	}
	else {
		$(this).removeClass('open');
		$(this).addClass('close');
		$('#leftBar').removeClass('open');
		$('#leftBar').addClass('close');

	}
});