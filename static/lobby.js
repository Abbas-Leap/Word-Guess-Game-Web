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
