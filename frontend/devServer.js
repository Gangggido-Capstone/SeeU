// const Bundler = require("parcel-bundler");
// const express = require("express");
// const http = require("http");
// const path = require("path");
// const app = express();

// // const bundlePath = path.join(__dirname, "public", "index.html"); // 정적 파일 경로 설정

// const port = 8082; // devServer.js는 8082 포트에서 동작

// // const bundlePath = "src/components/index.html";

// // const bundler = new Bundler(bundlePath);

// // app.use(bundler.middleware());

// // 헤더 설정
// app.use((req, res, next) => {
//     res.setHeader("Cross-Origin-Opener-Policy", "same-origin");
//     res.setHeader("Cross-Origin-Embedder-Policy", "require-corp");
//     res.setHeader("Cross-Origin-Resource-Policy", "cross-origin");
//     next();
// });

// // 정적 파일 서빙 설정
// app.use(express.static(path.join(__dirname, "public")));

// // React 애플리케이션에 필요한 정적 파일들을 서빙
// app.use(express.static(path.join(__dirname, "public")));

// app.get("/test", (req, res) => {
//     res.sendFile(path.join(__dirname, "public", "seeso.html"));
// });
// const server = http.createServer(app);
// server.listen(port);

// server.on("error", (err) => console.error(err));
// server.on("listening", async () => {
//     console.info("Server is running");
//     console.info(`  NODE_ENV=[${process.env.NODE_ENV}]`);
//     console.info(`  Port=[${port}]`);

//     // 동적 import로 open 모듈 불러오기
//     const open = await import("open").then((module) => module.default);
//     open(`http://localhost:${port}`);
// });

const express = require("express");
const { createProxyMiddleware } = require("http-proxy-middleware");

const app = express();
//res.setHeader("Cross-Origin-Opener-Policy", "same-origin");
// YouTube 프록시 설정
app.use(
    "/proxy/youtube",
    createProxyMiddleware({
        target: "https://www.youtube.com",
        changeOrigin: true,
        pathRewrite: {
            "^/proxy/youtube": "", // 프록시 경로에서 `/proxy/youtube` 부분을 제거
        },
        onProxyReq: (proxyReq, req, res) => {
            // 여기서 추가적인 헤더를 설정할 수 있습니다.
            proxyReq.setHeader("Cross-Origin-Embedder-Policy", "require-corp");
            proxyReq.setHeader("Cross-Origin-Opener-Policy", "same-origin");
        },
    })
);

app.listen(3000, () => {
    console.log("Proxy server is running on http://localhost:3000");
});
