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

import Picture from './mediaCom/Picture';

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
        height: "93vh",
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
    }

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
            'focus_news': ['--高雄淹水 王浩宇竟跳出來為韓國瑜說話', '教育部推大學生紓困 網看到全怒：不該當勞工！', '刺胳針》發布陸新冠疫苗試驗：安全且誘導免疫', '農民退休儲金條例通過 蘇揆：農民退休新制月領37K ']
        },
        4: {'name': '三立',
            'news_number': 2000,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': ['1高雄淹水 王浩宇竟跳出來為韓國瑜說話', '2教育部推大學生紓困 網看到全怒：不該當勞工！', '3刺胳針》發布陸新冠疫苗試驗：安全且誘導免疫', '4農民退休儲金條例通過 蘇揆：農民退休新制月領37K ']
        },
        5: {'name': '三立',
            'news_number': 1000,
            'sentiment': [91, 25, 11],
            'standpoint': [25, 74],
            'focus_news': ['3333高雄淹水 王浩宇竟跳出來為韓國瑜說話', '2教育部推大學生紓困 網看到全怒：不該當勞工！', '3刺胳針》發布陸新冠疫苗試驗：安全且誘導免疫', '4農民退休儲金條例通過 蘇揆：農民退休新制月領37K ']
        },
        7: {'name': '三立',
            'news_number': 7,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': ['1高雄淹水 王浩宇竟跳出來為韓國瑜說話', '2教育部推大學生紓困 網看到全怒：不該當勞工！', '3刺胳針》發布陸新冠疫苗試驗：安全且誘導免疫', '4農民退休儲金條例通過 蘇揆：農民退休新制月領37K ']
        },
        8: {'name': '三立',
            'news_number': 8,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': ['1高雄淹水 王浩宇竟跳出來為韓國瑜說話', '2教育部推大學生紓困 網看到全怒：不該當勞工！', '3刺胳針》發布陸新冠疫苗試驗：安全且誘導免疫', '4農民退休儲金條例通過 蘇揆：農民退休新制月領37K ']
        },
        9: {'name': '三立',
            'news_number': 9,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': ['1高雄淹水 王浩宇竟跳出來為韓國瑜說話', '2教育部推大學生紓困 網看到全怒：不該當勞工！', '3刺胳針》發布陸新冠疫苗試驗：安全且誘導免疫', '4農民退休儲金條例通過 蘇揆：農民退休新制月領37K ']
        },
        11: {'name': '三立',
            'news_number': 11,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': ['1高雄淹水 王浩宇竟跳出來為韓國瑜說話', '2教育部推大學生紓困 網看到全怒：不該當勞工！', '3刺胳針》發布陸新冠疫苗試驗：安全且誘導免疫', '4農民退休儲金條例通過 蘇揆：農民退休新制月領37K ']
        },
        12: {'name': '三立',
            'news_number': 12,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': ['1高雄淹水 王浩宇竟跳出來為韓國瑜說話', '2教育部推大學生紓困 網看到全怒：不該當勞工！', '3刺胳針》發布陸新冠疫苗試驗：安全且誘導免疫', '4農民退休儲金條例通過 蘇揆：農民退休新制月領37K ']
        },
        13: {'name': '三立',
            'news_number': 13,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': ['1高雄淹水 王浩宇竟跳出來為韓國瑜說話', '2教育部推大學生紓困 網看到全怒：不該當勞工！', '3刺胳針》發布陸新冠疫苗試驗：安全且誘導免疫', '4農民退休儲金條例通過 蘇揆：農民退休新制月領37K ']
        },
        14: {'name': '三立',
            'news_number': 14,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': ['1高雄淹水 王浩宇竟跳出來為韓國瑜說話', '2教育部推大學生紓困 網看到全怒：不該當勞工！', '3刺胳針》發布陸新冠疫苗試驗：安全且誘導免疫', '4農民退休儲金條例通過 蘇揆：農民退休新制月領37K ']
        },
        15: {'name': '三立',
            'news_number': 15,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': ['1高雄淹水 王浩宇竟跳出來為韓國瑜說話', '2教育部推大學生紓困 網看到全怒：不該當勞工！', '3刺胳針》發布陸新冠疫苗試驗：安全且誘導免疫', '4農民退休儲金條例通過 蘇揆：農民退休新制月領37K ']
        },
        16: {'name': '三立',
            'news_number': 16,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': ['1高雄淹水 王浩宇竟跳出來為韓國瑜說話', '2教育部推大學生紓困 網看到全怒：不該當勞工！', '3刺胳針》發布陸新冠疫苗試驗：安全且誘導免疫', '4農民退休儲金條例通過 蘇揆：農民退休新制月領37K ']
        },
        18: {'name': '三立',
            'news_number': 18,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': ['1高雄淹水 王浩宇竟跳出來為韓國瑜說話', '2教育部推大學生紓困 網看到全怒：不該當勞工！', '3刺胳針》發布陸新冠疫苗試驗：安全且誘導免疫', '4農民退休儲金條例通過 蘇揆：農民退休新制月領37K ']
        },        
    }

    const media_map = {
        1: {'name': 'TVBS', 
            'img': 'https://imgur.com/edI5QMN.png',
            'content': 'TVBS，公司正式名稱為聯利媒體股份有限公司（原名聯意製作股份有限公司），是台灣有線電視頻道經營者之一，為台灣首家衛星電視台。',},
        4: {'name': '三立', 
            'img': 'https://imgur.com/HsDdh8C.png',
            'content': '三立電視股份有限公司（英語：Sanlih E-Television，簡稱：三立電視、三立、SET），是台灣最大型有線電視媒體。',},
        5: {'name': '上報', 
            'img': 'https://imgur.com/98Ec7R0.png',
            'content': '上報（UP Media），是一間臺灣的網路新媒體，由「世代傳媒」集團旗下「上昇整合行銷公司」經營。',},
        7: {'name': '中央社', 
            'img': 'https://imgur.com/uu3KeZh.png',
            'content': '財團法人中央通訊社（英語：Central News Agency，縮寫：CNA），簡稱中央社，是中華民國的國家通訊社',},
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
        window.scrollTo({
            top: document.body.scrollHeight,
            behavior: 'smooth'
        })
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
        ],
    }

    var barChartOptions = {
        // high: 100,
        // low: -15,
        height: '45vh',
        width: '40vw',
        axisX: {
            showGrid: false,
            labelInterpolationFnc: function(value, index) {
                // return index % 2 === 0 ? value : null;
                return value
            }
        },
        axisY: {
            offset: 50,
            showGrid: false,
            // showLabel: false,
            scaleMinSpace: 20,
        },
    }

    var sentimentChartData = {
        labels: ['正面', '中立', '負面'],
        series: tmp_obj[nowidx].sentiment,
    }
    var sentimentChartOptions = {
        height: '20rem',
        width: '20rem',
        donut: true,
        donutWidth: 60,
        donutSolid: true,
        startAngle: 150,
        total: tmp_obj[nowidx].sentiment.reduce((a, b) => a + b, 0),
        showLabel: true,
    }

    var standpointChartData = {
        // labels: ['中時', '三立'],
        series: tmp_obj[nowidx].standpoint,
    }
    var standpointChartOptions = {
        height: '20rem',
        width: '20rem',
        donut: true,
        donutWidth: 60,
        donutSolid: true,
        startAngle: 150,
        total: tmp_obj[nowidx].standpoint.reduce((a, b) => a + b, 0),
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

    return (
        <div>
            <NavigationBar brand="媒體分析"/>
            <Container maxWidth="xl" >
                <div className={classes.head_grid}>
                    <Grid container spacing={1} className={classes.grid_container}>
                        <Grid item sm={6}>
                            <h1 className={classes.head_title}>媒體分析</h1>
                            <ChartistGraph
                                className={"ctbar-chart"}
                                data={barChartData}
                                options={barChartOptions}
                                type={"Bar"}
                            />
                        </Grid>
                        <Grid item sm={6}>
                            <Picture imgSrc={"https://i.imgur.com/nse6KrE.jpeg"}/>
                        </Grid>
                    </Grid>
                </div>
            </Container>
            
            <Container maxWidth="xl" >
                <Slider {...slide_setting}> 
                    {media_index.map((value, index) => (
                        <Paper className={classNames(classes.carousel_grid, chooseColor(index))} onClick={()=>handleClick(value)}>
                            <img src = {media_map[value].img} className={classes.img} />
                            <h1 className={classes.carousel_title}> {media_map[value].name}{value} </h1>
                            {/* <p>{media_map[value].content}</p> */}
                        </Paper>
                    ))}
                </Slider>
            </Container>

            <Container maxWidth="xl">
                <div className={classes.main_grid}>
                    <Grid container spacing={3}>
                        <Grid item sm={12}>
                            <h1> {media_map[nowidx].name} </h1>
                            <h3> 報導篇數: {tmp_obj[nowidx].news_number} 篇 </h3>
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
                                data={standpointChartData}
                                options={standpointChartOptions}
                                type={"Pie"}
                                style={paddings.stand_graph}
                            />
                        </Grid>
                        <Grid item sm={3}/>
                        <Grid item sm={6}>
                            <h2>重點新聞</h2>
                            <List component="nav" className={classes.list_item} aria-label="mailbox folders">
                                <ListItem >
                                    <ListItemText primary={tmp_obj[nowidx].focus_news[0]} />
                                </ListItem>
                                <Divider />
                                <ListItem  divider>
                                    <ListItemText primary={tmp_obj[nowidx].focus_news[1]} />
                                </ListItem>
                                <ListItem >
                                    <ListItemText primary={tmp_obj[nowidx].focus_news[2]} />
                                </ListItem>
                                <Divider light />
                                <ListItem >
                                    <ListItemText primary={tmp_obj[nowidx].focus_news[3]} />
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
