const input = document.getElementById("searchQuiz");
const grid = document.querySelector(".quiz-grid");

let timeout = null;
let controller = null; // 🔥 biar bisa abort request lama

input.addEventListener("input", () => {
    clearTimeout(timeout);

    timeout = setTimeout(() => {
        fetchQuiz(input.value);
    }, 300);
});

async function fetchQuiz(keyword) {
    try {
        // abort request sebelumnya
        if (controller) controller.abort();
        controller = new AbortController();

        const res = await fetch(`/quiz/search?q=${encodeURIComponent(keyword)}`, {
            signal: controller.signal
        });

        const data = await res.json();
        renderQuiz(data);

    } catch (err) {
        if (err.name !== "AbortError") {
            console.error("Error:", err);
        }
    }
}

function renderQuiz(data) {
    if (!grid) return;

    // fade out dulu
    grid.classList.add("fade-out");

    setTimeout(() => {
        grid.innerHTML = "";

        if (data.length === 0) {
            grid.innerHTML = `
                <div class="no-results fade-in">
                    <h2>Quiz tidak ditemukan 😢</h2>
                </div>
            `;
            grid.classList.remove("fade-out");
            return;
        }

        data.forEach((q, i) => {
            const card = document.createElement("div");
            card.className = "quiz-card fade-in";
            card.style.animationDelay = `${i * 0.05}s`;

            card.innerHTML = `
                <div class="quiz-icon">
                    <i class="${q.icon}"></i>
                </div>
                <h3>${q.judul}</h3>
                <p>${q.soal_count} Pertanyaan</p>
                <a href="/quiz/kerjakan/${q.id}" class="btn-start">Mulai Kuis</a>
            `;

            grid.appendChild(card);
        });

        // fade in lagi
        grid.classList.remove("fade-out");

    }, 150);
}