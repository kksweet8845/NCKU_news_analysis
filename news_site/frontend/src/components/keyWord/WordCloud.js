import React, { PureComponent } from 'react'
import { Container } from '@material-ui/core'
import { Paper } from '@material-ui/core'


const paperStyle = {
    height: '300px',
    width: '100%',
    textAlign: 'center',
}


export class WordCloud extends PureComponent {
    render() {
        return (
            <Container maxWidth="lg">
                <Paper elevation={3} square style={paperStyle}>
                    <h1>Word Cloud</h1>
                    <div id="wordClould"></div>
                </Paper>
            </Container>
        )
    }
}

export default WordCloud
