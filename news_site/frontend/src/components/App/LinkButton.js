// react lib
import React, { useState } from 'react'
import ReactDOM from 'react-dom'
import { makeStyles } from '@material-ui/core'

const useStyle = makeStyles( {
    linkButton: {
        display: 'flex',
        alignSelf: 'center',
        alignContent: 'center',
        justifyContent: 'center',
        height: '90%',
        width: '32%',
        borderRadius: '5px',
        backgroundSize: '60%',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        cursor: 'pointer',
    },
    buttonTitle: {
        display: 'flex',
        height: 'fit-content',
        width: '200px',
        padding: '20px 5px',
        backgroundColor: 'rgba(246, 238, 223, .78)',
        alignSelf: 'center',
        alignItems: 'center',
        justifyContent: 'center',
        borderRadius: '5px',
        fontSize: '36px',
        fontWeight: 'bold',
        color: '#424874',
    },
    buttonDiscription: {
        display: 'flex',
        height: '100%',
        width: '100%',
        boxSizing: 'border-box',
        padding: '20px 20px',
        backgroundColor: 'rgba(246, 238, 223, .78)',
        alignSelf: 'center',
        alignItems: 'center',
        justifyContent: 'center',
        borderRadius: '5px',
        fontSize: '24px',
        fontWeight: '600',
        color: '#424874',
    },
    hideContent: {
        display: 'none'
    }
})


export default function LinkButton(props) {

    const classes = useStyle()
    const inlineStyle = {
        background: {
            backgroundImage: `url("/static/img/icon/${props.imgSrc}")`,
            backgroundColor: props.backgroundColor,
        },
        content: {
            color: props.fontColor
        }
    }
    const [topic, setTopic] = useState(true)
    const [dicription, setDiscription] = useState(false)

    const showDiscription = ()=>{
        setTopic(false)
        setDiscription(true)
    }

    const hideDiscription = ()=> {
        setTopic(true)
        setDiscription(false)
    }

    return (
        <a
            className={`${classes.linkButton}`}
            style={inlineStyle.background}
            onMouseEnter={showDiscription}
            onMouseLeave={hideDiscription}
            href={`/frontend/${props.category}`}
            data-aos='flip-up'
            data-aos-delay={props.aos_delay}
            data-aos-duration='800'
        >
            <h2
                className={`${classes.buttonTitle} ${(topic)? '': classes.hideContent}`}
                style={inlineStyle.content}
            >
                {props.topic}
            </h2>
            <p
                className={`${classes.buttonDiscription} ${(dicription)? '': classes.hideContent}`}
                style={inlineStyle.content}
            >
                {props.discription}
            </p>
        </a>
    )
}