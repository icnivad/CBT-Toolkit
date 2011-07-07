$(document).ready(function(){
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

	$.post('/getMoods', function(data){
		$.jqplot('chartdiv',  [data],
		{ title:'Mood Chart',
			axes:{xaxis: {
					renderer:$.jqplot.DateAxisRenderer,
					tickOptions:{formatString: '%b %#d'},
					min: 'June 15, 2011',
					max: 'July 15, 2011',
					tickInterval: '5 day'
				}, 
				yaxis:{min:0, max:10}},
					highlighter: {
						show: true,
						sizeAdjust: 7.5
					},
			series:[{color:'#5FAB78'}]		  
		});
	}, 'json');

})