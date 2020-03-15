import React, { PureComponent } from 'react'
import { Container } from '@material-ui/core'
import { Paper } from '@material-ui/core'
import Publisher from './Publisher'


const paperStyle = {
    height: '300px',
    width: '100%',
    textAlign: 'center',
}

export class KeyWordContent extends PureComponent {
    render() {
        return (
            <Container maxWidth="lg" className="container">
                <div className="inner">
                    <div className="title">
                        <span> 義大利 </span>
                    </div>
                    <Container>
                        <Paper elevation={3} style={paperStyle}>
                            <h1> Graph Area </h1>
                        </Paper>
                    </Container>
                    <Publisher/>
                </div>
            </Container>
        )
    }
}

export default KeyWordContent
