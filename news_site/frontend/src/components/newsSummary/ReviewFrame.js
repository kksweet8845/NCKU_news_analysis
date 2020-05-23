// react lib
import React, { useState } from 'react'
import ReactDOM from 'react-dom'
import ReactCSSTransitionGroup from 'react-transition-group';

import { makeStyles } from '@material-ui/core'

const useStyle = makeStyles( {
    frame: {
        height: 'auto',
        width: '80%',
        marginLeft: '100px',
        marginBottom: '10px',
        display: 'grid',
        boxSizing: 'border-box',
        borderRadius: '5px',
        border: '5px solid #5eb7b7',
        gridTemplateAreas:`
            'num     keyword'
            'content content'`,
        gridTemplateColumns: '100px 1fr',
        gridTemplateRows: '80px auto',
        transition: 'height 2s',
    },
    frameNum: {
        gridArea: 'num',
        display: 'flex',
        alignSelf: 'center',
        justifyContent: 'center',
        color: '#5eb7b7',
        fontSize: '28px',
        fontWeight: 'bold',
    },
    frameKeyword: {
        gridArea: 'keyword',
        display: 'flex',
        alignSelf: 'center',
        color: '#5eb7b7',
        fontSize: '28px',
        fontWeight: 'bold',
    },
    frameHover: {
        cursor: 'pointer',
    },
    frameExtend: {
        height: '500px',
        // transitionProperty: 'height',
        // transitionDuration: '2s',
    }
} )

export default function ReviewFrame(props) {

    const classes = useStyle()
    const colorClasses = {
        frame: {
            border: `4px solid ${props.color}`,
            width: `${props.width}`,
        },
        num: {
            color: `${props.color}`,
        },
        keyword: {
            color: `${props.color}`
        }
    }

    const [isExtend, setExtend] = useState(false);

    return (
        <article
            className={`${classes.frame} ${(isExtend)?classes.frameExtend: ''}`}
            style={colorClasses.frame}
            // data-aos='fade-right'
            // data-aos-easing='linear'
            onClick={() => setExtend((isExtend)? false:true)}
        >
            <h4 className={`${classes.frameNum}  ${classes.frameHover}`} style={colorClasses.num} >{props.num}</h4>
            <p className={`${classes.frameKeyword}  ${classes.frameHover}`} style={colorClasses.keyword}>{props.keyword}</p>
        </article>
    )
}