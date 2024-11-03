const webpack = require("webpack");
const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const dotenv = require("dotenv");

dotenv.config();

module.exports = {
    mode: "development",
    devtool: "cheap-module-source-map",
    entry: {
        app: "./src/index.js",
    },
    output: {
        path: path.join(__dirname, "dist"), // 빌드 경로
        filename: "bundle.js", // 번들 파일 이름
        publicPath: "/",
    },
    devServer: {
        hot: false, // HMR 비활성화
        port: 9000,
        open: true, // 브라우저 자동 실행
        watchFiles: {
            paths: "**/*",
            options: {
                ignored: "**/*",
            },
        },

        headers: {
            "Cross-Origin-Embedder-Policy": "require-corp",
            "Cross-Origin-Opener-Policy": "same-origin",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },

        historyApiFallback: {
            index: "/index.html",
        },

        devMiddleware: {
            publicPath: "/",
            writeToDisk: true, // 디스크에만 기록하고 자동 빌드하지 않음
        },

        static: {
            watch: false, // 정적 파일 감시 비활성화
        },
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: "./public/index.html",
            inject: true,
        }),
        new webpack.DefinePlugin({
            "process.env.REACT_APP_EYEDID_KEY": JSON.stringify(
                process.env.REACT_APP_EYEDID_KEY
            ),
        }),
    ],
    module: {
        rules: [
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: ["@babel/preset-env", "@babel/preset-react"],
                    },
                },
            },
            {
                test: /\.css$/,
                use: ["style-loader", "css-loader"],
            },
            {
                test: /\.svg$/,
                use: "file-loader",
            },
        ],
    },
    resolve: {
        extensions: [".js", ".jsx"],
    },
};