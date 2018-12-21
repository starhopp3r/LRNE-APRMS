// Var cache the previous broadcast message
var old_broadcast_message = '';
// Var cache the logistics response
var old_logistics_message = 'P';

function google_map(gps_ts, lat, lon, res_id) {
	// Initialize marker and requested resource
	var map_marker = "";
	var req_res = "";
	// Center point of the map to be rendered
	var centerlatlng = new google.maps.LatLng(lat, lon);
	var myOptions = {
		zoom: 19,
		gestureHandling: 'cooperative',
		center: centerlatlng,
		mapTypeId: google.maps.MapTypeId.HYBRID,
		labels: true
	};
	// Create a new map with custom options
	var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
	// Create and drop a marker on the map
	var latlng = new google.maps.LatLng(lat, lon);
	// Choose marker and resource
	if (res_id == "11") 
	{
		// Default request i.e no request
		map_marker = "http://www.googlemapsmarkers.com/v1/00FFFF/";
		req_res = "None";
	}
	else if (res_id == "0")
	{
		// Request for ration
		map_marker = "http://www.googlemapsmarkers.com/v1/FFFF00/";
		req_res = "Ration";
	}
	else if (res_id == "1")
	{
		// Request for shelter
		map_marker = "http://www.googlemapsmarkers.com/v1/00FF00/";
		req_res = "Shelter";
	}
	else if (res_id == "2")
	{
		// Request for medical aid
		map_marker = "http://www.googlemapsmarkers.com/v1/FF0000/";
		req_res = "Medical Aid";
	}
	else
	{
		// Default request i.e no request
		map_marker = "http://www.googlemapsmarkers.com/v1/00FFFF/";
		req_res = "None";
	}
	var img = new google.maps.MarkerImage(map_marker);
	var marker = new google.maps.Marker({
	title: "Trans. Time: " + gps_ts + "\nCoordinates: " + lat + ", " + lon + "\nResource: " + req_res,
	icon: img,
	position: latlng
	});
	marker.setMap(map);
}

function updateLogisticsOverview(gps_ts, lat, lon, res_id) {
	// keep the card status constant
	var cardStatus = "";
	if (this.statusHeader != res_id || old_logistics_message == 'P') {
		cardStatus = "PENDING";
	} else if (old_logistics_message == 'I') {
		cardStatus = "IN PROCESS";
	} else if (old_logistics_message == 'C') {
		cardStatus = "COMPLETE";
	}
	// Change the text in the card
	if (res_id == '0')
	{
		// Ration
		$('#status-header').text("Ration");
		$('#card-trans-time').text(gps_ts);
		$('#card-coordinates').text(lat + ", " + lon);
		$('#card-status').text(cardStatus);
		this.statusHeader = "0";
	}
	else if (res_id == '1')
	{
		// Shelter
		$('#status-header').text("Shelter");
		$('#card-trans-time').text(gps_ts);
		$('#card-coordinates').text(lat + ", " + lon);
		$('#card-status').text(cardStatus);
		this.statusHeader = "1";
	}
	else if (res_id == '2')
	{
		// Medical Aid
		$('#status-header').text("Medical Aid");
		$('#card-trans-time').text(gps_ts);
		$('#card-coordinates').text(lat + ", " + lon);
		$('#card-status').text(cardStatus);
		this.statusHeader = "2";
	}
}

$(document).ready(function(e) {
	// Connect to server
	var socket = io.connect('http://' + document.domain + ':' + location.port);
	// Set UI on data_stream message 
	socket.on('data_stream', function(msg) {
		// Fade in the info tab upon receiving first signal
		$('#info-tab').fadeIn(1000);
		// The number of active handsets will always be one
		$('#handsets').text('1');
		if (msg.res == '0') 
		{
			$('#ration').text('1');
			$('#shelter').text('0');
			$('#aid').text('0');
			// Render map
			google_map(msg.gps_ts, msg.lat, msg.lon, msg.res);
			// Update logistics card
			updateLogisticsOverview(msg.gps_ts, msg.lat, msg.lon, msg.res);
			// Fade in the logistics card
			$('#logistics-card').fadeIn(500).css("display", "inline-block");
		} 
		else if (msg.res == '1') 
		{
			$('#ration').text('0');
			$('#shelter').text('1');
			$('#aid').text('0');
			// Render map
			google_map(msg.gps_ts, msg.lat, msg.lon, msg.res);
			// Update logistics card
			updateLogisticsOverview(msg.gps_ts, msg.lat, msg.lon, msg.res);
			// Fade in the logistics card
			$('#logistics-card').fadeIn(500).css("display", "inline-block");
		} 
		else if (msg.res == '2') 
		{
			$('#ration').text('0');
			$('#shelter').text('0');
			$('#aid').text('1');
			// Render map
			google_map(msg.gps_ts, msg.lat, msg.lon, msg.res);
			// Update logistics card
			updateLogisticsOverview(msg.gps_ts, msg.lat, msg.lon, msg.res);
			// Fade in the logistics card
			$('#logistics-card').fadeIn(500).css("display", "inline-block");
		}
		else
		{
			$('#ration').text('0');
			$('#shelter').text('0');
			$('#aid').text('0');
			// Render map
			google_map(msg.gps_ts, msg.lat, msg.lon, msg.res);
		}
	});

	// Broadcast message when the user hits enter key
	$(".dialog-text").on('keyup', function (e) {
	    if (e.keyCode == 13) {
	    	// Set var cache
	    	old_broadcast_message = $('.dialog-text').val();
	    	// Emit broadcast message
	        socket.emit('broadcast_msg', {
	        	msg: $('.dialog-text').val(),
	        	status: old_logistics_message
	        });
	        // Close the broadcast dialog box
	        $("#broadcast-dialog").fadeOut(200);
	        // Clear input value
	        $('.dialog-text').val('');
	    }
	});

	// Status dropdown listeners
	$('#status-inprocess').click(function() {
		// Set the var cache
		old_logistics_message = 'I';
		// In process
		$('#card-status').text("IN PROCESS");
		// Emit broadcast message
	    socket.emit('broadcast_msg', {
	    	msg: old_broadcast_message,
	    	status: 'I'
	    });
	});

	$('#status-complete').click(function() {
		// Set the var cache
		old_logistics_message = 'C';
		// Complete
		$('#card-status').text("COMPLETE");
		// Emit broadcast message
	    socket.emit('broadcast_msg', {
	    	msg: old_broadcast_message,
	    	status: 'C'
	    });
	});
});
