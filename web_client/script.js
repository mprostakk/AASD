const ws = new WebSocket('ws://127.0.0.1:9007');

var agentMap = {}

ws.onmessage = ({data}) => {
    var data = JSON.parse(data);
    agentMap[data.id] = data;
};

function cleanerAgentStateToColor(state) {
    if (state == "HANDLE_CLEAN") {
        return [0, 0, 255];
    }
    else if (state == "PATROL") {
        return [0, 255, 0];
    }
    else if (state == "DRIVING_TO_DESTINATION") {
        return [255, 0, 0];
    }
    else {
        return [100, 100, 100]
    }
 }

 function guardAgentStateToColor(state) {
    if (state == "PATROL") {
        return [0, 255, 0];
    }
    else {
        return [100, 100, 100]
    }
 }

  function guideAgentStateToColor(state) {
    if (state == "WAITING") {
        return [255, 0, 255];
    }
    else if (state == "DRIVING_TO_SOURCE") {
        return [120, 255, 120];
    }
    else if (state == "GUIDING_TO_DESTINATION") {
        return [255, 0, 0];
    }
    else {
        return [100, 100, 100];
    }
 }


function setup() {
    createCanvas(2200, 1200);
}

function draw() {
    background(51);
    fill(color(42, 141, 184));
    rect(0, 0, 1200, 1200);
    fill(color(182, 191, 61));
    rect(1200, 0, 1000, 700);
    fill(color(168, 44, 44));
    rect(1200, 700, 1000, 500);
    for (var key in agentMap){
        const x = agentMap[key].position.x;
        const y = agentMap[key].position.y;
        const state = agentMap[key].state;
        const agentType = agentMap[key].type;

        strokeWeight(2);
        if (agentType == "CLEANER") {
            const color = cleanerAgentStateToColor(state);
            stroke(color[0], color[1], color[2]);
            fill(color[0], color[1], color[2]);
            circle(x, y, 30);
        }
        else if (agentType == "GUARD") {
            const color = guardAgentStateToColor(state);
            stroke(color[0], color[1], color[2]);
            fill(color[0], color[1], color[2]);
            rect(x - 15, y - 15, 30, 30);
        }
        else if (agentType == "GUIDE") {
            const color = guideAgentStateToColor(state);
            stroke(color[0], color[1], color[2]);
            fill(color[0], color[1], color[2]);
            circle(x, y, 30);
        }

        strokeWeight(0);
        textSize(12);
        stroke(255);
        fill(255)
        text("(" + agentType + ")", x+25, y-4);
        text(state, x+25, y+10);
    }
}