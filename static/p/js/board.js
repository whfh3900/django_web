

demo = {

  initDashboardPageCharts: function() {



    gradientChartOptionsConfigurationWithTooltipPurple = {
      maintainAspectRatio: false,
      legend: {
        display: false
      },

      tooltips: {
        backgroundColor: '#f5f5f5',
        titleFontColor: '#333',
        bodyFontColor: '#666',
        bodySpacing: 4,
        xPadding: 12,
        mode: "nearest",
        intersect: 0,
        position: "nearest"
      },
      responsive: true,
      scales: {
        yAxes: [{
          barPercentage: 1.6,
          gridLines: {
            drawBorder: false,
            color: 'rgba(29,140,248,0.0)',
            zeroLineColor: "transparent",
          },
          ticks: {
            suggestedMin: 60,
            suggestedMax: 125,
            padding: 20,
            fontColor: "#9a9a9a"
          }
        }],

        xAxes: [{
          barPercentage: 1.6,
          gridLines: {
            drawBorder: false,
            color: 'rgba(225,78,202,0.1)',
            zeroLineColor: "transparent",
          },
          ticks: {
            padding: 20,
            fontColor: "#9a9a9a"
          }
        }]
      }
    };



    gradientBarChartConfiguration = {
      maintainAspectRatio: false,
      legend: {
        display: false
      },

      tooltips: {
        backgroundColor: '#f5f5f5',
        titleFontColor: '#333',
        bodyFontColor: '#666',
        bodySpacing: 4,
        xPadding: 12,
        mode: "nearest",
        intersect: 0,
        position: "nearest"
      },
      responsive: true,
      scales: {
        yAxes: [{

          gridLines: {
            drawBorder: false,
            color: 'rgba(29,140,248,0.1)',
            zeroLineColor: "transparent",
          },
          ticks: {
            suggestedMin: 60,
            suggestedMax: 120,
            padding: 20,
            fontColor: "#9e9e9e"
          }
        }],

        xAxes: [{

          gridLines: {
            drawBorder: false,
            color: 'rgba(29,140,248,0.1)',
            zeroLineColor: "transparent",
          },
          ticks: {
            padding: 20,
            fontColor: "#9e9e9e"
          }
        }]
      }
    };


    var chart_labels = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
    var chart_data = [542,480, 430, 550,530,453,380,434,568,610,700, 630];
    var chart_data2 = [368, 750,120,330,450,480,630,720,310,190,150,250];


    var line_ctx = document.getElementById("LineChart1").getContext('2d');

    var gradientStroke = line_ctx.createLinearGradient(0, 230, 0, 50);
    var gradientStroke1 = line_ctx.createLinearGradient(0, 230, 0, 50);

    gradientStroke.addColorStop(1, 'rgba(72,72,176,0.1)');
    gradientStroke.addColorStop(0.4, 'rgba(72,72,176,0)');
    gradientStroke.addColorStop(0, 'rgba(71,58,236,1)'); //red

    gradientStroke1.addColorStop(1, 'rgba(72,72,176,0.1)');
    gradientStroke1.addColorStop(0.4, 'rgba(72,72,176,0.0)');
    gradientStroke1.addColorStop(0, 'rgba(222,76,49,1)'); //purple colors
    var config = {
      type: 'line',
      data: {
        labels: chart_labels,
        datasets: [{
          //label: "My First dataset",
          fill: true,
          backgroundColor: gradientStroke1,
          borderColor: '#e3144f',
          borderWidth: 2,
          borderDash: [],
          borderDashOffset: 0.0,
          pointBackgroundColor: '#e3144f',
          pointBorderColor: 'rgba(255,255,255,0)',
          pointHoverBackgroundColor: '#e3144f',
          pointBorderWidth: 20,
          pointHoverRadius: 4,
          pointHoverBorderWidth: 15,
          pointRadius: 4,
          data: chart_data,
        },
        {
          //label: "My First dataset",
          fill: true,
          backgroundColor: gradientStroke,
          borderColor: '#3c37db',
          borderWidth: 2,
          borderDash: [],
          borderDashOffset: 0.0,
          pointBackgroundColor: '#3c37db',
          pointBorderColor: 'rgba(255,255,255,0)',
          pointHoverBackgroundColor: '#3c37db',
          pointBorderWidth: 20,
          pointHoverRadius: 4,
          pointHoverBorderWidth: 15,
          pointRadius: 4,
          data: chart_data2,
        }]
      },
      options: gradientChartOptionsConfigurationWithTooltipPurple
    };
    var LineChart1 = new Chart(line_ctx, config);
    $("#0").click(function() {
      var data = LineChart1.config.data;
      data.datasets[0].data = chart_data;
      data.labels = chart_labels;
      LineChart1.update();
    });
    $("#1").click(function() {
      var chart_data = [80, 120, 105, 110, 95, 105, 90, 100, 80, 95, 70, 120];
      var data = LineChart1.config.data;
      data.datasets[0].data = chart_data;
      data.labels = chart_labels;
      LineChart1.update();
    });

    $("#2").click(function() {
      var chart_data = [6000, 80, 65, 130, 80, 105, 90, 130, 70, 115, 60, 130];
      var data = LineChart1.config.data;
      data.datasets[0].data = chart_data;
      data.labels = chart_labels;
      LineChart1.update();
    });


    var thickness = {
        id: "thickness",
        beforeDraw: function (chart, options) {
            let thickness = chart.options.plugins.thickness.thickness;
            thickness.forEach((item,index) => {
            chart.getDatasetMeta(0).data[index]._view.innerRadius = item[0];
            chart.getDatasetMeta(0).data[index]._view.outerRadius = item[1];
            });
        }
    };

    $(document).ready(
        function () {
                var Round_ctx = document.getElementById("RoundChart1").getContext("2d");
                var RoundChart1 = new Chart(Round_ctx, {
      type: "doughnut",
      plugins: [thickness],
      //responsive: false,


      data: {
        labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
        datasets: [
          {
            //label: "# of Votes",
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
              "rgba(255, 99, 132, 0.2)",
              "rgba(54, 162, 235, 0.2)",
              "rgba(255, 206, 86, 0.2)",
              "rgba(75, 192, 192, 0.2)",
              "rgba(153, 102, 255, 0.2)",
              "rgba(255, 159, 64, 0.2)"
            ],
            borderColor: [
              "rgba(255, 99, 132, 1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(153, 102, 255, 1)",
              "rgba(255, 159, 64, 1)"
            ],
            borderWidth: 0.5,

          }
        ]
      },
      options: {
        legend:{display:false},
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          thickness: {
            thickness: [[50,200],[50,200],[50,200],[50,200],[50,200],[50,200]],
          }
        },
      }
    });
                document.getElementById("RoundChart1").onclick = function(evt){
                    var activePoints = RoundChart1.getElementsAtEvent(evt);
                    if (activePoints[0]){
                    var chartData = activePoints[0]['_chart'].config.data;
                    var idx = activePoints[0]['_index'];
                    var label = chartData.labels[idx];
//                    alert(label);
                    var chart_data = [6000, 80, 65, 130, 80, 105];
                    var data = RainbowChart1.config.data;
                    data.datasets[0].data = chart_data;
                    RainbowChart1.update();
                    }
                    }
            }
        );



    $(document).ready(
        function () {
                var Round_ctx = document.getElementById("RoundChart2").getContext("2d");
                var RoundChart2 = new Chart(Round_ctx, {
      type: "doughnut",
      plugins: [thickness],
      //responsive: false,


      data: {
        labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
        datasets: [
          {
            //label: "# of Votes",
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
              "rgba(255, 99, 132, 0.2)",
              "rgba(54, 162, 235, 0.2)",
              "rgba(255, 206, 86, 0.2)",
              "rgba(75, 192, 192, 0.2)",
              "rgba(153, 102, 255, 0.2)",
              "rgba(255, 159, 64, 0.2)"
            ],
            borderColor: [
              "rgba(255, 99, 132, 1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(153, 102, 255, 1)",
              "rgba(255, 159, 64, 1)"
            ],
            borderWidth: 0.5,

          }
        ]
      },
      options: {
        legend:{display:false},
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          thickness: {
            thickness: [[50,200],[50,200],[50,200],[50,200],[50,200],[50,200]],
          }
        },
      }
    });
                document.getElementById("RoundChart2").onclick = function(evt){
                    var activePoints = RoundChart2.getElementsAtEvent(evt);
                    if (activePoints[0]){
                    var chartData = activePoints[0]['_chart'].config.data;
                    var idx = activePoints[0]['_index'];
                    var label = chartData.labels[idx];
                    //alert(label);
                    var chart_data = [6000, 80, 65, 130, 80, 105];
                    var data = RainbowChart2.config.data;
                    data.datasets[0].data = chart_data;
                    RainbowChart2.update();
                    }
                    }
            }
        );



    var Rainbow_ctx = document.getElementById('RainbowChart1').getContext('2d');
    var RainbowChart1 = new Chart(Rainbow_ctx, {
        type: 'bar',
        data: {
            labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
            datasets: [{
                //label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: gradientBarChartConfiguration
    });




    var Rainbow_ctx = document.getElementById('RainbowChart2').getContext('2d');
    var RainbowChart2 = new Chart(Rainbow_ctx, {
        type: 'bar',
        data: {
            labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
            datasets: [{
                //label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: gradientBarChartConfiguration
    });

  },


};