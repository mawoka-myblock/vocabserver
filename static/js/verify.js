const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
var url = "/api/v1/auth/verify";
var params = "token=" + urlParams.get("id");
var xhr = new XMLHttpRequest();
xhr.open("POST", url, true);
var data = '{"token": "' + urlParams.get("id") + '"}'; 
xhr.setRequestHeader("Content-type", "application/json");
xhr.send(data);
console.log("Hallo");
xhr.onload = function() {
    if (xhr.status == 400) { // analyze HTTP status of the response
        alert("Token ungültig!");
        //alert(`Error ${xhr.status}: ${xhr.statusText}`); // e.g. 404: Not Found
    } else if (xhr.status == 200) { // show the result
        alert(`Mail-Adresse erfolgreich verifiziert!`); // response is the server response
        window.localStorage.clear();
        window.location.replace("/")
    } else {
        alert("Da war ein Fehler bei der Verifizierung!");
    }
  };