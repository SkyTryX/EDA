async function getJSON() {
    return await (await fetch("api/queue")).json();
}

const interval_chrono = setInterval(chrono, 1000);

function chrono() {
    data = getJSON();
    data.then(function (result) {
        site = document.getElementsByTagName('html')[0].innerHTML;
        if (site.includes("course")) {
            if (result["course"] === "None") {
                location.href = '/course';
                clearInterval(interval_chrono);
            }
        } else if (site.includes("combat")) {
            if (result["combat"] === "None") {
                location.href = '/combat';
                clearInterval(interval_chrono);
            }
        }
    });
}
