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
		var thought=$(this).closest('.thought_box').find('div.thought').html()
		result=confirm("Are you sure you want to delete your thought: "+thought)
		if(result){
			$.get($(this).attr("href"));
			$.get('/thought/list/', function(data){
				$('div.thoughts').html(data);
			});
		}
		return false;
	});
	
	// onShow : show+make the window translucent
	var myOpen=function(hash){ hash.w.css('opacity',0.88).show(); };
	$('#dialog').jqm({onShow:myOpen}); 

	$('.detail_field').jqm({overlay:0});
	$('.detail_icon img').live('mouseenter', function(){
		var el=$(this).closest('.detail').find('.detail_field');
		el.jqmShow({});
		el.position({'at':'bottom', 'my':'top', 'of':$(this), 'offset':"10 10"});
	});
		
	$('.detail').live('mouseleave', function(){
		$('.detail_field').jqmHide();
	});
	
	$('#jqm_popup_msg').jqm({overlay:20, ajax:"@href", trigger:"a.challenge", modal:true});
	$('.cancel').live('click', function(){
		$('#jqm_popup_msg').jqmHide();
	});
		
	$('tr.thought_box').live('mouseenter', function(){
		$(this).find("div.thought_challenge").show();
	});
	$('tr.thought_box').live('mouseleave', function(){
		$(this).find("div.thought_challenge").hide();
	});
	
//	$('a.challenge').live('click', function(){
//		var el=$('#jqm_popup_msg');
//		el.jqmShow({});
//		el.position({'at':'top', 'my':'top', 'of':$(this).closest(".thought_box"), 'offset':"0 -50"});
//		return false;
//	});
});
