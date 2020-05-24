import React, { useEffect } from 'react'
import * as d3 from 'd3'
import { CircularProgress } from '@material-ui/core'

const circleRender = (data, nodeId, treshold) => {
    let width = window.innerWidth*0.6, height = 1000, sizeDivisor = 0.4, nodePadding = 2.5;

    let svg = d3.select(`#${nodeId}`)
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("align", "center")

    // let color = d3.scaleOrdinal(["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854", "#ffd92f", "#e5c494", "#b3b3b3"]);
    let color = d3.scaleOrdinal(["#FA7C92", "#6EC4DB", "#FFF7C0", "#66AB8C"])
    let simulation = d3.forceSimulation()
        .force("forceX", d3.forceX().strength(.1).x(width * .5))
        .force("forceY", d3.forceY().strength(.1).y(height * .5))
        .force("center", d3.forceCenter().x(width * .5).y(height * .5))
        .force("charge", d3.forceManyBody().strength(-15))

    let graph = []
    for(let d of data) {
        d.size = d.tally / sizeDivisor
        d.size < 3 ? d.radius = 3 : d.radius = d.size;
        if(d.tally > treshold)
            graph.push(d)
    }
    // sort the nodes so that the bigger ones are at the back
    graph = graph.sort(function(a,b){ return b.size - a.size; })
    let min = graph[graph.length-1].radius, max = graph[0].radius, scale = 60, textScale=40
    graph = graph.map(d => {
        console.log(d.radius)
        return Object.assign({} , d, {
            radius: graph.length > 1 ? d.radius / (max-min) * scale : scale,
            textSize: graph.length > 1 ? d.radius / (max-min) * textScale : textScale,
        })
    })
    //update the simulation based on the data
    simulation
        .nodes(graph)
        .force("collide", d3.forceCollide().strength(.5).radius(function(d){ return d.radius + nodePadding; }).iterations(1))
        .on("tick", function(d){
        node
            .attr('transform', function(d){return `translate(${d.x}, ${d.y})` })
            .attr("cx", function(d){ return d.x; })
            .attr("cy", function(d){ return d.y; })
        })

    let node = svg.append("g")
    .attr('class', 'node')
    .selectAll("circle")
    .data(graph)
    .enter().append("g")
        .attr('transform', function(d){return `translate(${d.x}, ${d.y})` })
        .on('click', (d) => {
            document.getElementById(d.title).click()
        })
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended))

    d3.selectAll('g.node g')
    .append("circle")
        .attr("r", function(d) { return d.radius; })
        .attr("fill", function(d) { return 'white'; })

    d3.selectAll('g.node g')
    .append('text')
    .attr('x', 0)
    .attr('y', 0)
    .style('font-size', d => `${d.textSize}px`)
    .text(function (d){
        return d.title
    })
    .attr('text-anchor', 'middle')

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


export default function (props) {
    useEffect(() => {
        if(props.data){
            let preData = []
            Object.keys(props.data).map( index => {
                console.log(index)
                preData.push({
                    'title': props.data[index]['text'],
                    'tally': props.data[index]['num'],
                })
            })
            console.log(preData)
            circleRender(preData, props.id, 0)
        }
    }, [props.data])

    if(props.ready){
        return (
            <div>
                <div id={props.id}></div>
            </div>
        )
    }else{
        return (
            <div>
                <h1> Wait a min! </h1>
                <CircularProgress />
            </div>
        )
    }
}
