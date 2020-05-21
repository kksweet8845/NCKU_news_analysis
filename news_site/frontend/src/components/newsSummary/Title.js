// react lib
import React, { useState } from 'react'
import ReactDOM from 'react-dom'
import Button from '@material-ui/core/Button';

import { makeStyles } from '@material-ui/core'

const useStyle = makeStyles( {
    title: {
        gridArea: 'title',
        display: 'flex',
        flexWrap: 'wrap',
        alignSelf: 'center',
        justifySelf: 'center',
        boxSizeing: 'border-box', 
        alignContent: 'center',
        width: '70%',
        height: '100%',
    },
    topic: {
        display: 'block',
        width: '100%',
        margin: '10px',
        boxSizeing: 'border-box', 
        textAlign: 'left',
        fontSize:  "100px",
        fontWeight: 'bold',
        letterSpacing: '10px',
        color: "black",
    },
    content: {
        display: 'block',
        width: '100%',
        margin: '10px',
        boxSizeing: 'border-box', 
        fontSize:  "20px",
        fontWeight: '200',
        lineHeight: '28px',
        textAlign:'left',
        color: "black",
    },
    button: {
        display: 'block',
        width: '100%',
        boxSizeing: 'border-box', 
        fontSize:  "24px",
        fontWeight: '200',
        textAlign:'left',
        color: "black",
    }
} )


export default function Title(props) {

    const classes = useStyle()

    return (
        <section className={classes.title}>
            <h1 className={classes.topic}>{props.topic}</h1>
            <p className={classes.content}>
                為您整理出本週報導數最高的主題，搭配數據與當週新聞之最，帶您快速了這個星期到底夯什麼
            </p>
        </section>
    )
}