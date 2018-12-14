$(document).ready(function(e) {
	var socket = io.connect('http://' + document.domain + ':' + location.port);
	socket.on('data_stream', function(msg) {
		$('#handsets').text('1');
		if (msg.data == '0') 
		{
			$('#ration').text('1');
			$('#shelter').text('0');
			$('#aid').text('0');
			$('#iframe-content').attr('src', window.location.href + 'static/map.html');
		} 
		else if (msg.data == '1') 
		{
			$('#ration').text('0');
			$('#shelter').text('1');
			$('#aid').text('0');
			$('#iframe-content').attr('src', window.location.href + 'static/map.html');
		} 
		else if (msg.data == '2') 
		{
			$('#ration').text('0');
			$('#shelter').text('0');
			$('#aid').text('1');
			$('#iframe-content').attr('src', window.location.href + 'static/map.html');
		}
	});
});