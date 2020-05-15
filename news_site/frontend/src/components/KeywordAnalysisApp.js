import React, { useState } from 'react'
import ReactDOM from 'react-dom'
import { makeStyles } from '@material-ui/core'

import Topic from './keywordAnalysis/Topic';
import Picture from './keywordAnalysis/Picture';

import NavigationBar from './common/NavigationBar'

const useStyles = makeStyles({
    background: {
        display: "grid",
        height: "100%",
        backgroundColor: "black",
        gridTemplateAreas:`
            "intro"
            "timeline"`,
        gridTemplateRows: '100vh 100vh',
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
        display: "grid",
        gridArea: "timeline",
        height: "100%",
        width: "100%",
        backgroundColor: "green",
        gridTemplateAreas:`
            "topic  picture"
            "charts picture"`,
        gridTemplateColumns: '7fr 3fr',
        gridTemplateRows: '3fr 2fr',       
    }
})

export default function ForeignPubApp(props) {

    const [imgSrc, setImgSrc] = useState('/static/img/photo/covid19.jpg')
    const [topic, setTopic] = useState('新冠肺炎')
    const classes = useStyles();

    return (
        <div className={classes.background} >
            <NavigationBar brand="關鍵字"/>
            <section className={classes.intro}>
                <Topic topic={topic}/>
                <Picture imgSrc={imgSrc}/>
            </section>
            <section className={classes.timeline}>
            </section> 
        </div> 
    )
}

ReactDOM.render(<ForeignPubApp/>, document.getElementById('app'))
