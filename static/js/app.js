
$(function(){
	$('#mainform').on('submit',function(event){
		event.preventDefault();
        $('#button').addClass('m-progress');
    $('#curve_chart').html('');
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
                $('#curve_chart').html(error.responseText);
            }
        });
	});
});
var fixBinary = function fixBinary (bin) {
    var length = bin.length;
    var buf = new ArrayBuffer(length);
    var arr = new Uint8Array(buf);
    for (var i = 0; i < length; i++) {
      arr[i] = bin.charCodeAt(i);
    }
    return buf;
  }