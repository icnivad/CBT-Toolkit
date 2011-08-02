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
	$('a.thought_delete').live('click', function(){
		$.post($(this).attr("href"), {}, function(data){
			$("#jqm_popup_msg").jqmHide();
			refresh_thoughts();
		});
		return false;
	});
	
	// onShow : show+make the window translucent
	$(".details").hide();
	$(".detail_trigger").live("click", function(){
		$(".details").toggle();
		var msg=$(this).children("a")
		if($(".details").is(":visible")){
			msg.html("Click to Hide Optional Details");
		}
		else {
			msg.html("Click to Show Optional Details");
		}
	});
	
	
	// CSS3 rounded corners / shadows
	function fix_form_css(){
		$("div#header li.active a").css({ '-moz-border-radius': '6px', '-webkit-border-radius': '6px', 'border-radius': '6px' });
		$("div.sidebar_box").css({ '-moz-border-radius': '8px', '-webkit-border-radius': '8px', 'border-radius': '8px' });
		$("div#price_table table").css({ '-moz-border-radius': '8px', '-webkit-border-radius': '8px', 'border-radius': '8px' });
		$("span.highlight_dark, span.highlight_light").css({ '-moz-border-radius': '2px', '-webkit-border-radius': '2px', 'border-radius': '2px' });
		$("div#about .team ul li a").css({ '-moz-border-radius': '8px', '-webkit-border-radius': '8px', 'border-radius': '8px' });
		$("form .text_field").css({ '-moz-border-radius': '8px', '-webkit-border-radius': '8px', 'border-radius': '8px' });
		$("a.button span").css({ 'text-shadow': '#000 0px -0px 2px' });
		$("div#page .section_title h3").css({ 'text-shadow': '#3e2828 0px 0px 2px' });
	}
	fix_form_css();
	
	$('#jqm_popup_msg').jqm({overlay:20, ajax:"@href", modal:true, trigger:'a.jqm_trigger', onLoad:fix_form_css});
	$('.cancel').live('click', function(){
		$('#jqm_popup_msg').jqmHide();
	});
	
	$("div.thought_challenge").show();
//	$('tr.thought_box').live('mouseenter', function(){
//		$(this).find("div.thought_challenge").show();
//	});
//	$('tr.thought_box').live('mouseleave', function(){
//		$(this).find("div.thought_challenge").hide();
//	});
	
	function refresh_thoughts(){
		$.get('/thought/list/', function(data){
			$('div.thoughts').html(data);
			$('#jqm_popup_msg').jqm({overlay:20, ajax:"@href", modal:true, trigger:'a.jqm_trigger'});
			$("div.thought_challenge").show();
		});
	}
	
	function ajax_submit(form, callback){
		$.ajax({
			type:'POST',
			url:form.attr("action"),
			data:form.serialize(),
			success: callback,
		});
	}
	
	$("a.submit", "#challenge_thought_form").live('click', function(){
		ajax_submit($(this).closest("form"), refresh_thoughts);
		$('#jqm_popup_msg').jqmHide();
	});
	
	$("a.submit", "#edit_thought_form").live('click', function(){
		ajax_submit($(this).closest("form"), refresh_thoughts);
		$('#jqm_popup_msg').jqmHide();
	});
	
	$('a.submit', '#add_thought_form').live('click', function(){
		ajax_submit($(this).closest("form"), refresh_thoughts);
		$(':input','#add_thought_form')
		.not(':button, :submit, :reset, :hidden')
		.val('')
		.removeAttr('checked')
		.removeAttr('selected');

		$('#id_thought').focus();
	});

});
