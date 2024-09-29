// helper functions to display gaze information and dot in browser.

// show gaze information on screen.
function showGazeInfoOnDom(gazeInfo) {
    let gazeInfoDiv = document.getElementById("gazeInfo");
    if (gazeInfoDiv) {
        // 요소가 존재하는지 확인
        gazeInfoDiv.innerText = `x: ${gazeInfo.x} y: ${gazeInfo.y}`;
    }
    // console.log(gazeInfo.x, gazeInfo.y);
}

// hide gaze information on screen.
function hideGazeInfoOnDom() {
    let gazeInfoDiv = document.getElementById("gazeInfo");
    if (gazeInfoDiv) {
        // 요소가 존재하는지 확인
        gazeInfoDiv.innerText = "";
    }
}

// show gaze dot on screen.
function showGazeDotOnDom(gazeInfo) {
    let canvas = document.getElementById("output");
    if (canvas) {
        // 요소가 존재하는지 확인
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        let ctx = canvas.getContext("2d");
        ctx.fillStyle = "rgba(250, 250, 250, 0.5)";
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.beginPath();
        ctx.arc(gazeInfo.x, gazeInfo.y, 20, 0, Math.PI * 2, true);
        ctx.fill();
    }
}

function hideGazeDotOnDom() {
    let canvas = document.getElementById("output");
    if (canvas) {
        // 요소가 존재하는지 확인
        let ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
}

function showGaze(gazeInfo) {
    showGazeInfoOnDom(gazeInfo);
    showGazeDotOnDom(gazeInfo);
}

function hideGaze() {
    hideGazeInfoOnDom();
    hideGazeDotOnDom();
}

export { showGaze, hideGaze };
