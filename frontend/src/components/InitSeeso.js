import React, { useEffect } from "react";
import "regenerator-runtime/runtime";
import EasySeeSo from "seeso/easy-seeso";
import { showGaze } from "./showGaze.js";

const InitSeeso = () => {
    const licenseKey = process.env.REACT_APP_EYEDID_KEY;

    if (!licenseKey) {
        console.error("환경 변수 REACT_APP_EYEDID_KEY가 설정되지 않았습니다.");
    }
    useEffect(() => {
        const onGaze = (gazeInfo) => {
            showGaze(gazeInfo); // 시선 정보를 화면에 표시
        };

        const onDebug = (FPS, latency_min, latency_max, latency_avg) => {
            // console.log(
            //     `FPS: ${FPS}, Latency: ${latency_min}-${latency_max}ms (Avg: ${latency_avg}ms)`
            // );
        };

        async function initializeSeeso() {
            const seeSo = new EasySeeSo();
            /**
             * set monitor size.    default: 16 inch.
             * set face distance.   default: 30 cm.
             * set camera position. default:
             * camera x: right center
             * cameraOnTop: true
             */
            await seeSo.init(
                licenseKey,
                () => {
                    seeSo.setMonitorSize(16);
                    seeSo.setFaceDistance(50);
                    seeSo.setCameraPosition(window.outerWidth / 2, true);
                    seeSo.startTracking(onGaze, onDebug);
                }, // callback when init succeeded.
                () => console.log("callback when init failed") // callback when init failed.
            );
        }

        initializeSeeso();
    }, []);

    return (
        <div>
            <canvas
                id='output'
                style={{
                    position: "fixed",
                    top: 0,
                    left: 0,
                    width: "100vw",
                    height: "100vh",
                    zIndex: 1, // 시선 추적 캔버스가 가장 아래에 표시되도록 설정
                    pointerEvents: "none",
                }}></canvas>

            <p id='gazeInfo' style={{ textAlign: "center", zIndex: 2 }}>
                시선 추적 중...
            </p>
        </div>
    );
};

export default InitSeeso;