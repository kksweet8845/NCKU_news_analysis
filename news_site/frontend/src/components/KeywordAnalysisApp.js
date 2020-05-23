import React, { useState } from 'react'
import ReactDOM from 'react-dom'
import { makeStyles } from '@material-ui/core'

import Topic from './keywordAnalysis/Topic';
import Picture from './keywordAnalysis/Picture';
import Title from './keywordAnalysis/Title';
import Timeline from './keywordAnalysis/Timeline';

import NavigationBar from './common/NavigationBar'

const useStyles = makeStyles({
    background: {
        display: "grid",
        height: "100%",
        width: "100%",
        backgroundColor: "black",
        gridTemplateAreas:`
            "intro"
            "timeline"`,
        gridTemplateRows: '100vh auto',
    },
    intro: {
        display: "grid",
        gridArea: "intro",
        height: "100%",
        width: "100%",
        backgroundColor: "white",
        gridTemplateAreas:`
            "topic  picture"
            "charts picture"`,
        gridTemplateColumns: '6fr 4fr',
        gridTemplateRows: '3fr 2fr',
    },
    timeline: {
        display: "block",
        gridArea: "timeline",
        height: "fix-content",
        width: "100%",
        backgroundColor: "white",
        marginBottom: '5vh',
    }
})

const data = [{
        sentiment: 'pos',
        date: '2020-02-21',
        keyword: '口罩',
        links: [
            '疾管署召開「因應中國不明原因肺炎疫情專家諮詢會議」',
            '政府派專家赴陸訪查'
        ]
    }, {
        sentiment: 'neg',
        date: '2020-03-01',
        keyword: '鑽石公主號',
        links: [
            '中港澳旅客入境需填「入境健康聲明卡」',
            '中國大陸湖北省旅遊疫情升至第三級警告(warning)，民眾避免前往'
        ]
    }, {
        sentiment: 'neg',
        date: '2020-03-13',
        keyword: '美國',
        links: [
            '中港澳旅客入境需填「入境健康聲明卡」',
            '中國大陸湖北省旅遊疫情升至第三級警告(warning)，民眾避免前往'
        ]
    }, {
        sentiment: 'neg',
        date: '2020-03-24',
        keyword: '義大利',
        links: [
            '中港澳旅客入境需填「入境健康聲明卡」',
            '中國大陸湖北省旅遊疫情升至第三級警告(warning)，民眾避免前往'
        ]
    }, {
        sentiment: 'pos',
        date: '2020-03-28',
        keyword: '疫苗',
        links: [
            '中港澳旅客入境需填「入境健康聲明卡」',
            '中國大陸湖北省旅遊疫情升至第三級警告(warning)，民眾避免前往',
            '中國大陸湖北省旅遊疫情升至第三級警告(warning)，民眾避免前往'
        ]
    }]

export default function ForeignPubApp(props) {

    const [imgSrc, setImgSrc] = useState('/static/img/photo/covid19.jpg')
    const [topic, setTopic] = useState('新冠肺炎')
    const classes = useStyles();
    const timelineDOM = data.map(item=>{
        return <Timeline data={item}/>
    })

    return (
        <div className={classes.background} >
            <NavigationBar brand="關鍵字"/>
            <section className={classes.intro}>
                <Topic topic={topic}/>
                <Picture imgSrc={imgSrc}/>
            </section>
            <section className={classes.timeline}>
                <Title/>
                {timelineDOM}
            </section>
        </div>
    )
}

ReactDOM.render(<ForeignPubApp/>, document.getElementById('app'))
