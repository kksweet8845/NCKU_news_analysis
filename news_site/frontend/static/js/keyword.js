function collision(){
  let width = window.innerWidth * 0.6, height = 200, sizeDivisor = 0.4, nodePadding = 2.5;

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
      'title': '中天',
      'count': 14,
    },
    {
      'title': '蘋果',
      'count': 16,
    },
    {
      'title': '風傳媒',
      'count': 18,
    },
    {
      'title': '三立',
      'count': 12,
    },
  ]
  let graph = []
  for(let d of data){
    d.size = d.count / sizeDivisor
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
      .attr("fill", function(d) { return color(d.count); })

  d3.selectAll('g.node g')
    .append('text')
    .attr('x', 0)
    .attr('y', 0)
    .text(function (d){
      return d.title
    })
    .attr('text-anchor', 'middle')
    .style('font-size', 12)
    .append('tspan')
    .attr('x', 0)
    .attr('dy', '1.2em')
    .text(function (d){
      return d.count
    })

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