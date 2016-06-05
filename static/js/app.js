
$(function(){
	$('#mainform').on('submit',function(event){
		event.preventDefault();
        $('#button').addClass('m-progress');
    $('#curve_chart').html('');
    $('#download').css('visibility','hidden');
    console.log("Button Clicked");
		$.ajax({
            url: '/view',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                $('#button').removeClass('m-progress');
                mpld3.draw_figure('curve_chart',response);
                $('#download').css('visibility','visible')
            },
            dataType: "json",
            error: function(error) {
                //console.log(error);
                $('#button').removeClass('m-progress');
                //$('#curve_chart').html(error.responseText);
                $('#curve_chart').html("<div class='error'><h2>Sorry!</h2><p>Till now no data for your search term or to low data points to generate the curve.<br>Stay tuned we are still in development more and more data are added on regular basis.</p><h3>Thank you for visiting us.</h3></div>");
                
            }
        });
	});
});
