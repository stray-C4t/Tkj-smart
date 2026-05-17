const input = document.getElementById("searchInput");
const grid = document.getElementById("videoGrid");

let timeout = null;
let controller = null;

input.addEventListener("input", () => {
    clearTimeout(timeout);

    timeout = setTimeout(() => {
        searchVideos(input.value);
    }, 300);
});

async function searchVideos(keyword) {
    try {
        // abort request lama
        if (controller) controller.abort();
        controller = new AbortController();

        const res = await fetch(`/video/search?q=${encodeURIComponent(keyword)}`, {
            signal: controller.signal
        });

        const data = await res.json();
        console.log("RESULT:", data);

        renderVideos(data);

    } catch (err) {
        if (err.name !== "AbortError") {
            console.error(err);
        }
    }
}

function renderVideos(videos) {
    if (!grid) return;

    // fade out
    grid.classList.add("fade-out");

    setTimeout(() => {
        grid.innerHTML = "";

        if (videos.length === 0) {
            grid.innerHTML = `
                <div class="no-results fade-in">
                    <i class="fas fa-video-slash"></i>
                    <p>Maaf, video yang kamu cari tidak ditemukan.</p>
                    <a href="/video">Lihat Semua Video</a>
                </div>
            `;
            grid.classList.remove("fade-out");
            return;
        }

        videos.forEach((v, i) => {
            const card = document.createElement("div");
            card.className = "video-card fade-in";
            card.style.animationDelay = `${i * 0.05}s`;

            card.innerHTML = `
                <div class="video-thumbnail">
                    <img src="${v.thumbnail}" alt="${v.judul}">
                    <div class="play-btn">
                        <i class="fas fa-play"></i>
                    </div>
                    <span class="vid-duration">${v.durasi}</span>
                </div>
                <div class="video-body">
                    <span class="vid-tag">Tutorial</span>
                    <h3>${v.judul}</h3>
                    <p>${v.desc || "Tidak ada deskripsi"}</p>
                    <a href="/video/watch/${v.id}" class="btn-watch-now">Tonton Sekarang</a>
                </div>
            `;

            grid.appendChild(card);
        });

        // fade in
        grid.classList.remove("fade-out");

    }, 150);
}