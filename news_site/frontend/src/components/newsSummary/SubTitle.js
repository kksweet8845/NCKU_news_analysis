// react lib
import React, { useState } from 'react'
import ReactDOM from 'react-dom'
import Button from '@material-ui/core/Button';

import { makeStyles } from '@material-ui/core'

const useStyle = makeStyles( {
    topic: {
        gridArea: 'subtitle',
        display: 'flex',
        width: '100%',
        height: '100%',
        justifyContent: 'center',
        alignItems: 'center',
        fontSize:  "60px",
        fontWeight: 'bold',
        letterSpacing: '10px',
        color: "black",
    },
} )


export default function SubTitle(props) {

    const classes = useStyle()

    return (
        <h2 className={classes.topic}>{props.topic}</h2>
    )
}