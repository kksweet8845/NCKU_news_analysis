import React, {Component} from 'react'
import ReactDOM from 'react-dom'

/** Component */
import WordCloud from './keyWord/WordCloud'
import KeyWordContent from './keyWord/KeyWordContent'
import Header from "./frameCom/Header/Header"
import axios from "axios"
import {
    BrowserRouter as Router,
    HashRouter,
    Switch,
    Route,
    Link
} from 'react-router-dom'

import { CircularProgress, Container } from '@material-ui/core'

/** Css  */
import './css/App.css'

class KeywordApp extends Component {


    constructor(props) {
        super(props)
        this.state = {
            ready: false,
            data: null,
            rawData: null,
        }

        const instance = axios.create({
            baseURL: 'http://localhost:8000/',
            timeout: 0,
        })
    }

    transformData(data) {
        let serializedData = []
        Object.keys(data).map(keyword => {
            let news = []
            Object.keys(data[keyword]).map(pub => {
                news.push({
                    pubName : pub,
                    news : data[keyword][pub].news,
                    tally : data[keyword][pub].tally
                })
            })
            serializedData.push({
                keyword,
                news,
            })
        })
        console.log(serializedData[0])
        return serializedData
    }


    componentDidMount() {
        axios({
            method: 'get',
            url: '/analysis/keyword',
            response: 'json'
        }).then((res) => {
            this.setState(() => ({
                data: this.transformData(res.data),
                rawData: res.data
            }))
            this.setState({
                ready: true
            })
        }).catch(err=> {
            console.log(err)
        })

    }

    renderKeywordContent() {
        if(this.state.data){
            return (
                <Container>
                    <ul style={{
                        display: 'none'
                    }}>
                    {
                        this.state.data.map( d => {
                            return (
                                <li>
                                    <Link
                                        to={`/${d.keyword}`}
                                        id={`${d.keyword}`}
                                    >{d.keyword}</Link>
                                </li>
                            )
                        })
                    }
                    </ul>
                    <Route exact path="/">
                        <KeyWordContent
                            data={this.state.data[0]}
                            ready={this.state.ready}
                        />
                    </Route>
                    {
                        this.state.data.map( d => {
                            return(
                                <Route path={`/${d.keyword}`}>
                                    <KeyWordContent
                                        data={d}
                                        ready={this.state.ready}
                                    />
                                </Route>
                            )
                        })
                    }
                </Container>
            )
        }
    }

    render() {

        return (
            <HashRouter
                basename={'/'}
                forceRefresh={true}
            >
                <div>
                    <Header
                        color="transparent"
                        brand="關鍵字頁面"
                        fixed
                        changeColorOnScroll={{
                            height: 300,
                            color: "dark"
                        }}
                    />
                    <WordCloud
                        data={this.state.rawData}
                        ready={this.state.ready}
                        id={'keywordCloud'}
                        treshold={1}
                    />
                    <Switch>
                        {this.renderKeywordContent()}
                    </Switch>
                </div>
            </HashRouter>
        )
    }
}

ReactDOM.render(<KeywordApp />, document.getElementById('app'))
