import "regenerator-runtime/runtime";
import EasySeeSo from "seeso/easy-seeso";
import { showGaze } from "../showGaze";

const licenseKey = process.env.EYEDID_KEY; // Issue license key! -> https://console.seeso.io
const seeSo = new EasySeeSo();
// gaze callback.
function onGaze(gazeInfo) {
    // do something with gaze info.
    showGaze(gazeInfo);
}

// debug callback.
function onDebug(FPS, latency_min, latency_max, latency_avg) {
    // do something with debug info.
}
function onFace(faceInfo) {
    // console.log(`Face score: ${faceInfo.score}`);
    // console.log(
    //     `Face position: (${faceInfo.left}, ${faceInfo.top}) - (${faceInfo.right}, ${faceInfo.bottom})`
    // );
}

function onAttention(timestampBegin, timestampEnd, score) {}

async function main() {
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
            seeSo.onAttention = 1;
            seeSo.setMonitorSize(16);
            seeSo.setFaceDistance(50);
            seeSo.setFaceCallback(onFace);
            seeSo.setCameraPosition(window.outerWidth / 2, true);
            seeSo.setAttentionInterval(10);
            seeSo.startTracking(onGaze, onDebug);
        }, // callback when init succeeded.
        () => console.log("callback when init failed") // callback when init failed.
    );
}

(async () => {
    await main();
    const interval = setInterval(() => {
        const attentionScore = seeSo.getAttentionScore();
        console.log(`Attention Score: ${attentionScore}`);
    }, 1000); // 1초마다 attention score 불러옴
})();
