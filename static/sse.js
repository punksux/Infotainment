$(document).ready(function() {
    sse = new EventSource('/my_event_source');
    sse.addEventListener('dayNight', function(message) {
        $('#test').html(message.data);
        if (message.data === 'night'){
            $('#day').fadeOut(1000);
            $('#clockBoxCoverDay').fadeOut(1000);
            $( "#clockBox" ).stop(true).animate({backgroundColor: '#141f31', borderColor: '#fff'}, 1000 );
            $( "#content .ui-state-default a, #tabList .ui-state-default, #tabList .ui-state-default" ).css('background', "#151532");
            $( "#content .ui-state-active a" ).css('background',"#1f1f3f");
            $( "#tabList .ui-state-active" ).css('background',"#1f1f3f");
            $('#tom').css('display','inline-block');
        } else {
            $('#day').fadeIn(1000);
            $( "#clockBox" ).stop(true).animate({backgroundColor: '#c9e3fb', borderColor: '#5382cc'}, 1000 );
            $('#clockBoxCoverDay').fadeIn(1000);
            $( "#content .ui-state-default a, #tabList .ui-state-default, #tabList .ui-state-default" ).css('background', "#afc9e1");
            $( "#content .ui-state-active a").css('background', "#c2ddf5;");
            $( "#tabList .ui-state-active" ).css('background', "#c2ddf5;");
            $('#tom').css('display','none');
        }
    });
    // ^^^^^^Figure out why tabs are not switching inistantly^^^^^
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
    sse.addEventListener('tomTemp', function(message) {
        jQuery({someValue: $('#tomTemp').html()}).animate({someValue: message.data}, {
            duration: 1000,
            easing:'swing',
            step: function() {
                $('#tomTemp').text(Math.ceil(this.someValue));
            }
        })});
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

    sse.addEventListener('forecastDay', function(message) {
        message = JSON.parse(message.data);
        $('#day1name').html(message[0]);
        $('#day2name').html(message[1]);
        $('#day3name').html(message[2]);
        $('#day4name').html(message[3]);
        $('#day5name').html(message[4]);
    });
    sse.addEventListener('forecastHigh', function(message) {
        message = JSON.parse(message.data);
        $('#day1high').html(message[0]);
        $('#day2high').html(message[1]);
        $('#day3high').html(message[2]);
        $('#day4high').html(message[3]);
        $('#day5high').html(message[4]);
    });
    sse.addEventListener('forecastLow', function(message) {
        message = JSON.parse(message.data);
        $('#day1low').html(message[0]);
        $('#day2low').html(message[1]);
        $('#day3low').html(message[2]);
        $('#day4low').html(message[3]);
        $('#day5low').html(message[4]);
    });
    var skycons = new Skycons({"color": "white"});
    sse.addEventListener('forecastCond', function(message) {
        message = JSON.parse(message.data);
        var i;
        for(i in message){
            switch (message[i]){
                case 'partlycloudy':
                case 'mostlysunny':
                    message[i] = 'partly-cloudy-day';
                    break;
                case 'clear':
                    message[i] = 'clear-day';
                    break;
                case 'mostlycloudy':
                case 'partlysunny':
                    message[i] = 'cloudy';
                    break;
                case 'flurries':
                    message[i] = 'snow';
                    break;
                case 'chancetstorms':
                    message[i] = 'rain';
                    break;

            }
        }
        skycons.set("icon1", message[0]);
        skycons.set("icon2", message[1]);
        skycons.set("icon3", message[2]);
        skycons.set("icon4", message[3]);
        skycons.set("icon5", message[4]);

    });


    skycons.play();
    $("ul#ticker01").webTicker('update');
});

