import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'
import className from 'classnames'
//core components
import Card from "components/Card/Card"
import CardBody from "components/Card/CardBody"
import CardHeader from "components/Card/CardHeader"
import { Container, makeStyles } from "@material-ui/core"
import GridContainer from "components/Grid/GridContainer"
import GridItem from "components/Grid/GridItem"
// chartist
import ChartistGraph from "react-chartist"

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
        donutWidth: 60,
        donutSolid: true,
        startAngle: 270,
        showLabel: true
    }

    let newsData = [
        {
            title: '武漢肺炎',
            numOfNews: 12,
            newsPreview: [
                '反送終',
                '每天都是可以吃的'
            ]
        },
        {
            title: '香港',
            numOfNews: 12,
            newsPreview: [
                '反送終',
                '每天都是可以吃的'
            ]
        },
        {
            title: '反送中',
            numOfNews: 12,
            newsPreview: [
                '反送終',
                '每天都是可以吃的'
            ]
        },
        {
            title: '美國川普',
            numOfNews: 12,
            newsPreview: [
                '反送終',
                '每天都是可以吃的'
            ]
        },
        {
            title: '比爾概資',
            numOfNews: 12,
            newsPreview: [
                '反送終',
                '每天都是可以吃的'
            ]
        }
    ]

    return (
        <Container maxWidth="lg">
            <Card>
                <CardHeader color="primary" className={classes.publisherTitle}>
                    <h1 className={classes.textCenter}>公視</h1>
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
                                <NewsSel news={newsData.map(d=>d.title)}/>
                            </GridItem>
                        </GridContainer>
                    </Container>
                    <Container>
                        {newsData.map(d => <KeywordNews
                            data={d}
                        />)}
                    </Container>
                </CardBody>
            </Card>
        </Container>
    )
}
