function login() {
    const passwordField = document.getElementById("passwordField");
    if (!passwordField.value || passwordField.value == "") {
        alert("Please enter your password.");
        return
    }

    const password = passwordField.value

    axios({
        method: 'post',
        url: '/api/login'
    })
}