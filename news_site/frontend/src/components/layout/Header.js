import React, { Component } from 'react'
import { AppBar, Toolbar, Typography } from '@material-ui/core'
import { makeStyles } from '@material-ui/core/styles'
import './css/Header.css'
// const useStyle = makeStyles(theme => ({
//     root: {
//         flexGrow: 1,
//     },
//     title: {
//         flexGrow: 1,
//     }
// }))

// const classes = useStyle();

export class Header extends Component {

    render() {
        return (
            <div className="box">
                <AppBar position="static">
                    <Toolbar>
                        <Typography variant="h6">
                            News
                        </Typography>
                    </Toolbar>
                </AppBar>
            </div>
        )
    }
}




export default Header
