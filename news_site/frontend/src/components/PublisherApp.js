import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import ReactDOM from 'react-dom'
// core components
import Header from "./frameCom/Header/Header"
import PubCircle from "./publisher/PubCircle"
import PubCloud from './publisher/PubCloud'
import PubContent from "./publisher/PubContent"
// Components
import axios from "axios"
import {
    BrowserRouter as Router,
    HashRouter,
    Switch,
    Route,
    Link,
    useLocation
} from 'react-router-dom'
import {
    TransitionGroup,
    CSSTransition
} from "react-transition-group"
import { CircularProgress, Container, CssBaseline } from '@material-ui/core'

/** Css */
import './css/App.css'




const transformData = (data) => {
    let serializedData = []
    Object.keys(data).map(brand => {
        let news = []
        let num = 0
        Object.keys(data[brand]).map(keyword => {
            news.push({
                keyword: keyword,
                news: data[brand][keyword].news,
                tally: data[brand][keyword].tally
            })

        })


        news.sort((a, b) => {
            return b.tally - a.tally
        })
        news = news.slice(0, 100)
        serializedData.push({
            brand,
            news,
        })
    })
    serializedData = serializedData.sort(function compare(a, b) {
        return b.total - a.total
    })
    return serializedData
}

const instance = axios.create({
    baseURL: 'http://localhost:8000/',
    timeout: 0,
})

const renderPubContent = (ready, data) => {
    console.log('In render ' + ready )
    console.log(data)
    if(data){
        return (
        <Container >
            <ul style={{
                display: 'none'
            }}>
                {
                    data.map( d => {
                        return (
                            <li>
                                <Link
                                to ={`/${d.brand}`}
                                id={`${d.brand}`}
                                >{d.brand}</Link>
                            </li>
                        )
                    })
                }
            </ul>
            <Route exact path="/">
                <PubContent
                    data={data[0]}
                    ready={ready}
                />
            </Route>
            {
                data.map( d => {
                    return (
                        <Route path={`/${d.brand}`}>
                            <PubContent
                                data={d}
                                ready={ready}
                            />
                        </Route>
                    )
                })
            }
        </Container>
        )
    }
}

function PublisherApp(props) {

    let location = useLocation()

    const [ ready, setReady ] = useState(false)
    const [ data, setData ] = useState(null)
    const [ rawData, setRawData ] = useState(null)

    useEffect(() => {
        axios({
            method: 'get',
            url: '/analysis/pubKeyword',
            response: 'json'
        }).then((res) => {
            setData(transformData(res.data))
            setReady(true)
            setRawData(res.data)
        }).catch(err => {
            console.log(err)
        })
    }, [])


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
                <PubCloud
                    data={rawData}
                    ready={ready}
                    id={'pubCloud'}
                    treshold={2}
                />
                <TransitionGroup>
                    <CSSTransition
                        key={location.key}
                        classNames="fade"
                        timeout={300}
                    >
                        <Switch location={location}>
                            {renderPubContent(ready, data)}
                        </Switch>
                    </CSSTransition>
                </TransitionGroup>
            </div>
    )

}





ReactDOM.render(
    <HashRouter>
        <PublisherApp/>
    </HashRouter>, document.getElementById('app'))


