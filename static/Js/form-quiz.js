document.addEventListener("DOMContentLoaded", () => {

    const raw = document.getElementById('quiz-data');

    if (!raw) {
        console.error("Data quiz tidak ditemukan!");
        return;
    }

    const DATA = JSON.parse(raw.textContent);

    let isEdit = DATA.isEdit;
    let quiz = DATA.quiz;
    let quizId = quiz ? quiz.id : null;
    let questions = DATA.questions || [];

    // LOAD DATA
    if (isEdit && quiz) {
        document.getElementById("judul").value = quiz.judul || '';
        document.getElementById("icon").value = quiz.icon || '';
    }

    renderList();

    // TAMBAH SOAL
    window.tambahSoal = function () {
        let pertanyaan = document.getElementById("pertanyaan").value;

        if (!pertanyaan.trim()) {
            alert("Pertanyaan tidak boleh kosong!");
            return;
        }

        let q = {
            pertanyaan: pertanyaan,
            a: document.getElementById("a").value,
            b: document.getElementById("b").value,
            c: document.getElementById("c").value,
            d: document.getElementById("d").value,
            jawaban: document.getElementById("jawaban").value
        };

        questions.push(q);
        renderList();

        // reset
        document.getElementById("pertanyaan").value = "";
        document.getElementById("a").value = "";
        document.getElementById("b").value = "";
        document.getElementById("c").value = "";
        document.getElementById("d").value = "";
    };

    // HAPUS SOAL
    window.hapusSoal = function (index) {
        questions.splice(index, 1);
        renderList();
    };

    // RENDER LIST
    function renderList() {
        let list = document.getElementById("list-soal");
        list.innerHTML = "";

        questions.forEach((q, i) => {
            let li = document.createElement("li");
            li.innerHTML = `
                ${i + 1}. ${q.pertanyaan}
                <button onclick="hapusSoal(${i})" style="margin-left:10px;">❌</button>
            `;
            list.appendChild(li);
        });
    }

    // SIMPAN
    window.simpanSemua = function () {
        let data = {
            judul: document.getElementById("judul").value.trim(),
            icon: document.getElementById("icon").value,
            questions: questions
        };

        console.log("DEBUG:", data);

        if (data.judul === "" || questions.length === 0) {
            alert("Judul dan soal harus diisi!");
            return;
        }

        let url = isEdit
            ? `/admin/update-quiz/${quizId}`
            : `/admin/save-full-quiz`;

        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(res => {
            if (!res.ok) {
                throw new Error("Server error: " + res.status);
            }
            return res.json();
        })
        .then(res => {
            console.log("Response:", res);
            alert("Berhasil disimpan!");
            window.location.href = "/admin/dashboard";
        })
        .catch(err => {
            console.error("ERROR:", err);
            alert("Terjadi error! Cek console (F12)");
        });
    };

});