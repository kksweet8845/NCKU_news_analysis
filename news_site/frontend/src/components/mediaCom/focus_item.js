// react lib
import React, { useState } from 'react'
import ReactDOM from 'react-dom'
import { makeStyles } from '@material-ui/core'

const useStyle = makeStyles( {
    frame: {
        height: 'auto',
        width: '80%',
        marginLeft: 'auto',
        marginRight: 'auto',
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
        fontSize: '1.45rem',
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
        marginTop: '0vh',
        marginBottom: '3vh',
        // marginBottom: '10px'
    },
    linkTitle: {
        display: 'flex',
        width: '200px',
        // padding: '10px 5px',
        fontSize: '20px',
        fontWeight: '600',
        marginTop: '0',
    },
    linkHref: {
        display: 'block',
        // color: 'block',
        fontSize: '1.35rem',
        fontWeight: '500',
        lineHeight: '1.2',
        textAlign: 'left',
        textDecoration: 'none',
        color: 'inherit',
        marginBottom: '10px',
        paddingLeft: '40px', 
    },
    frameHover: {
        cursor: 'pointer',
    },
    hideContent: {
        display: 'none'
    }
} )


export default function Focus_item(props) {

    const classes = useStyle()
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
        e.stopPropagation()
    }

    const linkDOM = props.links.map((obj)=> {
        return <a 
                className={classes.linkHref} 
                href={obj.href}
                target="_blank"
                onClick={stopPropagation}>
                {obj.title}
                </a>
    })

    let linkDOM2 = []
    for(const [i, obj] of props.links.entries()){
        if(i>=10){
            break
        }
        linkDOM2.push(<a 
            className={classes.linkHref} 
            href={obj.href}
            target="_blank"
            onClick={stopPropagation}>
            {obj.title}
            </a>)
    }

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
                {/* <p className={`${classes.contentSummary}`}>{props.summary}</p> */}
                <article className={classes.contentLink}>
                    {/* <h4 className={`${classes.linkTitle}`} style={colorClasses.fontColor}>新聞連結</h4> */}
                    {linkDOM2}
                </article>
                {/* <p className={`${classes.contentReadmore}`} style={colorClasses.fontColor}> watch more </p> */}
            </section>
        </article>
    )
}