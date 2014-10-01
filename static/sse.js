var cover = 1;
$(document).ready(function() {
    var dayOrNight = '';
    var icon = '';
    sse = new EventSource('/my_event_source');
    sse.addEventListener('dayNight', function(message) {
//        $('#test').html(message.data);
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
        $("ul#ticker01").webTicker('update','<li id="rss1">' + message[0].replace('#PrepareU: @Utah_Football', '') + ' - </li>'+
                                            '<li id="rss2">' + message[1].replace('#PrepareU: @Utah_Football', '') + ' - </li>'+
                                            '<li id="rss3">' + message[2].replace('#PrepareU: @Utah_Football', '') + ' - </li>'+
                                            '<li id="rss4">' + message[3].replace('#PrepareU: @Utah_Football', '') + ' - </li>'+
                                            '<li id="rss5">' + message[4].replace('#PrepareU: @Utah_Football', '') + ' - </li>'+
                                            '<li id="rss6">' + message[5].replace('#PrepareU: @Utah_Football', '') + ' - </li>'+
                                            '<li id="rss7">' + message[6].replace('#PrepareU: @Utah_Football', '') + ' - </li>'+
                                            '<li id="rss8">' + message[7].replace('#PrepareU: @Utah_Football', '') + ' - </li>'+
                                            '<li id="rss9">' + message[8].replace('#PrepareU: @Utah_Football', '') + ' - </li>'+
                                            '<li id="rss10">' + message[9].replace('#PrepareU: @Utah_Football', '') + ' </li>','reset');
        $('#rss1').click(function(){
            $('#rss1sum, #screenCover, #popupContent').css('display','table');
        });
        $('#rss2').click(function(){
            $('#rss2sum, #screenCover, #popupContent').css('display','inline-block');
        });
        $('#rss3').click(function(){
            $('#rss3sum, #screenCover, #popupContent').css('display','inline-block');
        });
        $('#rss4').click(function(){
            $('#rss4sum, #screenCover, #popupContent').css('display','inline-block');
        });
        $('#rss5').click(function(){
            $('#rss5sum, #screenCover, #popupContent').css('display','inline-block');
        });
        $('#rss6').click(function(){
            $('#rss6sum, #screenCover, #popupContent').css('display','inline-block');
        });
        $('#rss7').click(function(){
            $('#rss7sum, #screenCover, #popupContent').css('display','inline-block');
        });
        $('#rss8').click(function(){
            $('#rss8sum, #screenCover, #popupContent').css('display','inline-block');
        });
        $('#rss9').click(function(){
            $('#rss9sum, #screenCover, #popupContent').css('display','inline-block');
        });
        $('#rss10').click(function(){
            $('#rss10sum, #screenCover, #popupContent').css('display','inline-block');
        });
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
    sse.addEventListener('rssSource', function(message) {
        $('div#sourceText').html(message.data);
    });
    sse.addEventListener('icon', function(message) {
        var rand = Math.floor(Math.random() * (5 - 1 + 1)) + 1;
        if (message.data === 'partlysunny'){icon = 'mostlycloudy'}
        else if (message.data === 'mostlysunny'){icon = 'partlycloudy'}
        else if (message.data === 'sunny'){icon = 'clear'}
        else if (message.data.slice(0,6) === 'chance'){icon = message.data.slice(6)}
        else {icon = message.data}
        $('#test2').html(message.data + ' - ' + icon + ' - ' + rand);
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
            $('#tom').hide(1000);
        } else {

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
     sse.addEventListener('allergyForecast', function(message) {
        message = JSON.parse(message.data);
        var color = ['','','',''];
         for (i = 0; i < 5; i++){
             if (message[i] < 5) {color[i]='#00ff00'}else if (message[i] >= 9){color[i]='#ff0000'}else{color[i]='#E4E368'}
         }
         $('#allergyDay1').css({height: parseFloat(message[0])*10, 'background': '-moz-linear-gradient(bottom, #00ff00 0%, ' + color[0] + ' 80%'});
         $('#allergyDay1:before').css({'border-width': parseFloat(message[0])*10 + 'px 70px 0 0'});
         $('#allergyDay2').css({height: parseFloat(message[1])*10, 'background': '-moz-linear-gradient(bottom, #00ff00 0%, ' + color[1] + ' 80%' });
         $('#allergyDay3').css({height: parseFloat(message[2])*10, 'background': '-moz-linear-gradient(bottom, #00ff00 0%, ' + color[2] + ' 80%' });
         $('#allergyDay4').css({height: parseFloat(message[3])*10, 'background': '-moz-linear-gradient(bottom, #00ff00 0%, ' + color[3] + ' 80%' });
         $('#allergyNumber1').html(message[0]);
         $('#allergyNumber2').html(message[1]);
         $('#allergyNumber3').html(message[2]);
         $('#allergyNumber4').html(message[3]);

        var d = new Date();
        var weekday = new Array(7);
        weekday[0]=  "Sunday";
        weekday[1] = "Monday";
        weekday[2] = "Tuesday";
        weekday[3] = "Wednesday";
        weekday[4] = "Thursday";
        weekday[5] = "Friday";
        weekday[6] = "Saturday";

        var plus = [];
        for (i=1;i<4;i++){
            if ((d.getDay()+i)>6){
                plus[i] = (d.getDay()+i)-7;
            } else {
                plus[i] = d.getDay()+i
            }
        }

        $('#allergyDayName2').html(weekday[plus[1]]);
        $('#allergyDayName3').html(weekday[plus[2]]);
        $('#allergyDayName4').html(weekday[plus[3]]);

    });
    sse.addEventListener('predominantPollen', function(message) {
       $('#predominantPollen').html(message.data);
    });
    sse.addEventListener('fullWeather', function(message) {
        message = JSON.parse(message.data);
        $('#cityName').html(message[0]);
        $('#updateTime').html('Last Update: ' + message[1]);
        $('#condition').html('Condition: ' + message[2]);
        $('#sunsetTime').html('Sunset: ' + (parseInt(message[3])-12) + ':' + message[4] + ' PM');
        $('#sunriseTime').html('Sunrise: ' + message[5] + ':' + message[6] + ' AM');
        $('#humidity').html('Humidity: ' + message[7]);
        $('#precip').html('Precipitation: ' + message[8]);
        $('#wind').html('Wind: ' + message[9]);
        $('#gif').attr('src','/static/images/radar.gif');
//        $('#gif').attr('src','http://api.wunderground.com/api/c5e9d80d2269cb64/animatedradar/q/84123.gif?radius=100&width=200&height=200&newmaps=1&noclutter=1&num=15');
    });
    sse.addEventListener('hourlyTemps', function(message) {
        var d = new Date();
            var i;
            for (i=0;i<12;i++) {
                var hours = (d.getHours()+i) % 12;
                if (hours == 0) {hours += 12;}
                $('tr#hourlyTimes td:nth-child('+(i+1)+')').html(hours);
            }
        message = JSON.parse(message.data);
        for (i=0;i<12;i++) {
            $('tr#hourlyTemps td:nth-child(' + (i+1) + ')').html(message[i] + '°');
        }
    });
    sse.addEventListener('alert', function(message) {
        message = JSON.parse(message.data);
        $('#test').html(message[0])
        if (message[0] != ''){
            $('#alert').html(message[0]).show().click(function(){
            $('#alertDescription, #screenCover, #popupContent').css('display','inline-block');
            });
            $('#alertDescription').html(message[1]);
        } else {
            $('#alert').html(message[0]).hide();
        }
    });

    skycons.play();
});

