var cont;
var i = 0;
var colors = ['255,0,0', '0,255,0', '0,0,255', '255,255,0', '255,0,255', '0,255,255'];
var newNews;

function ticker(content) {
    cont = content;
    $('#tickerOff').hide('slide', {direction: 'down'});
    setTickerWidth();
    $('#newsSource, #ticker').show('slide', {direction: 'down'});
    $.each(content, function(index, value){
        $('#tickerText').queue(function(next) {
                $(this).click(function () {
                    tickerStory(index);
                    $('#rss1sum, #screenCover, #popupContent').fadeIn(300);
                })
                .html(value[0]);
                if(value[4] != $('div#newsSource').html()){
                    $('#newsSource').html(value[4]);
                    setTickerWidth();
                }
                $('div#newsSource, #ticker').animate({backgroundColor: 'rgba(' + colors[parseInt(index/10)] + ',.5)'}, {duration: 1000, queue: false});
                next();
        })
            .fadeIn(1000)
            .delay(10000)
            .fadeOut(1000);
    });

    $('#tickerText').promise().done(function() {
        $('#newsSource, #ticker').hide('slide', {direction: 'down'});
        setTickerOffWidth();
        $('#tickerOff').show('slide', {direction: 'down'});
    });
}

function tickerStory(number) {
    $('div#rss1sum .movieName').html(cont[number][4]);
    $('div#rss1sum .synopsis').html(cont[number][1]);
    $('div#rss1sum .image').css({'background': 'url(' + cont[number][2] + ') no-repeat center'});
    $('div#rss1sum .sendToPhone').attr('onclick', 'sendToPhone("' + cont[number][0] + '","' + cont[number][3] + '")').click(function () {
        $(this).animate({backgroundColor: '#30ba6f'}, {duration: 500}).html('Sent').css('pointer-events', 'none');
    });
}
