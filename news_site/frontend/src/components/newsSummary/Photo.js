// react lib
import React, { useState } from 'react'
import ReactDOM from 'react-dom'
import { makeStyles } from '@material-ui/core'

const useStyles = makeStyles(
    {
        background: {
            gridArea: 'photo',
            display: 'flex',
            alignSelf: 'center',
            justifySelf: 'center',
            position: 'relative',
            marginLeft: '10%',
            width: "90%",
            height: "80%",
            backgroundColor: "white",
        },
        bg_1: {
            display: 'block',
            position: 'absolute',
            top: '0px',
            left: '0px',
            height: '100%',
            width: '80%',
            backgroundColor: '#ccedd2',
            zIndex: 0,
        },
        bg_2: {
            display: 'block',
            position: 'absolute',
            bottom: '0px',
            left: '10%',
            height: '70%',
            width: '60%',
            backgroundColor: '#94d3ac',
            zIndex: 1,
        },
        bg_image: {
            display: 'block',
            position: 'absolute',
            bottom: '0px',
            left: '20%',
            height: 'auto',
            width: '80%',
            zIndex: 2,
        }
    }
)


export default function Photo(props) {
    const imageUrl = '/static/img/photo/person-holding-a-newspaper.jpg'
    const classes = useStyles()
    return (
        <section className={classes.background}>
            <figure 
                class={classes.bg_1}
            ></figure>
            <figure 
                class={classes.bg_2}
            ></figure>
            <img 
                src={imageUrl}
                class={classes.bg_image}
            />
        </section>
    )
}