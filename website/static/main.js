const openBtn = document.getElementById('game-config');
const modalOverlay = document.querySelector('.game-setup-container');
const closeSetup = document.querySelector('.game-setup-close');
const contentBlur = document.getElementById('content');

openBtn.addEventListener('click', () => {
    modalOverlay.classList.add('open-modal');
    contentBlur.classList.add('blur-bg');    
});

closeSetup.addEventListener('click', () => {
    modalOverlay.classList.remove('open-modal');
    contentBlur.classList.remove('blur-bg');
});