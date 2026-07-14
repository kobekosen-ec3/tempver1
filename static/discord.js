async function loadSetting() {

    const res = await fetch("/discord_setting");
    const data = await res.json();

    document.getElementById("webhook").value = data.webhook;
}

document.getElementById("save").onclick = async () => {

    const body = {
        webhook: document.getElementById("webhook").value
    };

    const res = await fetch("/discord_setting", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    });

    if (res.ok) {
        alert("保存しました");
    }

};

document.getElementById("test").onclick = async () => {

    const res = await fetch("/discord_test", {
        method: "POST"
    });

    if (res.ok) {
        alert("テスト通知を送信しました");
    } else {
        alert("送信に失敗しました");
    }

};

loadSetting();
