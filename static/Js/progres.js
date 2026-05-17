document.addEventListener("DOMContentLoaded", () => {

    const raw = document.getElementById("modul-data");

    if (!raw) {
        console.error("Data modul tidak ditemukan!");
        return;
    }

    const DATA = JSON.parse(raw.textContent);

    const modulId = DATA.modulId;
    const kategori = DATA.kategori;

    let lastSent = 0;

    // SCROLL TRACKING
    window.addEventListener("scroll", () => {

        let scrollTop = document.documentElement.scrollTop;
        let scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;

        let progress = Math.round((scrollTop / scrollHeight) * 100);

        // update progress bar
        const bar = document.getElementById("progressBar");
        if (bar) bar.style.width = progress + "%";

        // kirim tiap 10%
        if (progress - lastSent >= 10) {
            lastSent = progress;

            fetch("/update-progress", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    modul_id: modulId,
                    progress: progress
                })
            })
            .catch(err => console.log("Progress error:", err));
        }
    });

    // 🔥 biar bisa dipanggil dari HTML onclick
    window.selesaiBelajar = function () {

        fetch("/update-progress", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                modul_id: modulId,
                progress: 100
            })
        })
        .then(res => res.json())
        .then(() => {
            alert("🎉 Modul selesai!");
            window.location.href = `/modul/${kategori}`;
        })
        .catch(() => alert("Terjadi error!"));
    };

});