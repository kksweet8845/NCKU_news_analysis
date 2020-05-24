// react lib
import React, { useState } from 'react'
import ReactDOM from 'react-dom'

import SentimentChart from './SentimentChart';

import { makeStyles } from '@material-ui/core'

const useStyle = makeStyles( {
    background: {
        display: 'grid',
        width: '100%',
        height: 'auto',
        gridTemplateAreas: `
            't t a a'
            'd e a a'
            'b c f g'`,
        gridTemplateColumns: '22vw 22vw 22vw 22vw',
        gridTemplateRows: '22vw 22vw 22vw',
        justifyContent: 'center',
        gridRowGap: '10px',
        gridColumnGap: '10px',
        marginLeft: 'auto',
        marginRight: 'auto',
    },
    small_topic: {
        gridArea: 'topic',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontSize: '42px',
        fontWeight: '600',
    },
    small_title: {
        gridArea: 'title',
        display: 'flex',
        width: '100%',
        boxSizing: 'border-box',
        paddingLeft: '20px',
        paddingRight: '20px',
        jsutifyContent: 'center',
        alignItems: 'center',
        fontSize: '24px',
        fontWeight: '400',
    },
    small_frame: {
        display: 'grid',
        gridTemplateAreas:`
            'topic'
            'title'`,
        gridTemplateRows: '5fr 5fr',
        backgroundSize: '80%',
        backgroundRepeat: 'no-repeat',
        backgroundPosition: 'center',
        cursor: 'pointer',
    },
    frame: {
        cursor: 'pointer',
        display: 'grid',
    },
    frame_a: {
        gridArea: 'a',
        display: 'grid',
        gridTemplateAreas:`
            '.'
            'topic'
            'title'`,
        gridTemplateRows: '70% 60px auto',
        alignItems: 'flex-end',
        backgroundColor: '#f6e5f5',
        backgroundImage: 'url("/static/img/photo/smiling-woman-wearing-black-sweater.jpg")',
        backgroundRepeat: 'no-repeat',
        backgroundSize: 'cover',
    },
    a_topic: {
        gridArea: 'topic',
        display: 'flex',
        justifyContent: 'left',
        alignItems: 'center',
        width: '80%',
        marginLeft: 'auto',
        marginRight: 'auto',
        height: 'auto',
        fontSize: '60px',
        fontWeight: '600',
        color: 'rgba(245, 123, 81, 1)',
    },
    a_title: {
        gridArea: 'title',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        alignSelf: 'flex-start',
        marginLeft: 'auto',
        marginRight: 'auto',
        width: '90%',
        height: '100px',
        padding: '10px 5%',
        boxSizing: 'border-box',
        borderRadius: '5px',
        lineHeight: '1.2',
        backgroundColor: 'rgba(245, 123, 81, .7)',
        fontSize: '28px',
        fontWeight: '400',
        color: 'white',
    },
    frame_b: {
        gridArea: 'b',
    },
    b_topic: {
        backgroundColor: 'rgba(255, 186, 90, .8)',
        color: '#af460f',
    },
    b_title: {
        backgroundColor: 'rgba(255, 186, 90, .8)',
        color: 'white',
    },
    frame_c: {
        gridArea: 'c',
    },
    c_topic: {
        backgroundColor: 'rgba(50, 130, 184, .6)',
        color: '#0f4c75',
    },
    c_title: {
        backgroundColor: 'rgba(50, 130, 184, .6)',
        color: 'white',
    },
    frame_d: {
        gridArea: 'd',
        backgroundColor: '#f3dfe3',
        backgroundImage: 'url("/static/img/photo/adult-businessman-close-up-corporate.jpg")',
        backgroundRepeat: 'no-repeat',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
    },
    frame_e: {
        display: 'grid',
        gridTemplateAreas:`
            'title'
            'topic'`,
        gridTemplateRows: '6fr 4fr',
        gridArea: 'e',
        backgroundColor: 'rgba(105, 131, 170, .7)',
    },
    e_topic: {
        gridArea: 'topic',
        display: 'flex',
        justifyContent: 'right',
        alignItems: 'center',
        width: '80%',
        marginLeft: 'auto',
        marginRight: 'auto',
        height: 'auto',
        fontSize: '52px',
        fontWeight: '600',
        color: '#204051',
    },
    e_title: {
        gridArea: 'title',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        alignSelf: 'center',
        marginLeft: 'auto',
        marginRight: 'auto',
        width: '90%',
        height: '100px',
        padding: '10px 5%',
        boxSizing: 'border-box',
        borderRadius: '5px',
        lineHeight: '1.2',
        fontSize: '24px',
        fontWeight: '400',
        color: 'white',
    },
    frame_f: {
        gridArea: 'f',
    },
    f_topic: {
        backgroundColor: '#a278b5',
        color: '#381460',
    },
    f_title: {
        backgroundColor: '#a278b5',
        color: 'white',
    },
    frame_g: {
        gridArea: 'g',
    },
    g_topic: {
        backgroundColor: 'rgba(50, 130, 184, .6)',
        color: '#0f4c75',
    },
    g_title: {
        backgroundColor: 'rgba(50, 130, 184, .6)',
        color: 'white',
    },
    topic: {
        gridArea: 't',
        display: 'flex',
        height: '100%',
        width: '100%',
        backgroundColor: 'white',
        fontSize: '80px',
        fontWeight: 'bold',
        justifyContent: 'center',
        alignItems: 'center',
    }
} )

