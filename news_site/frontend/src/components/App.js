import React, {Component} from 'react'
import ReactDOM from 'react-dom'
import NavigationBar from './common/NavigationBar'

import Topic from './App/Topic';
import { makeStyles } from '@material-ui/core'

import './css/App.css';
import LinkButton from './App/LinkButton';

const useStyle = makeStyles({
    background: {
        display: 'grid',
        gridTemplateAreas:`
            'topic'
            'links'`,
        gridTemplateRows:
            '6fr 4fr',
        height: '100%',
        width: '100%',
        backgroundColor: 'white',
        backgroundImage: 'url("/static/img/photo/coffee-cup-smartphone-notebook.jpg")',
        backgroundSize: '90% 60vh ',
        backgroundRepeat: 'no-repeat',
        backgroundPosition: 'top',
        filter: 'grayscale(30%)'
    },
    topic: {
        gridArea: 'topic',
    },
    links: {
        gridArea: 'links',
        display: 'flex',
        width: '90%',
        height: '100%',
        justifySelf: 'center',
        justifyContent: 'space-between',
        alignContent: 'center',
    },
})

export default function App(props) {
    const classes = useStyle();

    const buttonInfo = [
        {
            imgSrc: 'index_button1.png',
            backgroundColor: '#b590ca',
            fontColor: '#7f78d2',
            topic: '關鍵字分析',
            discription: '用時間軸帶您深度了解時事議題',
            category: 'keyword_choose'
        },{
            imgSrc: 'index_button2.png',
            backgroundColor: '#a8d3da',
            fontColor: '#0c7b93',
            topic: '媒體分析',
            discription: '用數據呈現各家媒體的立場',
            category: 'media'
        }, {
            imgSrc: 'index_button3.png',
            backgroundColor: '#f5cab3',
            fontColor: '#cd8d7b',
            topic: '新聞回顧',
            discription: '為您整理最近大家關注什麼議題',
            category: 'news_summary'
        },
    ]

    const linkDOM = buttonInfo.map((obj, index)=>{
        return <LinkButton
                    imgSrc={obj.imgSrc}
                    backgroundColor={obj.backgroundColor}
                    fontColor={obj.fontColor}
                    topic={obj.topic}
                    discription={obj.discription}
                    category={obj.category}
                    aos_delay={1600+index*500}
                />
    })
    return (
        <main className={classes.background}>
            <Topic topic='捕聞燈'/>
            <section className={classes.links}>
                {linkDOM}
            </section>
        </main>
    );
}

ReactDOM.render(<App />, document.getElementById('app'))