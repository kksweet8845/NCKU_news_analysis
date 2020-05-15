// react lib
import React, { useState } from 'react'
import Button from '@material-ui/core/Button';
import ReactDOM from 'react-dom'

const styles = {
    nav: {
        display: 'flex',
        flexWrap: 'wrap',
        marginLeft: '32px',
        color: '#888888'
    }
}


export default function BreadLink(props) {
    console.log(props.contents)

    const links = props.contents.map((content)=> {
        return <Button color="inherit">{content.name}</Button>
    });

    return (
        <nav style={styles.nav}>  
            {links}
        </nav>
    )
}