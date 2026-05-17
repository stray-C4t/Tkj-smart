let barLabels = [];
let modulData = [];
let quizData = [];
let videoData = [];
let pieLabels = [];
let pieData = [];

const raw = document.getElementById('chart-data');

if (!raw) {
    console.error("Data chart tidak ditemukan!");
} else {
    const DATA = JSON.parse(raw.textContent);

    barLabels = DATA.barLabels || [];
    modulData = DATA.modulData || [];
    quizData = DATA.quizData || [];
    videoData = DATA.videoData || [];

    pieLabels = DATA.pieLabels || [];
    pieData = DATA.pieData || [];

    console.log("DATA:", DATA);
}

console.log("PIE:", pieLabels, pieData);

const barCanvas = document.getElementById('barChart');

if (barCanvas) {
    const barCtx = barCanvas.getContext('2d');

    if (window.myBarChart instanceof Chart) {
        window.myBarChart.destroy();
    }

    window.myBarChart = new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: barLabels,
            datasets: [
                {
                    label: 'Modul',
                    data: modulData,
                    backgroundColor: 'rgba(52, 152, 219, 0.7)'
                },
                {
                    label: 'Quiz',
                    data: quizData,
                    backgroundColor: 'rgba(231, 76, 60, 0.7)'
                },
                {
                    label: 'Video',
                    data: videoData,
                    backgroundColor: 'rgba(46, 204, 113, 0.7)'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false
        }
    });
} else {
    console.error("Canvas barChart tidak ditemukan!");
}

const pieCanvas = document.getElementById('pieChart');

if (pieCanvas) {
    const pieCtx = pieCanvas.getContext('2d');

    if (window.myPieChart instanceof Chart) {
        window.myPieChart.destroy();
    }

    window.myPieChart = new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: pieLabels,
            datasets: [{
                data: pieData,
                backgroundColor: [
                    '#3498db',
                    '#e74c3c',
                    '#2ecc71',
                    '#f1c40f',
                    '#9b59b6'
                ]
            }]
        },
        options: {
            responsive: true,
            animation: true
        }
    });
} else {
    console.error("Canvas pieChart tidak ditemukan!");
}