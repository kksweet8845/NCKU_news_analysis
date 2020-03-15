import React, { Component } from 'react'
import ReactDom from 'react-dom'
import PropTypes from 'prop-types'
import { makeStyles } from '@material-ui/core/styles'
import { container } from 'assets/jss/material-kit-react.js'

// core componenets
import Header from "./frameCom/Header/Header"
import Parallax from "./frameCom/Parallax/Parallax"
import GridContainer from "./frameCom/Grid/GridContainer"
import GridItem from './frameCom/Grid/GridItem'
import Footer from "./frameCom/Footer/Footer"
import HeaderLinks from "./frameCom/Header/HeaderLinks"
// css components
// import "./css/component.css"
import "assets/scss/material-kit-react.scss"

const useStyles = makeStyles({
    container,
    brand: {
      color: "#FFFFFF",
      textAlign: "left"
    },
    title: {
      fontSize: "4.2rem",
      fontWeight: "600",
      display: "inline-block",
      position: "relative",
      zIndex: "10"
    },
    subtitle: {
      fontSize: "1.313rem",
      maxWidth: "500px",
      margin: "10px 0 0",
      position: "relative",
      zIndex: "10"
    },
    main: {
      background: "#FFFFFF",
      position: "relative",
      zIndex: "3"
    },
    mainRaised: {
      margin: "-60px 30px 0px",
      borderRadius: "6px",
      boxShadow:
        "0 16px 24px 2px rgba(0, 0, 0, 0.14), 0 6px 30px 5px rgba(0, 0, 0, 0.12), 0 8px 10px -5px rgba(0, 0, 0, 0.2)"
    },
    link: {
      textDecoration: "none"
    },
    textCenter: {
      textAlign: "center"
    }
  })


export default function IndexApp(props) {
    const classes = useStyles()
    return (
        <div>
            <Header
                color="transparent"
                rightLinks={<HeaderLinks />}
                brand="News"
                fixed
                changeColorScroll={{
                    height: 400,
                    color: "white"
                }}
            />
            <Parallax filter image={"/static/img/bg4.jpg"}>
                <div className={classes.container}>
                    <GridContainer>
                        <GridItem>
                            <div className={classes.brand}>
                                <h1 className={classes.title}> News Mining </h1>
                                <h3 className={classes.subtitle}> A overall news mining website </h3>
                            </div>
                        </GridItem>
                    </GridContainer>
                </div>
            </Parallax>
            <div className="main mainRaised">

            </div>
        </div>
    )
}


ReactDom.render(<IndexApp/>, document.getElementById("app"))