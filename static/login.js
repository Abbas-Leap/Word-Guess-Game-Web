document.getElementById("loginForm").addEventListener("submit", async function (event) {
    event.preventDefault();
    //
    let usernameNode = document.getElementById("usernameInput");
    let passwordNode = document.getElementById("passwordInput");

    let username = usernameNode.value;
    let password = passwordNode.value;

    if (username.length > 15 || username.length < 3) {
        alert("Username must be between 15 and 3 characters long!")
        return;
    }

    if (password.length < 3) {
        alert("Type a longer password");
        return;
    }
    //
    let response = await fetch("/loginComms", {
        "headers": { "Content-Type": "application/json" },
        "method": "POST",
        "body": JSON.stringify({ "username": username, "password": password })
    });

    let responseData = await response.json();

    alert(responseData["msg"])

    if (responseData["status"] == "declined") {
        alert(responseData["msg"]);
        return;
    }

    if (responseData["status"] == "createdAccount") {
        alert(responseData["msg"]);
        window.location.reload();
        return;
    }
});
