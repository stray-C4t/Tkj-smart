const observer = new IntersectionObserver((entries) => {
	entries.forEach((entry) => {
		if (entry.isIntersecting) {
			entry.target.classList.add('active');
		}
	});
}, {
	threshold: 0.1 
});
const revealElements = document.querySelectorAll('.reveal');
revealElements.forEach((el) => observer.observe(el));