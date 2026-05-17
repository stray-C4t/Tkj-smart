document.addEventListener("DOMContentLoaded", () => {

    const raw = document.getElementById('modul-form-data');

    if (!raw) {
        console.error("Data modul tidak ditemukan!");
        return;
    }

    const DATA = JSON.parse(raw.textContent);

    const isEdit = DATA.isEdit;
    const modul = DATA.modul;

    // 🔥 INIT SUMMERNOTE
    $('#summernote').summernote({
        placeholder: 'Tulis tutorial atau materi TKJ di sini...',
        height: 300,
        toolbar: [
            ['style', ['style']],
            ['font', ['bold', 'underline', 'clear']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['insert', ['link', 'picture', 'video']],
            ['view', ['fullscreen', 'codeview', 'help']]
        ]
    });

    // 🔥 MODE EDIT
    if (isEdit && modul) {

        // isi field
        document.querySelector('input[name="judul"]').value = modul.judul || '';
        document.querySelector('select[name="kategori"]').value = modul.kategori || '';
        document.querySelector('select[name="icon"]').value = modul.icon || '';
        document.querySelector('textarea[name="deskripsi_singkat"]').value = modul.deskripsi_singkat || '';

        // 🔥 isi summernote (penting)
        $('#summernote').summernote('code', modul.konten || '');

        // form action
        document.querySelector('form').action = `/admin/update-modul/${modul.id}`;

        // tombol
        document.querySelector('button[type="submit"]').innerText = "Update Modul";

        // judul
        document.querySelector('h2').innerText = "Edit Modul";
    }

});