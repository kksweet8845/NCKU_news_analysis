import React, { PureComponent } from 'react'
import { Component } from '@material-ui/core'
import { Paper } from '@material-ui/core'
import { Container } from '@material-ui/core'
import { Grid } from '@material-ui/core'



const paperStyle = {
    width: '100%',
    textAlign: 'center'
}

export class Publisher extends PureComponent {
    render() {
        return (
            <Container className="container">
                <div className="small-title">
                    <span> 中天 </span>
                </div>
                <Grid container spacing={5}>
                    <Grid item xs={4}>
                        <Paper elevation={3} style={paperStyle}>
                            <h1>
                                Sensation Indicator graph
                            </h1>
                        </Paper>
                    </Grid>
                    <Grid item xs={8}>
                        <Paper elevation={3} style={paperStyle}>
                            <h1>
                                News
                            </h1>
                        </Paper>
                    </Grid>
                </Grid>
            </Container>
        )
    }
}

export default Publisher
