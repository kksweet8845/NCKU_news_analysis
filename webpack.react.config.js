const path = require('path')
const config = require('./config.js')


const isDevMode = process.env.NODE_ENV === 'development'

const webpackJsConfigTemplate = {
    devtool: isDevMode ? 'inline-sourcemap' : false,
    mode   : isDevMode ? 'development' : 'production',
    target: 'web',
    resolve: {
        alias: {
            'projectRoot': config.projectRoot,
            'assets': path.join(config.projectRoot, 'news_site/frontend/src/assets'),
            'components': path.join(config.projectRoot,'news_site/frontend/src/components/frameCom')
        }
    },
    module : {
        rules: [
            {
                test : /\.js$/,
                exclude: /node_modules/,
                use: [
                    {
                        loader : "babel-loader",
                        options: {
                            cacheDirectory: true,
                            presets: ['@babel/preset-env'],
                            babelrc: true,
                        },
                    }
                ]
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            },
            {
                test: /\.(gif|png|jpe?g|svg)$/,
                use: [
                    'file-loader',
                    {
                        loader: 'image-webpack-loader',
                        options: {
                            disable: true,
                        }
                    }
                ]
            },
            {
                test: /\.s[ac]ss$/,
                use: [
                    'style-loader',
                    'css-loader',
                    'sass-loader',
                ]
            }
        ]
    }
}

const srcRoot = path.join(config.projectRoot, 'news_site/frontend/src')
const srcDis = path.join(config.projectRoot, 'news_site/frontend/static')
const srcJsConfig = Object.assign({}, webpackJsConfigTemplate, {
    entry: {
        'index': path.join(srcRoot, 'index.js'),
        'keyword': path.join(srcRoot, 'keywordPage.js'),
        'publisher': path.join(srcRoot, 'publisherPage.js'),
        'foreign': path.join(srcRoot, 'foreignPubPage.js')
    },
    output: {
        path: srcDis,
        filename: '[name].min.js'
    },
})

module.exports = [
    srcJsConfig
]