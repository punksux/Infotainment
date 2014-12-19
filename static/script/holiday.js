function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}


//    --== Christmas ==--
function christmas() {
    $('head').append($('<link rel="stylesheet" type="text/css" id="holidayStyle" />').attr('href', '/static/holiday/christmas.css'));
    $('#holiday').html('<div id="bulbs"></div>');
    var width = $('div#bulbs').width();
    var colors = ['red', 'blue', 'yellow', 'green', 'purple', 'orange'];

    var j = 0;
    var op = 0;
    var odist = 0;
    for (var p = getRandomInt(1, 15); p < width; p += getRandomInt(60, 90)) {
        var dist = getRandomInt(0, 4);
        $('#bulbs').append('<div class="cord" style="left:' + (op) + 'px;top:' + (dist) + 'px;width:' + ((p - op)+11) + 'px;-webkit-transform:rotate(' + (dist-odist) + 'deg);-webkit-transform-origin:100%;"></div>' +
                '<div class="bulbHolder" style="left:' + p + 'px;-moz-transform:rotate(' + getRandomInt(-15, 15) + 'deg);-webkit-transform:rotate(' + getRandomInt(-15, 15) + 'deg);top:' + dist + 'px"><div class="bases"></div><div class="bulb ' + colors[j] + '"></div></div>');
        j++;
        if (j > 5) {
            j = 0
        }
        op = p+11;
        odist = dist;
    }
    $('div#holiday div#bulbs').append('<div class="cord" style="left:' + (op+5) + 'px;width:' + ((p - op)+5) + 'px;-webkit-transform:rotate(' + -dist + 'deg);top:' + (dist/2) + 'px"></div>')
}

function turnOnLights() {
    $('.bulb').addClass('lights_on');
    var rand = getRandomInt(0,16);
    $('#bulbs .bulbHolder div:nth-child(rand)').removeClass('lights_on');
    $('#onOffButton').html('<div id="manualOff" class="button"><span>Turn lights off</span></div>');
    $('#manualOff').on('click', function () {
        manualLights('off');
    });
}

function turnOffLights() {
    $('#onOffButton').html('<div id="manualOn" class="button"><span>Turn lights on</span></div>');
    $('.bulb').removeClass('lights_on');
    $('#manualOn').on('click', function () {
        manualLights('on');
    });
}

//    --== Thanksgiving ==--
function hats() {
    $('head').append($('<link rel="stylesheet" type="text/css" id="holidayStyle" />').attr('href', '/static/holiday/thanksgiving.css'));
    $('#holiday').html('<div id="hats"></div>');
    var width = $('div#hats').width();

    for (var p = getRandomInt(1, 15); p < width; p += getRandomInt(60, 90)) {
        var dist = getRandomInt(0, 14);
        $('#hats').append('<div class="turk" style="left:' + p + 'px;-moz-transform:rotate(' + getRandomInt(-15, 15) + 'deg);-webkit-transform:rotate(' + getRandomInt(-15, 15) + 'deg);top:-' + dist + 'px"></div>');
    }
}

//    --== New Years ==--
function newYears(){
    $('head').append($('<link rel="stylesheet" type="text/css" id="holidayStyle" />').attr('href', '/static/holiday/newYears.css'));
    var date = new Date();
    $('#holiday').html('<img src="/static/holiday/images/fireworks.png" /><div id="newYear">' + (date.getFullYear() + 1) + '</div>')
}

//    --== Day or Night Switch ==--
function dayNight(dN){
    if (dN === 'day'){
        switch (holiday2){
            case "christmas":
               turnOffLights();
                break
        }
    } else if (dN === 'night') {
        switch (holiday2) {
            case "christmas":
                turnOnLights();
                break
        }
    }
}


//    --== Clean Up ==--
function cleanup(){
    $('#holiday').html('');
    $('#holidayStyle').remove()
}