function timeStamp() {
    var now = new Date();
    var date = [ now.getMonth() + 1, now.getDate(), now.getFullYear() ];
    var time = [ now.getHours(), now.getMinutes(), now.getSeconds() ];
    var suffix = ( time[0] < 12 ) ? "AM" : "PM";
    time[0] = ( time[0] < 12 ) ? time[0] : time[0] - 12;
    time[0] = time[0] || 12;
    for ( var i = 1; i < 3; i++ ) {
        if ( time[i] < 10 ) {
            time[i] = "0" + time[i];
        }
    }
    return date.join("/") + " " + time.join(":") + " " + suffix;
}

var holiday2;
function holiday(holiday){
    cleanup();
    if (holiday === 'christmas'){
        christmas();
    } else if (holiday === 'thanksgiving') {
        hats();
    } else if (holiday === 'new year\'s day') {
        newYears();
    }
}

function changeTab(tis){
    var list = ['view1', 'view2','view3','view4','view5','view6'];
    for (var i = 0; i < list.length; i++){
        if (tis === list[i]){
            $('div#' + list[i]).fadeIn(300);
            $('ul#tabList li:nth-child(' + (i+1) + ')').addClass('selected');

        } else {
            $('div#' + list[i]).hide();
            $('ul#tabList li:nth-child(' + (i+1) + ')').removeClass('selected');
        }
    }
}

var dateSet = false;

function startTime() {
    var today=new Date();
    var am_pm = 'AM';
    var h=today.getHours();
    var m=today.getMinutes();
    if (h===12){
        am_pm = 'PM';
        if (dateSet === false){
            setDate();
            dateSet = true;
        }
    }
    if (h === 13){dateSet = false}
    if (h>12){h-=12; am_pm = 'PM';}
    if (h === 1){dateSet = false}
    if (h === 0){
        h = 12;
        if (dateSet === false){
            setDate();
            dateSet = true;
        }
    }
    m = checkTime(m);
    $('#time').html(h+":"+m+" "+am_pm);
    setTimeout(startTime, 3000);
}

function checkTime(i) {
    if (i<10) {i = "0" + i}
    return i;
}

var dateWidth = 0;

function setDate(){
    var date = new Date();
    var months = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May.', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.'];
    $('#dateText').html(months[date.getMonth()] + ' ' + date.getDate() + ' ' + date.getFullYear());
    dateWidth = $('#date').width();
    setTickerWidth(150);
    setTickerOffWidth();
    if (hday != ''){
        countdownTimer(hday);
        if (parseInt(($('#tickerOff').html()).split(' ')[0]) === 0){
            hday = '';
            $('#tickerOff').html('');
            cleanup()
        }
    }
}

var close;
var tomOn = true;
var panelOut = false;

function weatherSlider(){
    if (panelOut) {
        clearTimeout(close);
    }
    if ($('div#homeMusicDisplay').is(':visible')) {
        $('#homeMusicDisplay').hide('slide', {direction: 'right'});
    } else if ($('#musicPlaying').is(':visible')) {
        $('#homeMusicDisplay').show('slide', {direction: 'right'});
    }
    if ($('#tom').is(':visible')){
        if (tomOn){
            $('#tom').fadeTo(500, .25);
            tomOn = false;
        } else {
            $('#tom').fadeTo(500, 1);
            tomOn = true;
        }
    }
    if ($('#alert').html() != ''){
        $('#alert').fadeToggle(500);
    }
    $('#weatherSlider').toggle('slide', {direction: 'right'});
    panelOut = !panelOut;
    if(panelOut){
        close = setTimeout(weatherSlider, 30000);
    }
}

function setTickerWidth (wdth) {
    $('div#tickerOn').css({width: (1280 - (dateWidth + 220) - 15) + 'px'}, 500);
    $('div#newsSource').animate({width: (wdth) + 'px'}, 1000);
    $('div#ticker').animate({width: ($('div#tickerOn').width() - wdth) - 5 - 10 - 10 + 'px'}, 1000);
}

function setTickerOffWidth () {
    $('div#tickerOff').css({width: (1280 - (dateWidth + 220) - 15) + 'px'}, 500);
}

var hday = '';

function countdownTimer(data){
    var date = data[0].split("-");
    var day = countdown(new Date(date[0], date[1]-1, date[2]), null ,countdown.DAYS | countdown.HOURS, 1);
    $('#tickerOff').html(day.toString() + ' Until ' + data[1]);
}