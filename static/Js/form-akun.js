document.addEventListener("DOMContentLoaded", () => {
    const raw = document.getElementById('form-data');

    if (!raw) {
        console.error("Data form tidak ditemukan!");
        return;
    }

    const DATA = JSON.parse(raw.textContent);

    const isEdit = DATA.isEdit;
    const user = DATA.user;

    if (isEdit && user) {

        // isi field
        document.querySelector('input[name="nama_lengkap"]').value = user.nama_lengkap || '';
        document.querySelector('input[name="username"]').value = user.username || '';
        document.querySelector('input[name="email"]').value = user.email || '';

        // set role
        document.querySelector('select[name="role"]').value = user.role || '';

        // password
        const passwordInput = document.querySelector('input[name="password"]');
        passwordInput.placeholder = "Kosongkan jika tidak ingin mengubah password";
        passwordInput.required = false;

        // form action
        document.querySelector('form').action = `/admin/update-user/${user.id}`;

        // tombol
        document.querySelector('button[type="submit"]').innerText = "Update Akun";

        // judul
        document.querySelector('h2').innerText = "Edit Akun";
    }
});