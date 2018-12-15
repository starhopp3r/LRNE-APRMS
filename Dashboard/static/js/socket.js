function google_map(gps_ts, lat, lon, res_id) {
	// Initialize marker and requested resource
	var map_marker = "";
	var req_res = "";
	// Center point of the map to be rendered
	var centerlatlng = new google.maps.LatLng(lat, lon);
	var myOptions = {
		zoom: 15,
		center: centerlatlng,
		mapTypeId: google.maps.MapTypeId.ROADMAP
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

$(document).ready(function(e) {
	var socket = io.connect('http://' + document.domain + ':' + location.port);
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
		} 
		else if (msg.res == '1') 
		{
			$('#ration').text('0');
			$('#shelter').text('1');
			$('#aid').text('0');
			// Render map
			google_map(msg.gps_ts, msg.lat, msg.lon, msg.res);
		} 
		else if (msg.res == '2') 
		{
			$('#ration').text('0');
			$('#shelter').text('0');
			$('#aid').text('1');
			// Render map
			google_map(msg.gps_ts, msg.lat, msg.lon, msg.res);
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
});