// react lib
import React, { useState } from 'react'
import ReactDOM from 'react-dom'

const styles = {
    topic: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center', 
        width: "100%",
        height: "30%",
        fontSize:  "32px",
        color: "white",
    }
}


export default function Topic(props) {
    const [topic, setTopic] = useState('請選擇關鍵字');

    return (
        <h1 style={styles.topic}>{topic}</h1>
    )
}