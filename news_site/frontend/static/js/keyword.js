new Chartist.Line('#chart1', {
    labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    series: [
      [12, 9, 7, 8, 5],
      [2, 1, 3.5, 7, 3],
      [1, 3, 4, 5, 6]
    ]
  }, {
    fullWidth: true,
    chartPadding: {
      right: 40
    }
  });

let chart = new Chartist.Pie('#chart2', 
  {
      series: [40, 60 ],
      labels: ['', '']
  }, {
      donut: true,
      donutWidth: 20,
      startAngle: 0,
      total: 100,
      showLabel: false,
      plugins: [
          Chartist.plugins.fillDonut({
              items: [{
                  content: '<i class="fa fa-tachometer"></i>',
                  position: 'bottom',
                  offsetY : 10,
                  offsetX: -2
              }, {
                  content: '<h3>40</h3>'
              }]
          })
      ],
  });

chart.on('draw', function(data) {
  if(data.type === 'slice' && data.index == 0) {
      // Get the total path length in order to use for dash array animation
      var pathLength = data.element._node.getTotalLength();

      // Set a dasharray that matches the path length as prerequisite to animate dashoffset
      data.element.attr({
          'stroke-dasharray': pathLength + 'px ' + pathLength + 'px'
      });

      // Create animation definition while also assigning an ID to the animation for later sync usage
      var animationDefinition = {
          'stroke-dashoffset': {
              id: 'anim' + data.index,
              dur: 1200,
              from: -pathLength + 'px',
              to:  '0px',
              easing: Chartist.Svg.Easing.easeOutQuint,
              fill: 'freeze'
          }
      };

      // We need to set an initial value before the animation starts as we are not in guided mode which would do that for us
      data.element.attr({
          'stroke-dashoffset': -pathLength + 'px'
      });

      // We can't use guided mode as the animations need to rely on setting begin manually
      // See http://gionkunz.github.io/chartist-js/api-documentation.html#chartistsvg-function-animate
      data.element.animate(animationDefinition, true);
  }
});


function collision(){
  let width = window.innerWidth, height = 200, sizeDivisor = 0.5, nodePadding = 2.5;

  let svg = d3.select("#wordClould")
      .append("svg")
      .attr("width", width)
      .attr("height", height);

  let color = d3.scaleOrdinal(["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854", "#ffd92f", "#e5c494", "#b3b3b3"]);

  let simulation = d3.forceSimulation()
      .force("forceX", d3.forceX().strength(.1).x(width * .5))
      .force("forceY", d3.forceY().strength(.1).y(height * .5))
      .force("center", d3.forceCenter().x(width * .5).y(height * .5))
      .force("charge", d3.forceManyBody().strength(-15));
  let data = [
    {
      'country': 'Afghanistan',
      'gdp': 18.4,
      'continent': 'Asia',
    },
    {
      'country': 'Albania',
      'gdp': 12.14,
      'continent': 'Europe',
    },
    {
      'country': 'Algeria',
      'gdp': 16.32,
      'continent': 'Africa',
    },
    {
      'country': 'Angola',
      'gdp': 20.94,
      'continent': 'Africa',
    },
  ]
  let graph = []
  for(let d of data){
    d.size = d.gdp / sizeDivisor
    d.size < 3 ? d.radius = 3 : d.radius = d.size;
    graph.push(d)
  }
  // sort the nodes so that the bigger ones are at the back
  graph = graph.sort(function(a,b){ return b.size - a.size; });
  //update the simulation based on the data
  simulation
      .nodes(graph)
      .force("collide", d3.forceCollide().strength(.5).radius(function(d){ return d.radius + nodePadding; }).iterations(1))
      .on("tick", function(d){
        node
            .attr('transform', function(d){return `translate(${d.x}, ${d.y})` })
            .attr("cx", function(d){ return d.x; })
            .attr("cy", function(d){ return d.y; })
      });

  let node = svg.append("g")
    .attr('class', 'node')
    .selectAll("circle")
    .data(graph)
    .enter().append("g")
      .attr('transform', function(d){return `translate(${d.x}, ${d.y})` })
      .attr('onclick', 'myfunc()')
      .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended))

          

  d3.selectAll('g.node g')
    .append("circle")
      .attr("r", function(d) { return d.radius; })
      .attr("fill", function(d) { return color(d.continent); })
  
  d3.selectAll('g.node g')
    .append('text')
    .text(function (d){
      return d.country
    })
    .attr('text-anchor', 'middle')
    .style("font-size", 12)


  function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(.03).restart();
    d.fx = d.x;
    d.fy = d.y;
  }
  
  function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }
  
  function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(.03);
    d.fx = null;
    d.fy = null;
  }
}

collision()