import React from 'react'
import PropTypes from 'prop-types'
import ReactDOM from 'react-dom'
import { makeStyles } from '@material-ui/core'

import Card from 'components/Card/Card'
import CardHeader from 'components/Card/CardHeader'
import CardBody from 'components/Card/CardBody'

import GridContainer from 'components/Grid/GridContainer'
import GridItem from 'components/Grid/GridItem'
import SnackbarContent from "components/Snackbar/SnackbarContent"

import { Container } from '@material-ui/core'
import { Paper } from '@material-ui/core'

import ChartistGraph from "react-chartist"

const paperStyle = {
    height: "600px",
    width: "100%",
    textAlign: "center"
}
const useStyles = makeStyles({
    title: {
        float: "left",
        width: "150px"
    },
    textCenter: {
        textAlign: "center"
    }
})

export default function ForeignPubApp(props) {

    const classes = useStyles()


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

    let newsData = [
        '武漢封城',
        '意大力死百萬人',
        '中國毀滅'
    ]

    return (
        <div>
            <Container maxWidth="lg">
                <Paper style={paperStyle} elevation={3}>
                    <h1> 新疫情衝擊 </h1>
                    <div id="pubCloud"></div>
                </Paper>
            </Container>
            <Container maxWidth="lg">
                <Card>
                    <CardHeader color="primary" className={classes.title}>
                        <h1> 紐約時報 </h1>
                    </CardHeader>
                    <CardBody>
                        <Container>
                            <Paper>
                                <h1 style={paperStyle}> 文字雲 </h1>
                            </Paper>
                        </Container>
                        <Card>
                            <CardHeader>
                                <h1> 中國 </h1>
                            </CardHeader>
                            <CardBody>
                                <GridContainer>
                                    <GridItem xs={12} sm={12} md={4} lg={4}>
                                        <ChartistGraph
                                            className={"ct-chart"}
                                            data={lineChartData}
                                            options={lineChartOptions}
                                            type={"Line"}
                                        />
                                    </GridItem>
                                    <GridItem xs={12} sm={12} md={8} lg={8}>
                                        {newsData.map(d => <SnackbarContent
                                            message={d}
                                        />)}
                                    </GridItem>
                                </GridContainer>
                            </CardBody>
                        </Card>
                    </CardBody>
                </Card>
            </Container>
        </div>
    )
}

// ForeignPubApp.propTypes = {

// }

ReactDOM.render(<ForeignPubApp/>, document.getElementById('app'))
