import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import { makeStyles } from '@material-ui/core';

import NavigationBar from './common/NavigationBar';
import Photo from './newsSummary/Photo';
import Title from './newsSummary/Title';
import SubTitle from './newsSummary/SubTitle';
import News from './newsSummary/News'

const useStyles = makeStyles({
    background: {
        display: "block",
        height: "auto",
        width: "100vw",
        backgroundColor: "black",
    },
    intro: {
        display: 'grid',
        height: '100vh',
        width: '100vw',
        backgroundColor: 'white',
        gridTemplateAreas: `
            'photo title'`,
        gridTemplateColumns: '1fr 1fr',
    },
    semantic: {
        display: 'grid',
        height: 'auto',
        width: '100vw',
        backgroundColor: 'white',
        gridTemplateAreas: `
            'subtitle .    '
            'news     news '`,
        gridTemplateRows: '200px auto',
        gridTemplateColumns: ' 4fr 4fr ',
    },
    review: {
        display: 'grid',
        height: 'auto',
        width: '100vw',
        backgroundColor: 'white',
        gridTemplateAreas: `
            'subtitle .    '
            'news     news '`,
        gridTemplateRows: '10vh auto',
        gridTemplateColumns: '4fr 4fr',
    },
    news: {
        gridArea: 'news',
        display:　'block',
    }
})

export default function KeywordChoose(props) {
    
    const topic = {
            main: '新聞回顧',
            semantic: '本週之最',
        };
    const classes = useStyles();

    return (
        <main className={classes.background}>
            <NavigationBar brand="新聞回顧"/>
            <section className={classes.intro}>
                <Photo/>
                <Title topic={topic.main}/>
            </section>
            <section className={classes.semantic}>
                {/* <SubTitle topic={topic.semantic}/> */}
                <News location='right'/>
            </section>
        </main>
    )
}

ReactDOM.render(<KeywordChoose/>, document.getElementById('app'))
