async function updateStatus(){

    const res = await fetch("/line_setting");
    const data = await res.json();

    const status = document.getElementById("status");
    const test = document.getElementById("test");

    if(data.connected){

        status.textContent = "取得状況：登録済み";
        test.disabled = false;

    }else{

        status.textContent = "取得状況：未登録";
        test.disabled = true;

    }

}

document.getElementById("test").onclick = async ()=>{

    const res = await fetch("/line_test",{
        method:"POST"
    });

    if(res.ok){
        alert("テスト通知を送信しました");
    }
};

updateStatus();
setInterval(updateStatus,3000);
