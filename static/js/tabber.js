document.querySelectorAll('.tabber__tab').forEach(tab => {
    tab.onclick = () => {
        const tabName = tab.innerText.toLowerCase().replaceAll(' ', '-');
        document.querySelector('.tabber__tab.active').classList.remove('active');
        tab.classList.add('active');
        document.querySelector('.tabber__content>.active').classList.remove('active');
        document.querySelector('.tabber__content>#'+tabName).classList.add('active');
    }
});
