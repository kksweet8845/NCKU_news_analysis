// react lib
import React, { useState } from 'react'
import ReactDOM from 'react-dom'

import { makeStyles } from '@material-ui/core'

const useStyle = makeStyles( {
    content: {
        gridArea: 'topic',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        boxSizeing: 'border-box', 
        width: '100%',
        height: '100%',
        fontSize:  "64px",
        fontWeight: 'bold',
        letterSpacing: '10px',
        color: "black",
    },
    most: {
        gridArea: 'most',
    },
    review: {
        gridArea: 'review',
    }
} )


export default function SubtitleButton(props) {
    const classes = useStyle();
    const content = props.content
    const classType = (props.type === 'most')? classes.most : classes.review;

    return (
        <p className={`${classes.content} ${classType}`}>{content}</p>
    )
}