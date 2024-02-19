// contient les articles de presse, qui doivent être 
// gardés en mémoire même après affichage du graphique
let news_data;

// Palette de couleurs utilisée par tous les graphiques
let colors = ["#1D507A", "#2F6999", "#66A0D1", "#8FC0E9", "#4682B4"];

// Chargement des articles de presse
$.ajax({
          url: "/api/news",
          success: display_news
});

// Chargement des données météo
d3.json('/api/meteo', display_nvd3_graph);

// Chargement des données finance
d3.json('/api/finance', display_nvd3_graph_finance);

function display_news(result) {
    console.log(1)
	console.log(typeof(result))
	console.log((result))
    news_data = result["data"];
    console.log(2)
    console.log(typeof(news_data))
    console.log((news_data))
    display_wordcloud(news_data);
    display_all_articles();
}

function display_wordcloud(news_data) {

    let data = [];

    let keywords = news_data["keywords"];

    for (i in keywords) {
        data.push({
            name: keywords[i]["word"],
            weight: keywords[i]['cnt'],
            events: {
                click: function(event) {
                    let keyword = event.point.name;
                    display_articles_from_word(keyword);
                }
            }
        })
    }
    console.log("Voici les données formatées pour Highcharts :", data);

    Highcharts.chart('nuage', {
        series: [{
            type: 'wordcloud',
            data: data,
            name: 'Occurrences',
            colors: 
                colors,
            rotation: {
                from: -60,
                to: 60,
                orientations: 8
            },
        }],
        title: {
            text: 'Actualité : nuage de mots'
        },
        chart: {
            backgroundColor: 'None'
        }
    });
}

function display_all_articles() {
    let all_articles = []
    for (i = 0; i < news_data['articles'].length; i++)
        all_articles.push(i);
    display_articles(all_articles);
}

function display_articles_from_word(word) {
    let articles;
    for (i in news_data['keywords']) {
        if (news_data['keywords'][i]['word'] == word) {
            articles = news_data['keywords'][i]['articles'];
            break;
        }
    }
    display_articles(articles);
};

function display_articles(articles) {
    let div = $("#tableauArticles").html("");
    div.append("<table></table");
    let tab = $("#tableauArticles table");
    for (i in articles) {
        let article = news_data['articles'][articles[i]];
        let title = article["title"];
        let source = article["source"];
        let url = article["url"];
        let newLine = "<tr><td class='newspaper'>" + source + "</td><td><a target='_blank'href='" + url + "'>" + title + "</a></td></tr>"
        tab.append(newLine);
    }
}

function display_nvd3_graph(data) {
    console.log(typeof(data))
    if (data["status"] == "ok") {
        let temperature_data = [{
            key: 'Température',
            values: data["data"]
        }]
        console.log(3)
        console.log(typeof(temperature_data))
        let first_date = temperature_data[0]['values'][0][0];
        console.log(4)
        console.log(typeof(first_date))
        nv.addGraph(function() {

            let chart = nv.models.lineWithFocusChart()
                .x(function(d) {
                    return d[0]
                })
                .y(function(d) {
                    return d[1]
                })
                .yDomain([-5, 35])
                .height(270)
                .color(colors);

            chart.brushExtent([new Date(first_date), new Date(first_date + 24*3600*1000)]); // 24*3600*1000ms = 1jour

            chart.xAxis
                .showMaxMin(false)
                .tickFormat(function(d) {
                    return d3.time.format('%H:00 (%a)')(new Date(d))
                });

            chart.x2Axis
                .showMaxMin(false)
                .tickFormat(function(d) {
                    return d3.time.format('%a %-d/%-m')(new Date(d))
                });

            chart.yAxis //Chart y-axis settings
                .showMaxMin(false)
                .axisLabel('Température (°c)')
                .tickFormat(d3.format('.00f'));

            chart.y2Axis
                .showMaxMin(false)
                .ticks(false);

            d3.select('#meteo svg')
                .datum(temperature_data)
                .call(chart);

            //Update the chart when window resizes.
            nv.utils.windowResize(chart.update);

            return chart;
        });
    }
}

function display_nvd3_graph_finance(data) {

    console.log(typeof(data))
    if (data["status"] == "ok") {
         let boulbi = data['data'];
    console.log(5)
    console.log(typeof(boulbi))

    // for (i in boulbi){
    //     console.log('boulbi :')
    //     console.log(i)
    // };
         
    for (values in data) {
        console.log(data[values])
        console.log(typeof(data[values]))
        console.log(values.Open)
        console.log(values.valueOf())
        
        // let High = data.High 
        // let Low = data.Low 
        // let Close = data.Close 
        // let Adj_Close = data.Adj_Close 
        // let Volume = data.Volume 
        // console.log(Open) 
        // console.log(High) 
        // console.log(Low) 
        // console.log(Close) 
        // console.log(Adj_Close) 
        // console.log(Volume) 
        ;
}
        }
    
//     display_articles(articles);
};

// chart = {
//     // Declare the chart dimensions and margins.
//     const width = 928;
//     const height = 500;
//     const marginTop = 20;
//     const marginRight = 30;
//     const marginBottom = 30;
//     const marginLeft = 40;
  
//     // Declare the x (horizontal position) scale.
//     const x = d3.scaleUtc(d3.extent(aapl, d => d.date), [marginLeft, width - marginRight]);
  
//     // Declare the y (vertical position) scale.
//     const y = d3.scaleLinear([0, d3.max(aapl, d => d.close)], [height - marginBottom, marginTop]);
  
//     // Declare the line generator.
//     const line = d3.line()
//         .x(d => x(d.date))
//         .y(d => y(d.close));
  
//     // Create the SVG container.
//     const svg = d3.create("svg")
//         .attr("width", width)
//         .attr("height", height)
//         .attr("viewBox", [0, 0, width, height])
//         .attr("style", "max-width: 100%; height: auto; height: intrinsic;");
  
//     // Add the x-axis.
//     svg.append("g")
//         .attr("transform", `translate(0,${height - marginBottom})`)
//         .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0));
  
//     // Add the y-axis, remove the domain line, add grid lines and a label.
//     svg.append("g")
//         .attr("transform", `translate(${marginLeft},0)`)
//         .call(d3.axisLeft(y).ticks(height / 40))
//         .call(g => g.select(".domain").remove())
//         .call(g => g.selectAll(".tick line").clone()
//             .attr("x2", width - marginLeft - marginRight)
//             .attr("stroke-opacity", 0.1))
//         .call(g => g.append("text")
//             .attr("x", -marginLeft)
//             .attr("y", 10)
//             .attr("fill", "currentColor")
//             .attr("text-anchor", "start")
//             .text("↑ Daily close ($)"));
  
//     // Append a path for the line.
//     svg.append("path")
//         .attr("fill", "none")
//         .attr("stroke", "steelblue")
//         .attr("stroke-width", 1.5)
//         .attr("d", line(aapl));
  
//     return svg.node();
//   }