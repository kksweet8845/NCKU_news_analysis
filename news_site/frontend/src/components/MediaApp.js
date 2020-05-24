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
import { Grid } from '@material-ui/core'

import classNames from 'classnames'
import ChartistGraph from "react-chartist"

import './css/mediaApp.css'

import Slider from "react-slick"
import "slick-carousel/slick/slick.css"
import "slick-carousel/slick/slick-theme.css"

import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Divider from '@material-ui/core/Divider';

import NavigationBar from './common/NavigationBar'


const paperStyle = {
    height: "98vh",
    width: "100%",
    textAlign: "center"
}
const paddings = {
    senti_h3: {
        paddingRight: "11rem",
    },
    senti_graph: {
        paddingRight: "3rem",
    },
    stand_h3: {
        paddingLeft: "11rem",
    },
    stand_graph: {
        paddingLeft: "3rem",
    },
}
const useStyles = makeStyles({
    title: {
        float: "left",
        width: "150px"
    },
    textCenter: {
        textAlign: "center"
    },
    textRight: {
        textAlign: "right"
    },
    textLeft: {
        textAlign: "left"
    },
    root: {
        flexGrow: 1,
    },
    carousel_grid: {
        height: "88vh",
        paddingTop: "10vh",
        width: "30%",
        textAlign: "center",
        backgroundColor: "white",
        color: "black",
        marginTop: "3vh",
        marginBottom: "3vh",
    },
    title_t: {
        color: "black",
        // position: "absolute", 
        // display: "inline-block",           
        bottom: 0,
        textAlign: "center",
        // marginLeft: "auto",
        // marginRight: "auto",
    },
    contain:{
        overflowX: "visible",
    },
    slicksss:{
        maxWidth: "100%",
        maxWeight: "100%",
        marginLeft: "auto",
        marginRight: "auto",
    },
    img: {
        maxWidth: 250,
        maxHeight: 250,
        marginLeft: "auto",
        marginRight: "auto",
        marginTop: 10,
    },
    bg0: {
        backgroundColor: "#e6b2c6",
    },
    bg1: {
        backgroundColor: "#FEF6FB",
    },
    bg2: {
        backgroundColor: "#d6e5fa",
    },
    table: {
        minWidth: 650,
    },
    list_item: {
        width: '100%',
        // maxWidth: "55em",
    },
    main_grid: {
        flexGrow: 1,
        height: "92vh",
        paddingTop: "10vh",
        textAlign: "center",
        backgroundColor: "white",
        marginTop: "3vh",
    },
    header_paper: {
        height: "98vh",
        // textAlign: "center",
        marginBottom: "3vh",
    },
    head_grid: {
        flexGrow: 1,
        height: "88vh",
        paddingTop: "10vh",
        textAlign: "center",
        backgroundColor: "white",
        marginBottom: "3vh",
    },

})

