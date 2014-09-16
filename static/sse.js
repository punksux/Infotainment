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
    sse.addEventListener('rss1', function(message) {
        $('#rss1').html(message.data + ' - ')
    });
    sse.addEventListener('rss1sum', function(message) {
        $('#rss1sum').html(message.data)
    });
    sse.addEventListener('rss2', function(message) {
        $('#rss2').html(message.data + ' - ')
    });
    sse.addEventListener('rss2sum', function(message) {
        $('#rss2sum').html(message.data)
    });
    sse.addEventListener('rss3', function(message) {
        $('#rss3').html(message.data + ' - ')
    });
    sse.addEventListener('rss3sum', function(message) {
        $('#rss3sum').html(message.data)
    });
    sse.addEventListener('rss4', function(message) {
        $('#rss4').html(message.data + ' - ')
    });
    sse.addEventListener('rss4sum', function(message) {
        $('#rss4sum').html(message.data)
    });
    sse.addEventListener('rss5', function(message) {
        $('#rss5').html(message.data + ' - ')
    });
    sse.addEventListener('rss5sum', function(message) {
        $('#rss5sum').html(message.data)
    });
    sse.addEventListener('iconBack', function(message) {
        if (message.data == 'sun'){
            $('#back').html('<div id="sun"></div>');}
        else if (message.data == 'moon') {
            $('#back').html('<div id="moon"><img src="/static/images/moon.png"></div>');}
        else {
            $('#back').html('');}
    });
    sse.addEventListener('iconMid', function(message) {
        if (message.data == ''){
            $('#mid').css('visibility', 'hidden');}
        else {
            $('#mid').html('<img src="/static/images/' + message.data + '" >').css('visibility', 'visible');}
    });
     sse.addEventListener('iconFront', function(message) {
        if (message.data == ''){
            $('#front').css('visibility', 'hidden');}
        else {
            $('#front').html('<img src="/static/images/' + message.data + '" >').css('visibility', 'visible');}
    });
    $("ul#ticker01").webTicker('update');
});

