import React, { useEffect } from 'react'
import className from 'classnames'
//core components
import Card from "components/Card/Card"
import CardBody from "components/Card/CardBody"
import CardHeader from "components/Card/CardHeader"
import { Container, makeStyles, CircularProgress } from "@material-ui/core"
import GridContainer from "components/Grid/GridContainer"
import GridItem from "components/Grid/GridItem"
// chartist
import ChartistGraph from "react-chartist"
import Chartist from 'chartist'
import 'chartist-plugin-fill-donut'
// custom components
import KeywordNews from "./KeywordNews"
import NewsSel from "./NewsSel"


const styles = {
    pie: {
        marginTop: "50px",
        marginBottom: "auto",
        marginLeft: "auto"
    },
    publisherTitle: {
        width: "150px",
        float: "left"
    },
    textCenter: {
        textAlign: "center"
    },
    cardCollection: {
        maxHeight: '1000px',
        overflowY: 'scroll'
    }
}

const useStyles = makeStyles(styles)


export default function PubContent(props) {
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
    if(props.ready){
        return (
            <Container maxWidth="lg">
                <Card>
                    <CardHeader color="primary" className={classes.publisherTitle}>
                        <h1 className={classes.textCenter}>{props.data.brand}</h1>
                    </CardHeader>
                    <CardBody>
                        <Container>
                            <GridContainer>
                                <GridItem xs={12} sm={12} md={4} lg={4}>
                                    <div className={classes.pie}>
                                        <ChartistGraph
                                            className={"ct-chart"}
                                            data={data}
                                            options={options}
                                            type={"Pie"}
                                        />
                                    </div>
                                </GridItem>
                                <GridItem xs={12} sm={12} md={8} lg={8}>
                                    <NewsSel news={props.data.news.map(d=>d.keyword)}/>
                                </GridItem>
                            </GridContainer>
                        </Container>
                        <Container className={classes.cardCollection}>
                            {props.data.news.map(d => <KeywordNews
                                data={d}
                            />)}
                        </Container>
                    </CardBody>
                </Card>
            </Container>
        )
    }else{
        return (
            <Container maxWidth="lg">
                <Card>
                    <CardHeader color="primary" className={classes.publisherTitle}>
                        <CircularProgress />
                    </CardHeader>
                    <CardBody>
                        <Container>
                            <GridContainer>
                                <GridItem xs={12} sm={12} md={4} lg={4}>
                                    <CircularProgress />
                                </GridItem>
                                <GridItem xs={12} sm={12} md={8} lg={8}>
                                    <CircularProgress />
                                </GridItem>
                            </GridContainer>
                        </Container>
                        <Container>
                            <CircularProgress />
                        </Container>
                    </CardBody>
                </Card>
            </Container>
        )
    }
}
