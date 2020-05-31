import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import ReactDOM from 'react-dom'
import { makeStyles } from '@material-ui/core'

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
import PieChart from './common/pieChart'
import BarChart from './common/barChart'

import Picture from './mediaCom/Picture';
import Focus_item from './mediaCom/focus_item';

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
    textRight: {
        textAlign: "right"
    },
    textLeft: {
        textAlign: "left"
    },
    carousel_grid: {
        height: "45vh",
        // height: "88vh",
        paddingTop: "10vh",
        width: "30%",
        textAlign: "center",
        backgroundColor: "white",
        color: "black",
        marginTop: "13vh",
        marginBottom: "6vh",
    },
    carousel_title: {
        color: "black",
        // position: "absolute",
        // display: "inline-block",
        // bottom: 0,
        textAlign: "center",
        // marginLeft: "auto",
        // marginRight: "auto",
        marginTop: "8vh",
    },
    img: {
        // maxWidth: 250,
        // maxHeight: 250,
        height: "20vh",
        marginLeft: "auto",
        marginRight: "auto",
        marginTop: 10,
    },
    bg0: {
        // backgroundColor: "#e6b2c6",
        backgroundColor: "#c8d6ca",
    },
    bg1: {
        // backgroundColor: "#FEF6FB",
        backgroundColor: "#99bfaa",
    },
    bg2: {
        // backgroundColor: "#d6e5fa",
        backgroundColor: "#81a3a7",
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
    head_grid: {
        flexGrow: 1,
        height: "100vh",
        paddingTop: "7vh",
        textAlign: "center",
        backgroundColor: "white",
        marginBottom: "4vh",
    },
    grid_container :{
        height: "100%",
    },
    head_title: {
        fontSize: "5rem",
    },
    pieChart: {
        height: "40vh",
    },
    news_block: {
        marginTop: "10vh",
        marginBottom: "15vh",
    },
    barchart_layout: {
        height: "60vh",
        width: "100%",
        marginTop: "10vh",
    },
    h2_style: {
        fontSize: '28px',
    },
    h1_style: {
        fontSize: '45px',
    },
})

