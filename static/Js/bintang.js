const container = document.getElementById('star-container');
for (let i = 0; i < 50; i++) {
    const star = document.createElement('div');
    star.className = 'star';
    star.style.setProperty('--top-offset', Math.random() * 100 + 'vh');
    star.style.setProperty('--fall-duration', (Math.random() * 6 + 6) + 's');
    star.style.setProperty('--fall-delay', (Math.random() * 10) + 's');
    star.style.setProperty('--star-tail-length', (Math.random() * 2 + 5) + 'em');
    container.appendChild(star);
}