// react lib
import React, { useState } from 'react'
import ReactDOM from 'react-dom'
import Button from '@material-ui/core/Button';

import { makeStyles } from '@material-ui/core'

const useStyle = makeStyles( {
    background: {
        gridArea: 'news',
        display: 'grid',
        width: '100%',
        height: 'auto',
        gridTemplateAreas: `
            't t a a'
            'b c a a'
            'd e f g'`,
        gridTemplateColumns: '22vw 22vw 22vw 22vw',
        gridTemplateRows: '22vw 22vw 22vw',
        justifyContent: 'center',
        gridRowGap: '10px',
        gridColumnGap: '10px',
        marginLeft: 'auto',
        marginRight: 'auto',
    },
    frame: {
        display: 'grid',
    },
    frame_a: {
        gridArea: 'a',
        backgroundColor: '#f6e5f5',
        backgroundImage: 'url("/static/img/photo/smiling-woman-wearing-black-sweater.jpg")',
        backgroundRepeat: 'no-repeat',
        backgroundSize: 'cover',
        backggroundPosition: 'center',
    },
    frame_b: {
        gridArea: 'b',
        backgroundColor: '#fbf4f9',
    },
    frame_c: {
        gridArea: 'c',
        backgroundColor: '#f6e7e6',
    },
    frame_d: {
        gridArea: 'd',
        backgroundColor: '#f3dfe3',
        backgroundImage: 'url("/static/img/photo/adult-businessman-close-up-corporate.jpg")',
        backgroundRepeat: 'no-repeat',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
    },
    frame_e: {
        gridArea: 'e',
        backgroundColor: '#e1f2fb',
    },
    frame_f: {
        gridArea: 'f',
        backgroundColor: '#f1f9f9',
    },
    frame_g: {
        gridArea: 'g',
        backgroundColor: '#f6e5f5',
    },
    topic: {
        gridArea: 't',
        display: 'flex',
        height: '100%',
        width: '100%',
        backgroundColor: 'white',
        fontSize: '60px',
        fontWeight: 'bold',
        justifyContent: 'center',
        alignItems: 'center',
    }
} )


export default function News(props) {

    const classes = useStyle()
    const bgLocation = (props.location === 'left')? classes.bgLeft: classes.bgRight;

    return (
        <section className={`${classes.background} ${bgLocation}`}>
            <h2 className={classes.topic}>本週之最</h2>
            <section className={`${classes.frame} ${classes.frame_a}`}></section>
            <section className={`${classes.frame} ${classes.frame_b}`}></section>
            <section className={`${classes.frame} ${classes.frame_c}`}></section>
            <section className={`${classes.frame} ${classes.frame_d}`}></section>
            <section className={`${classes.frame} ${classes.frame_e}`}></section>
            <section className={`${classes.frame} ${classes.frame_f}`}></section>
            <section className={`${classes.frame} ${classes.frame_g}`}></section>
        </section>
    )
}