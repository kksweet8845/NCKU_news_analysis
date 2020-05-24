// react lib
import React, { useEffect } from 'react'
import ChartistGraph from 'react-chartist'
import Chartist from 'chartist'
import { makeStyles } from '@material-ui/core/styles';
import { CircularProgress } from '@material-ui/core'
import color from '@material-ui/core/colors/amber';
import legend from 'chartist-plugin-legend'

import './md5'
import '../css/pieChart.css'

const renderPie = (grades, nodeId)=>{
    let chart = new Chartist.Pie(`.${nodeId}`, {
            series: [
                {
                    value: grades[0],
                    className: 'positive-stroke',
                },
                {
                    value: grades[1],
                    className: 'neutral-stroke',
                },
                {
                    value: grades[2],
                    className: 'negative-stroke',
                }
            ],
            showLabel: false,
            labels: [1, 2, 3],
            plugins: [
                legend(),
            ]
        }, {
            donut: true,
            showLabel: false
        },
    );
    chart.on('draw', function(data) {
        if(data.type === 'slice') {
        // Get the total path length in order to use for dash array animation
        let pathLength = data.element._node.getTotalLength();
        // Set a dasharray that matches the path length as prerequisite to animate dashoffset
        data.element.attr({
            'stroke-dasharray': pathLength + 'px ' + pathLength + 'px'
        });
        // Create animation definition while also assigning an ID to the animation for later sync usage
        let animationDefinition = {
            'stroke-dashoffset': {
            id: 'anim' + data.index,
            dur: 1000,
            from: -pathLength + 'px',
            to:  '0px',
            easing: Chartist.Svg.Easing.easeOutQuint,
            // We need to use `fill: 'freeze'` otherwise our animation will fall back to initial (not visible)
            fill: 'freeze'
            }
        };
        // If this was not the first slice, we need to time the animation so that it uses the end sync event of the previous animation
        if(data.index !== 0) {
            animationDefinition['stroke-dashoffset'].begin = 'anim' + (data.index - 1) + '.end';
        }
        // We need to set an initial value before the animation starts as we are not in guided mode which would do that for us
        data.element.attr({
            'stroke-dashoffset': -pathLength + 'px'
        });
        // We can't use guided mode as the animations need to rely on setting begin manually
        // See http://gionkunz.github.io/chartist-js/api-documentation.html#chartistsvg-function-animate
        data.element.animate(animationDefinition, false);
        }
    });
    // For the sake of the example we update the chart every time it's created with a delay of 8 seconds
    // chart.on('created', function() {
    //     if(window.__anim21278907124) {
    //     clearTimeout(window.__anim21278907124);
    //     window.__anim21278907124 = null;
    // }
    //     window.__anim21278907124 = setTimeout(chart.update.bind(chart), 5000);
    // });
}

export default function (props) {

    props.nodeId = '_' + parseInt(Math.random()*100000).toString()

    useEffect(()=>{
        console.log(props.nodeId)
        renderPie(props.grades, props.nodeId)
    })

    return (
        <div className={props.nodeId}>
        </div>
    )
}