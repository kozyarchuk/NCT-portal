$(function	()	{

  	//Flot Chart (Total Sales)
	var d1 = [];
	for (var i = 0; i <= 10; i += 1) {
		//d1.push([i, parseInt(Math.random() * 30)]);
		d1 = [[-5,-2.2],[-4,-15.2],[-3,-23.0],[-2,-16.2],[-1,-8.4],[0,0],[1,7.3],[2,16.6],[3,31],[4,43],[5,48]];
	}

	function plotWithOptions() {
		$.plot("#placeholder", [d1], {
			series: {
				lines: {
					show: true,
					fill: true,
					fillColor: '#eee',
					steps: false,
					
				},
				points: { 
					show: true, 
					fill: false 
				}
			},

			grid: {
				color: '#fff',
				hoverable: true,
    			autoHighlight: true,
			},
			colors: [ '#bbb'],
		});
	}

	$("<div id='tooltip'></div>").css({
		position: "absolute",
		display: "none",
		border: "1px solid #222",
		padding: "4px",
		color: "#fff",
		"border-radius": "4px",
		"background-color": "rgb(0,0,0)",
		opacity: 0.90
	}).appendTo("body");

	$("#placeholder").bind("plothover", function (event, pos, item) {

		var str = "(" + pos.x.toFixed(2) + ", " + pos.y.toFixed(2) + ")";
		$("#hoverdata").text(str);
	
		if (item) {
			var x = item.datapoint[0],
				y = item.datapoint[1];
			
				$("#tooltip").html("Total Sales : " + y)
				.css({top: item.pageY+5, left: item.pageX+5})
				.fadeIn(200);
		} else {
			$("#tooltip").hide();
		}
	});

	plotWithOptions();

	//Morris Chart (Total Visits)
	var totalVisitChart = Morris.Bar({
	  element: 'totalSalesChart',
	  data: [
	    { y: '1 week', a: -1034500, b: 453000, c: 13500 },
	    { y: '2 weeks', a: 706700,  b: 350000, c: 0 },
        { y: '3 weeks', a: -989000,  b: -69000, c: 33000 },
	    { y: '1 month', a: 1450000,  b: 680000, c: 36000 },
	    { y: '2 month', a: 860000,  b: 350000, c: 120000 },
	    { y: '3 month', a: 650000,  b: 250000, c: 64000 },

	  ],
	  xkey: 'y',
	  ykeys: ['a', 'b','c'],
	  labels: ['USD', 'EUR', 'Other(USD Equivalent)'],
	  barColors: ['#999', '#eee', '#bbb'],
	  grid: false,
	  gridTextColor: '#666',
	});
	

	//Datepicker
	$('#calendar').DatePicker({
		flat: true,
		date: '2014-06-07',
		current: '2014-06-07',
		calendars: 1,
		starts: 1
	});

	//Skycon
	var icons = new Skycons({"color": "white"});
    icons.set("skycon1", "sleet");
    icons.set("skycon2", "partly-cloudy-day");
    icons.set("skycon3", "wind");
    icons.set("skycon4", "clear-day");
    icons.play();

	//Scrollable Chat Widget
	$('#chatScroll').slimScroll({
		height:'230px'
	});

	//Chat notification
	setTimeout(function() {
		$('.chat-notification').find('.badge').addClass('active');
		$('.chat-alert').addClass('active');
	}, 3000);

	setTimeout(function() {
		$('.chat-alert').removeClass('active');
	}, 8000);
	
	$(window).resize(function(e)	{
		// Redraw All Chart
		setTimeout(function() {
			totalVisitChart.redraw();
			plotWithOptions();
		},500);
	});

	$('#sidebarToggleLG').click(function()	{
		// Redraw All Chart
		setTimeout(function() {
			totalVisitChart.redraw();
			plotWithOptions();
		},500);
	});

	$('#sidebarToggleSM').click(function()	{
		// Redraw All Chart
		setTimeout(function() {
			totalVisitChart.redraw();
			plotWithOptions();
		},500);
	});
});
