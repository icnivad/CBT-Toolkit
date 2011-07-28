$(document).ready(function(){
	
	$('#id_thought').focus();
	
	//allow ajax to work with django
	$('html').ajaxSend(function(event, xhr, settings) {
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
	if(!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
		// Only send the token to relative URLs i.e. locally.
		xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
		}
	});
	
	//basic crud for thoughts
	$('a.check_delete').live('click', function(){
		var thought=$(this).closest('.thought_box').find('span.thought').html()
		result=confirm("Are you sure you want to delete your thought: "+thought)
		if(result){
			$.get($(this).attr("href"));
			$.get('/thought/list/', function(data){
				$('div.thoughts').html(data);
			});
		}
		return false;
	});
	
	$('.detail > div').live('hover', function(){
		$(this).closest('.detail').find('.hidden').toggle();
        $(this).closest('.detail').find('[id^="id_"]').focus();
	});
});
