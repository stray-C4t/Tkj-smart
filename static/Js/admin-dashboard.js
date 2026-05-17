function setupSearch(inputId, tableId, url, renderRow) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);

    if (!input || !table) return;

    let timeout = null;

    input.addEventListener("keyup", function () {
        clearTimeout(timeout);

        timeout = setTimeout(() => {
            fetch(`${url}?q=${encodeURIComponent(this.value)}`)
                .then(res => res.json())
                .then(data => {
                    table.style.opacity = "0.4";
                    table.innerHTML = "";

                    // reset pagination active
                    const paginations = document.querySelectorAll(".pagination a");
                    paginations.forEach(a => a.classList.remove("active"));

                    if (data.length === 0) {
                        table.innerHTML = `
                            <tr>
                                <td colspan="6" style="text-align:center;">
                                    Tidak ditemukan
                                </td>
                            </tr>
                        `;
                        table.style.opacity = "1";
                        return;
                    }

                    data.forEach(item => {
                        table.innerHTML += renderRow(item);
                    });

                    table.style.opacity = "1";
                })
                .catch(err => console.error("Search error:", err));
        }, 300);
    });
}

// ==========================
// PAGINATION AJAX
// ==========================
function setupPagination(tableId, paginationId, endpoint) {
    const table = document.getElementById(tableId);
    const pagination = document.getElementById(paginationId);

    if (!table || !pagination) return;

    pagination.addEventListener("click", async (e) => {
        if (e.target.tagName !== "A") return;

        e.preventDefault();

        const page = e.target.dataset.page;

        try {
            table.style.opacity = "0.4";

            const res = await fetch(`${endpoint}?page=${page}`);
            const html = await res.text();

            table.innerHTML = html;

            pagination.querySelectorAll("a")
                .forEach(a => a.classList.remove("active"));

            e.target.classList.add("active");

            table.style.opacity = "1";

        } catch (err) {
            console.error("Pagination error:", err);
        }
    });
}

// ==========================
// SEARCH
// ==========================
setupSearch(
    "search-modul",
    "modulTable",
    "/admin/search-modul",
    (m) => `
        <tr>
            <td>${m.judul}</td>
            <td><span class="badge">${m.kategori}</span></td>
            <td>
                <a href="/admin/delete-modul/${m.id}" class="btn-icon delete">
                    <i class="fas fa-trash"></i>
                </a>
            </td>
            <td>
                <a href="/admin/edit-modul/${m.id}">
                    <i class="fas fa-edit"></i>
                </a>
            </td>
        </tr>
    `
);

setupSearch(
    "search-video",
    "videoTable",
    "/admin/search-video",
    (v) => `
        <tr>
            <td>${v.judul}</td>
            <td><code>${v.youtube_id}</code></td>
            <td>
                <a href="/admin/delete-video/${v.id}" class="btn-icon delete">
                    <i class="fas fa-trash"></i>
                </a>
            </td>
            <td>
                <a href="/admin/edit-video/${v.id}">
                    <i class="fas fa-edit"></i>
                </a>
            </td>
        </tr>
    `
);

setupSearch(
    "search-quiz",
    "quizTable",
    "/admin/search-quiz",
    (q) => `
        <tr>
            <td>${q.judul}</td>
            <td><span class="badge">${q.jumlah_soal} Soal</span></td>
            <td>
                <a href="/admin/delete-latihan/${q.id}" class="btn-icon delete">
                    <i class="fas fa-trash"></i>
                </a>
            </td>
            <td>
                <a href="/admin/edit-quiz/${q.id}">
                    <i class="fas fa-edit"></i>
                </a>
            </td>
        </tr>
    `
);

setupSearch(
    "search-user",
    "userTable",
    "/admin/search-user",
    (u) => `
        <tr>
            <td>${u.username}</td>
            <td>${u.nama}</td>
            <td>${u.kelas}</td>
            <td><span class="badge">${u.role}</span></td>
            <td>
                <a href="/admin/delete-user/${u.id}" class="btn-icon delete">
                    <i class="fas fa-trash"></i>
                </a>
            </td>
            <td>
                <a href="/admin/edit-user/${u.id}">
                    <i class="fas fa-edit"></i>
                </a>
            </td>
        </tr>
    `
);

// ==========================
// PAGINATION
// ==========================
setupPagination("modulTable", "modulPagination", "/admin/modul-page");
setupPagination("videoTable", "videoPagination", "/admin/video-page");
setupPagination("quizTable", "quizPagination", "/admin/quiz-page");
setupPagination("userTable", "userPagination", "/admin/user-page");