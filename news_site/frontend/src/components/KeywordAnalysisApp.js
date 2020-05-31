import React, { useState, useEffect } from 'react'
import ReactDOM from 'react-dom'
import { makeStyles } from '@material-ui/core'

import Topic from './keywordAnalysis/Topic';
import Picture from './keywordAnalysis/Picture';
import Title from './keywordAnalysis/Title';
import Timeline from './keywordAnalysis/Timeline';
import Clould from './App/clould'

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

// const data = [{
//         sentiment: 'pos',
//         date: '2020-02-21',
//         keyword: '口罩',
//         posLinks: [
//             '疾管署召開「因應中國不明原因肺炎疫情專家諮詢會議」POS',
//             '政府派專家赴陸訪查 POS',
//             '疾管署召開「因應中國不明原因肺炎疫情專家諮詢會議」POS',
//             '政府派專家赴陸訪查 POS',
//         ],
//         negLinks: [
//             '疾管署召開「因應中國不明原因肺炎疫情專家諮詢會議」NEG',
//             '政府派專家赴陸訪查NEG',
//             '中國大陸湖北省旅遊疫情升至第三級警告(warning)，民眾避免前往',
//         ]
//     }, {
//         sentiment: 'neg',
//         date: '2020-03-01',
//         keyword: '鑽石公主號',
//         posLinks: [],
//         negLinks: [
//             '疾管署召開「因應中國不明原因肺炎疫情專家諮詢會議」NEG',
//             '政府派專家赴陸訪查NEG'
//         ]
//     }, {
//         sentiment: 'neg',
//         date: '2020-03-13',
//         keyword: '美國',
//         posLinks: [],
//         negLinks: [
//             '疾管署召開「因應中國不明原因肺炎疫情專家諮詢會議」NEG',
//             '政府派專家赴陸訪查NEG'
//         ]
//     }, {
//         sentiment: 'neg',
//         date: '2020-03-24',
//         keyword: '義大利',
//         posLinks: [
//             '疾管署召開「因應中國不明原因肺炎疫情專家諮詢會議」POS',
//             '政府派專家赴陸訪查 POS'
//         ],
//         negLinks: []
//     }, {
//         sentiment: 'pos',
//         date: '2020-03-28',
//         keyword: '疫苗',
//         posLinks: [
//             '疾管署召開「因應中國不明原因肺炎疫情專家諮詢會議」POS',
//             '政府派專家赴陸訪查 POS'
//         ],
//         negLinks: [
//             '疾管署召開「因應中國不明原因肺炎疫情專家諮詢會議」NEG',
//             '政府派專家赴陸訪查NEG'
//         ]
//     }]
// const wordCloudData = [{
//     text: '罷韓',
//     size: 67,
// },{
//     text: '罷免',
//     size: 54,
// },{
//     text: '時中',
//     size: 81,
// },{
//     text: '罷韓',
//     size: 61,
// },{
//     text: '罷免',
//     size: 92,
// },{
//     text: '時中',
//     size: 61,
// },{
//     text: '罷韓',
//     size: 80,
// },{
//     text: '罷免',
//     size: 61,
// },{
//     text: '時中',
//     size: 90,
// },{
//     text: '罷韓',
//     size: 60,
// },{
//     text: '罷免',
//     size: 81,
// },{
//     text: '時中',
//     size: 65,
// },{
//     text: '罷韓',
//     size: 48,
// },{
//     text: '罷免',
//     size: 55,
// },{
//     text: '時中',
//     size: 66,
// },{
//     text: '罷韓',
//     size: 56,
// },{
//     text: '罷免',
//     size: 71,
// },{
//     text: '時中',
//     size: 65,
// },{
//     text: '罷韓',
//     size: 89,
// },{
//     text: '罷免',
//     size: 67,
// },{
//     text: '時中',
//     size: 75,
// },{
//     text: '罷韓',
//     size: 61,
// },{
//     text: '罷免',
//     size: 55,
// },{
//     text: '時中',
//     size: 70,
// },{
//     text: '罷韓',
//     size: 60,
// },{
//     text: '罷免',
//     size: 50,
// },{
//     text: '時中',
//     size: 40,
// }]

export default function ForeignPubApp(props) {
    const [imgSrc, setImgSrc] = useState('/static/img/photo/covid19.jpg')
    const [topic, setTopic] = useState(window.location.pathname.split('/')[3])
    const [wordCloudData, setWordCloudData] = useState([])
    const [timelineData, setTimelineData] = useState([])

    const [isFetchWordcloud, setIsFetchWordcloud] = useState(false)
    const [isFetchTimeline, setIsFetchTimeline] = useState(false)

    useEffect(() => {
        if(isFetchWordcloud == false) {
            fetch(`/analysis/relativeKeyword/${topic}`, {
                method: "get",
            })
            .then((res) => {
                return res.json()
            })
            .then((data)=> {
                setIsFetchWordcloud(true)
                setWordCloudData(data);
            })
        }

        if(isFetchTimeline == false) {
            fetch(`/analysis/keywordAnalysis/${topic}`, {
                method: "get",
            })
            .then((res) => {
                return res.json()
            })
            .then((data)=> {
                setIsFetchTimeline(true)
                setTimelineData(data);
            })
        }
    });

    const classes = useStyles();
    const timelineDOM = timelineData.map(item=>{
        return <Timeline data={item}/>
    })

    return (
        <div className={classes.background} >
            <NavigationBar brand="關鍵字分析"/>
            <section className={classes.intro}>
                <Topic topic={topic}/>
                <Clould
                    ready={true}
                    data={wordCloudData}
                    id={'clould'}
                />
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
