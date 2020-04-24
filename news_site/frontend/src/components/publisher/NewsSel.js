import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'

import Card from "components/Card/Card"
import CardBody from "components/Card/CardBody"
import CardHeader from "components/Card/CardHeader"

import dashboardStyle from "assets/jss/material-dashboard-react/views/dashboardStyle.js";
import { makeStyles } from '@material-ui/core'



var styles = {
    ...dashboardStyle,
    cardTitle: {
      marginTop: "0",
      minHeight: "auto",
      fontWeight: "300",
      fontFamily: "'Roboto', 'Helvetica', 'Arial', sans-serif",
      marginBottom: "3px",
      textDecoration: "none"
    },
    relativeKeyword: {
        height: '300px',
        overflowY: 'scroll'
    }
  };

const useStyles = makeStyles(styles)

function NewsSel(props) {

    const classes = useStyles()

    let numOfkeyword = props.news.length
    let news = props.news.map(d => <li>{d}</li>)

    return (
        <Card>
            <CardHeader>
                <h2 className={classes.cardTitle}>{numOfkeyword} 個相關關鍵字 </h2>
            </CardHeader>
            <CardBody className={classes.relativeKeyword}>
                <ul>
                    {news}
                </ul>
            </CardBody>
        </Card>
    )

}

export default NewsSel
