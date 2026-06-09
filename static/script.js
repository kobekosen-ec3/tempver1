// static/script.js
const logs = document.getElementById("logleft");
const logbtn = document.getElementById("logopen");
const hyoujitx = document.getElementById("hyoujitx");
const logbox = document.getElementById("logbox");
// const ctx = document.getElementById("tempgraph");

// let chart = null;

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


    for (let i = log.length - 1; i >= 0; i--) {
    
        const item = log[i];
    
        const li = document.createElement("li");
    
        // const device = document.createElement("span");
        // device.className = "log-device";
        // device.textContent = "機器:" + item.device_id;
    
        const date = document.createElement("span");
        date.className = "log-date";
    
        const parts = item.time.split(" ");
        date.textContent = parts[0];
    
        const time = document.createElement("span");
        time.className = "log-time";
        time.textContent = parts[1];
    
        const dstemp = document.createElement("span");
        dstemp.className = "log-dstemp";
        dstemp.textContent =
            "センサー温度:" +
            (item.ds != null && item.ds !== ""
                ? Number(item.ds).toFixed(2)
                : "--")
            + "℃";
    
        const picotemp = document.createElement("span");
        picotemp.className = "log-picotemp";
        picotemp.textContent =
            "室内温度:" +
            (item.pico != null
                ? Number(item.pico).toFixed(2)
                : "--")
            + "℃";
    
        // li.appendChild(device);
        li.appendChild(date);
        li.appendChild(time);
        li.appendChild(dstemp);
        li.appendChild(picotemp);
    
        list.appendChild(li);
    }
    

    // for (let i = log.length-1; i >= 0; i--) {
    
    //     const li = document.createElement("li");
    
    //     // 日付
    //     const date = document.createElement("span");
    //     date.className = "log-date";
    
    //     const parts = log[i].time.split(" ");
    //     date.textContent = parts[0];
    
    //     // 時間
    //     const time = document.createElement("span");
    //     time.className = "log-time";
    //     time.textContent = parts[1];
    
    //     // 温度
    //     const dstemp = document.createElement("span");
    //     dstemp.className = "log-dstemp";
    //     dstemp.textContent ="センサー温度:" + (log[i].ds != null ? log[i].ds.toFixed(2) : "--") + "℃";

    //     const picotemp = document.createElement("span");
    //     picotemp.className = "log-picotemp";
    //     picotemp.textContent ="室内温度:" + (log[i].pico != null ? log[i].pico.toFixed(2) : "--")+ "℃";
    
    //     li.appendChild(date);
    //     li.appendChild(time);
    //     li.appendChild(dstemp);
    //     li.appendChild(picotemp);
    //     list.appendChild(li);
    // }

    //---グラフ


    // const labels = [];
    // const dsTemps = [];
    // const picoTemps = [];
    
    // const graphLog = log.slice(-10);

    // for (let i = 0; i < graphLog.length; i++) {
    //     if (graphLog[i].ds != null && graphLog[i].pico != null) {
    //         labels.push(graphLog[i].time);
    //         dsTemps.push(graphLog[i].ds);
    //         picoTemps.push(graphLog[i].pico);
    //     }
    // }

//     if (chart) {
//         chart.destroy();
//     }
    
//     chart = new Chart(ctx, {
//         type: "line",
    
//         data: {
//             labels: labels,
//             datasets: [
//                 {
//                     label: "DS18B20",
//                     data: dsTemps
//                 },
//                 {
//                     label: "Pico",
//                     data: picoTemps
//                 }
//             ]
//         },
    
//         options: {
//             responsive: true
//         }
//     });
    
}

// ログ表示ボタン
logbtn.addEventListener("click", () => {
    if (loghyouji) {
        logs.style.display = "none";
        hyoujitx.textContent = "表示";
        loghyouji = false;
    } else {
        logs.style.display = "flex";
        // logbox.scrollTop = logbox.scrollHeight;
        hyoujitx.textContent = "非表示";
        loghyouji = true;
    }
});

setInterval(update, 2000);
update();
