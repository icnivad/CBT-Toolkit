$(document).ready(function(){
	
	$('#id_thought').focus();

	$("#sortTable").tablesorter();
	
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
	
	$("a.submit").click(function(){
		$(this).closest('form').submit();
	});
	
	
	/*Really, really hackish!*/
	function refresh_thoughts(){
		var getURL=document.URL
		if(getURL.indexOf("?")!=-1){
			getURL=getURL+"&xhr"
		}
		else {
			getURL=getURL+"?xhr"
		}
		$.get(getURL, function(data){
			$('#thought_contents').html(data);
		});
	}
		
	$('a.launch_thought_modal').live('click', function(){
		$.get($(this).attr("href"), success=function(data){
			$('#thought_modal').html(data);
			$('#thought_modal').modal('show');
		});
		return false;
	});
	
	$(".modal_cancel").live('click', function(){
		$(this).closest('.modal').modal('hide');
		return false;
	});
	
	$(".modal_action").live('click', function(){
		$.post($(this).attr("href"), function(){
			refresh_thoughts();
		});
		$(this).closest('.modal').modal('hide');
		return false;
	});
	
	#hackish, but what are you going to do?
	if(!$.browser.msie){
		$('.distortions input[name="distortions"]').iphoneStyle({checkedLabel:'Yes', uncheckedLabel: 'No'});
	}
});