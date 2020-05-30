// react lib
import React, { useState } from 'react'
import ReactDOM from 'react-dom';
import Button from '@material-ui/core/Button';

import { makeStyles } from '@material-ui/core';
import ReviewFrame from './ReviewFrame';

const useStyle = makeStyles( {
    background: {
        marginTop: '50px',
        display: 'block',
        height: 'auto',
        width: '100%',
    },
    topic: {
        display: 'block',
        width: '80%',
        height: 'auto',
        marginLeft: 'auto',
        marginRight: 'auto',
        marginBottom: '50px',
        boxSizing: 'border-box',
        textAlign: 'right',
        fontSize:  "80px",
        fontWeight: 'bold',
        letterSpacing: '10px',
        color: "black",
    },
    frame: {
        height: 'auto',
        width: '80%',
        marginLeft: '100px',
        display: 'grid',
        boxSizing: 'border-box',
        borderRadius: '5px',
        border: '5px solid #5eb7b7',
        gridTemplateAreas:`
            'num     keyword'
            'content content'`,
        gridTemplateColumns: '100px 1fr',
        gridTemplateRows: '80px auto',
    },
    frameNum: {
        gridArea: 'num',
        display: 'flex',
        alignSelf: 'center',
        justifyContent: 'center',
        color: '#5eb7b7',
        fontSize: '32px',
        fontWeight: 'bold',
    },
    frameKeyword: {
        gridArea: 'keyword',
        display: 'flex',
        alignSelf: 'center',
        color: '#5eb7b7',
        fontSize: '32px',
        fontWeight: 'bold',
    }
} )

const reviewContent = [
    {
        keyword: '武漢肺炎',
        summary: '新冠肺炎疫情從1月底開始爆發，迄今已延燒近四個月，據內政部移民署最新統計顯示，今年2、3、4月疫情嚴重的時候，來台旅客量逐月驟減，4月份來台旅客數僅2,559人，創下歷史新低量，而三個月來台旅客量較去年同期狂減260.9萬人次，觀光收益減損多達969.3億元。',
        news_num: 60,
        links: [
            '新冠肺炎燒三個月 來台觀光收益損近千億元',
            '蘆洲驚見核能燃料棒輻射量爆表？原能會到場鬆了一口氣',
            '陳時中：樂活長照都顧到 防疫才算成功',
        ]
    },{
        keyword: '美國',
        summary: '新冠肺炎疫情從1月底開始爆發，迄今已延燒近四個月，據內政部移民署最新統計顯示，今年2、3、4月疫情嚴重的時候，來台旅客量逐月驟減，4月份來台旅客數僅2,559人，創下歷史新低量，而三個月來台旅客量較去年同期狂減260.9萬人次，觀光收益減損多達969.3億元。',
        news_num: 55,
        links: [
            '新冠肺炎燒三個月 來台觀光收益損近千億元',
            '蘆洲驚見核能燃料棒輻射量爆表？原能會到場鬆了一口氣',
            '陳時中：樂活長照都顧到 防疫才算成功',
        ]
    },{
        keyword: '義大利',
        summary: '新冠肺炎疫情從1月底開始爆發，迄今已延燒近四個月，據內政部移民署最新統計顯示，今年2、3、4月疫情嚴重的時候，來台旅客量逐月驟減，4月份來台旅客數僅2,559人，創下歷史新低量，而三個月來台旅客量較去年同期狂減260.9萬人次，觀光收益減損多達969.3億元。',
        news_num: 45,
        links: [
            '新冠肺炎燒三個月 來台觀光收益損近千億元',
            '蘆洲驚見核能燃料棒輻射量爆表？原能會到場鬆了一口氣',
            '陳時中：樂活長照都顧到 防疫才算成功',
        ]
    },{
        keyword: '中國',
        summary: '新冠肺炎疫情從1月底開始爆發，迄今已延燒近四個月，據內政部移民署最新統計顯示，今年2、3、4月疫情嚴重的時候，來台旅客量逐月驟減，4月份來台旅客數僅2,559人，創下歷史新低量，而三個月來台旅客量較去年同期狂減260.9萬人次，觀光收益減損多達969.3億元。',
        news_num: 44,
        links: [],
    },{
        keyword: '蔡英文',
        summary: '新冠肺炎疫情從1月底開始爆發，迄今已延燒近四個月，據內政部移民署最新統計顯示，今年2、3、4月疫情嚴重的時候，來台旅客量逐月驟減，4月份來台旅客數僅2,559人，創下歷史新低量，而三個月來台旅客量較去年同期狂減260.9萬人次，觀光收益減損多達969.3億元。',
        news_num: 40,
        links: [],
    },{
        keyword: '香港',
        summary: '新冠肺炎疫情從1月底開始爆發，迄今已延燒近四個月，據內政部移民署最新統計顯示，今年2、3、4月疫情嚴重的時候，來台旅客量逐月驟減，4月份來台旅客數僅2,559人，創下歷史新低量，而三個月來台旅客量較去年同期狂減260.9萬人次，觀光收益減損多達969.3億元。',
        news_num: 35,
        links: [],
    },
]


export default function Review(props) {

    const classes = useStyle()
    const colorReview = ['#39375b', '#745c97', '#4b8e8d', '#396362'];
    const widthReview = ['60%', '66%', '71%', '76%', '80%', '75%', '70%', '65%'];

    const content = reviewContent.map((obj, index)=>{
        return  <ReviewFrame
                    color= {colorReview[index%4]}
                    num= {index + 1}
                    keyword= {obj.keyword}
                    summary= {obj.summary}
                    links={obj.links}
                    width= {`${50 + (obj.news_num/reviewContent[0].news_num) * 40}%`}>
                </ReviewFrame>
    })

    return (
        <section className={classes.background}>
            <h1
                className={classes.topic}
                data-aos='fade-left'
            >
                新聞回憶錄
            </h1>
            {content}
        </section>
    )
}