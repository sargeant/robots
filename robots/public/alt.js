function get_next_message() {
	var animate_in = {'opacity': 1}
	var animate_out = {'opacity': 0}
	
	$.ajax({url: '/queue/get', dataType: 'json', 
		success: function(message) {
			var div = $('#' + message.keyword);
			div.html(message.content);
			div.animate(animate_in, {duration: 4000});
			div.delay(5000);
			div.animate(animate_out, 2000);
		},
		error: function() {
			
		}
	});
}

$(document).ready(function () {
	jQuery.whileAsync({
		delay: 15000,
		bulk: 0,
		loop: get_next_message
	})
});