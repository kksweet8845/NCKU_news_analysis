import React, { useState } from "react";
import ReactApexChart from "react-apexcharts";
import { makeStyles } from '@material-ui/core';

const useStyle = makeStyles({
    background: {
        display: 'flex',
        height: '90%',
        width: '95%',
        alignSelf: 'center',
        justifySelf: 'center',
        backgroundColor: 'rgba(255, 255, 255, .7)'
    },
    hideChart: {
        display: 'none',
    }
})

export default function SentimentChart(props) {
    const classes = useStyle()
    const inlineStyle = {
        gridArea: props.gridArea,
    }
    const [series, setSeries] = useState([{
        data: props.data
    }])

    const [options, setOptions] = useState({
        chart: {
            type: 'bar',
            height: '100%',
        },
        plotOptions: {
            bar: {
                horizontal: false,
            }
        },
        dataLabels: {
            enabled: false
        },
        xaxis: {
            categories: ['快樂', '正向', '憤怒', '哀傷', '恐懼', '負面', '驚奇',],
        },
    })

    return (
        <section
            className={`${classes.background} ${(props.show)? '':classes.hideChart}`}
            style={inlineStyle}
        >
            <ReactApexChart
                options={options}
                series={[{
                    data: props.data
                }]}
                type="bar"
                height='100%'
            />
        </section>
    )
}