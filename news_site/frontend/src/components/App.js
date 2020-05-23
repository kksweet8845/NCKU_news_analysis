import React, {Component} from 'react'
import ReactDOM from 'react-dom'
import ChooseMenu from './App/choose'
import NewsList from './App/newsList'
import Clould from './App/clould'
import FrontImg from './App/frontImg'
import {Container} from '@material-ui/core'

import './css/App.css';

class App extends Component {

    render() {
        return (
            <div>
                <FrontImg />
                <ChooseMenu />
                <NewsList />
                <Clould
                    ready={true}
                    data={[{
                        text: '確診',
                        num: 2.5,
                    },{
                        text: '66',
                        num: 2,
                    },{
                        text: '罷韓',
                        num: 0.5,
                    },{
                        text: '罷免',
                        num: 1.5,
                    },{
                        text: '時中',
                        num: 3,
                    }]}
                    id={'clould'}
                />
            </div>
        );
    }
}

ReactDOM.render(<App />, document.getElementById('app'))