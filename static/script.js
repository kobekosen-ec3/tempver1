// static/script.js
const logs = document.getElementById("logs");
const logbtn = document.getElementById("logopen");
const hyoujitx = document.getElementById("hyoujitx");

let loghyouji = false;

async function update() {
    const res = await fetch("/get");
    const data = await res.json();

    if (data.ds !== null) {
        document.getElementById("ds").textContent =
            data.ds.toFixed(2) + " ℃";

        document.getElementById("pico").textContent =
            data.pico.toFixed(2) + " ℃";

        const now = new Date();
        const hh = String(now.getHours()).padStart(2, "0");
        const mm = String(now.getMinutes()).padStart(2, "0");
        const ss = String(now.getSeconds()).padStart(2, "0");

        document.getElementById("time").textContent =
            hh + ":" + mm + ":" + ss;
    }

    // ログ取得
    const logRes = await fetch("/log");
    const log = await logRes.json();

    const list = document.getElementById("log");
    list.innerHTML = "";

    for (let i = 0; i <= log.length - 1; i++) {
        const li = document.createElement("li");

        li.textContent =
            log[i].time +
            " / DS:" + log[i].ds.toFixed(2) +
            " / Pico:" + log[i].pico.toFixed(2);

        list.appendChild(li);
    }
}

// ログ表示ボタン
logbtn.addEventListener("click", () => {
    if (loghyouji) {
        logs.style.display = "none";
        hyoujitx.textContent = "表示";
        loghyouji = false;
    } else {
        logs.style.display = "block";
        hyoujitx.textContent = "非表示";
        loghyouji = true;
    }
});

setInterval(update, 2000);
update();
