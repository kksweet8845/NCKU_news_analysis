import React, { PureComponent } from 'react'
import { Component, makeStyles } from '@material-ui/core'
import { Paper } from '@material-ui/core'
import { Container } from '@material-ui/core'
import { Grid } from '@material-ui/core'
// import { makeStyles } from '@material-ui/core/styles'


import GridContainer from 'components/Grid/GridContainer'
import GridItem from 'components/Grid/GridItem'
import Card from "components/Card/Card"
import CardBody from "components/Card/CardBody"
import CardHeader from "components/Card/CardHeader"
import CardIcon from "components/Card/CardIcon"
import SnackbarContent from "components/Snackbar/SnackbarContent"
import ChartistGraph from "react-chartist"
import Chartist from 'chartist'
import 'chartist-plugin-fill-donut'


const paperStyle = {
    width: '100%',
    textAlign: 'center'
}

const useStyles = makeStyles({
    title: {
        float: "left",
        width: "100px"
    },
    textCenter: {
        textAlign: "center"
    }
})

function Publisher(props) {

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

    let listOfNews = props.news
    const newsComponents = listOfNews.map((x) =>
        <SnackbarContent message={<a href={x.url}>{x.title}</a>} />)


    return (
        <Card className={classes.textCenter}>
            <CardHeader color={props.color} className={classes.title}>
                <h4>{props.name}</h4>
            </CardHeader>
            <CardBody>
                <GridContainer>
                    <GridItem xs={12} sm={12} md={4} lg={4}>
                        <ChartistGraph
                            className={"ct-chart"}
                            data={data}
                            options={options}
                            type={"Pie"}
                        />
                    </GridItem>
                    <GridItem xs={12} sm={12} md={8} lg={8}>
                        <h2> 相關新聞 </h2>
                        {newsComponents}
                    </GridItem>
                </GridContainer>
            </CardBody>
        </Card>
    )
}


export default Publisher
