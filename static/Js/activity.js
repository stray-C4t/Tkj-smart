document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById('activity-container');

    if (!container) {
        console.error("activity-container tidak ditemukan!");
        return;
    }

    let lastActivityId = 0;

    async function loadActivity() {
        try {
            const res = await fetch(`/admin/recent-activity?last_id=${lastActivityId}`);
            const data = await res.json();

            if (!data.length) return;

            data.reverse().forEach((a, i) => {
                const div = document.createElement('div');

                div.className = 'activity-item fade-in';
                div.style.animationDelay = (i * 0.1) + "s";

                div.innerHTML = `
                    <div class="activity-left">
                        <strong>${a.nama_lengkap}</strong>
                        <small>${a.activity}</small>
                    </div>
                    <div class="activity-time">
                        ${a.created_at}
                    </div>
                `;

                container.prepend(div);

                // maksimal 7
                while (container.children.length > 7) {
                    container.removeChild(container.lastElementChild);
                }

                if (a.id > lastActivityId) {
                    lastActivityId = a.id;
                }
            });

        } catch (err) {
            console.error("Gagal load activity:", err);
        }
    }

    loadActivity();
    setInterval(loadActivity, 5000);
});