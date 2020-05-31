// react lib
import React, { useEffect } from 'react'
import ReactApexChart from "react-apexcharts";
// import './chartist-bar-labels'

import '../css/pieChart.css'

export default function (props) {
    let state = {
        series: [{
                data: props.data
        }],
        options: {
            chart: {
                type: 'bar',
            },
            plotOptions: {
                bar: {
                    dataLabels: {
                        position: 'center',
                    }
                }
            },
            dataLabels: {
                enabled: true,
                formatter: function(val) {
                    return val
                },
                offsetY: -20,
                style: {
                    fontSize: '12px',
                    colors: ['#304758']
                }
            },
            xaxis: {
                categories: props.categories,
            },
            yaxis: {
                axisBorder: {
                    show: false,
                },
                axisTicks: {
                    show: false,
                },
                labels: {
                    show: false,
                }
            },
        },
    }

    return (
        <ReactApexChart options={state.options} series={state.series} type="bar" height={`auto`} />
    )
}