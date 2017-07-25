
    // ----- Script of lazy loading embedded playlist ----- //

    var playerBlockId = 'youtube-player-block';
    var youtubeApiKey = 'AIzaSyDVfQOWRkbFzU0StAYEykiwhSvs1nHwOcY'; // DON'T CHANGE!!!
    var currentPlayList;

    // PlayLists from https://www.youtube.com/channel/UCsI0ASqbW0AjE7wVX7gYuiQ/playlists
    // PlayLists from https://www.youtube.com/channel/UCO43-DKucgtc6NrUTed8lHg/playlists
    var channels = [
        "UCsI0ASqbW0AjE7wVX7gYuiQ"
    ];
        /*var channels = [
        "UCsI0ASqbW0AjE7wVX7gYuiQ",
        "UCO43-DKucgtc6NrUTed8lHg"
    ];*/
    imagePreload(channels); // запуск предзагрузки

    document.getElementById(playerBlockId).addEventListener("click", function(){
        videoLoad();
    });

    function imagePreload(channels) {
        var playlists = [];
        var count = 0;
        for (var j=0; j<channels.length; j++) {
            loadPlayList(j, count, channels, playlists);
        }
    }

    function loadPlayList(j, count, channels, playlists) {
        $.get(
            "https://www.googleapis.com/youtube/v3/playlists", {
                part: 'id',
                channelId: channels[j],
                maxResults: 50,
                key: youtubeApiKey
            },
            function (data) {
                count += data.items.length;
                $.each(data.items, function (i, item) {
                    count--;
                    playlists.push(item.id);
                });
                if ((count == 0) && (channels.length == j+1)) {

                    // Список плейлистов получен.
                    // Выбор 1 случайного, установка в currentPlayList и загрузка картинки
                    var randomPlayListIndex;

                    /* - заглушка для текущего плейлиста (увеличиваем вероятность канала с 1 плейлистом)- */
                    if (channels.length == 2                                                            //
                            && playlists.length == 7                                                    //
                            && channels[0] == "UCsI0ASqbW0AjE7wVX7gYuiQ"                                //
                            && channels[1] == "UCO43-DKucgtc6NrUTed8lHg") {                             //
                        var tmpRandom = getRandomInt(0, 8);                                             //
                        randomPlayListIndex = (tmpRandom > 5) ? 6 : tmpRandom;                          //
                    } else {                                                                            //
                        randomPlayListIndex = getRandomInt(0, playlists.length-1);                      //
                    }                                                                                   //
                    /* ----------------------------------------------------------------------------------- */

                    var playlistId = playlists[randomPlayListIndex];
                    currentPlayList = playlistId;
                    $.get(
                        "https://www.googleapis.com/youtube/v3/playlistItems",{
                            part : 'snippet',
                            maxResults : 1,
                            playlistId : playlistId,
                            key: youtubeApiKey
                        },
                        function(data) {
                            $.each( data.items, function( i, item ) {
                                var imageUrl = item.snippet.thumbnails.high.url;
                                var imgBlock = $('<img/>', {
                                    src: imageUrl
                                });
                                $('#'+playerBlockId).append(imgBlock);
                                return;
                            });
                        }
                    );
                }
            }
        );
    }

    function getRandomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    function videoLoad() {
        var playerId = playerBlockId;
        var tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    }

    var player;
    function onYouTubeIframeAPIReady() {
        player = new YT.Player(playerBlockId, {
            playerVars: {
                listType:'playlist',
                list: currentPlayList,
                'controls': 1
            },
            events: {
                'onReady': onPlayerReady
            }
        });
    }
    function onPlayerReady(event) {
        event.target.playVideo();
    }