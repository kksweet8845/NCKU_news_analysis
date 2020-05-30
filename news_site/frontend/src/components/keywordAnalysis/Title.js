// react lib
import React, { useState } from 'react'
import ReactDOM from 'react-dom'

import { makeStyles } from '@material-ui/core'

const useStyles = makeStyles({
    background: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center', 
        width: "100%",
        height: "100px",
        backgroundColor: "white",
    },
    text: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        width: "200px",
        fontSize: "20px",
        padding: "15px 3px",
        border: "2px solid #888888",
        fontWeight: 'bold',
    },
    textPos: {
        backgroundColor: '#679b9b',
        borderTopLeftRadius: "5px",
        borderBottomLeftRadius: "5px",
        border: '3px solid #679b9b',
        color: 'white',
    },
    textNeg: {
        backgroundColor: 'white',
        borderTopRightRadius: "5px",
        borderBottomRightRadius: "5px",
        border: '3px solid #b21f66',
        borderLeft: 'none',
        color: '#b21f66',
    }
})


export default function Title(props) {
    const classes = useStyles()
    return (
        <article 
            className={classes.background} 
            data-aos='fade-up' 
            data-aos-duration='1000'
        >    
            <h2 className={`${classes.text} ${classes.textPos}`}>正面新聞</h2>
            <h2 className={`${classes.text} ${classes.textNeg}`}>負面新聞</h2>
        </article>
    )
}