document.addEventListener("DOMContentLoaded", () => {

    const raw = document.getElementById('video-data');

    if (!raw) {
        console.error("Data video tidak ditemukan!");
        return;
    }

    const DATA = JSON.parse(raw.textContent);

    const isEdit = DATA.isEdit;
    const video = DATA.video;

    if (isEdit && video) {

        // isi field
        document.querySelector('input[name="judul"]').value = video.judul || '';
        document.querySelector('input[name="youtube_id"]').value = video.youtube_id || '';

        // optional
        if (video.durasi) {
            document.querySelector('input[name="durasi"]').value = video.durasi;
        }

        if (video.deskripsi) {
            document.querySelector('textarea[name="deskripsi"]').value = video.deskripsi;
        }

        // ubah form action
        document.querySelector('form').action = `/admin/update-video/${video.id}`;

        // tombol
        document.querySelector('button[type="submit"]').innerText = "Update Video";

        // judul halaman
        document.querySelector('h2').innerText = "Edit Video Tutorial";
    }

});