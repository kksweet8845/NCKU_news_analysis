import React, { PureComponent } from 'react'
import { Container } from '@material-ui/core'
import { Paper } from '@material-ui/core'
import Publisher from './Publisher'

//core components
import Card from "components/Card/Card"
import CardBody from "components/Card/CardBody"
import CardHeader from "components/Card/CardHeader"
// chartist
import ChartistGraph from "react-chartist"

const paperStyle = {
    height: '300px',
    width: '100%',
    textAlign: 'center',
}

export class KeyWordContent extends PureComponent {
    render() {

        var data = {
            series: [20,10,30,40]
        }
        var options = {
            donut: true,
            donutWidth: 60,
            donutSolid: true,
            startAngle: 270,
            showLabel: true
        }

        var lineChartData = {
            labels: ["3/1","3/2","3/3","3/4","3/5","3/6","3/7","3/8"],
            series: [
                [5,9,7,8,5,3,5,4]
            ]
        }

        var lineChartOptions = {
            low: 0,
            showArea: true
        }

        let publishers = [
        {
            name: '中天',
            news: ['蔡英文', '誠實中']
        },
        {
            name: '自由時報',
            news: ['蔡一文','誠實中']
        },
        {
            name: '自由時報',
            news: ['蔡一文','誠實中']
        },
        {
            name: '自由時報',
            news: ['蔡一文','誠實中']
        },
        {
            name: '自由時報',
            news: ['蔡一文','誠實中']
        }]
        let color = ["info", "success", "warning", "danger"]
        return (
            <Container maxWidth="lg">
                <Card>
                    <CardHeader color="primary">
                        <h2> 義大利 </h2>
                    </CardHeader>
                    <CardBody>
                        <Container>
                            <ChartistGraph
                                className={"ct-chart"}
                                data={lineChartData}
                                options={lineChartOptions}
                                type={"Line"}
                            />
                        </Container>
                        <Container>
                            {publishers.map((d,i,arr) => {
                                return (
                                    <Publisher
                                        name={d.name}
                                        news={d.news}
                                        color={color[i%4]}
                                    />
                                )
                            })}
                        </Container>
                    </CardBody>
                </Card>
            </Container>
        )
    }
}

export default KeyWordContent
