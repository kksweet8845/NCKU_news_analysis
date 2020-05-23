import React, { useEffect } from 'react'
import * as d3 from 'd3'
import cloud from 'd3-cloud'
import { CircularProgress } from '@material-ui/core'

const circleRender = (data, nodeId, treshold) => {
    let width = window.innerWidth*0.5, height = 500, sizeDivisor = 0.4, nodePadding = 2.5;
    let fill = d3.scaleOrdinal(d3.schemeCategory10);
    cloud().size([width, height])
            .words(data)
            .padding(2)
            .rotate(function () {
                return ~~(Math.random() * 2) * 90;
            })
            .rotate(function () {
                return 0;
            })
            .fontSize(function (d) {
                return d.size;
            })
            .on('end', draw)
            .start();

    function draw(words) {
        d3.select(`#${nodeId}`).append('svg')
                .attr('width', width)
                .attr('height', height)
                .append('g')
                .attr('transform', 'translate(' + width / 2 + ',' + height / 2 + ')')
                .selectAll('text')
                .data(words)
                .enter()
                    .append('text')
                    .style('font-size', function (d) {
                        return d.size + 'px';
                    })
                    .style('font-family', 'Microsoft JhengHei')
                    .style('cursor', 'pointer')
                    .style('fill', function (d, i) {
                        return fill(i);
                    })
                    .attr('text-anchor', 'middle')
                    .attr('transform', function (d) {
                        return 'translate(' + [d.x, d.y] + ')rotate(' + d.rotate + ')';
                    })
                    .text(function (d) {
                        return d.text;
                    })
                    .on('click', function (d) {
                        window.open('https://www.google.com/search?q=' + d.text, '_blank');
                    });
    }
}


export default function (props) {
    useEffect(() => {
        if(props.data){
            let preData = []
            Object.keys(props.data).map( index => {
                preData.push({
                    'text': props.data[index]['text'],
                    'size': props.data[index]['size'],
                })
            })
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
