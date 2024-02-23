async function getPROG(prog) {
    return await (await fetch("api/translator?prog=" + prog)).json();
}
var end = new Date().getTime() + 15000;

var x = setInterval(function () {
    var distance = end - new Date().getTime();
    document.getElementById("count").innerHTML = (distance / 1000) + "s";

    if (distance <= 0) {
        clearInterval(x);
        var prog = document.getElementById("prog").value;
        var promise = getPROG(prog);
        promise.then(value => {
            console.log(value);
        });
    }
}, 1000);