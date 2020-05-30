import React from 'react'
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
    frontImg: {
        backgroundImage: 'url("/static/img/frontImg.jpg")',
        backgroundSize: 'cover',
        width: '100vw',
        height: '90vh'
    },
}))

export default function() {
    const classes = useStyles();
    return (
        <div className={classes.frontImg}></div>
    );
}
