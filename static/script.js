// static/script.js
const logbox = document.getElementById("logbox");
const loading = document.getElementById("loading");
const list = document.getElementById("log");
const saveTempBtn = document.getElementById("savetempbtn");

loading.style.display = "block";
list.style.display = "none";

let firstLoad = true;
let lastTime = null;

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
    if (firstLoad) {
        loading.style.display = "block";
        list.style.display = "none";
    }
    
    try {
        const logRes = await fetch("/log");
        const log = await logRes.json();
    
        list.innerHTML = "";
    
        for (let i = log.length - 1; i >= 0; i--) {
            const item = log[i];
            const li = document.createElement("li");
            const parts = item.time.split(" ");
            
            const datetime = document.createElement("div");
            datetime.className = "log-datetime";
            datetime.textContent = parts[0];
    
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
    
    } finally {
        if (firstLoad) {
            loading.style.display = "none";
            list.style.display = "block";
            firstLoad = false;
        }
    }
}

    saveTempBtn.addEventListener("click", async () => {
    const threshold = Number(document.getElementById("threshold").value);

    const res = await fetch("/threshold", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            threshold: threshold
        })
    });

    if (res.ok) {
        alert("設定を保存しました");
    } else {
        alert("保存に失敗しました");
    }
});

setInterval(update, 2000);
update();
