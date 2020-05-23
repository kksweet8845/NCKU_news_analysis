// react lib
import React, { useState } from 'react'
import ReactDOM from 'react-dom'

import Header from '../frameCom/Header/Header'
import BreadLink from './BreadLink'

const linkContents = [
    {
        name: '關鍵字分析',
    },
    {
        name: '媒體分析',
    },
    {
        name: '新聞回顧'
    }
]


export default function NavigationBar(props) {
    let   links = <BreadLink contents={linkContents}/>;

    return (
        <Header
            color="white"
            brand={props.brand}
            fixed
            changeColorOnScroll={{
                height: 300,
                color: "white"
            }}
            leftLinks={links} 
        />
    )
}