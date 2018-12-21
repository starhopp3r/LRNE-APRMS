var serveLoc = 'http://' + document.domain + ':' + location.port;

// Scroll to top on page refresh
window.onbeforeunload = function () {
  window.scrollTo(0, 0);
}

/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function mapOptions() {
  document.getElementById("myDropdown").classList.toggle("show");
}

/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function statusOptions() {
  document.getElementById("statusDropList").classList.toggle("look");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    for (var i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

window.onclick = function(event) {
  if (!event.target.matches('.status-dropbtn')) {
    var dropdowns = document.getElementsByClassName("status-dropdown-content");
    for (var i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('look')) {
        openDropdown.classList.remove('look');
      }
    }
  }
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

	// Dropdown listner
	$('#satImg').click(function() {
		// Show satellite imagery
		slider.rightImage.children[0].src = serveLoc + "/static/img/2014.jpg"
		juxtapose.scanPage()
	});

	$('#cvAnalysis').click(function() {
		// Show computer vision analysis
		slider.rightImage.children[0].src = serveLoc + "/static/img/diff.jpg"
		juxtapose.scanPage()
	});
});