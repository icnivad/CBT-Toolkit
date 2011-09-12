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
	
	//basic crud for thoughts
	$('a.thought_delete').live('click', function(e){
		var href=$(this).attr("href");
		$.post(href, "delete", function(data){
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
	

	$('#jqm_popup_msg').jqm({overlay:20, ajax:"@href", modal:true, trigger:'a.jqm_trigger'});
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
			success: callback
		});
	}

	$("a.submit").click(function() {
		$(this).closest('form').submit();
	});	

	$("a.ajax_submit", "#challenge_thought_form").live('click', function(){
		ajax_submit($(this).closest("form"), refresh_thoughts);
		$('#jqm_popup_msg').jqmHide();
	});
	
	$("a.ajax_submit", "#edit_thought_form").live('click', function(){
		ajax_submit($(this).closest("form"), refresh_thoughts);
		$('#jqm_popup_msg').jqmHide();
	});
	
	function add_thought(data){
		$("#header_message").html(data);
		refresh_thoughts();
	}
	
	$('a.ajax_submit', '#add_thought_form').live('click', function(){
		ajax_submit($(this).closest("form"), add_thought);
		$(':input','#add_thought_form')
		.not(':button, :submit, :reset, :hidden')
		.val('')
		.removeAttr('checked')
		.removeAttr('selected');
	});
	
	
	function show_tab(el){
		var id=el.attr("id").split("_").pop();
		$("#distortion_tab_content_"+id).show();
	}
	
	function hide_tabs(){
		$("[id^='distortion_tab_content']").hide();
	}
	hide_tabs();
	show_tab($(".active a"));
	$(".tabs a").live("click", function(){
		hide_tabs();
		show_tab($(this));
		$(".tabs .active").removeClass("active");
		$(this).closest("li").addClass("active");
		$(this).blur();
		return false;
	});
	
});