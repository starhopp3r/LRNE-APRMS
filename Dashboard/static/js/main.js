// Scroll to top on page refresh
window.onbeforeunload = function () {
  window.scrollTo(0, 0);
}

$(document).ready(function(e) {
	// Fade out splashscreen 3 seconds after page load
	// and load the map with GPS locations marked  
	setTimeout(function() {
		// Fade out splashscreen
		$('#splashscreen').fadeOut(500);
		// Add map source attribute to iframe
		$('#iframe-content').attr('src', window.location.href + 'static/map.html');
		// Fade in information tab
		$('#info-tab').fadeIn(500);
    }, 3000);
});