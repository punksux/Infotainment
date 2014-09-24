var cover = 1;
$(document).ready(function() {
    var dayOrNight = '';
    var icon = '';
    sse = new EventSource('/my_event_source');
    sse.addEventListener('dayNight', function(message) {
        $('#test').html(message.data);
        if (message.data === 'night'){
            dayOrNight = 'night'
        } else {
            dayOrNight = 'day'
        }
    });
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
//    Figure out how to update rss
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
        var rand = Math.floor(Math.random() * (5 - 1 + 1)) + 1;
        if (message.data === 'partlysunny'){icon = 'mostlycloudy'}
        else if (message.data === 'mostlysunny'){icon = 'partlycloudy'}
        else if (message.data === 'sunny'){icon = 'clear'}
        else {icon = message.data}
        $('#test2').html(icon + ' - ' + rand);
        if (cover === 1){
            $.get('/static/images/' + dayOrNight + '-' + icon + '-' + rand + '.jpg')
                .done(function() {
                    $('#day').css('background', 'url(/static/images/' + dayOrNight + '-' + icon + '-' + rand + '.jpg)').fadeIn(1000);
                }).fail(function() {
                    $('#day').css('background', 'url(/static/images/' + dayOrNight + '-' + icon + '-1.jpg)').fadeIn(1000);
                });
            $('#night').fadeOut(1000);
            cover = 2;
        } else {
            $.get('/static/images/' + dayOrNight + '-' + icon + '-' + rand + '.jpg')
                .done(function() {
                    $('#night').css('background', 'url(/static/images/' + dayOrNight + '-' + icon + '-' + rand + '.jpg)').fadeIn(1000);
                }).fail(function() {
                    $('#night').css('background', 'url(/static/images/' + dayOrNight + '-' + icon + '-1.jpg)').fadeIn(1000);
                });
            $('#day').fadeOut(1000);
            cover = 1;
        }



        if (dayOrNight === 'day'){
//            $('#day').css('background', 'url(/static/images/day-' + icon + '-1.jpg)').fadeIn(1000);
            $('#tom').hide(1000);
        } else {
//            $('#night').css('background', 'url(/static/images/night-' + icon + '-1.jpg)');
//            $('#day').fadeOut(1000);
            $('#tom').show(1000);
        }
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
                case 'sunny':
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
                case 'hazy':
                    message[i] = 'fog';
                    break;
                case 'tstorms':
                    message[i] = 'rain';
                    break;
                case 'unknown':
                    message[i] = 'wind';
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

