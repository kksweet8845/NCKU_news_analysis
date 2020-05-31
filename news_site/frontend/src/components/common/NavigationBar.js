// react lib
import React, { useState } from 'react'
import ReactDOM from 'react-dom'

import Header from '../frameCom/Header/Header'
import BreadLink from './BreadLink'

const linkContents = [
    {
        name: '關鍵字分析',
        link: 'keyword_choose'
    },
    {
        name: '媒體分析',
        link: 'media'
    },
    {
        name: '新聞回顧',
        link: 'news_summary'
    }
]

const backContent = [
    {
        name: '回到主頁',
        link: '/frontend/'
    }
]

export default function NavigationBar(props) {
    let links = <BreadLink contents={linkContents}/>;
    let back_link = <BreadLink contents={backContent}/>;

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
            rightLinks={back_link}
        />
    )
}