const data = {
    a: {
        topic: '正向',
        title: '屏榮高中陳守心錄取醫學系 盼未來結合興趣回饋部落',
        data: [400, 430, 448, 470, 540, 1200, 1380],
    },
    b: {
        topic: '驚奇',
        title: '北市助攻都會農友 讓農業變有趣又吸睛',
        data: [400, 430, 448, 470, 540, 200, 1380],
    },
    c: {
        topic: '哀傷',
        title: '新冠肺炎燒三個月 來台觀光收益損近千億元',
        data: [400, 430, 448, 1470, 540, 1200, 380],
    },
    e: {
        topic: '負面',
        title: '48公斤「世界最胖山貓」大叔照爆紅 因心臟病死亡',
        data: [400, 430, 448, 470, 540, 1200, 1380],
    },
    f: {
        topic: '開心',
        title: '屏榮高中陳守心錄取醫學系 盼未來結合興趣回饋部落',
        data: [1400, 430, 448, 470, 540, 200, 380],
    },
    g: {
        topic: '憤怒',
        title: '屏榮高中陳守心錄取醫學系 盼未來結合興趣回饋部落',
        data: [400, 430, 1048, 470, 540, 100, 130],
    },
}

export default function News(props) {

    const classes = useStyle()
    const bgLocation = (props.location === 'left')? classes.bgLeft: classes.bgRight;

    const [chartB, setChartB] = useState(false)
    const [chart, setChart] = useState({
        gridArea: 'a',
        show: false,
        data: data.a.data
    })

    return (
        <section
            className={`${classes.background} ${bgLocation}`}
            onMouseEnter={()=>{setChart({gridArea: 'b', show: false, data: data.g.data})}}
        >
            <h2
                className={classes.topic}
                data-aos='flip-left'
                data-aos-duration='1000'
            >
                本週之最
            </h2>
            <section
                className={`${classes.frame} ${classes.frame_a}`}
                data-aos='zoom-in'
                data-aos-delay='1000'
                data-aos-duration='800'
                // onMouseEnter={()=>{setChart({gridArea: 'a', show: true, data: data.a.data})}}
            >
                <h4 className={classes.a_topic}>{data.a.topic}</h4>
                <p className={classes.a_title}>{data.a.title}</p>
            </section>
            <section
                className={`${classes.small_frame} ${classes.frame_b}`}
                data-aos='flip-up'
                data-aos-duration='800'
                onMouseEnter={()=>{setChart({gridArea: 'b', show: true, data: data.b.data})}}
            >
                <h4 className={`${classes.small_topic} ${classes.b_topic}`}>{data.b.topic}</h4>
                <p className={`${classes.small_title} ${classes.b_title}`}>{data.b.title}</p>
            </section>
            <section
                className={`${classes.small_frame} ${classes.frame_c}`}
                data-aos='flip-up'
                data-aos-duration='800'
                onMouseEnter={()=>{setChart({gridArea: 'c', show: true, data: data.c.data})}}
            >
                <h4 className={`${classes.small_topic} ${classes.c_topic}`}>{data.c.topic}</h4>
                <p className={`${classes.small_title} ${classes.c_title}`}>{data.c.title}</p>
            </section>
            <section
                className={`${classes.frame} ${classes.frame_d}`}
                data-aos='zoom-in'
                data-aos-duration='1000'
            ></section>
            <section
                className={`${classes.frame} ${classes.frame_e}`}
                data-aos='zoom-in'
                data-aos-duration='1200'
                onMouseEnter={()=>{setChart({gridArea: 'e', show: true, data: data.e.data})}}
            >
                <h4 className={classes.e_topic}>{data.e.topic}</h4>
                <p className={classes.e_title}>{data.e.title}</p>
            </section>
            <section
                className={`${classes.small_frame} ${classes.frame_f}`}
                data-aos='flip-up'
                data-aos-duration='800'
                onMouseEnter={()=>{setChart({gridArea: 'f', show: true, data: data.f.data})}}
            >
                <h4 className={`${classes.small_topic} ${classes.f_topic}`}>{data.f.topic}</h4>
                <p className={`${classes.small_title} ${classes.f_title}`}>{data.f.title}</p>
            </section>
            <section
                className={`${classes.small_frame} ${classes.frame_g}`}
                data-aos='flip-up'
                data-aos-duration='800'
                onMouseEnter={()=>{setChart({gridArea: 'g', show: true, data: data.g.data})}}
            >
                <h4 className={`${classes.small_topic} ${classes.g_topic}`}>{data.g.topic}</h4>
                <p className={`${classes.small_title} ${classes.g_title}`}>{data.g.title}</p>
            </section>
            <SentimentChart
                gridArea={chart.gridArea}
                show={chart.show}
                data={chart.data}
            />
        </section>
    )
}