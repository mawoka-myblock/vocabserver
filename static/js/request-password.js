var captcha
function captcha_done() {
    var captcha = true;
    globalThis.captcha = true;
}



function submit() {
    document.getElementById("mail").classList.remove("is-danger")
    document.getElementById("errorlabel").style.visibility = "hidden"
    document.getElementById("errorlabel").innerHTML = ""
    var mail = document.getElementById("mail").value
    if (captcha != true) {
        document.getElementById("errorlabel").style.color = "red"
        document.getElementById("errorlabel").style.visibility = "visible"
        document.getElementById("errorlabel").innerHTML = "Captcha fehlt!"
    }


    if (/[^@]+@[^@]+\.[^@]+/.test(mail)) {
        email = true
    } else {
        document.getElementById("mail").classList.add("is-danger")
        email = false
        document.getElementById("errorlabel").style.color = "red"
        document.getElementById("errorlabel").style.visibility = "visible"
        document.getElementById("errorlabel").innerHTML = "Keine gültige E-Mail-Adresse!"
    }
    if (email == true && captcha == true) {
        document.getElementById("submit").classList.add("is-loading")
        document.getElementById("submit").classList.add("is-disabled")
        var url = "/api/v1/auth/forgot-password";
        var xhr = new XMLHttpRequest();
        xhr.open("POST", url, true);
        var data = '{"email": "' + mail + '"}'
        xhr.setRequestHeader("Content-type", "application/json");
        xhr.send(data);
        xhr.onload = function() {
            if (xhr.status == 400) { // analyze HTTP status of the response
                alert("Der User existiert Wahrschinlich schon!");
            } else if (xhr.status == 202) { // show the result
                alert("Erfolgreich! Bitte guck in dein Postfach!")
                document.getElementById("submit").classList.remove("is-loading")
            } else {
                alert("Fehler!");
            }
        };
    }

}


