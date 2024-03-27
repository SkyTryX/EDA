async function getJSON() {
    return await (await fetch("api/queue")).json();
}

setInterval(function () {
    data = getJSON();
    data.then(function (result) {
        site = document.getElementsByTagName('html')[0].innerHTML;
        if (site.includes("course")) {
            if (result["course"] === "None") {
                location.href = '/course';
                clearInterval(this);
            }
        } else if (site.includes("combat")) {
            if (result["combat"] === "None") {
                location.href = '/combat';
                clearInterval(this);
            }
        }
    });
}, 1000);

