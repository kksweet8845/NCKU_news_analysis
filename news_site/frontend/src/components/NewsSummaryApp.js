import React, { useState } from 'react';
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

    return (
        <main className={classes.background}>
            <NavigationBar brand="新聞回顧"/>
            <section className={classes.intro}>
                <Photo/>
                <Title topic={topic.main}/>
            </section>
            <section className={classes.semantic}>
                <News location='right'/>
            </section>
            <section className={classes.review}>
                <Review/>
            </section>
        </main>
    )
}

ReactDOM.render(<KeywordChoose/>, document.getElementById('app'))
