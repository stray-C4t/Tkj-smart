document.addEventListener("DOMContentLoaded", () => {
    const raw = document.getElementById("chart-data");

    if (!raw) {
        console.error("Data chart tidak ditemukan!");
        return;
    }

    const DATA = JSON.parse(raw.textContent);

    const labels = DATA.labels || [];
    const values = DATA.values || [];

    const chart = document.getElementById("chart");
    if (!chart) return;

    const maxValue = Math.max(...values, 1);

    chart.innerHTML = '';

    labels.forEach((label, i) => {
        const bar = document.createElement("div");
        bar.className = "bar-wrapper";

        const height = (values[i] / maxValue) * 200;

        bar.innerHTML = `
            <div class="bar" style="height:${height}px"></div>
            <div class="label">${label}</div>
            <div class="value">${values[i]}</div>
        `;

        chart.appendChild(bar);
    });
});