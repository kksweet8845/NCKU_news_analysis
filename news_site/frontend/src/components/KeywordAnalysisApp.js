import React, { useState } from 'react'
import PropTypes from 'prop-types'
import ReactDOM from 'react-dom'
import { makeStyles } from '@material-ui/core'

import Card from 'components/Card/Card'
import CardHeader from 'components/Card/CardHeader'
import CardBody from 'components/Card/CardBody'

import GridContainer from 'components/Grid/GridContainer'
import GridItem from 'components/Grid/GridItem'
import SnackbarContent from "components/Snackbar/SnackbarContent"

import Header from 'components/Header/Header'
import HeaderLinks from 'components/Header/HeaderLinks'

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
    const [topic, setTopic] = useState('COVID-19')
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
        <div>
            <Header
                color="transparent"
                brand="出版社頁面"
                fixed
                changeColorOnScroll={{
                    height: 300,
                    color: "white"
                }}
            />
            <Container>
                <GridItem xs={12} sm={12} md={4} lg={4}>
                    <ChartistGraph
                        className={"ct-chart"}
                        data={lineChartData}
                        options={lineChartOptions}
                        type={"Line"}
                    />
                </GridItem>
            </Container>
            <main>
                <h1>{topic}</h1>
            </main>
        </div>
    )
}

ReactDOM.render(<ForeignPubApp/>, document.getElementById('app'))