export default function MediaApp(props) {

    const classes = useStyles()

    const images = [
        "https://static.chinatimes.com/images/2019/logo-chinatimes2019-1200x635.png",
        "https://img.vpnclub.cc/content/zh/2018/09/SET-News-Logo.jpg",
        "https://obs.line-scdn.net/0h17LLDchObhhxNUZnYD0RT0hjbXdCWX0bFQM_GzJbMCwIBSBOH1d2KVMzNCtZVylGGFMheF1wMXtYACxMSAQ",
        "https://ramennagi.com.sg/wp-content/uploads/2018/08/tvbs-news.png",
        "https://imgcdn.cna.com.tw/www/website/img/pic_fb.jpg",
    ]


    var handleClick = (e) => {
        console.log('click: ' + e)
        document.getElementById('contents')
    }

    const slide_setting = {
        dots: false,
        infinite: true,
        speed: 400,
        slidesToShow: 3,
        slidesToScroll: 3,
        // variableWidth: true,
    }

    var barChartData = {
        labels: ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9', 'W10'],
        series: [
            [4500, 3000, 4000, 800, 600, 2500, 3000, 700, 600, 250],
        ]
    }

    var barChartOptions = {
        // high: 100,
        // low: -15,
        height: '20rem',
        width: '50vw',
        axisX: {
            labelInterpolationFnc: function(value, index) {
                // return index % 2 === 0 ? value : null;
                return value
            }
        },
        axisY: {
            offset: 100,
            labelInterpolationFnc: function(value) {
              return value + ' 篇'
            },
            scaleMinSpace: 20,
        },
    }

    var sentimentChartData = {
        labels: ['正面', '中立', '負面'],
        series: [30, 20, 50],
    }
    var sentimentChartOptions = {
        height: '20rem',
        width: '20rem',
        donut: true,
        donutWidth: 60,
        donutSolid: true,
        startAngle: 150,
        total: 100,
        showLabel: true,
    }

    var chooseColor = (e) => {
        if(e%3==0)
            return classes.bg0
        if(e%3==1)
            return classes.bg1
        if(e%3==2)
            return classes.bg2
    }

    const rows_data = [
        {title:'hello 1'},
        {title:'hello 2'},
        {title:'hello 3'},
        {title:'hello 4'},
        {title:'hello 5'}
    ]

    return (
        <div>
            <NavigationBar brand="媒體分析"/>
            <Container maxWidth="xl" >
                <div className={classes.head_grid}>
                    <Grid container spacing={1}>
                        <Grid item sm={6}>
                            <h1>媒體分析</h1>
                            <ChartistGraph
                                className={"ct-chart"}
                                data={barChartData}
                                options={barChartOptions}
                                type={"Bar"}
                            />
                        </Grid>
                        <Grid item sm={6}>
                            <h1> rectangle </h1>
                        </Grid>
                    </Grid>
                </div>
            </Container>
            
            <Container maxWidth="xl" >
                <Slider {...slide_setting}> 
                    {images.map((value, index) => (
                        <Paper className={classNames(classes.carousel_grid, chooseColor(index))} onClick={()=>handleClick(index)}>
                            <img src = {value} className={classes.img} />
                            <h1 className={classes.title_t}> media:{index} </h1>
                        </Paper>
                    ))}
                </Slider>
            </Container>

            <Container maxWidth="xl">
                <div className={classes.main_grid}>
                    <Grid container spacing={3}>
                        <Grid item sm={12}>
                            <h1> 中國時報 </h1>
                            <h3> 報導篇數: 3000篇 </h3>
                        </Grid>
                        <Grid item sm={6} className={classes.textRight}>
                            <h3 style={paddings.senti_h3}> 情緒分數 </h3>
                            <ChartistGraph
                                className={"ct-chart"}
                                data={sentimentChartData}
                                options={sentimentChartOptions}
                                type={"Pie"}
                                style={paddings.senti_graph}
                            />
                        </Grid>
                        <Grid item sm={6} className={classes.textLeft}>
                            <h3 style={paddings.stand_h3}> 立場分數 </h3>
                            <ChartistGraph
                                className={"ct-chart"}
                                data={sentimentChartData}
                                options={sentimentChartOptions}
                                type={"Pie"}
                                style={paddings.stand_graph}
                            />
                        </Grid>
                        <Grid item sm={3}/>
                        <Grid item sm={6}>
                            <h2>重點新聞</h2>
                            <List component="nav" className={classes.list_item} aria-label="mailbox folders">
                                <ListItem >
                                    <ListItemText primary="高雄淹水 王浩宇竟跳出來為韓國瑜說話" />
                                </ListItem>
                                <Divider />
                                <ListItem  divider>
                                    <ListItemText primary="教育部推大學生紓困 網看到全怒：不該當勞工！" />
                                </ListItem>
                                <ListItem >
                                    <ListItemText primary="刺胳針》發布陸新冠疫苗試驗：安全且誘導免疫" />
                                </ListItem>
                                <Divider light />
                                <ListItem >
                                    <ListItemText primary="農民退休儲金條例通過 蘇揆：農民退休新制月領37K" />
                                </ListItem>
                            </List>
                        </Grid>
                        <Grid item sm={3}/>
                    </Grid>
                </div>
            </Container>
            
        </div>
    )
}

// ForeignPubApp.propTypes = {

// }

ReactDOM.render(<MediaApp/>, document.getElementById('app'))
