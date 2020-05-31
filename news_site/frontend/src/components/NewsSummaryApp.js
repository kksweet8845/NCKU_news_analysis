import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { makeStyles } from '@material-ui/core';

import NavigationBar from './common/NavigationBar';
import Photo from './newsSummary/Photo';
import Title from './newsSummary/Title';
import News from './newsSummary/News';
import Review from './newsSummary/Review';

const useStyles = makeStyles({
    background: {
        display: "block",
        height: "auto",
        width: "100vw",
    },
    intro: {
        display: 'grid',
        height: '100vh',
        width: '100vw',
        gridTemplateAreas: `
            'photo title'`,
        gridTemplateColumns: '1fr 1fr',
    },
    semantic: {
        display: 'block',
        height: 'auto',
        width: '100vw',
        marginBottom: '50px',
    },
    review: {
        display: 'block',
        height: '100vh',
        width: '100vw',
    },
})

export default function KeywordChoose(props) {

    const topic = {
            main: '新聞回顧',
            semantic: '本週之最',
        };
    const classes = useStyles();

    const [sentiment, setSentiment] = useState({
        a: {
            topic: '正向',
            title: '屏榮高中陳守心錄取醫學系 盼未來結合興趣回饋部落',
            data: [400, 430, 448, 470, 540, 1200, 1380],
        },
        b: {
            topic: '驚奇',
            title: '北市助攻都會農友 讓農業變有趣又吸睛',
            data: [400, 430, 448, 470, 540, 200, 1380],
        },
        c: {
            topic: '哀傷',
            title: '新冠肺炎燒三個月 來台觀光收益損近千億元',
            data: [400, 430, 448, 1470, 540, 1200, 380],
        },
        e: {
            topic: '負面',
            title: '48公斤「世界最胖山貓」大叔照爆紅 因心臟病死亡',
            data: [400, 430, 448, 470, 540, 1200, 1380],
        },
        f: {
            topic: '快樂',
            title: '屏榮高中陳守心錄取醫學系 盼未來結合興趣回饋部落',
            data: [1400, 430, 448, 470, 540, 200, 380],
        },
        g: {
            topic: '憤怒',
            title: '屏榮高中陳守心錄取醫學系 盼未來結合興趣回饋部落',
            data: [400, 430, 1048, 470, 540, 100, 130],
        },
    })

    const [reviewContent, setReviewContent] = useState([
        {
            keyword: '武漢肺炎',
            summary: '新冠肺炎疫情從1月底開始爆發，迄今已延燒近四個月，據內政部移民署最新統計顯示，今年2、3、4月疫情嚴重的時候，來台旅客量逐月驟減，4月份來台旅客數僅2,559人，創下歷史新低量，而三個月來台旅客量較去年同期狂減260.9萬人次，觀光收益減損多達969.3億元。',
            news_num: 60,
            reportNum: [44, 55, 41, 67, 22, 43, 44, 55, 41, 67, 22, 43],
            sentiment: [4.51, 1, 2.18],
            standpoint: [3.51, 2],
            links: [
                {
                    title: '新冠肺炎燒三個月 來台觀光收益損近千億元',
                    url:   'https://www.google.com',
                },
                {
                    title: '蘆洲驚見核能燃料棒輻射量爆表？原能會到場鬆了一口氣',
                    url:   'https://www.google.com',
                },
                {
                    title: '陳時中：樂活長照都顧到 防疫才算成功',
                    url: 'https://www.google.com'
                }
            ]
        },{
            keyword: '美國',
            summary: '新冠肺炎疫情從1月底開始爆發，迄今已延燒近四個月，據內政部移民署最新統計顯示，今年2、3、4月疫情嚴重的時候，來台旅客量逐月驟減，4月份來台旅客數僅2,559人，創下歷史新低量，而三個月來台旅客量較去年同期狂減260.9萬人次，觀光收益減損多達969.3億元。',
            news_num: 55,
            reportNum: [44, 55, 41, 67, 22, 43, 44, 55, 41, 67, 22, 43],
            sentiment: [4.51, 1, 2.18],
            standpoint: [3.51, 2],
            links: [
                {
                    title: '新冠肺炎燒三個月 來台觀光收益損近千億元',
                    url:   'https://www.google.com',
                },
                {
                    title: '蘆洲驚見核能燃料棒輻射量爆表？原能會到場鬆了一口氣',
                    url:   'https://www.google.com',
                },
                {
                    title: '陳時中：樂活長照都顧到 防疫才算成功',
                    url: 'https://www.google.com'
                }
            ]
        },{
            keyword: '義大利',
            summary: '新冠肺炎疫情從1月底開始爆發，迄今已延燒近四個月，據內政部移民署最新統計顯示，今年2、3、4月疫情嚴重的時候，來台旅客量逐月驟減，4月份來台旅客數僅2,559人，創下歷史新低量，而三個月來台旅客量較去年同期狂減260.9萬人次，觀光收益減損多達969.3億元。',
            news_num: 45,
            reportNum: [44, 55, 41, 67, 22, 43, 44, 55, 41, 67, 22, 43],
            sentiment: [4.51, 1, 2.18],
            standpoint: [3.51, 2],
            links: [
                {
                    title: '新冠肺炎燒三個月 來台觀光收益損近千億元',
                    url:   'https://www.google.com',
                },
                {
                    title: '蘆洲驚見核能燃料棒輻射量爆表？原能會到場鬆了一口氣',
                    url:   'https://www.google.com',
                },
                {
                    title: '陳時中：樂活長照都顧到 防疫才算成功',
                    url: 'https://www.google.com'
                }
            ]
        },{
            keyword: '中國',
            summary: '新冠肺炎疫情從1月底開始爆發，迄今已延燒近四個月，據內政部移民署最新統計顯示，今年2、3、4月疫情嚴重的時候，來台旅客量逐月驟減，4月份來台旅客數僅2,559人，創下歷史新低量，而三個月來台旅客量較去年同期狂減260.9萬人次，觀光收益減損多達969.3億元。',
            news_num: 44,
            reportNum: [44, 55, 41, 67, 22, 43, 44, 55, 41, 67, 22, 43],
            sentiment: [4.51, 1, 2.18],
            standpoint: [3.51, 2],
            links: [],
        },{
            keyword: '蔡英文',
            summary: '新冠肺炎疫情從1月底開始爆發，迄今已延燒近四個月，據內政部移民署最新統計顯示，今年2、3、4月疫情嚴重的時候，來台旅客量逐月驟減，4月份來台旅客數僅2,559人，創下歷史新低量，而三個月來台旅客量較去年同期狂減260.9萬人次，觀光收益減損多達969.3億元。',
            news_num: 40,
            reportNum: [44, 55, 41, 67, 22, 43, 44, 55, 41, 67, 22, 43],
            sentiment: [4.51, 1, 2.18],
            standpoint: [3.51, 2],
            links: [],
        },{
            keyword: '香港',
            summary: '新冠肺炎疫情從1月底開始爆發，迄今已延燒近四個月，據內政部移民署最新統計顯示，今年2、3、4月疫情嚴重的時候，來台旅客量逐月驟減，4月份來台旅客數僅2,559人，創下歷史新低量，而三個月來台旅客量較去年同期狂減260.9萬人次，觀光收益減損多達969.3億元。',
            news_num: 35,
            reportNum: [44, 55, 41, 67, 22, 43, 44, 55, 41, 67, 22, 43],
            sentiment: [4.51, 1, 2.18],
            standpoint: [3.51, 2],
            links: [],
        },
    ])

    const [isFetchSentiment, setIsFetchSentiment] = useState(false)
    const [isFetchReview, setIsFetchReview] = useState(false)

    useEffect(() => {
        if(isFetchSentiment == false) {
            fetch('/analysis/sentimentWeek', {
                method: "get",
            })
            .then((res) => {
                return res.json()
            })
            .then((data)=> {
                setSentiment(data);
                setIsFetchSentiment(true)
            })
        }

        if(isFetchReview == false) {
            fetch('/analysis/newsAnalysis', {
                method: "get",
            })
            .then((res) => {
                return res.json()
            })
            .then((data)=> {
                setReviewContent(data);
                setIsFetchReview(true)
            })
        }
    });

    return (
        <main className={classes.background}>
            <NavigationBar brand="新聞回顧"/>
            <section className={classes.intro}>
                <Photo/>
                <Title topic={topic.main}/>
            </section>
            <section className={classes.semantic}>
                <News location='right' sentiment={sentiment}/>
            </section>
            <section className={classes.review}>
                <Review reviewContent={reviewContent}/>
            </section>
        </main>
    )
}

ReactDOM.render(<KeywordChoose/>, document.getElementById('app'))
