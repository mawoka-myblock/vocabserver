var captcha
function captcha_done() {
    var captcha = true;
    globalThis.captcha = true;
}



function submit() {
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
        if (passwd1.length > 8) {
            passwords = true
        } else {
            passwords = false
            document.getElementById("errorlabel").style.color = "red"
            document.getElementById("errorlabel").style.visibility = "visible"
            document.getElementById("errorlabel").innerHTML = "Password is too short. At least 8 characters"
        }
    } else {
        document.getElementById("errorlabel").style.color = "red"
        document.getElementById("errorlabel").style.visibility = "visible"
        document.getElementById("errorlabel").innerHTML = "Passwords do NOT match"
        passwords = false
    }
    

    if (/[^@]+@[^@]+\.[^@]+/.test(mail)) {
        email = true
    } else {
        email = false
        document.getElementById("errorlabel").style.color = "red"
        document.getElementById("errorlabel").style.visibility = "visible"
        document.getElementById("errorlabel").innerHTML = "Not a valid e-mail adress"
    }
    if (email == true && passwords == true && captcha == true) {
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
                        alert(`Deine Bestätigungs-Mail sollte auf dem Weg sein! Bitte gucke in dein Postfac und in den Spam-Ordner!`); // response is the server response
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


