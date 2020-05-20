// react lib
import React, { useState } from 'react'
import ReactDOM from 'react-dom'

import { makeStyles } from '@material-ui/core'

const useStyle = makeStyles( {
    title: {
        gridArea: 'title',
        display: 'grid',
        flexWrap: 'wrap',
        gridTemplateAreas:`
            'background'`,
        alignSelf: 'center',
        boxSizeing: 'border-box', 
        width: '80%',
        height: '80%',
        marginLeft: 'auto',
        marginRight: 'auto',
    },
    image: {
        gridArea: 'background',
        display: 'flex',
        justifySelf: 'flex-start',
        alignSelf: 'flex-start',
        height: 'auto',
        width:  '75%',
        zIndex: '0',
    },
    word: {
        gridArea: 'background',
        display: 'flex',
        flexWrap: 'wrap',
        justifySelf: 'flex-end',
        alignSelf: 'flex-end',
        alignContent: 'center',
        width: '75%',
        height: '60%',
        zIndex: '1',
        backgroundColor: 'rgba(140,203,190,.5)',
    },
    topic: {
        display: 'block',
        width: '100%',
        marginTop: '10px',
        marginBottom: '10px',
        boxSizeing: 'border-box', 
        textAlign: 'center',
        fontSize:  "64px",
        fontWeight: 'bold',
        letterSpacing: '10px',
        color: "black",
    },
    content: {
        display: 'block',
        width: '100%',
        marginTop: '10px',
        boxSizeing: 'border-box', 
        fontSize:  "24px",
        fontWeight: 'bold',
        textAlign:'center',
        color: "#888888",
    }
} )


export default function Title(props) {

    const classes = useStyle()

    return (
        <section className={classes.title}>
            <img className={classes.image} src='/static/img/photo/person-holding-a-newspaper.jpg'/>
            <article className={classes.word}>
                <h1 className={classes.topic}>{props.topic}</h1>
                <p className={classes.content}>
                    看看這個星期大家都在關注什麼議題
                </p>
            </article>
        </section>
    )
}