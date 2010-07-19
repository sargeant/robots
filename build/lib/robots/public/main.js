function get_next_message() {
	$.ajax({url: '/queue/get', dataType: 'json', 
		success: function(message) {
			$('h1').html(message.content);
		},
		error: reset_message()
	});
}

function reset_message() {
	var default_message = 'Placeholder';
	if ($('h1').html() != default_message) {
		$('h1').html(default_message);	
	}
}

$(document).ready(function () {
	jQuery.whileAsync({
		delay: 15000,
		bulk: 0,
		loop: get_next_message
	})
});