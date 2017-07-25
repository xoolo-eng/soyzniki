$(document).ready(function(){
	close_message();
});

function close_message(){
	var messages = document.getElementsByClassName('messages');
	if (messages.length > 0){
		setTimeout(function(){
			$('ul.messages').slideUp(400);
		}, 4000);
		setTimeout(function(){
			messages[0].remove();
		}, 4450);
		
	}
}