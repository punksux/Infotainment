var cover = 1;
$(document).ready(function () {
    var dayOrNight = '';
    var icon = '';
    var sse;
    sse = new EventSource('/my_event_source');
    sse.addEventListener('dayNight', function (message) {
        if (message.data === 'night') {
            dayOrNight = 'night';
            dayNight('night');
            $('#dimmer').fadeTo(500, .25);
        } else {
            dayOrNight = 'day';
            dayNight('day');
            $('#dimmer').fadeTo(500, 0);
        }
    });

    sse.addEventListener('outTemp', function (message) {
        jQuery({someValue: $('#outTemp').html().replace('<span>°</span>', '').replace('·', '-')}).animate({someValue: message.data}, {
            duration: 2000,
            easing: 'swing',
            step: function () {
                $('#outTemp').html(Math.ceil(this.someValue).toString().replace('-', '·') + '<span>°</span>');
            }
        })
    });
    sse.addEventListener('inTemp', function (message) {
        jQuery({someValue: $('#inTemp').html().replace('<span>°</span>', '').replace('·', '-')}).animate({someValue: message.data}, {
            duration: 2000,
            easing: 'swing',
            step: function () {
                $('#inTemp').html(Math.ceil(this.someValue).toString().replace('-', '·') + '<span>°</span>');
            }
        })
    });
    sse.addEventListener('tomTemp', function (message) {
        jQuery({someValue: $('#tomTemp').html().replace('<span>°</span>', '').replace('·', '-')}).animate({someValue: message.data}, {
            duration: 2000,
            easing: 'swing',
            step: function () {
                $('#tomTemp').html(Math.ceil(this.someValue).toString().replace('-', '·') + '<span>°</span>');
            }
        })
    });
    sse.addEventListener('rssFeed', function (message) {
        var now = new Date();
        console.log(timeStamp() + ' - New RSS');
        message = JSON.parse(message.data);
        ticker(message);
    });
    sse.addEventListener('icon', function (message) {
        $('#test2').html(message.data);
        if (cover === 1) {
            $('#day').css('background', 'url(/' + message.data + ')').fadeIn(1000);
            $('#night').fadeOut(1000);
            cover = 2;
        } else {
            $('#night').css('background', 'url(/' + message.data + ')').fadeIn(1000);
            $('#day').fadeOut(1000);
            cover = 1;
        }
        if (dayOrNight === 'day') {
            $('#out').animate({left: 210}, 1000);
            $('#tom').hide('slide', {direction: 'right', duration: 1000})
        } else {
            $('#out').animate({left: 2}, 1000);
            $('#tom').show('slide', {direction: 'right', duration: 1000}).fadeTo(0, 1)
        }
    });
    sse.addEventListener('forecastDay', function (message) {
        message = JSON.parse(message.data);
        $('#day1name').html(message[0]);
        $('#day2name').html(message[1]);
        $('#day3name').html(message[2]);
        $('#day4name').html(message[3]);
        $('#day5name').html(message[4]);
    });
    sse.addEventListener('forecastHigh', function (message) {
        message = JSON.parse(message.data);
        $('#day1high').html(message[0]);
        $('#day2high').html(message[1]);
        $('#day3high').html(message[2]);
        $('#day4high').html(message[3]);
        $('#day5high').html(message[4]);
    });
    sse.addEventListener('forecastLow', function (message) {
        message = JSON.parse(message.data);
        $('#day1low').html(message[0]);
        $('#day2low').html(message[1]);
        $('#day3low').html(message[2]);
        $('#day4low').html(message[3]);
        $('#day5low').html(message[4]);
    });
    var skycons = new Skycons({"color": "white"});
    sse.addEventListener('forecastCond', function (message) {
        message = JSON.parse(message.data);
        for (var i = 0;i < message.length; i++) {
            switch (message[i]) {
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
                case 'chanceflurries':
                case 'chancesleet':
                case 'chancesnow':
                case 'sleet':
                    message[i] = 'snow';
                    break;
                case 'chancetstorms':
                case 'chancerain':
                case 'tstorms':
                    message[i] = 'rain';
                    break;
                case 'hazy':
                    message[i] = 'fog';
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
    sse.addEventListener('forecastDecription', function (message) {
        message = JSON.parse(message.data);
        var i;
        for (i = 0; i < 5; i++) {
            (function (e) {
                $('#day' + (e + 1) + 'cover').click(function () {
                    $('#day1description .synopsis').html(message[e].replace(/\./g, '.<br><br>'));
                    $('#day1description, #screenCover, #popupContent').fadeIn(300);
                });
            })(i);
        }
    });
    sse.addEventListener('allergyForecast', function (message) {
        message = JSON.parse(message.data);
        var color = ['', '', '', ''];
        var i;
        for (i = 0; i < 5; i++) {
            if (message[i] < 5) {
                color[i] = '#00ff00'
            } else if (message[i] >= 9) {
                color[i] = '#ff0000'
            } else {
                color[i] = '#F9F230'
            }
        }

        $('#allergyDay1').css({height: parseFloat(message[0]) * 10, 'background': '-webkit-linear-gradient(bottom, #00ff00 0%, ' + color[0] + ' 80%)'});
        $('#allergyDay2').css({height: parseFloat(message[1]) * 10, 'background': '-webkit-linear-gradient(bottom, #00ff00 0%, ' + color[1] + ' 80%)'});
        $('#allergyDay3').css({height: parseFloat(message[2]) * 10, 'background': '-webkit-linear-gradient(bottom, #00ff00 0%, ' + color[2] + ' 80%)'});
        $('#allergyDay4').css({height: parseFloat(message[3]) * 10, 'background': '-webkit-linear-gradient(bottom, #00ff00 0%, ' + color[3] + ' 80%)'});
        $('#allergyNumber1').html(message[0]);
        $('#allergyNumber2').html(message[1]);
        $('#allergyNumber3').html(message[2]);
        $('#allergyNumber4').html(message[3]);

        var d = new Date();
        var weekday = new Array(7);
        weekday[0] = "Sunday";
        weekday[1] = "Monday";
        weekday[2] = "Tuesday";
        weekday[3] = "Wednesday";
        weekday[4] = "Thursday";
        weekday[5] = "Friday";
        weekday[6] = "Saturday";

        var plus = [];
        for (i = 1; i < 4; i++) {
            if ((d.getDay() + i) > 6) {
                plus[i] = (d.getDay() + i) - 7;
            } else {
                plus[i] = d.getDay() + i
            }
        }

        $('#allergyDayName2').html(weekday[plus[1]]);
        $('#allergyDayName3').html(weekday[plus[2]]);
        $('#allergyDayName4').html(weekday[plus[3]]);

    });
    sse.addEventListener('predominantPollen', function (message) {
        if(message.data === 'None') {
            message.data = '';
        }
        $('#predominantPollen').html(message.data);
    });
    sse.addEventListener('fullWeather', function (message) {
        message = JSON.parse(message.data);
        $('#cityName').html(message[0]);
        $('#updateTime').html('Last Update: ' + message[1]);
        $('#condition').html('Condition: ' + message[2]);
        $('#sunsetTime').html('Sunset: ' + (parseInt(message[3]) - 12) + ':' + message[4] + ' PM');
        $('#sunriseTime').html('Sunrise: ' + message[5] + ':' + message[6] + ' AM');
        $('#humidity').html('Humidity: ' + message[7]);
        $('#precip').html('Precipitation: ' + message[8]);
        $('#wind').html('Wind: ' + message[9]);
        $('#gif').attr('src', '/static/images/radar.gif');
//        $('#gif').attr('src','http://api.wunderground.com/api/c5e9d80d2269cb64/animatedradar/q/84123.gif?radius=100&width=200&height=200&newmaps=1&noclutter=1&num=15');
    });
    sse.addEventListener('hourlyTemps', function (message) {
        var d = new Date();
        var i;
        for (i = 0; i < 12; i++) {
            var hours = (d.getHours() + i) % 12;
            if (hours == 0) {
                hours += 12;
            }
            $('tr#hourlyTimes td:nth-child(' + (i + 1) + ')').html(hours);
        }
        message = JSON.parse(message.data);
        for (i = 0; i < 12; i++) {
            $('tr#hourlyTemps td:nth-child(' + (i + 1) + ')').html(message[i] + '°');
        }
    });
    sse.addEventListener('alert', function (message) {
        message = JSON.parse(message.data);

//        message = ['Big Ass Fire', 'There is a big ass fire somewhere'];
        if (message[0] != '') {
            $('#alert').html('Alert: ' + message[0]).show().click(function () {
                $('#alertDescription, #screenCover, #popupContent').css('display', 'inline-block');
            });
            $('#alertDescription .movieName').html(message[0]);
            $('#alertDescription .synopsis').html('<pre><span>' + message[1] + '</span></pre>');
        } else {
            $('#alert').html(message[0]).hide();
        }

    });
    /*sse.addEventListener('utahInfo', function (message) {
        message = JSON.parse(message.data);
        $('div#utah div.home .text').html(message[1]);
        $('div#utah div.away .text').html(message[2]);
        $('div#utah div.home .logo').css('background-image', 'url("/static/images/ncaa/' + message[1] + '.png")');
        $('div#utah div.away .logo').css('background-image', 'url("/static/images/ncaa/' + message[2] + '.png")');
        $('div#utah .timeText').html(message[3] + '<br />' + message[5] + '<br />' + message[6]);
        if (message[2] === 'BYE') {
            $('div#utah').hide();
            $('div#utahCover').hide();
        } else {
            $('div#utah').show();
            $('div#utahCover').show();
        }
    });
    sse.addEventListener('utahScore', function (message) {
        message = JSON.parse(message.data);
        $('div#utah div.home .score').html(message[3]);
        $('div#utah div.away .score').html(message[4]);
        $('div#utah .timeText').html('Quarter: ' + message[1] + '<br />' + 'Clock: ' + message[2]);
    });
    var sf_info = '';
    var kc_info = '';
    sse.addEventListener('sfInfo', function (message) {
        message = JSON.parse(message.data);
        sf_info = message[1];
        $('div#49ers div.home .text').html(message[1]);
        $('div#49ers div.away .text').html(message[2]);
        $('div#49ers div.home .logo').css('background-image', 'url("/static/images/nfl/' + message[1].replace('.', '') + '.png")');
        $('div#49ers div.away .logo').css('background-image', 'url("/static/images/nfl/' + message[2].replace('.', '') + '.png")');
        $('div#49ers .timeText').html(message[3] + '<br />' + message[5] + '<br />' + message[6]);
        if (message[2] === 'BYE') {
            $('div#49ers').hide();
            $('div#49ersCover').hide();
        } else {
            $('div#49ers').show();
            $('div#49ersCover').show();
        }

    });
    sse.addEventListener('kcInfo', function (message) {
        message = JSON.parse(message.data);
        kc_info = message[1];
        $('div#kc div.home .text').html(message[1]);
        $('div#kc div.away .text').html(message[2]);
        $('div#kc div.home .logo').css('background-image', 'url("/static/images/nfl/' + message[1] + '.png")');
        $('div#kc div.away .logo').css('background-image', 'url("/static/images/nfl/' + message[2] + '.png")');
        $('div#kc .timeText').html(message[3] + '<br />' + message[5] + '<br />' + message[6]);
        if (sf_info === kc_info || message[2] === "BYE") {
            $('div#kc').hide();
            $('div#kcCover').hide();
        } else {
            $('div#kc').show();
            $('div#kcCover').show();
        }
    });
    sse.addEventListener('rslInfo', function (message) {
        message = JSON.parse(message.data);
        $('div#rsl div.home .text').html(message[1]);
        $('div#rsl div.away .text').html(message[2]);
        $('div#rsl div.home .logo').css('background-image', 'url("/static/images/mls/' + message[1] + '.png")');
        $('div#rsl div.away .logo').css('background-image', 'url("/static/images/mls/' + message[2] + '.png")');
        $('div#rsl .timeText').html(message[3] + '<br />' + message[5]);
        if (message[3] === undefined){
            $('div#rsl').hide();
        } else {
            $('div#rsl').show();
        }
    });
    sse.addEventListener('ncaaRankings', function (message) {
        message = JSON.parse(message.data);
        var i;
        for (i = 0; i < 25; i += 1) {
            $('table#ncaaRankings tr:nth-child(' + (i + 1) + ') td:nth-child(2)').html(message[i][0]);
            $('table#ncaaRankings tr:nth-child(' + (i + 1) + ') td:nth-child(3)').html(message[i][1] + ' - ' + message[i][2]);
        }
    });
    sse.addEventListener('pac12Standings', function (message) {
        message = JSON.parse(message.data);
        var i;
        var j = 2;
        for (i = 0; i < 12; i += 1) {
            if (i > 5) {
                j = 3
            }
            $('table#pac12Standings tr:nth-child(' + (i + j) + ') td:nth-child(1)').html(message[i][0]);
            $('table#pac12Standings tr:nth-child(' + (i + j) + ') td:nth-child(2)').html(message[i][2] + ' - ' + message[i][3]);
            $('table#pac12Standings tr:nth-child(' + (i + j) + ') td:nth-child(3)').html(message[i][4] + ' - ' + message[i][5]);
        }
    });
    sse.addEventListener('soccerStandings', function (message) {
        message = JSON.parse(message.data);
        var i;
        for (i = 0; i < 19; i += 1) {
            $('table#mlsStandings tr:nth-child(' + (i + 2) + ') td:nth-child(2)').html(message[i][0]);
            $('table#mlsStandings tr:nth-child(' + (i + 2) + ') td:nth-child(3)').html(message[i][1] + ' - ' + message[i][2] + ' - ' + message[i][3]);
        }
    });
    sse.addEventListener('nflRankings', function (message) {
        message = JSON.parse(message.data);
        var i;
        var j = 2;
        for (i = 0; i < 16; i += 1) {
            if (i > 3 && i < 8) {
                j = 3
            } else if (i > 7 && i < 12) {
                j = 4
            } else if (i > 11) {
                j = 5
            }
            $('table#nflAFCRankings tr:nth-child(' + (i + j) + ') td:nth-child(1)').html(message[i][1]);
            $('table#nflAFCRankings tr:nth-child(' + (i + j) + ') td:nth-child(2)').html(message[i][3] + ' - ' + message[i][4]);
            $('table#nflAFCRankings tr:nth-child(' + (i + j) + ') td:nth-child(3)').html(message[i][5] + ' - ' + message[i][6]);
        }
        j = 2;
        for (i = 0; i < 16; i += 1) {
            if (i > 3 && i < 8) {
                j = 3
            } else if (i > 7 && i < 12) {
                j = 4
            } else if (i > 11) {
                j = 5
            }
            $('table#nflNFCRankings tr:nth-child(' + (i + j) + ') td:nth-child(1)').html(message[i + 16][1]);
            $('table#nflNFCRankings tr:nth-child(' + (i + j) + ') td:nth-child(2)').html(message[i + 16][3] + ' - ' + message[i][4]);
            $('table#nflNFCRankings tr:nth-child(' + (i + j) + ') td:nth-child(3)').html(message[i + 16][5] + ' - ' + message[i][6]);
        }
    });*/
    sse.addEventListener('openingMovies', function (message) {
        message = JSON.parse(message.data);
        var i;
        var j = 2;
        for (i = 0; i < 10; i += 1) {
            $('table#openingMovies tr:nth-child(' + (i + j) + ') td:nth-child(1)').html('<img src="' + message[i][8] + '">');
            $('table#openingMovies tr:nth-child(' + (i + j) + ') td:nth-child(2)').html(message[i][0]);
            if (message[i][4] != '') {
                $('table#openingMovies tr:nth-child(' + (i + j) + ') td:nth-child(3)').html('<img src="/static/images/rottenTomatoes/' + message[i][4] + '.png">');
            }
            $('table#openingMovies tr:nth-child(' + (i + j) + ') td:nth-child(4)').html(message[i][5]);
            $('table#openingMovies tr:nth-child(' + (i + j) + ') td:nth-child(5)').html(message[i][6]);
            $('#movie' + (i + 1) + 'sum .synopsis').html(message[i][7]);
            $('#movie' + (i + 1) + 'sum .movieName').html(message[i][0]);
            $('#movie' + (i + 1) + 'sum .rating').html('Rating: ' + message[i][1]);
            $('#movie' + (i + 1) + 'sum .length').html('Runtime: ' + message[i][2] + ' min.');
            $('#movie' + (i + 1) + 'sum .image').css({'background': 'url(' + message[i][8].replace('tmb', 'det') + ') no-repeat center'}).click(function(){
                $(this).parent().find('.synopsis').toggle(300);
                $(this).parent().find('.trailer').toggle(300);
            });
            $('#movie' + (i + 1) + 'sum iframe.trailerSrc').attr('src', message[i][11]);
            $('#movie' + (i + 1) + 'sum .sendToPhone').attr('onclick', 'sendToPhone("' + message[i][0] + '","' + message[i][10] + '")').click(function(){
                $(this).animate({backgroundColor: '#30ba6f'}, {duration: 500}).html('Sent').css('pointer-events', 'none');
            });
            $('#movie' + (i + 1) + 'sum .actors').html('Cast: <br />' + String(message[i][9]).replace(/,/g, '<br />'));
            (function (e) {
                $('table#openingMovies tr:nth-child(' + (e + j) + ')').click(function () {
                    $('#movie' + (e + 1) + 'sum, #screenCover, #popupContent').fadeIn(300);
                    $('#popupContent').addClass('movieCover');
                });
            })(i);
        }
    });
    sse.addEventListener('localEvents', function (message) {
        message = JSON.parse(message.data);
        var i;
        var j = 2;
        for (i = 0; i < 10; i += 1) {
            if (message[i][5] != '') {
                $('table#localEvents tr:nth-child(' + (i + j) + ') td:nth-child(1)').html('<img src="' + message[i][5] + '">');
            }
            $('table#localEvents tr:nth-child(' + (i + j) + ') td:nth-child(2)').html(message[i][0]);
            $('table#localEvents tr:nth-child(' + (i + j) + ') td:nth-child(3)').html(message[i][2]);

            $('#ent' + (i + 1) + 'sum .synopsis').html(message[i][1]);
            $('#ent' + (i + 1) + 'sum .rating').html('Venue: <br />' + message[i][4]);
            $('#ent' + (i + 1) + 'sum .movieName').html(message[i][0]);
            if(message[i][5] != '') {
                $('#ent' + (i + 1) + 'sum .image').css({'background': 'url(' + message[i][5].replace('small', 'medium') + ') no-repeat center'});
            }
            $('#ent' + (i + 1) + 'sum .sendToPhone').attr('onclick', 'sendToPhone("' + message[i][0] + '","' + message[i][6] + '")').click(function(){
                $(this).animate({backgroundColor: '#30ba6f'}, {duration: 500}).html('Sent').css('pointer-events', 'none');
            });
            (function (e) {
                $('table#localEvents tr:nth-child(' + (e + j) + ')').click(function () {
                    $('#ent' + (e + 1) + 'sum, #screenCover, #popupContent').fadeIn(300);
                    $('#popupContent').addClass('movieCover');
                });
            })(i);
        }
    });
    sse.addEventListener('albumInfo', function (message) {
        message = JSON.parse(message.data);
        $('td.songName').html(message[0]);
        $('td.artistName').html(message[1]);
        $('td.albumName').html(message[2]);
        if(typeof message[3] === 'undefined'){
            $('div.albumArt').css('background', 'url("/static/images/pandora/blank.jpg") no-repeat center');
        } else {
            $('div.albumArt').css('background', 'url("' + message[3] + '") no-repeat center');
        }
        if (message[6] === ''){
            $('#albumSummary').html(message[4]).css('text-align', 'left');
        } else {
            $('#albumSummary').html(message[6]).css('text-align', 'center');
        }
        if(message[5] === '1'){
            $('#upButton').css('background', 'url(/static/images/pandora/btn_up_like.png) no-repeat center');
        } else {
            $('#upButton').css('background', 'url(/static/images/pandora/btn_up.png) no-repeat center');
        }
    });
    sse.addEventListener('stations', function (message) {
        message = JSON.parse(message.data);
        $('div#stationList').html('');
        var i;
        for(i=0;i<message.length;i++){
            $('#stationList').append('<div class="station" onclick="changeStation(' + message[i][0] + ', this)">' + message[i][1] + '</div>');
        }
    });
    sse.addEventListener('holiday', function (message) {
        message = JSON.parse(message.data);
        console.log(message);
        hday = message;
        holiday2 = message[1].toLowerCase();
        holiday(holiday2);
        countdownTimer(hday);
    });
    var infoOn = false;
    sse.addEventListener('jeopardy', function (message) {
        message = JSON.parse(message.data);
        console.log(message);
        $('#jeopardyReview').html('I\'ll take <i>"' + message[3] + '"</i> for ' + message[2] + ' Alex.').click(function(){
            console.log(infoOn);
            if (infoOn === true) {
                display();
            } else {
                go()
            }
        });

        function display(){
            $('#jeopardyPopup').show("scale", {}, 200);
            $('#catText').html(message[3]);
            $('#jepCategory').delay(500).show("scale", {}, 200);
            $('#jepValue').html(message[2]).delay(1000).show("scale", {}, 200);
            $('#jepQuestion').html(message[1]).delay(1500).show("scale", {}, 200);
            $('#jepAnswer').delay(1700).show(10);
        }

        function go() {
            infoOn = true;
            display();

            var t = 30;
            var answer = setInterval(function () {
                if (t === 0) {
                    $('#jepAnswer').html(message[0]);
                    clearInterval(answer);
                    setTimeout(function () {
                        $('#screenCover, #jepCategory, #jepValue, #jepQuestion, #jepAnswer').hide();
                        $('#jeopardyPopup').hide("scale", {}, 200);
                        infoOn = false;
                    }, 10000)
                } else {
                    $('#jepAnswer').html(t);
                }

                t--;
            }, 1000);
        }

         if (infoOn === true) {
                var int = setInterval(function(){
                    if (infoOn === false) {
                        clearInterval(int);
                        go()
                    }
                }, 5000)
            } else {
                go()
            }
    });
    sse.addEventListener('cheezburger', function (message) {
        console.log(message.data);
        $('#cheezReview').css({backgroundImage: 'url(' + message.data + ')'}).click(function(){
            go()
        });
        function go(){
            infoOn = true;
            $('#jeopardyPopup').show("scale",{}, 200);
            $('#imageLogo img').attr('src', '/static/images/logos/cheezburger.png');
            $('#cheezImg img').attr('src', message.data);
            $('#cheezImg, #imageLogo').delay(200).show(1);
            setTimeout(function(){
                $('#cheezImg, #imageLogo').hide();
                $('#jeopardyPopup').hide("scale",{}, 200);
                infoOn = false;
            }, 30000);
        }

        if(infoOn){
            var int = setInterval(function(){
                if (infoOn === false) {
                    clearInterval(int);
                    go()
                }
            }, 5000)
        } else {
            go()
        }
    });

    sse.addEventListener('flickr', function (message) {
        console.log(message.data);
        $('#flickrReview').css({backgroundImage: 'url(' + message.data + ')'}).click(function(){go()});
        function go(){
            infoOn = true;
            $('#jeopardyPopup').show("scale",{}, 200);
            $('#imageLogo img').attr('src', '/static/images/logos/flickr.png');

            $('#cheezImg img').attr('src', message.data);
            $('#cheezImg, #imageLogo').delay(200).show(1);
            setTimeout(function(){
                $('#cheezImg, #imageLogo').hide();
                $('#jeopardyPopup').hide("scale",{}, 200);
                infoOn = false;
            }, 30000);
        }

        if(infoOn){
            var int = setInterval(function(){
                if (infoOn === false) {
                    clearInterval(int);
                    go()
                }
            }, 5000)
        } else {
            go()
        }
    });
    sse.addEventListener('facts', function (message) {
        console.log(message.data);
        $('#factsReview').css({backgroundImage: 'url(' + message.data + ')'}).click(function(){go()});

        function go(){
            infoOn = true;
            $('#jeopardyPopup').show("scale",{}, 200);
            if((message.data).split('.')[1] === 'lolsotrue'){
                $('#imageLogo img').attr('src', '/static/images/logos/lol.png');
            } else {
                $('#imageLogo img').attr('src', '/static/images/logos/sotrue.png');
            }

            $('#cheezImg img').attr('src', message.data);
            $('#cheezImg, #imageLogo').delay(200).show(1);
            setTimeout(function(){
                $('#cheezImg, #imageLogo').hide();
                $('#jeopardyPopup').hide("scale",{}, 200);
                infoOn = false;
            }, 30000);
        }

        if(infoOn){
            var int = setInterval(function(){
                if (infoOn === false) {
                    clearInterval(int);
                    go()
                }
            }, 5000)
        } else {
            go()
        }
    });
});

