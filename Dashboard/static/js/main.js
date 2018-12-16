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
		// Fade in top header
		$('#top-header').fadeIn(500);
    }, 3000);

    // Listen for broadcast button clicks
    // and show the broadcast dialog box
    $('#broadcast-btn').click(function(e) {
    	$('#broadcast-dialog').fadeIn(200);
    	e.stopPropagation();
    });

    $("#broadcast-dialog").click(function(e){
    	e.stopPropagation();
	});

	// Close the dialog box when mouse click
	// is elsewhere in the document
	$(document).click(function(){
	    $("#broadcast-dialog").fadeOut(200);
	});
});