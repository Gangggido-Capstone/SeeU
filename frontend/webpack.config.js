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
        path: path.join(__dirname, "dist"), // 빌드하면 만들어질 경로
        filename: "bundle.js", // 파일 이름,
        publicPath: "/",
    },
    devServer: {
        hot: true, // HRM(새로 고침 안해도 변경된 모듈 자동으로 적용)
        port: 9000,
        open: true, // 브라우저 자동 실행 설정
        historyApiFallback: {
            index: "/index.html",
        },

        devMiddleware: {
            publicPath: "/",
        },

        static: {
            watch: true, // 파일 변경을 감지하도록 설정
        },

        setupMiddlewares: (middlewares, devServer) => {
            if (!devServer) {
                throw new Error("webpack-dev-server is not defined");
            }
            devServer.app.use((req, res, next) => {
                if (req.url.startsWith("/seeso")) {
                    res.setHeader(
                        "Cross-Origin-Embedder-Policy",
                        "credentialless"
                    );
                    res.setHeader("Cross-Origin-Opener-Policy", "same-origin");
                } else if (req.url.startsWith("/play-video")) {
                    res.setHeader(
                        "Cross-Origin-Embedder-Policy",
                        "unsafe-none"
                    );
                    res.setHeader("Cross-Origin-Opener-Policy", "same-origin");
                }

                // CORS 관련 헤더 추가
                res.setHeader("Cross-Origin-Resource-Policy", "cross-origin");

                res.setHeader("Access-Control-Allow-Origin", "*");
                res.setHeader(
                    "Access-Control-Allow-Methods",
                    "GET, POST, PUT, DELETE, OPTIONS"
                );
                res.setHeader(
                    "Access-Control-Allow-Headers",
                    "Origin, X-Requested-With, Content-Type, Accept"
                );

                console.log("CORS 및 Cross-Origin 설정이 완료되었습니다.");

                next();
            });

            return middlewares;
        },
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: "./public/index.html",
            inject: true,
        }),
        new webpack.DefinePlugin({
            // 환경 변수 브라우저 환경에 전달
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
        ],
    },
    resolve: {
        extensions: [".js", ".jsx"],
    },
};
