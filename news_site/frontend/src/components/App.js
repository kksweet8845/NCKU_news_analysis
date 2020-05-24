import React, {Component} from 'react'
import ReactDOM from 'react-dom'
import ChooseMenu from './App/choose'
import NewsList from './App/newsList'
import FrontImg from './App/frontImg'
import {Container} from '@material-ui/core'
import NavigationBar from './common/NavigationBar'

import Topic from './App/Topic';
import { makeStyles } from '@material-ui/core'

import './css/App.css';

const useStyle = makeStyles({
    background: {
        display: 'grid',
        gridTemplateAreas:`
            'topic'
            'links'`,
        gridTemplateRows:
            '1fr 1fr',
        height: '100%',
        width: '100%',
        backgroundColor: 'white',
        backgroundImage: 'url("/static/img/photo/coffee-cup-smartphone-notebook.jpg")',
        backgroundSize: '90% 50vh ',
        backgroundRepeat: 'no-repeat',
        backgroundPosition: 'top',
        filter: 'grayscale(30%)'
    },
    topic: {
        gridArea: 'topic',
    },
    links: {
        gridArea: 'links',
        display: 'flex',
        width: '90%',
        height: '100%',
        justifySelf: 'center',
        justifyContent: 'space-between',
        alignContent: 'center',
    },
    linkButton: {
        display: 'flex',
        alignSelf: 'center',
        height: '90%',
        width: '32%',
        borderRadius: '5px',
        backgroundColor: 'rgba(77, 62, 62, .7)'
    },
})

export default function App(props) {
    const classes = useStyle();
    return (
        <main className={classes.background}>
            <Topic topic='捕聞燈'/>
            <section className={classes.links}>
                <article className={`${classes.linkButton}`}>
                    <h2>新聞分析</h2>
                </article>
                <article className={`${classes.linkButton}`}>
                    <h2>媒體分析</h2>
                </article>
                <article className={`${classes.linkButton}`}>
                    <h2>新聞回顧</h2>
                </article>
            </section>
            {/* <NavigationBar /> */}
        </main>
    );
}

// class App extends Component {
//     const classes = useStyle();

//     render() {
//         return (
//             <main cl>
//                 {/* <NavigationBar /> */}
//                 {/* <FrontImg />
//                 <ChooseMenu />
//                 <NewsList /> */}
//             </main>
//         );
//     }
// }

ReactDOM.render(<App />, document.getElementById('app'))