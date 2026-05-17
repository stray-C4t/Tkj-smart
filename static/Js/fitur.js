document.addEventListener("DOMContentLoaded", () => {

    const raw = document.getElementById('guru-data');

    if (!raw) {
        console.error("Data guru tidak ditemukan!");
        return;
    }

    const dataGuru = JSON.parse(raw.textContent);

    let centerIndex = 1;

    function renderGuru() {
        const display = document.getElementById('guru-display');
        if (!display) return;

        display.innerHTML = '';

        const offsets = [-2, -1, 0, 1, 2];

        offsets.forEach(offset => {
            let targetIndex = (centerIndex + offset + dataGuru.length) % dataGuru.length;
            const g = dataGuru[targetIndex];

            const statusClass = (offset === 0) ? 'focus' : 'side';

            display.innerHTML += `
                <div class="card-guru ${statusClass}">
                    <img src="${g.img}" class="foto-kubah">
                    <div class="nama-box">${g.nama}</div>
                    <div class="mapel-box">${g.mapel}</div>
                </div>
            `;
        });

        console.log("Guru tengah index:", centerIndex);
        console.log("Nama guru tengah:", dataGuru[centerIndex]?.nama);
    }

    // 🔥 penting: biar bisa dipanggil dari HTML
    window.moveSlider = function(direction) {
        centerIndex = (centerIndex + direction + dataGuru.length) % dataGuru.length;
        renderGuru();
    };

    renderGuru();
});

const radios = document.querySelectorAll('input[name="radio-card"]');
const bg = document.querySelector('.fitur-bg');
function updateBackground() {
	const active = document.querySelector('input[name="radio-card"]:checked');
	if (!active) return;
	const img = active.dataset.img;
	bg.style.backgroundImage = `url('${img}')`;
}
window.addEventListener('load', updateBackground);
radios.forEach(r => {
	r.addEventListener('change', updateBackground);
});

const radiosAuto = document.querySelectorAll('input[name="radio-card"]');
let currentIndex = 0;
function autoSlide() {
	radiosAuto[currentIndex].checked = false;
	currentIndex = (currentIndex + 1) % radiosAuto.length;
	radiosAuto[currentIndex].checked = true;
	const event = new Event('change');
	radiosAuto[currentIndex].dispatchEvent(event);
}
setInterval(autoSlide, 5000);

new Swiper('.card-wrapper', {  
	loop: true,
	speed: 600,
	centeredSlides: true,
	centeredSlidesBounds: true,
	slidesPerView: 7,
	spaceBetween: 25,
	grabCursor: true,
	autoplay: {
		delay: 3000,
		disableOnInteraction: false,
	},
	navigation: {  
		nextEl: '.swiper-button-next',  
		prevEl: '.swiper-button-prev',  
	},
	breakpoints: {
		0: { slidesPerView: 1 },
		768: { slidesPerView: 3 },
		1024: { slidesPerView: 5 },
		1024: { slidesPerView: 5 },
		1280: { slidesPerView: 5 },
	}
});

const accordionBtns = document.querySelectorAll(".item__header");
accordionBtns.forEach((header) => {
    header.addEventListener("click", function () {
        const item = this.parentElement;
        const content = this.nextElementSibling;
        document.querySelectorAll(".accordion__item").forEach(i => {
            if (i !== item) {
                i.classList.remove("active");
                i.querySelector(".item__content").style.maxHeight = null;
            }
        });
        item.classList.toggle("active");
        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        }
    });
});