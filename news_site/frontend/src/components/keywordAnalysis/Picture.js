// react lib
import React, { useState } from 'react'
import ReactDOM from 'react-dom'
import { makeStyles } from '@material-ui/core'

const useStyles = makeStyles(
    {
        background: {
            gridArea: 'picture',
            display: 'flex',
            position: 'relative',
            width: "100%",
            height: "100%",
            backgroundColor: "white",
        },
        bg_black: {
            display: 'block',
            position: 'absolute',
            top: '0px',
            right: '0px',
            height: '100%',
            width: '75%',
            backgroundColor: 'black',
            zIndex: 0,
        },
        bg_color: {
            display: 'block',
            position: 'absolute',
            bottom: '0px',
            left: '0px',
            height: '45%',
            width: '85%',
            backgroundColor: '#f4a548',
            zIndex: 1,
        },
        bg_image: {
            display: 'block',
            position: 'absolute',
            bottom: '0px',
            left: '0px',
            height: 'auto',
            width: '60%',
            zIndex: 2,
        }
    }
)


export default function Picture(props) {

    const classes = useStyles()
    return (
        <section className={classes.background}>
            <figure 
                class={classes.bg_black}
                data-aos-delay='500'
                data-aos='zoom-in-left'
                data-aos-duration='2000'
            ></figure>
            <figure 
                class={classes.bg_color}
                data-aos='zoom-in-right'
                data-aos-delay='1000'
                data-aos-duration='1500'
            ></figure>
            <img 
                src={props.imgSrc} 
                class={classes.bg_image}
                data-aos='fade-down'
                data-aos-delay='2000'
                data-aos-duration='2000'
            />
        </section>
    )
}