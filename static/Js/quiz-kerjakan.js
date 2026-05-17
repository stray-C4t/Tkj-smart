document.addEventListener("DOMContentLoaded", () => {

    const raw = document.getElementById('quiz-play-data');

    if (!raw) {
        console.error("Data quiz tidak ditemukan!");
        return;
    }

    const DATA = JSON.parse(raw.textContent);

    const soalData = DATA.soal || [];
    const quizId = DATA.quizId;

    let currentIdx = 0;
    let score = 0;
    let timer;
    const totalTime = 15;

    function loadQuestion() {
        if (!soalData.length) {
            document.getElementById('question-text').innerText = "Data soal tidak ditemukan.";
            return;
        }

        if (currentIdx >= soalData.length) {
            showFinalResult();
            return;
        }

        const data = soalData[currentIdx];

        document.getElementById('question-text').innerText = data.tanya;
        document.getElementById('current-quest-num').innerText = currentIdx + 1;

        const container = document.getElementById('options-container');
        container.innerHTML = '';

        data.opsi.forEach((text, i) => {
            const huruf = ["A", "B", "C", "D"][i];

            const btn = document.createElement('div');
            btn.className = 'option-box';

            btn.innerHTML = `<span class="opt-letter">${huruf}.</span> ${text}`;

            btn.onclick = () => handleSelection(btn, huruf, data.kunci);

            container.appendChild(btn);
        });

        startTimer();
    }

    function handleSelection(selectedBtn, selectedLetter, correctLetter) {
        clearInterval(timer);

        const allBtns = document.querySelectorAll('.option-box');
        allBtns.forEach(b => b.style.pointerEvents = 'none');

        if (selectedLetter === correctLetter) {
            selectedBtn?.classList.add('correct-anim');
            score += 100;
        } else {
            selectedBtn?.classList.add('wrong-anim');
            score = Math.max(0, score - 50);

            const correctIdx = ["A","B","C","D"].indexOf(correctLetter);
            allBtns[correctIdx]?.classList.add('correct-anim');
        }

        document.getElementById('score-val').innerText = score;

        setTimeout(() => {
            currentIdx++;
            loadQuestion();
        }, 1500);
    }

    function startTimer() {
        let timeLeft = totalTime;
        const bar = document.getElementById('timer-bar');

        if (bar) bar.style.width = '100%';

        clearInterval(timer);

        timer = setInterval(() => {
            timeLeft -= 0.1;

            let width = (timeLeft / totalTime) * 100;
            if (bar) bar.style.width = width + '%';

            if (timeLeft <= 0) {
                clearInterval(timer);
                handleSelection(null, '', soalData[currentIdx].kunci);
            }
        }, 100);
    }

    function showConfetti() {
        const duration = 2500;
        const end = Date.now() + duration;

        (function frame() {
            confetti({
                particleCount: 5,
                angle: 60,
                spread: 80,
                origin: { x: 0 }
            });

            confetti({
                particleCount: 5,
                angle: 120,
                spread: 80,
                origin: { x: 1 }
            });

            if (Date.now() < end) {
                requestAnimationFrame(frame);
            }
        })();
    }

    function showFinalResult() {
        document.getElementById('quiz-content').style.display = 'none';
        document.getElementById('options-container').style.display = 'none';

        document.getElementById('result-screen').classList.remove('hidden');
        showConfetti();
        document.getElementById('final-score').innerText = score;

        fetch('/submit-quiz', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                quiz_id: quizId,
                score: score,
                max_score: soalData.length * 100
            })
        });
    }

    // START
    loadQuestion();

});

