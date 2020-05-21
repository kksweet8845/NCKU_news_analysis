import React, { useState } from 'react'
import ReactDOM from 'react-dom'
import { makeStyles } from '@material-ui/core'

import NavigationBar from './common/NavigationBar'
import Photo from './newsSummary/Photo'
import SubtitleButton from './newsSummary/SubtitleButton'
import Title from './newsSummary/Title';

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
        display: 'grid',
        gridArea: 'intro',
        height: '100%',
        width: '100%',
        backgroundColor: 'white',
        gridTemplateAreas: `
            'photo title'`,
        gridTemplateColumns: '1fr 1fr',
        gridTemplateRows: '100vh 1fr'
    }
})

export default function KeywordChoose(props) {
    
    const topic = '新聞回顧';
    const classes = useStyles();

    return (
        <div className={classes.background}>
            <NavigationBar brand="新聞回顧"/>
            <div className={classes.intro}>
                <Photo/>
                <Title topic={topic}/>
                {/* <SubtitleButton content='本週之最' type='most'/>
                <SubtitleButton content='新聞回憶錄' type='review'/> */}
            </div>
        </div>
    )
}

ReactDOM.render(<KeywordChoose/>, document.getElementById('app'))
