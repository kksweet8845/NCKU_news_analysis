import React, {Component} from 'react'
import ReactDOM from 'react-dom'
import ChooseMenu from './App/choose'
import NewsList from './App/newsList'
import FrontImg from './App/frontImg'
import {Container} from '@material-ui/core'
import NavigationBar from './common/NavigationBar'

import './css/App.css';

class App extends Component {

    render() {
        return (
            <div>
                <NavigationBar />
                <FrontImg />
                <ChooseMenu />
                <NewsList />
            </div>
        );
    }
}

ReactDOM.render(<App />, document.getElementById('app'))