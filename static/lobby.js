// Start up
document.addEventListener("DOMContentLoaded", async function () {
    // Grab Info
    let serverResponse = await fetch("/lobbyOneTimeComm");

    let data = await serverResponse.json();

    if (data["status"] != "ok") {
        alert(`${data["status"]}: ${data["msg"]}`);
        return;
    }

    // Players related
    let usernameNode = document.getElementById("username");
    let pointsNode = document.getElementById("points");
    let numOfActiveUsers1 = document.getElementById("numOfActivePlayers1");
    let numOfActiveUsers2 = document.getElementById("numOfActivePlayers2");
    let numOfReadyUsers = document.getElementById("numOfReadyPlayers");

    usernameNode.textContent = data["data"]["username"];
    pointsNode.textContent = data["data"]["points"];
    numOfActiveUsers1.textContent = data["data"]["numOfActiveUsers"];
    numOfActiveUsers2.textContent = data["data"]["numOfActiveUsers"];
    numOfReadyUsers.textContent = data["data"]["numOfReadyUsers"];
    // Chat related
    alert(data["data"]["chatHistory"]);
    for (let i = 0; i < data["data"]["chatHistory"].length; i++) {
        renderMessage(data["data"]["chatHistory"][i]);
    }
});
// Info Track
new EventSource(`${window.location.origin}/lobbyUsersStatusComm`).onmessage = (event) => {
    let numOfActiveUsers1 = document.getElementById("numOfActivePlayers1");
    let numOfActiveUsers2 = document.getElementById("numOfActivePlayers2");
    let numOfReadyUsers = document.getElementById("numOfReadyPlayers");

    let eventData = JSON.parse(event.data)

    numOfActiveUsers1.textContent = eventData.activeUsers;
    numOfActiveUsers2.textContent = eventData.activeUsers;

    numOfReadyUsers.textContent = eventData.readyUsers;
    // Chat
    if (eventData.message == "Null")
        return;
    else if (eventData.message == "Game Started") {
        alert("Game Started");
        window.location.href = `${window.location.origin}/game`;
        return;
    }
    renderMessage(eventData.message);
};
// ------------------
// Ready
async function toggleReady() {
    let readyButton = document.getElementById("ready");

    let response = await fetch("/lobbyReadyComm", { "method": "POST" });

    let responseJson = await response.json();

    if (responseJson["status"] != "ok")
        return;

    // Unready
    if (responseJson["newState"] == "Unready") {
        readyButton.textContent = "Ready";
        readyButton.style.backgroundColor = "green";
    }
    // Ready
    else {
        readyButton.textContent = "Unready";
        readyButton.style.backgroundColor = "red";
    }
}
// ------------------
// Chat
async function sendMessage(event) {
    event.preventDefault();

    let chatBoxNode = document.getElementById("chatBox");
    let message = chatBoxNode.value.trim();

    chatBoxNode.value = "";

    if (!isMessageValid(message)) {
        alert("Invalid or empty text");
        return;
    }

    await fetch("/chatSendComm", {
        "headers": { "Content-Type": "application/json" },
        "method": "POST",
        "body": JSON.stringify({ "message": message }),
    });
};
// Utilities
function isMessageValid(message) {
    if (message.length > 0) {
        return true;
    }
    return false;
};

function renderMessage(message) {
    let chatArea = document.getElementById("Chat");

    let messageNode = document.createElement("p");
    messageNode.id = "message";
    messageNode.textContent = message;

    chatArea.prepend(messageNode);
};
