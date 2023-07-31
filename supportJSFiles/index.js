const statusLabel = document.getElementById("statusLabel");

function login() {
    const passwordField = document.getElementById("passwordField");
    if (!passwordField.value || passwordField.value == "") {
        alert("Please enter your password.");
        return
    }

    statusLabel.innerText = 'Processing...'
    statusLabel.style.visibility = 'visible'

    const password = passwordField.value

    axios({
        method: 'post',
        url: `${origin}/api/login`,
        headers: {
            "Content-Type": "application/json",
            "APIKey": "\{{ API_KEY }}"
        },
        data: {
            "password": password
        }
    })
    .then(response => {
        if (response.status == 200) {
            if (!response.data.startsWith("ERROR")) {
                if (!response.data.startsWith("UERROR")) {
                    if (response.data.startsWith("SUCCESS")) {
                        statusLabel.innerText = "Logged in! Redirecting...";

                        location.href = `${origin}/session/${response.data.substring("SUCCESS: Token: ".length)}/list`
                    } else {
                        alert("Something went wrong. Please try again.")
                        console.log("Unknown response received; response: " + response.data)
                        statusLabel.style.visibility = 'hidden'
                    }
                } else {
                    statusLabel.innerText = response.data.substring("UERROR: ".length)
                    console.log("User error received; response: " + response.data)
                }
            } else {
                alert("Something went wrong. Please try again.")
                console.log("Error received; response: " + response.data)
                statusLabel.style.visibility = 'hidden'
            }
        } else {
            alert("Something went wrong. Please try again.")
            console.log("Unknown status code received; status code: " + response.status)
            statusLabel.style.visibility = 'hidden'
        }
    })
    .catch(error => {
        alert("An error occurred. Please try again.")
        console.log("Error occurred in connecting to server; error: " + error)
        statusLabel.style.visibility = 'hidden'
    })
}