// react lib
import React, { useState } from 'react'
import ReactDOM from 'react-dom'

const styles = {
    topic: {
        gridArea: 'topic',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center', 
        width: "100%",
        height: "100%",
        fontSize:  "64px",
        fontWeight: 'bold',
        letterSpacing: '10px',
        color: "black",
    }
}


export default function Topic(props) {

    return (
        <h1 style={styles.topic}>{props.topic}</h1>
    )
}