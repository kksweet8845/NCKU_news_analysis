import React, {Component} from 'react'
import ReactDOM from 'react-dom'

/** Component */
import Header from './layout/Header'
import WordCloud from './keyWord/WordCloud'
import KeyWordContent from './keyWord/KeyWordContent'

/** Css  */
import './css/App.css'

class KeywordApp extends Component {
    render() {
        return (
            <div>
                <Header />
                <WordCloud/>
                <KeyWordContent/>
            </div>
        )
    }
}

ReactDOM.render(<KeywordApp />, document.getElementById('app'))
