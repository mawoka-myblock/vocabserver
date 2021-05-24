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
        passwords = true
    } else {
        document.getElementById("errorlabel").style.color = "red"
        document.getElementById("errorlabel").style.visibility = "visible"
        document.getElementById("errorlabel").innerHTML = "Passwords do NOT match"
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
                alert("Token ungültig!");
                //alert(`Error ${xhr.status}: ${xhr.statusText}`); // e.g. 404: Not Found
            } else if (xhr.status == 200) { // show the result
                alert(`Mail-Adresse erfolgreich verifiziert!`); // response is the server response
                window.location.replace("/")
            } else {
                alert("Da war ein Fehler bei der Verifizierung!");
            }
          };
    }
        



   captcha  = false
   globalThis.captcha
}


