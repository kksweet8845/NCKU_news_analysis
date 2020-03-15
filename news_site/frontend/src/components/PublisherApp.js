import React, { Component } from 'react'
import PropTypes from 'prop-types'
import ReactDOM from 'react-dom'
// core components
import Header from "./frameCom/Header/Header"
import PubCircle from "./publisher/PubCircle"
import PubContent from "./publisher/PubContent"
// Components


function PublisherApp(props) {

    return (
        <div>
            <Header
                color="transparent"
                brand="出版社頁面"
                fixed
                changeColorOnScroll={{
                    height: 300,
                    color: "dark"
                }}
            />
            <PubCircle />
            <PubContent />
        </div>
    )

}


ReactDOM.render(<PublisherApp/>, document.getElementById('app'))


