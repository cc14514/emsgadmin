// JavaScript Document

	
	var clientFactor = function(){ return Math.round(Math.random()*100)};
		var clientLineChartData = {
			labels : ["一","二","三","四","五","六","七"],
			datasets : [
				{
					label: "客户数量",
					fillColor : "rgba(145,199,62,0.2)",
					strokeColor : "#91c73e",
					pointColor : "#669900",
					pointStrokeColor : "#fff",
					pointHighlightFill : "#fff",
					pointHighlightStroke : "rgba(220,220,220,1)",
					data : [clientFactor(),clientFactor(),clientFactor(),clientFactor(),clientFactor(),clientFactor(),clientFactor()]
				}
			]

		}
		
		
		var lawyerFactor = function(){ return Math.round(Math.random()*100)};
		var lawyerLineChartData = {
			labels : ["一","二","三","四","五","六","七"],
			datasets : [
				{
					label: "律师数量",
					fillColor : "rgba(145,199,62,0.2)",
					strokeColor : "#91c73e",
					pointColor : "#669900",
					pointStrokeColor : "#fff",
					pointHighlightFill : "#fff",
					pointHighlightStroke : "rgba(220,220,220,1)",
					data : [10,30,20,50,40,70,60]
				}
				
			]

		}

			
	
		//客户来源
		var clientPieData = [
				{
					value: 300,
					color:"#F7464A",
					highlight: "#FF5A5E",
					label: "北京"
				},
				{
					value: 50,
					color: "#46BFBD",
					highlight: "#5AD3D1",
					label: "上海"
				},
				{
					value: 100,
					color: "#FDB45C",
					highlight: "#FFC870",
					label: "成都"
				},
				{
					value: 40,
					color: "#949FB1",
					highlight: "#A8B3C5",
					label: "杭州"
				},
				{
					value: 120,
					color: "#4D5360",
					highlight: "#616774",
					label: "四川"
				}

			];
			
			//律师来源
			var lawyerPieData = [
				{
					value: 100,
					color:"#F7464A",
					highlight: "#FF5A5E",
					label: "北京"
				},
				{
					value: 50,
					color: "#46BFBD",
					highlight: "#5AD3D1",
					label: "上海"
				},
				{
					value: 100,
					color: "#FDB45C",
					highlight: "#FFC870",
					label: "成都"
				},
				{
					value: 40,
					color: "#949FB1",
					highlight: "#A8B3C5",
					label: "杭州"
				},
				{
					value: 120,
					color: "#4D5360",
					highlight: "#616774",
					label: "四川"
				}

			];
			
			window.onload = function(){
				//客户数量
				var ctx = document.getElementById("client").getContext("2d");
				window.clientLine = new Chart(ctx).Line(clientLineChartData, {
					responsive: true
				});				
				//律师数量
				var ctx = document.getElementById("lawyer").getContext("2d");
				window.lawyerLine = new Chart(ctx).Line(lawyerLineChartData, {
					responsive: true
				});	
				
				//客户来源
				var ctx = document.getElementById("client-area").getContext("2d");
				window.clientPie = new Chart(ctx).Pie(clientPieData);
							
				//律师来源
				var ctx = document.getElementById("lawyer-area").getContext("2d");
				window.lawyerPie = new Chart(ctx).Pie(lawyerPieData);
			}