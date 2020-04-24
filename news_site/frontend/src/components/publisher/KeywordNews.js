import React, { PureComponent } from 'react'
import { makeStyles } from "@material-ui/core"
import className from 'classnames'

import GridContainer from "components/Grid/GridContainer"
import GridItem from "components/Grid/GridItem"
import Card from "components/Card/Card"
import CardHeader from "components/Card/CardHeader"
import CardBody from "components/Card/CardBody"
// chartist
import ChartistGraph from "react-chartist"
import SnackbarContent from "components/Snackbar/SnackbarContent"
import Chartist from 'chartist'
import 'chartist-plugin-fill-donut'

const styles = {
    pie: {
        margin: "20px auto"
    }
}

const useStyles = makeStyles(styles)


function KeywordNews(props) {

    const classes = useStyles()
    var data = {
        series: [20,10,30,40]
    }
    var options = {
        donut: true,
        donutWidth: 20,
        donutSolid: true,
        startAngle: 270,
        showLabel: true,
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
        ]
    }

    var lineChartData = {
        labels: ["3/1","3/2","3/3","3/4","3/5","3/6","3/7","3/8"],
        series: [
            [5,9,7,8,5,3,5,4]
        ]
    }

    var lineChartOptions = {
        low: 0,
        showArea: true
    }

    return (
        <Card>
            <CardHeader>
                <h1>{props.data.keyword}</h1>
                <p>{props.data.tally} 則新聞</p>
            </CardHeader>
            <CardBody>
                <GridContainer>
                    <GridItem xs={12} sm={12} md={6} lg={3}>
                        <ChartistGraph
                            className={className("ct-chart", classes.pie)}
                            data={data}
                            options={options}
                            type={"Pie"}
                        />
                    </GridItem>
                    <GridItem xs={12} sm={12} md={6} lg={3}>
                        <ChartistGraph
                            className={className("ct-chart", classes.pie)}
                            data={lineChartData}
                            options={lineChartOptions}
                            type={"Line"}
                        />
                    </GridItem>
                    <GridItem xs={12} sm={12} md={12} lg={6}>
                        {props.data.news.map(d => <SnackbarContent
                            message={<a href={d.url}>{d.title} <span>{d.date}</span></a>}
                        />)}
                    </GridItem>
                </GridContainer>
            </CardBody>
        </Card>
    )
}



export default KeywordNews
