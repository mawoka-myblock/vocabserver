var captcha
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
function captcha_done() {
    var captcha = true;
    globalThis.captcha = true;
}



function submit() {
    document.getElementById("passwd").classList.remove("is-danger")
    document.getElementById("passwd2").classList.remove("is-danger")
    document.getElementById("errorlabel").style.visibility = "hidden"
    document.getElementById("errorlabel").innerHTML = ""
    var passwd1 = document.getElementById("passwd").value
    var passwd2 = document.getElementById("passwd2").value
    if (captcha != true) {
        document.getElementById("errorlabel").style.color = "red"
        document.getElementById("errorlabel").style.visibility = "visible"
        document.getElementById("errorlabel").innerHTML = "Captcha missing"
    }

    if (passwd2 == passwd1) {
        if (passwd1.length >= 8) {
            passwords = true
        } else {
            document.getElementById("passwd").classList.add("is-danger")
            document.getElementById("passwd2").classList.add("is-danger")
            passwords = false
            document.getElementById("errorlabel").style.color = "red"
            document.getElementById("errorlabel").style.visibility = "visible"
            document.getElementById("errorlabel").innerHTML = "Passwort ist zu kurz. Mindestens 8 Zeichen"
        }
    } else {
        document.getElementById("passwd").classList.add("is-danger")
        document.getElementById("passwd2").classList.add("is-danger")
        document.getElementById("errorlabel").style.color = "red"
        document.getElementById("errorlabel").style.visibility = "visible"
        document.getElementById("errorlabel").innerHTML = "Passwörter sind nicht die gleichen"
        passwords = false
    }



    if (passwords == true && captcha == true) {
        document.getElementById("submit").classList.add("is-loading")
        document.getElementById("submit").classList.add("is-disabled")
        var url = "/api/v1/auth/reset-password";
        var xhr = new XMLHttpRequest();
        xhr.open("POST", url, true);
        var data = '{"token": "' + urlParams.get("id") + '", "password": "' + passwd1 + '"}'
        xhr.setRequestHeader("Content-type", "application/json");
        xhr.send(data);
        xhr.onload = function() {
            if (xhr.status == 400) { // analyze HTTP status of the response
                alert("Token Falsch!");
                //alert(`Error ${xhr.status}: ${xhr.statusText}`); // e.g. 404: Not Found
            } else if (xhr.status == 200) { // show the result
                alert("Nun kannst du dich mit deinem neuen Passwort anmelden!")
                document.getElementById("submit").classList.remove("is-loading")
                localStorage.clear();
                window.location.replace("/")
            } else {
                alert("Fehler beim Registrieren!");
            }
        };
    }

}


