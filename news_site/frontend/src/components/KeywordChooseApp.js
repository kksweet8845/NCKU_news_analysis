import React, { useState, useEffect } from 'react'
import ReactDOM from 'react-dom'

import Topic from './keywordChoose/Topic';
import Cards from './keywordChoose/Cards';

export default function KeywordChoose(props) {
    const [cardContents, setCardContents] = useState (
            ['新冠肺炎', '美國', '疫苗', '義大利', '測試', '貓咪', '韓國瑜', '小豬', '疫情', '學測', '罷免', '總統']
        )
    const [isFetch, setIsFetch] = useState(false)

    useEffect(() => {
        if(isFetch == false) {
            setIsFetch(true)
            fetch('/analysis/top20Keywords', {
                method: "get",
            })
            .then((res) => {
                return res.json()
            })
            .then((data)=> {
                setCardContents(data);
            })
        }
    });

    const style = {
        'main': {
            height: "100%",
            width:  "100%",
            backgroundColor: "#1C2854",
        },
        'main__cards': {
            height: 'auto',
            width:  '100%',
        }

    }

    return (
        <div className={'main'} style={style.main}>
            <Topic/>
            <Cards cards={cardContents}/>
      </div>
    )
}

ReactDOM.render(<KeywordChoose/>, document.getElementById('app'))
