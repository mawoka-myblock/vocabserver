var captcha
function captcha_done() {
    var captcha = true;
    globalThis.captcha = true;
}



function submit() {
    document.getElementById("errorlabel").style.visibility = "hidden"
    document.getElementById("errorlabel").innerHTML = ""
    var mail = document.getElementById("mail").value
    if (captcha != true) {
        document.getElementById("errorlabel").style.color = "red"
        document.getElementById("errorlabel").style.visibility = "visible"
        document.getElementById("errorlabel").innerHTML = "Captcha missing"
    }


    if (/[^@]+@[^@]+\.[^@]+/.test(mail)) {
        email = true
    } else {
        email = false
        document.getElementById("errorlabel").style.color = "red"
        document.getElementById("errorlabel").style.visibility = "visible"
        document.getElementById("errorlabel").innerHTML = "Not a valid e-mail adress"
    }
    if (email == true && captcha == true) {
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
            } else {
                alert("Fehler!");
            }
        };
    }

}


