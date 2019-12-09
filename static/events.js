

document.getElementById("input-equation").onkeydown = function(event) {
    if (event.keyCode === 13) {
        var input = document.getElementById("input-equation").value
        
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState === XMLHttpRequest.DONE) {
                var response = JSON.parse(this.response);
                update(response);
            }
        }
        xhttp.open("POST", "/api/check");
        xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhttp.send(JSON.stringify({
            value: input
        }));
    }
}