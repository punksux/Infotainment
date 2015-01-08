var cont;
var i = 0;
var colors = ['255,0,0', '0,255,0', '0,0,255', '255,255,0', '255,0,255', '0,255,255'];
var newNews;

function ticker(content) {
    cont = content;
//    setTickerWidth();
    $('#tickerOff').hide('slide', {direction: 'down', duration: 1000});
    $('#tickerOn').show('slide', {direction: 'down', duration: 1000});
    $.each(content, function(index, value){
        $('#tickerText').queue(function(next) {

                $(this).click(function () {
                    tickerStory(index);
                    $('#rss1sum, #screenCover, #popupContent').fadeIn(300);
                })
                .html(value[0]);
                if(value[4] != $('div#newsSource').html()){
                    var c=document.getElementById('myCanvas');
                    var ctx=c.getContext('2d');
                    ctx.font='20px Code';
                    var m=ctx.measureText(value[4]);
                    setTickerWidth(Math.ceil(m.width));
                    $('#newsSource').html(value[4]);
                }

                $('div#newsSource, #ticker').animate({backgroundColor: 'rgba(' + colors[parseInt(index/10)] + ',.5)'}, {duration: 1000, queue: false});
                next();
        })
            .fadeIn(1000)
            .delay(10000)
            .fadeOut(1000);
    });

    $('#tickerText').promise().done(function() {
        $('#tickerOn').hide('slide', {direction: 'down', duration: 1000});
        $('#tickerOff').show('slide', {direction: 'down', duration: 1000});
    });
}

function tickerStory(number) {
    $('div#rss1sum .movieName').html(cont[number][4]).css({backgroundColor: 'rgba('+ colors[parseInt(number/10)] +',.75)'});
    $('div#rss1sum .synopsis').html(cont[number][1]);
    if (cont[number][2] != '') {
        $('div#rss1sum .image').css({'background': 'url(' + cont[number][2] + ') no-repeat center'});
    }
    $('div#rss1sum .sendToPhone').attr('onclick', 'sendToPhone("' + cont[number][0] + '","' + cont[number][3] + '")').click(function () {
        $(this).animate({backgroundColor: '#30ba6f'}, {duration: 500}).html('Sent').css('pointer-events', 'none');
    });
}
