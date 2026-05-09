// static/script.js
const logs = document.getElementById("logs");
const logbtn = document.getElementById("logopen");
const hyoujitx = document.getElementById("hyoujitx");
const logbox = document.getElementById("logbox");

let loghyouji = false;

async function update() {
    const res = await fetch("/get");
    const data = await res.json();

    if (data.ds !== null) {
        document.getElementById("ds").textContent = data.ds.toFixed(2) + " ℃";

        document.getElementById("pico").textContent = data.pico.toFixed(2) + " ℃";

        const now = new Date();
        const hh = String(now.getHours()).padStart(2, "0");
        const mm = String(now.getMinutes()).padStart(2, "0");
        const ss = String(now.getSeconds()).padStart(2, "0");

        document.getElementById("time").textContent = hh + ":" + mm + ":" + ss;
    }

    // ログ取得
    const logRes = await fetch("/log");
    const log = await logRes.json();

    const list = document.getElementById("log");
    list.innerHTML = "";

    for (let i = log.length-1; i >= 0; i--) {
    
        const li = document.createElement("li");
    
        // 日付
        const date = document.createElement("span");
        date.className = "log-date";
    
        const parts = log[i].time.split(" ");
        date.textContent = parts[0];
    
        // 時間
        const time = document.createElement("span");
        time.className = "log-time";
        time.textContent = parts[1];
    
        // 温度
        const dstemp = document.createElement("span");
        dstemp.className = "log-dstemp";
        dstemp.textContent ="DS:" + log[i].ds.toFixed(2) +"℃";

        const picotemp = document.createElement("span");
        picotemp.className = "log-picotemp";
        picotemp.textContent ="Pico:" + log[i].pico.toFixed(2) + "℃";
    
        li.appendChild(date);
        li.appendChild(time);
        li.appendChild(dstemp);
        li.appendChild(picotemp);
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
        // logbox.scrollTop = logbox.scrollHeight;
        hyoujitx.textContent = "非表示";
        loghyouji = true;
    }
});

setInterval(update, 2000);
update();
