function loadSettings() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE) {
            var response = JSON.parse(this.response);
            
            var equation = MathJax.tex2chtml(response['latex'], {display: true});
            var identifier = MathJax.tex2chtml(response['variable'] + " = {}", {display: true});
            
            updateHistory(response['history'])

            document.getElementById("problem-rating").innerHTML = response['rating'];
            document.getElementById("math-equation").innerHTML = equation.outerHTML;
            document.getElementById("math-identifier").innerHTML = identifier.outerHTML;
            document.getElementById("MJX-CHTML-styles").innerHTML = MathJax.chtmlStylesheet().innerHTML;
        }
    }
    xhttp.open("GET", "/api/current");
    xhttp.send();
}

function updateHistory(history) {
    console.log(history);
    var keys = Object.keys(history);

    for (var index = 0; index < keys.length; index++) { 
        var currHistory = history[keys[index]];
        document.getElementById(keys[index] + "-link").href = "/problem/" + currHistory['id'];
        document.getElementById(keys[index]).innerHTML = "<span class='history-label no-select'>" + currHistory['gain'].toFixed(1) + "</span>";
        document.getElementById(keys[index]).classList.add(currHistory['correct'] ? "history-correct" : "history-incorrect");
        document.getElementById(keys[index]).classList.remove(currHistory['correct'] ? "history-incorrect" : "history-correct");
    }
}

function update(response) {
    console.log(response);
    
    var equation = MathJax.tex2chtml(response['equation']['latex'], {display: true});
    var identifier = MathJax.tex2chtml(response['equation']['variable'] + " = {}", {display: true});
    var diff = parseFloat(response['newRating'].toFixed(1)) - parseFloat(document.getElementById("current-rating").innerHTML);
    
    var ratingDiff = document.getElementById("rating-diff");
    ratingDiff.innerHTML = diff.toFixed(1);
    if (diff > 0) {
        ratingDiff.classList.remove("bad-diff");
        ratingDiff.classList.add("good-diff");
    } else {
        ratingDiff.classList.remove("good-diff");
        ratingDiff.classList.add("bad-diff");
    }
            
    document.getElementById("problem-rating").innerHTML = response['equation']['rating'];
    document.getElementById("current-rating").innerHTML = response['newRating'].toFixed(1);
    document.getElementById("math-equation").innerHTML = equation.outerHTML;
    document.getElementById("math-identifier").innerHTML = identifier.outerHTML;
    document.getElementById("MJX-CHTML-styles").innerHTML = MathJax.chtmlStylesheet().innerHTML;
    document.getElementById("input-equation").value = "";
    
    updateHistory(response['history']);
}
