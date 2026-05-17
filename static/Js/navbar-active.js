const sections = document.querySelectorAll("[id]");
const navLinks = document.querySelectorAll(".nav-link");

function updateActiveLink() {
    let current = "";

    sections.forEach(section => {
        const top = section.offsetTop;
        const height = section.offsetHeight;

        if (window.scrollY >= top - 200 &&
            window.scrollY < top + height - 200) {
            current = section.id;
        }
    });

    // kalau mentok bawah halaman → paksa kontak aktif
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 10) {
        current = "kontak";
    }

    navLinks.forEach(link => {
        link.classList.remove("active");

        if (link.getAttribute("href") === `#${current}`) {
            link.classList.add("active");
        }
    });
}

window.addEventListener("scroll", updateActiveLink);
window.addEventListener("load", updateActiveLink);