// static/script.js
// const logs = document.getElementById("logleft");
// const logbtn = document.getElementById("logopen");
// const hyoujitx = document.getElementById("hyoujitx");
const logbox = document.getElementById("logbox");
// const ctx = document.getElementById("tempgraph");
// let chart = null;

let lastTime = null;
let loghyouji = false;

async function update() {
    const res = await fetch("/get");
    const data = await res.json();
    
    const devices = Object.values(data);
    
    if (devices.length > 0) {
        const current = devices[0];
        
        document.getElementById("time").textContent = current.time;
        lastTime = current.time;
    
        document.getElementById("ds").textContent =
            Number(current.ds).toFixed(2) + " ℃";
    
        document.getElementById("pico").textContent =
            Number(current.pico).toFixed(2) + " ℃";
    }

    // ログ取得
    const logRes = await fetch("/log");
    const log = await logRes.json();

    const list = document.getElementById("log");
    list.innerHTML = "";


    for (let i = log.length - 1; i >= 0; i--) {
    
        const item = log[i];
    
        const li = document.createElement("li");
    
        const parts = item.time.split(" ");
    
        const datetime = document.createElement("div");
        datetime.className = "log-datetime";
        datetime.textContent = parts[0] + " " + parts[1];
    
        const dstemp = document.createElement("div");
        dstemp.className = "log-dstemp";
        dstemp.textContent =
            "センサ温度：" +
            (item.ds != null && item.ds !== "" ? Number(item.ds).toFixed(2) : "--") +
            " ℃";
    
        const picotemp = document.createElement("div");
        picotemp.className = "log-picotemp";
        picotemp.textContent =
            "本体温度　：" +
            (item.pico != null && item.pico !== "" ? Number(item.pico).toFixed(2) : "--") +
            " ℃";
    
        li.appendChild(datetime);
        li.appendChild(dstemp);
        li.appendChild(picotemp);
    
        list.appendChild(li);
    }

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

setInterval(update, 2000);
update();
