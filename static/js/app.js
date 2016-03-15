
$(function(){
	$('#mainform').on('submit',function(event){
		event.preventDefault();
		$.ajax({
            url: '/view',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                $('#curve_chart').append(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
	});
});
/*function drawChart(res) {
	// Create our data table out of JSON data loaded from server.
		var data = new google.visualization.DataTable(res);
  	// Instantiate and draw our chart, passing in some options.
        var options = {
          chart: {
          title: 'Google Ngram Viewer'
        },
        hAxis: {
            title: 'Year'
          },
          vAxis: {
            title: 'Frequency'
          },
        width: 1000,
        height: 450,
          axes: {
          x: {
            0: {side: 'top'}
          }
        }
        };
        //var chart = new google.charts.Line(document.getElementById('curve_chart'));
        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));
        chart.draw(data, options);
	}
  */