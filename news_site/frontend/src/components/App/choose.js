import React from 'react'
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';
import Box from '@material-ui/core/Box';
import { shadows, borders } from '@material-ui/system';

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    control: {
        padding: theme.spacing(2),
        textAlign: 'center',
    },
    paper: {
        transition: theme.transitions.create("all", {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen
        }),
        height: '30vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'black',
        fontSize: '3em',
        color: 'white',
        position: 'relative',
        top: '-20vh',
        borderColor: 'white',
    },
    whiteImg: {
        backgroundImage: 'url("/static/img/white.jpg")',
    },
    greenImg: {
        backgroundImage: 'url("/static/img/green.jpg")',
        backgroundSize: 'cover',
    },
    list: {
        marginTop: 'auto',
        height: '40vh',
    },
    wordBackground: {
        backgroundColor: 'blue',
        opacity: 0.5,
    },
}))

const toggleHover = (event) => {
	console.log(event.target)
}

export default function() {
    const classes = useStyles();
    return (
        <div>
            <Grid container className={classes.root} justify='center' spacing={2}>
                <Grid item xs={3}>
                    <Box data-aos="zoom-in" className={[classes.paper, classes.whiteImg]} border={1} boxShadow={3} onMouseEnter={toggleHover} onMouseLeave={toggleHover}>
                        <span className={classes.wordBackground}>關鍵字分析</span>
                    </Box>
                </Grid>
                <Grid item xs={3}>
                    <Box data-aos="zoom-in" className={[classes.paper, classes.greenImg]} border={1} boxShadow={3} onMouseEnter={toggleHover} onMouseLeave={toggleHover}>新聞分析</Box>
                </Grid>
                <Grid item xs={3}>
                    <Box data-aos="zoom-in" className={[classes.paper]} border={1} boxShadow={3} onMouseEnter={toggleHover} onMouseLeave={toggleHover}>媒體回顧</Box>
                </Grid>
            </Grid>
        </div>
    );
}
