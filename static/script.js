// static/script.js
async function update() {
    const res = await fetch("/get");
    const data = await res.json();

    if (data.ds !== null) {
        document.getElementById("ds").textContent =
            data.ds.toFixed(2) + " ℃";

        document.getElementById("pico").textContent =
            data.pico.toFixed(2) + " ℃";

        document.getElementById("time").textContent =
            data.time;
    }

    // ログ取得
    const logRes = await fetch("/log");
    const log = await logRes.json();

    const list = document.getElementById("log");
    list.innerHTML = "";

    for (let i = log.length - 1; i >= 0; i--) {
        const li = document.createElement("li");

        li.textContent =
            log[i].time +
            " / DS:" + log[i].ds.toFixed(2) +
            " / Pico:" + log[i].pico.toFixed(2);

        list.appendChild(li);
    }
}

setInterval(update, 2000);
update();
