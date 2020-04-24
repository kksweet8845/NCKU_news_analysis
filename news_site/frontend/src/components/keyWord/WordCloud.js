import React, { PureComponent } from 'react'
import { Container } from '@material-ui/core'
import { Paper, makeStyles } from '@material-ui/core'
import WordCircle from './WordCircle'

import { CircularProgress } from '@material-ui/core'

const paperStyle = {
    height: '800px',
    width: '100%',
    textAlign: 'center',
    overflow: 'scroll',
}


const useCircularStyle = makeStyles((theme) => ({
    root: {
        display: 'flex',
        '& > * + *': {
            marginLeft: theme.spacing(2),
          },
    }
}))

function CircularIndeterminate() {
    const classes = useCircularStyle();

    return (
        <div className={classes.root}>
            <CircularProgress />
        </div>
    )
}


export class WordCloud extends PureComponent {

    constructor(props) {
        super(props)
    }

    componentDidUpdate() {
        console.log(this.props.data)
    }


    render() {
        return (
            <Container maxWidth={false} style={{paddingLeft: '0', paddingRIght: '0'}}>
                <div style={paperStyle} className="hideScroll">
                    <WordCircle
                        ready={this.props.ready}
                        data={this.props.data}
                        id={this.props.id}
                        treshold={this.props.treshold}
                    />
                </div>
            </Container>
        )
    }
}

export default WordCloud
