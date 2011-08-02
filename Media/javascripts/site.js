$(document).ready(function() {
	// Default text field values
	$(".text_field").focus(function(srcc)
  {
      if ($(this).val() == $(this)[0].title)
      {
          $(this).addClass("default_text_active");
          $(this).val("");
      }
  });
  $(".text_field").blur(function()
  {
      if ($(this).val() == "")
      {
          $(this).removeClass("default_text_active");
          $(this).val($(this)[0].title);
      }
  });
  $(".text_field").blur();
	
	// Button Hover
	if($.browser.msie && $.browser.version == "7.0") {
		$(".button").css("padding-top", "0px");
	} else {
		jQuery('.button').hover(
			function() { jQuery(this).stop().animate({opacity:0.8},400); },
			function() { jQuery(this).stop().animate({opacity:1},400); }
		);
	}
		
	// Add form submit capability to buttons
	$("a.submit").click(function() {
		$(this).closest('form').submit();
	});
	
	// Ajax contact form
	$('#send').click(function() {
       var name = $('input#name').val();
       var email = $('input#email').val();
			 var subject = $('select#subject').val();
       var message = $('textarea#message').val();
       $.ajax({
           type: 'post',
           url: 'scripts/send_email.php',
           data: 'name=' + name + '&email=' + email + '&topic=' + subject + '&message=' + message,

           success: function(results) {
							if(results == "error") {
								$('p.validation').html("Please fill in all fields").addClass("error");
							} else {
								$("form#contact_form").fadeOut("fast");
               $('p.validation').html(results);
							}
           }
       }); // end ajax
   });

});