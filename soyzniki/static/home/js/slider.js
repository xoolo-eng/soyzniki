$('#country_img ul').css({width: $('#country_img li').length * 100 + '%'});
$(document).ready(function(){
    var country_links = $('#country_list a').get();
    for (i=0;i<country_links.length;i++) {
        $(country_links[i]).removeAttr('href');
        $(country_links[i]).css({cursor: 'pointer'});
    }
    var country_item = $('#country_list #'+ACTIV_COUNTRY).get(0);
    $(country_item).children('a').addClass('active');
    var country_image = $('[title="'+ACTIV_COUNTRY+'"]').get(0);
    var width_image = $(country_image).width();
    var position = $(country_image).position().left;
    for (i=0; i<(position/width_image);i++) {
       $(images[0]).remove();
       $('#country_img ul').append(images[0]);
   }
});
$('#country_list li').click(function(){
    var images = $('#country_img li').get();
    var list = $('#country_list li').get();
    var country_name = $(this).attr('id');
    var country_image = $('[title="'+country_name+'"]').get(0);
    var width_image = $(country_image).width();
    var position = $(country_image).position().left;
    for (i=0; i<(position/width_image);i++) {
       $(images[0]).remove();
       $('#country_img ul').append(images[0]);
    }
    for (i=0;i<list.length;i++) {
        $(list[i]).children('a').removeClass('active');
    }
    $(this).children('a').addClass('active');
});
$('#country_list li').click(function(){
    if ($('body').width() <= 620) {
        $('#map').removeClass('open');
    }
});
$('#country_button').click(function(){
    $('#map').toggleClass('open');
});