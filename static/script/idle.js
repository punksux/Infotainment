/**
* JQuery Idle.
* A dead simple jQuery plugin that executes a callback function if the user is idle.
* About: Author
* Henrique Boaventura (hboaventura@gmail.com).
* About: Version
* 1.1.2
**/
(function(a){a.fn.idle=function(c){var g={idle:60000,events:"mousemove keypress mousedown",onIdle:function(){},onActive:function(){},onHide:function(){},onShow:function(){},keepTracking:false};var d=false;var h=true;var e=a.extend({},g,c);var b=function(k,j){if(d){j.onActive.call();d=false}var i=(j.keepTracking?clearInterval:clearTimeout);i(k);return f(j)};var f=function(i){var k=(i.keepTracking?setInterval:setTimeout);var j=k(function(){d=true;i.onIdle.call()},i.idle);return j};return this.each(function(){var i=f(e);a(this).on(e.events,function(j){i=b(i,e)});if(c.onShow||c.onHide){a(document).on("visibilitychange webkitvisibilitychange mozvisibilitychange msvisibilitychange",function(){if(document.hidden||document.webkitHidden||document.mozHidden||document.msHidden){if(h){h=false;e.onHide.call()}}else{if(!h){h=true;e.onShow.call()}}})}})}})(jQuery);
