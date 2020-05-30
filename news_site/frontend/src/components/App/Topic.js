// react lib
import React, { useState } from 'react'
import ReactDOM from 'react-dom'
import { makeStyles } from '@material-ui/core'

const useStyle = makeStyles( {
    background: {
        gridArea: 'topic',
        display: 'flex',
        flexWrap: 'wrap',
        alignContent: 'center',
        justifyContent: 'center',
        boxSizeing: 'border-box',
        width: '90%',
        height: '100%',
        marginLeft: 'auto',
        marginRight: 'auto',
        backgroundColor: 'rgba(48, 71, 94, .3)'
    },
    topic: {
        gridArea: 'topic',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        boxSizeing: 'border-box',
        width: '100%',
        height: '200px',
        fontSize:  "120px",
        fontWeight: 'bold',
        letterSpacing: '10px',
        color: "white",
    },
    description: {
        display: 'flex',
        width: '100%',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'white',
        fontSize: '36px',
        lineHeight: '1.5',
    }
})


export default function Topic(props) {

    const classes = useStyle()
    return (
        <article className={classes.background}>
            <h1
                className={classes.topic}
                data-aos='zoom-in'
                data-aos-delay='300'
                data-aos-duration='500'
            >
                捕聞燈
            </h1>
            <p
                className={classes.description}
                data-aos='zoom-in'
                data-aos-delay='800'
                data-aos-duration='800'
            >
                使用最短的時間
            </p>
            <br/>
            <p
                className={classes.description}
                data-aos='zoom-in'
                data-aos-delay='800'
                data-aos-duration='800'
            >
                從淺到深看到大家都在討論些什麼
            </p>
        </article>
    )
}