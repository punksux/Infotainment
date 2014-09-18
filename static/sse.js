$(document).ready(function() {
    sse = new EventSource('/my_event_source');
    sse.addEventListener('outTemp', function(message) {
        jQuery({someValue: $('#outTemp').html()}).animate({someValue: message.data}, {
            duration: 1000,
            easing:'swing',
            step: function() {
                $('#outTemp').text(Math.ceil(this.someValue));
            }
        })});
    sse.addEventListener('inTemp', function(message) {
        jQuery({someValue: $('#inTemp').html()}).animate({someValue: message.data}, {
            duration: 1000,
            easing:'swing',
            step: function() {
                $('#inTemp').text(Math.ceil(this.someValue));
            }
        })});
    sse.addEventListener('time', function(message) {
        $('#clockBoxCover').html(message.data)
    });
    sse.addEventListener('rssTitle', function(message) {
        message = JSON.parse(message.data);
        $('#rss1').html('(1) - ' + message[0] + ' - ');
        $('#rss2').html(message[1] + ' - ');
        $('#rss3').html(message[2] + ' - ');
        $('#rss4').html(message[3] + ' - ');
        $('#rss5').html(message[4] + ' - ');
        $('#rss6').html(message[5] + ' - ');
        $('#rss7').html(message[6] + ' - ');
        $('#rss8').html(message[7] + ' - ');
        $('#rss9').html(message[8] + ' - ');
        $('#rss10').html(message[9] + ' - ');
    });
    sse.addEventListener('rssSum', function(message) {
        message = JSON.parse(message.data);
        $('#rss1sum').html(message[0]);
        $('#rss2sum').html(message[1]);
        $('#rss3sum').html(message[2]);
        $('#rss4sum').html(message[3]);
        $('#rss5sum').html(message[4]);
        $('#rss6sum').html(message[5]);
        $('#rss7sum').html(message[6]);
        $('#rss8sum').html(message[7]);
        $('#rss9sum').html(message[8]);
        $('#rss10sum').html(message[9]);
    });
    sse.addEventListener('icon', function(message) {
        message = JSON.parse(message.data);
        if (message[0] == 'sun'){
            $('#back').html('<div id="sun"></div>');}
        else if (message[0] == 'moon') {
            $('#back').html('<div id="moon"><img src="/static/images/moon.png"></div>');}
        else {
            $('#back').html('');}

        if (message[1] == ''){
            $('#mid').css('visibility', 'hidden');}
        else {
            $('#mid').html('<img src="/static/images/' + message[1] + '" >').css('visibility', 'visible');}

        if (message[2] == ''){
            $('#front').css('visibility', 'hidden');}
        else {
            $('#front').html('<img src="/static/images/' + message[2] + '" >').css('visibility', 'visible');}
    });

    $("ul#ticker01").webTicker('update');
});

