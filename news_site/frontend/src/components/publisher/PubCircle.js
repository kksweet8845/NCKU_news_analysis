import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'


import { Container } from '@material-ui/core'
import { Paper } from '@material-ui/core'

const paperStyle = {
    height: '300px',
    width: '100%',
    textAlign: 'center',
}

export default class PubCircle extends PureComponent {
    static propTypes = {

    }

    render() {
        return (
            <Container maxWidth="lg">
                <Paper elevation={3} square style={paperStyle}>
                    <h1> Publisher Circle </h1>
                </Paper>
            </Container>
        )
    }
}
