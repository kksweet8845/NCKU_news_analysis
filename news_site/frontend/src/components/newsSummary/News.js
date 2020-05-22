// react lib
import React, { useState } from 'react'
import ReactDOM from 'react-dom'
import Button from '@material-ui/core/Button';

import { makeStyles } from '@material-ui/core'

const useStyle = makeStyles( {
    background: {
        gridArea: 'news',
        display: 'grid',
        width: '95%',
        height: '90vh',
        gridTemplateAreas: `
            'a a b b b'
            'c d d d e'
            'f f f g g'`,
        gridTemplateColumns: '3fr 1fr 1fr 2fr 3fr',
        gridTemplateRows: '1fr 1fr 1fr',
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
} )


export default function News(props) {

    const classes = useStyle()
    const bgLocation = (props.location === 'left')? classes.bgLeft: classes.bgRight;

    return (
        <section className={`${classes.background} ${bgLocation}`}>
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