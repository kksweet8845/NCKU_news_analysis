import React, {Component} from 'react'
import ReactDOM from 'react-dom'
import ChooseMenu from './App/choose'
import NewsList from './App/newsList'
import Clould from './App/clould'
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
                <Clould
                    ready={true}
                    data={[{
                        text: '確診',
                        size: 13,
                    },{
                        text: '罷韓',
                        size: 20,
                    },{
                        text: '罷免',
                        size: 28,
                    },{
                        text: '時中',
                        size: 19,
                    },{
                        text: '罷韓',
                        size: 20,
                    },{
                        text: '罷免',
                        size: 28,
                    },{
                        text: '時中',
                        size: 19,
                    },{
                        text: '罷韓',
                        size: 20,
                    },{
                        text: '罷免',
                        size: 28,
                    },{
                        text: '時中',
                        size: 19,
                    },{
                        text: '罷韓',
                        size: 20,
                    },{
                        text: '罷免',
                        size: 28,
                    },{
                        text: '時中',
                        size: 19,
                    },{
                        text: '罷韓',
                        size: 20,
                    },{
                        text: '罷免',
                        size: 28,
                    },{
                        text: '時中',
                        size: 19,
                    },{
                        text: '罷韓',
                        size: 20,
                    },{
                        text: '罷免',
                        size: 28,
                    },{
                        text: '時中',
                        size: 19,
                    },{
                        text: '罷韓',
                        size: 20,
                    },{
                        text: '罷免',
                        size: 28,
                    },{
                        text: '時中',
                        size: 19,
                    },{
                        text: '罷韓',
                        size: 20,
                    },{
                        text: '罷免',
                        size: 28,
                    },{
                        text: '時中',
                        size: 19,
                    },{
                        text: '罷韓',
                        size: 20,
                    },{
                        text: '罷免',
                        size: 28,
                    },{
                        text: '時中',
                        size: 19,
                    },{
                        text: '罷韓',
                        size: 20,
                    },{
                        text: '罷免',
                        size: 28,
                    },{
                        text: '時中',
                        size: 19,
                    },{
                        text: '罷韓',
                        size: 20,
                    },{
                        text: '罷免',
                        size: 28,
                    },{
                        text: '時中',
                        size: 19,
                    },{
                        text: '罷韓',
                        size: 20,
                    },{
                        text: '罷免',
                        size: 28,
                    },{
                        text: '時中',
                        size: 19,
                    }]}
                    id={'clould'}
                />
            </div>
        );
    }
}

ReactDOM.render(<App />, document.getElementById('app'))