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

const paperStyle = {
    width: '100%',
    textAlign: 'center'
}

// export class Publisher extends PureComponent {
//     render() {



//         var data = {
//             series: [20,10,30,40]
//         }
//         var options = {
//             donut: true,
//             donutWidth: 60,
//             donutSolid: true,
//             startAngle: 270,
//             showLabel: true
//         }

//         let listOfNews = this.props.news
//         const newsComponents = listOfNews.map((x) =>
//             <SnackbarContent message={x} />)


//         return (
//             <Card>
//                 <CardHeader color={this.props.color}>
//                     <h4>{this.props.name}</h4>
//                 </CardHeader>
//                 <CardBody>
//                     <GridContainer>
//                         <GridItem xs={12} sm={12} md={4} lg={4}>
//                             <ChartistGraph
//                                 className={"ct-chart"}
//                                 data={data}
//                                 options={options}
//                                 type={"Pie"}
//                             />
//                         </GridItem>
//                         <GridItem xs={12} sm={12} md={4} lg={8}>
//                             {newsComponents}
//                         </GridItem>
//                     </GridContainer>
//                 </CardBody>
//             </Card>
//         )
//     }
// }

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
        donutWidth: 60,
        donutSolid: true,
        startAngle: 270,
        showLabel: true
    }

    let listOfNews = props.news
    const newsComponents = listOfNews.map((x) =>
        <SnackbarContent message={x} />)


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
                        {newsComponents}
                    </GridItem>
                </GridContainer>
            </CardBody>
        </Card>
    )
}


export default Publisher
