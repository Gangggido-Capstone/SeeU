const Bundler = require("parcel-bundler");
const express = require("express");
const http = require("http");
const open = require("open");
const app = express();
const cors = require("cors");
const bundlePath = process.argv[2]; // samples/gaze/index.html
const port = process.argv[3]; // 8082
app.use(cors());
app.options("*", cors()); // include before other routes
app.use((req, res, next) => {
    res.setHeader("Cross-Origin-Embedder-Policy", "require-corp");
    res.setHeader("Cross-Origin-Opener-Policy", "same-origin");

    // Add CORS headers
    res.setHeader("Access-Control-Allow-Origin", "*"); // Allow all origins, or specify your origin here
    res.setHeader(
        "Access-Control-Allow-Methods",
        "GET, POST, PUT, DELETE, OPTIONS"
    );
    res.setHeader(
        "Access-Control-Allow-Headers",
        "Content-Type, Authorization"
    );
    // Handle preflight requests
    if (req.method === "OPTIONS") {
        res.sendStatus(200);
    } else {
        next();
    }
});

const bundler = new Bundler(bundlePath);
app.use(bundler.middleware());

const server = http.createServer(app);
server.listen(port);

server.on("error", (err) => console.error(err));
server.on("listening", () => {
    console.info("Server is running");
    console.info(`  NODE_ENV=[${process.env.NODE_ENV}]`);
    console.info(`  Port=[${port}]`);
    open(`http://localhost:${port}`);
});