export default function MediaApp(props) {

    const classes = useStyles()

    const [nowidx, setNowidx] = useState(1)

    const media_index = [
        1,4,5,7,8,9,11,12,13,14,15,16,18
    ]

    const initObj = {
        '1': {'name': 'TVBS', 
            'news_number': 3000,
            'sentiment': [44, 55, 41],
            'standpoint': [44, 55],
            'focus_news': [[{'title': '', 'href': ''}]]
        },
        '4': {'name': '三立',
            'news_number': 2000,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '', 'href': ''}]]
        },
        '5': {'name': '上報',
            'news_number': 1000,
            'sentiment': [91, 25, 11],
            'standpoint': [25, 74],
            'focus_news': [[{'title': '', 'href': ''}]]
        },
        '7': {'name': '三立',
            'news_number': 7,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '', 'href': ''}]]
        },
        '8': {'name': '三立',
            'news_number': 8,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '', 'href': ''}]]
        },
        '9': {'name': '三立',
            'news_number': 9,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '', 'href': ''}]]
        },
        '11': {'name': '三立',
            'news_number': 11,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '', 'href': ''}]]
        },
        '12': {'name': '三立',
            'news_number': 12,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '', 'href': ''}]]
        },
        '13': {'name': '三立',
            'news_number': 13,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '', 'href': ''}]]
        },
        '14': {'name': '三立',
            'news_number': 14,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '', 'href': ''}]]
        },
        '15': {'name': '三立',
            'news_number': 15,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '', 'href': ''}]]
        },
        '16': {'name': '三立',
            'news_number': 16,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '', 'href': ''}]]
        },
        '18': {'name': '三立',
            'news_number': 18,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '', 'href': ''}]]
        },        
    }

    const initChartData = {
        'labels': ["Jan", "Feb", "Mar"],
        'series': [44, 55, 41],
    }

    const [isFetch, setIsFetch] = useState(false)
    const [dataObj, setDataObj] = useState(initObj)
    const [newsNumObj, setNewsNumObj] = useState(initChartData)

    useEffect(()=>{
        if(!isFetch){
            fetch('/analysis/mediaAnalysis', {
                method: 'get',
            }).then((res) => {
                return res.json()
            }).then((obj) => {
                setDataObj(obj)
                // setIsFetch(true)
            }).then(() => {
                fetch('/analysis/mediaReport', {
                    method: 'get',
                }).then((res) => {
                    return res.json()
                }).then((obj) => {
                    setNewsNumObj(obj)
                    setIsFetch(true)
                })
            })
        }
    })

    const media_map = {
        1: {'name': 'TVBS', 
            'img': 'https://imgur.com/edI5QMN.png',},
        4: {'name': '三立', 
            'img': 'https://imgur.com/HsDdh8C.png',},
        5: {'name': '上報', 
            'img': 'https://imgur.com/98Ec7R0.png',},
        7: {'name': '中央社', 
            'img': 'https://imgur.com/uu3KeZh.png',},
        8: {'name': '中時電子報',
            'img': 'https://imgur.com/VLtOCJQ.png',},
        9: {'name': '今日新聞',
            'img': 'https://imgur.com/KVdihFa.png',},
        11: {'name': '自由時報',
            'img': 'https://imgur.com/CU0Nq42.png',},
        12: {'name': '民視新聞',
            'img': 'https://imgur.com/XmifsA8.png',},
        13: {'name': '風傳媒',
            'img': 'https://imgur.com/6TzTmHZ.png',},
        14: {'name': '東森ETtoday',
            'img': 'https://imgur.com/yRuX5jc.png',},
        15: {'name': '新頭殼',
            'img': 'https://imgur.com/OM1u1BS.png',},
        16: {'name': '聯合新聞網',
            'img': 'https://imgur.com/Y8x2Ugi.png',},
        18: {'name': '華視',
            'img': 'https://imgur.com/Ajq8wTX.png',},
    }

    var handleClick = (e) => {
        // console.log('click: ' + e)
        setNowidx(e)
        document.getElementById('scroll_target').scrollIntoView({behavior:'smooth'})
    }

    const slide_setting = {
        dots: false,
        infinite: true,
        speed: 400,
        slidesToShow: 3,
        slidesToScroll: 3,
    }

    var chooseColor = (e) => {
        if(e%3==0)
            return classes.bg0
        if(e%3==1)
            return classes.bg1
        if(e%3==2)
            return classes.bg2
    }

    return (
        <div>
            <NavigationBar brand="媒體分析"/>
            <Container maxWidth="xl" >
                <div className={classes.head_grid}>
                    <Grid container spacing={1} className={classes.grid_container}>
                        <Grid item sm={6}>
                            <h1 className={classes.head_title}>媒體分析</h1>
                            <div className={classes.barchart_layout}>
                                <BarChart
                                    categories = {newsNumObj.labels}
                                    data = {newsNumObj.series}
                                />
                            </div>
                        </Grid>
                        <Grid item sm={6}>
                            <Picture imgSrc={"https://imgur.com/VoH43KC.png"}/>
                        </Grid>
                    </Grid>
                </div>
            </Container>

            <Container maxWidth="xl" >
                <Slider {...slide_setting}>
                    {media_index.map((value, index) => (
                        <Paper className={classNames(classes.carousel_grid, chooseColor(index))} onClick={()=>handleClick(value)}>
                            <img src = {media_map[value].img} className={classes.img} />
                            <h1 className={classes.carousel_title}> {media_map[value].name} </h1>
                        </Paper>
                    ))}
                </Slider>
            </Container>

            <Container maxWidth="xl" id='scroll_target'>
                <div className={classes.main_grid}>
                    <Grid container justify="center" spacing={3}>
                        <Grid item sm={12}>
                            <h1 className={classes.h1_style}> {media_map[nowidx].name} </h1>
                            <h2 className={classes.h2_style}> 報導篇數: {dataObj[nowidx].news_number} 篇 </h2>
                        </Grid>
                    </Grid>
                    <Grid container justify="center" spacing={3} className={classes.pieChart}>
                        <Grid item sm={3} className={[classes.textRight]}>
                            <h3 style={paddings.senti_h3}> 情緒分數 </h3>
                            <PieChart
                                // labels: ['正面', '中立', '負面'],
                                grades = {dataObj[nowidx].sentiment}
                                nodeId = {'sentiment'}
                                chartType = {0}
                            />
                        </Grid>
                        <Grid item sm={3} className={classes.textLeft}>
                            <h3 style={paddings.stand_h3}> 立場分數 </h3>
                            <PieChart
                                // labels: ['中時', '三立']
                                grades = {dataObj[nowidx].standpoint}
                                nodeId = {'position'}
                                chartType = {1}
                            />
                        </Grid>
                    </Grid>
                    <Grid className={classes.news_block} container justify="center" spacing={3}>
                        <Grid item sm={10}>
                            <h2  className={classes.h2_style}>重點新聞</h2>
                            {dataObj[nowidx].focus_news.map((obj, index) => {
                                return <Focus_item 
                                        color= "#27496d"
                                        num= {obj.length} // num= {index + 1}
                                        keyword= {obj[0].title}
                                        links= {obj}
                                        width= "80%"
                                        />
                            })}
                        </Grid>
                    </Grid>
                </div>
            </Container>
        </div>
    )
}

// ForeignPubApp.propTypes = {

// }

ReactDOM.render(<MediaApp/>, document.getElementById('app'))
