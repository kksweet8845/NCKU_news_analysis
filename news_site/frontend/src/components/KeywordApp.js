import React, {Component} from 'react'
import ReactDOM from 'react-dom'

/** Component */
import WordCloud from './keyWord/WordCloud'
import KeyWordContent from './keyWord/KeyWordContent'
import Header from "./frameCom/Header/Header"
/** Css  */
import './css/App.css'

class KeywordApp extends Component {
    render() {
        return (
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
                <WordCloud/>
                <KeyWordContent/>
            </div>
        )
    }
}

ReactDOM.render(<KeywordApp />, document.getElementById('app'))
