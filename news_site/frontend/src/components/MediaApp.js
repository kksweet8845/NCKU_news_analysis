import React, { useState } from 'react'
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

    var tmp_obj = {
        1: {'name': 'TVBS', 
            'news_number': 3000,
            'sentiment': [44, 55, 41],
            'standpoint': [44, 55],
            'focus_news': [[{title: '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', href: 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {title: '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', href: 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {title: '又是QR818班機！　83乘客16人染新冠肺炎', href: 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{title: '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', href: 'https://news.tvbs.com.tw/politics/1331974'},
                            {title: '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', href: 'https://news.tvbs.com.tw/politics/1332139'},
                            {title: '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', href: 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        4: {'name': '三立',
            'news_number': 2000,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{title: '1發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', href: 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {title: '1隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', href: 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {title: '1又是QR818班機！　83乘客16人染新冠肺炎', href: 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{title: '1拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', href: 'https://news.tvbs.com.tw/politics/1331974'},
                            {title: '1謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', href: 'https://news.tvbs.com.tw/politics/1332139'},
                            {title: '1罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', href: 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        5: {'name': '上報',
            'news_number': 1000,
            'sentiment': [91, 25, 11],
            'standpoint': [25, 74],
            'focus_news': [[{title: '2發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', href: 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {title: '2隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', href: 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {title: '2又是QR818班機！　83乘客16人染新冠肺炎', href: 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{title: '2拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', href: 'https://news.tvbs.com.tw/politics/1331974'},
                            {title: '2謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', href: 'https://news.tvbs.com.tw/politics/1332139'},
                            {title: '2罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', href: 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        7: {'name': '三立',
            'news_number': 7,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{title: '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', href: 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {title: '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', href: 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {title: '又是QR818班機！　83乘客16人染新冠肺炎', href: 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{title: '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', href: 'https://news.tvbs.com.tw/politics/1331974'},
                            {title: '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', href: 'https://news.tvbs.com.tw/politics/1332139'},
                            {title: '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', href: 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        8: {'name': '三立',
            'news_number': 8,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{title: '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', href: 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {title: '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', href: 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {title: '又是QR818班機！　83乘客16人染新冠肺炎', href: 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{title: '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', href: 'https://news.tvbs.com.tw/politics/1331974'},
                            {title: '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', href: 'https://news.tvbs.com.tw/politics/1332139'},
                            {title: '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', href: 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        9: {'name': '三立',
            'news_number': 9,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{title: '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', href: 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {title: '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', href: 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {title: '又是QR818班機！　83乘客16人染新冠肺炎', href: 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{title: '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', href: 'https://news.tvbs.com.tw/politics/1331974'},
                            {title: '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', href: 'https://news.tvbs.com.tw/politics/1332139'},
                            {title: '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', href: 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        11: {'name': '三立',
            'news_number': 11,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{title: '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', href: 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {title: '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', href: 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {title: '又是QR818班機！　83乘客16人染新冠肺炎', href: 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{title: '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', href: 'https://news.tvbs.com.tw/politics/1331974'},
                            {title: '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', href: 'https://news.tvbs.com.tw/politics/1332139'},
                            {title: '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', href: 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        12: {'name': '三立',
            'news_number': 12,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{title: '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', href: 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {title: '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', href: 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {title: '又是QR818班機！　83乘客16人染新冠肺炎', href: 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{title: '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', href: 'https://news.tvbs.com.tw/politics/1331974'},
                            {title: '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', href: 'https://news.tvbs.com.tw/politics/1332139'},
                            {title: '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', href: 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        13: {'name': '三立',
            'news_number': 13,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{title: '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', href: 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {title: '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', href: 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {title: '又是QR818班機！　83乘客16人染新冠肺炎', href: 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{title: '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', href: 'https://news.tvbs.com.tw/politics/1331974'},
                            {title: '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', href: 'https://news.tvbs.com.tw/politics/1332139'},
                            {title: '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', href: 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        14: {'name': '三立',
            'news_number': 14,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{title: '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', href: 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {title: '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', href: 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {title: '又是QR818班機！　83乘客16人染新冠肺炎', href: 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{title: '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', href: 'https://news.tvbs.com.tw/politics/1331974'},
                            {title: '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', href: 'https://news.tvbs.com.tw/politics/1332139'},
                            {title: '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', href: 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        15: {'name': '三立',
            'news_number': 15,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{title: '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', href: 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {title: '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', href: 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {title: '又是QR818班機！　83乘客16人染新冠肺炎', href: 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{title: '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', href: 'https://news.tvbs.com.tw/politics/1331974'},
                            {title: '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', href: 'https://news.tvbs.com.tw/politics/1332139'},
                            {title: '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', href: 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        16: {'name': '三立',
            'news_number': 16,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{title: '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', href: 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {title: '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', href: 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {title: '又是QR818班機！　83乘客16人染新冠肺炎', href: 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{title: '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', href: 'https://news.tvbs.com.tw/politics/1331974'},
                            {title: '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', href: 'https://news.tvbs.com.tw/politics/1332139'},
                            {title: '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', href: 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        18: {'name': '三立',
            'news_number': 18,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{title: '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', href: 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {title: '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', href: 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {title: '又是QR818班機！　83乘客16人染新冠肺炎', href: 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{title: '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', href: 'https://news.tvbs.com.tw/politics/1331974'},
                            {title: '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', href: 'https://news.tvbs.com.tw/politics/1332139'},
                            {title: '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', href: 'https://news.tvbs.com.tw/politics/1332298'}]]
        },        
    }

    const media_map = {
        1: {'name': 'TVBS', 
            'img': 'https://imgur.com/edI5QMN.png',
            'content': '',},
        4: {'name': '三立', 
            'img': 'https://imgur.com/HsDdh8C.png',
            'content': '',},
        5: {'name': '上報', 
            'img': 'https://imgur.com/98Ec7R0.png',
            'content': '',},
        7: {'name': '中央社', 
            'img': 'https://imgur.com/uu3KeZh.png',
            'content': '',},
        8: {'name': '中時電子報',
            'img': 'https://imgur.com/VLtOCJQ.png',
            'content': '',},
        9: {'name': '今日新聞',
            'img': 'https://imgur.com/KVdihFa.png',
            'content': '',},
        11: {'name': '自由時報',
            'img': 'https://imgur.com/CU0Nq42.png',
            'content': '',},
        12: {'name': '民視新聞',
            'img': 'https://imgur.com/XmifsA8.png',
            'content': '',},
        13: {'name': '風傳媒',
            'img': 'https://imgur.com/6TzTmHZ.png',
            'content': '',},
        14: {'name': '東森ETtoday',
            'img': 'https://imgur.com/yRuX5jc.png',
            'content': '',},
        15: {'name': '新頭殼',
            'img': 'https://imgur.com/OM1u1BS.png',
            'content': '',},
        16: {'name': '聯合新聞網',
            'img': 'https://imgur.com/Y8x2Ugi.png',
            'content': '',},
        18: {'name': '華視',
            'img': 'https://imgur.com/Ajq8wTX.png',
            'content': '',},
    }

    var handleClick = (e) => {
        console.log('click: ' + e)
        setNowidx(e)
        // window.scrollTo({
        //     top: '1750',
        //     behavior: 'smooth'
        // })
        document.getElementById('scroll_target').scrollIntoView({behavior:'smooth'})
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
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        series: [44, 55, 41, 67, 22, 43, 44, 55, 41, 67, 22, 43],
    }

    // var barChartOptions = {
    //     height: '45vh',
    //     width: '40vw',
    //     axisX: {
    //         showGrid: false,
    //         labelInterpolationFnc: function(value, index) {
    //             return value
    //         }
    //     },
    //     axisY: {
    //         offset: 50,
    //         showGrid: false,
    //         // showLabel: false,
    //         scaleMinSpace: 20,
    //     },
    // }

    // labels: ['中時', '三立'],
    var standpointChartData = tmp_obj[nowidx].standpoint

    // labels: ['正面', '中立', '負面'],
    var sentimentChartData = tmp_obj[nowidx].sentiment

    // var standpointChartOptions = {
    //     height: '20rem',
    //     width: '20rem',
    //     donut: true,
    //     donutWidth: 60,
    //     donutSolid: true,
    //     startAngle: 150,
    //     total: tmp_obj[nowidx].standpoint.reduce((a, b) => a + b, 0),
    //     showLabel: true,
    // }

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
                                    categories = {barChartData.labels}
                                    data = {barChartData.series}
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
                            {/* <p>{media_map[value].content}</p> */}
                        </Paper>
                    ))}
                </Slider>
            </Container>

            <Container maxWidth="xl" id='scroll_target'>
                <div className={classes.main_grid}>
                    <Grid container justify="center" spacing={3}>
                        <Grid item sm={12}>
                            <h1 className={classes.h1_style}> {media_map[nowidx].name} </h1>
                            <h2 className={classes.h2_style}> 報導篇數: {tmp_obj[nowidx].news_number} 篇 </h2>
                        </Grid>
                    </Grid>
                    <Grid container justify="center" spacing={3} className={classes.pieChart}>
                        <Grid item sm={3} className={[classes.textRight]}>
                            <h3 style={paddings.senti_h3}> 情緒分數 </h3>
                            <PieChart
                                // labels: ['正面', '中立', '負面'],
                                grades = {tmp_obj[nowidx].sentiment}
                                nodeId = {'sentiment'}
                                chartType = {0}
                            />
                        </Grid>
                        <Grid item sm={3} className={classes.textLeft}>
                            <h3 style={paddings.stand_h3}> 立場分數 </h3>
                            <PieChart
                                // labels: ['中時', '三立']
                                grades = {tmp_obj[nowidx].standpoint}
                                nodeId = {'position'}
                                chartType = {1}
                            />
                        </Grid>
                    </Grid>
                    <Grid className={classes.news_block} container justify="center" spacing={3}>
                        {/* <Grid item sm={6}>
                            <h2>重點新聞</h2>
                            <List component="nav" className={classes.list_item} aria-label="mailbox folders">
                                <ListItem button>
                                    <ListItemText primary={tmp_obj[nowidx].focus_news[0]} />
                                </ListItem>
                                <Divider />
                                <ListItem button divider>
                                    <ListItemText primary={tmp_obj[nowidx].focus_news[1]} />
                                </ListItem>
                                <ListItem button>
                                    <ListItemText primary={tmp_obj[nowidx].focus_news[2]} />
                                </ListItem>
                                <Divider light />
                                <ListItem button>
                                    <ListItemText primary={tmp_obj[nowidx].focus_news[3]} />
                                </ListItem>
                            </List>
                        </Grid> */}

                        <Grid item sm={10}>
                            <h2  className={classes.h2_style}>重點新聞</h2>
                            {tmp_obj[nowidx].focus_news.map((obj, index) => {
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
