
function get_next_message() {
	$.ajax({url: '/queue/get', success: new_orders});
}

function new_orders(message) {
	var animate_in = {'opacity': 1}
	var animate_out = {'opacity': 0}
	
	var div = $('#' + message.keyword);
	div.html(message.content);
	div.animate(animate_in, {duration: 5000});
	div.delay(5000);
	div.animate(animate_out, 7000);
}

function update_queue(size) {
	$('#message_queue').html(size.messages);
}

function get_qsize() {
	$.ajax({url: '/queue/size', success: update_queue});
}

function update() {
	get_next_message();
	get_qsize();
}

$(document).ready(function () {
	jQuery.whileAsync({
		delay: 15000,
		bulk: 0,
		loop: update
	})
});