// Recieving
new EventSource("/chatRecieveComm").onmessage = (event) => {
    let message = JSON.parse(event.data);

    renderMessage(message);
};
// --------
// Rendering
function renderMessage(message) {
    alert(`Rendering ${message}`);
};
// --------
// Sending
async function sendMessage() {
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
//-------
// Utilities

function isMessageValid(message) {
    if (message.length > 0) {
        return true;
    }
    return false;
};
