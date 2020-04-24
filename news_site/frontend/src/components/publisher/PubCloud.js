import React, { useState, useEffect } from 'react'
import { Container } from '@material-ui/core'
import { makeStyles } from '@material-ui/core'
import PubCircle from './PubCircle'
import { CircularProgress } from '@material-ui/core'


const svgStyle = {
    height: '800px',
    width: '100%',
    textAlign: 'center',
    overflow: 'scroll',
}


export default function PubCloud(props) {


    return (
        <Container
            maxWidth={false}
            style={{paddingLeft: '0', paddingRight: '0'}}
        >
            <div style={svgStyle} classname="hideScroll">
                <PubCircle
                    ready={props.ready}
                    data={props.data}
                    id={props.id}
                    treshold={props.treshold}
                />
            </div>
        </Container>
    )

}

