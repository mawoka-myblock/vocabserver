var captcha
console.log("")
function captcha_done() {
    var captcha = true;
    globalThis.captcha = true;
}



function submit() {
    document.getElementById("passwd").classList.remove("is-danger")
    document.getElementById("passwd2").classList.remove("is-danger")
    document.getElementById("mail").classList.remove("is-danger")
    document.getElementById("errorlabel").style.visibility = "hidden"
    document.getElementById("errorlabel").innerHTML = ""
    var mail = document.getElementById("mail").value
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
            document.getElementById("errorlabel").innerHTML = "Passwort ist zu kurz. Mindestens 8 Zeichen."
        }
    } else {
        document.getElementById("passwd").classList.add("is-danger")
        document.getElementById("passwd2").classList.add("is-danger")
        document.getElementById("errorlabel").style.color = "red"
        document.getElementById("errorlabel").style.visibility = "visible"
        document.getElementById("errorlabel").innerHTML = "Passwörter sind nicht die gleichen"
        passwords = false
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
    if (email == true && passwords == true && captcha == true) {
        document.getElementById("submit").classList.add("is-loading")
        document.getElementById("submit").classList.add("is-disabled")
        var url = "/api/v1/auth/register";
        var xhr = new XMLHttpRequest();
        xhr.open("POST", url, true);
        var data = '{"email": "' + mail + '", "password": "' + passwd1 + '", "is_active": true, "is_superuser": false, "is_verified": false}'
        xhr.setRequestHeader("Content-type", "application/json");
        xhr.send(data);
        xhr.onload = function() {
            if (xhr.status == 400) { // analyze HTTP status of the response
                alert("Der User existiert Wahrschinlich schon!");
                //alert(`Error ${xhr.status}: ${xhr.statusText}`); // e.g. 404: Not Found
            } else if (xhr.status == 201) { // show the result
                var url = "/api/v1/auth/request-verify-token";
                var req = new XMLHttpRequest();
                req.open("POST", url, true);
                var data = '{"email": "' + mail + '"}'
                req.send(data);
                req.onload = function() {
                    console.log(req.status)
                    if (req.status == 400) { // analyze HTTP status of the response
                        alert("Es gab einen Fehler beim Senden der Mail! (400)");
                        //alert(`Error ${xhr.status}: ${xhr.statusText}`); // e.g. 404: Not Found
                    } else if (req.status == 202) { // show the result
                        alert(`Deine Bestätigungs-Mail sollte auf dem Weg sein! Bitte gucke in dein Postfac und in den Spam-Ordner!`);
                        document.getElementById("submit").classList.remove("is-loading")
                    } else {
                        alert("Es gab einen Fehler beim Senden der Mail!");
                    }
                };
            } else {
                alert("Fehler beim Registrieren!");
            }
        };
    }
        
}


