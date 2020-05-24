// react lib
import React, { useState } from 'react'
import ReactDOM from 'react-dom'

const styles = {
    topic: {
        gridArea: 'topic',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        boxSizeing: 'border-box',
        width: '100%',
        height: '100%',
        fontSize:  "120px",
        fontWeight: 'bold',
        letterSpacing: '10px',
        color: "white",
    }
}


export default function Topic(props) {

    return (
        <h1 style={styles.topic} data-aos='zoom-in'>捕聞燈</h1>
    )
}