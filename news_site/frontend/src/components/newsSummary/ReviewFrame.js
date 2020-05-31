// react lib
import React, { useState } from 'react'
import ReactDOM from 'react-dom'
import ReactCSSTransitionGroup from 'react-transition-group'
import Grid from '@material-ui/core/Grid'
import PieChart from '../common/pieChart'
import BarChart from '../common/barChart'

import { makeStyles } from '@material-ui/core'

const useStyle = makeStyles( {
    frame: {
        height: 'auto',
        width: '80%',
        marginLeft: '100px',
        marginBottom: '10px',
        display: 'grid',
        boxSizing: 'border-box',
        borderRadius: '5px',
        border: '5px solid #5eb7b7',
        gridTemplateAreas:`
            'num     keyword'
            'content content'`,
        gridTemplateColumns: '100px 1fr',
        gridTemplateRows: '80px auto',
        transition: 'height 2s',
    },
    frameNum: {
        gridArea: 'num',
        display: 'flex',
        alignSelf: 'center',
        justifyContent: 'center',
        color: '#5eb7b7',
        fontSize: '28px',
        fontWeight: 'bold',
    },
    frameKeyword: {
        gridArea: 'keyword',
        display: 'flex',
        alignSelf: 'center',
        color: '#5eb7b7',
        fontSize: '28px',
        fontWeight: 'bold',
    },
    frameContent: {
        gridArea: 'content',
        display:  'flex',
        justifyContent: 'center',
        flexWrap: 'wrap',
        width: '100%',
        height: 'auto',
    },
    contentSummary: {
        display: 'block',
        fontSize: '20px',
        lineHeight: '1.2',
        fontWeight: '400',
        width: '90%',
        color: 'black',
        marginLeft: 'auto',
        marginRight: 'auto',
        marginBottom: '5px'
    },
    contentReadmore: {
        display: 'flex',
        width: '90%',
        fontSize: '20px',
        fontWeight: '600',
        marginLeft: 'auto',
        marginRight: 'auto',
        marginBottom: '10px',
        justifyContent: 'flex-end',
        padding: '10px',
    },
    contentLink: {
        display: 'block',
        width: '90%',
        marginLeft: 'auto',
        marginRight: 'auto',
        marginTop: '5px',
        marginBottom: '10px'
    },
    linkTitle: {
        display: 'flex',
        width: '200px',
        padding: '10px 5px',
        fontSize: '24px',
        fontWeight: '600',
    },
    linkHref: {
        display: 'block',
        color: 'black',
        fontSize: '20px',
        fontWeight: '400',
        lineHeight: '1.2',
    },
    frameHover: {
        cursor: 'pointer',
    },
    hideContent: {
        display: 'none'
    },
    chartContent: {
        marginTop: '20px',
        width: '80%',
    },
    aligner: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexWrap: 'wrap',
    },
} )

export default function ReviewFrame(props) {

    const classes = useStyle()
    const ref = React.createRef();
    const colorClasses = {
        frame: {
            border: `4px solid ${props.color}`,
            width: `${props.width}`,
        },
        fontColor: {
            color: `${props.color}`,
        },
    }

    const [isExtend, setExtend] = useState(false);
    const extendContent = ()=> {
        setExtend( (isExtend)? false: true )
    }
    const stopPropagation = (e)=>{
        e.stopPropagation();
    }

    const linkDOM = props.links.map((link)=> {
        return <a
                className={classes.linkHref}
                href={`${link.url}`}
                onClick={stopPropagation}
            >
                {link.title}
            </a>
    })

    return (
        <article
            className={`${classes.frame}`}
            style={colorClasses.frame}
            data-aos='fade-right'
            data-aos-easing='linear'
            onClick={extendContent}
        >
            <h4 className={`${classes.frameNum}  ${classes.frameHover}`} style={colorClasses.fontColor} >{props.num}</h4>
            <p className={`${classes.frameKeyword}  ${classes.frameHover}`} style={colorClasses.fontColor}>{props.keyword}</p>
            <section
                className={`${classes.frameContent} ${(isExtend)?'':classes.hideContent}`}
            >
                <p className={`${classes.contentSummary}`}>{props.summary}</p>
                <section className= {`${classes.chartContent}`}>
                    <Grid container justify="center" spacing={1}>
                        <Grid item xs={6}>
                            <BarChart
                                categories = {["TVBS", "Yahoo", "大紀元", "三立", "上報", "中天", "中央社", "中時電子報", "今日新聞", "公視 ", "自由時報", "民視新聞", "風傳媒", "東森EToday", "新頭殼", "聯合新聞網", "蘋果電子報", "華視"]}
                                data = {[44, 55, 41, 67, 22, 43, 44, 55, 41, 67, 22, 43]}
                                height={200}
                            />
                        </Grid>
                        <Grid className={`${classes.aligner}`} item xs={6} align="center" >
                            <Grid item xs={12}>
                                <PieChart
                                    grades = {[4.51, 1, 2.18]}
                                    nodeId = {'position'}
                                    chartType = {0}
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <PieChart
                                    grades = {[3.51, 2]}
                                    nodeId = {'sentiment'}
                                    chartType = {1}
                                />
                            </Grid>
                        </Grid>
                    </Grid>
                </section>
                <article className={classes.contentLink}>
                    <h4 className={`${classes.linkTitle}`} style={colorClasses.fontColor}>新聞連結</h4>
                    {linkDOM}
                </article>
                <p className={`${classes.contentReadmore}`} style={colorClasses.fontColor}>看更多</p>
            </section>
        </article>
    )
}