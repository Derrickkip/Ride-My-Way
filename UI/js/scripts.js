const nav_toggler = document.querySelector('.jsnavbar__toggle');
const nav_links = document.querySelector('.jsnavbar__links');

const acc = document.querySelectorAll('.js_accordion');

nav_toggler.addEventListener('click', show_nav);

function show_nav() {
    nav_links.classList.toggle('nav_show');
}


for (let i = 0; i < acc.length; i++) {
    acc[i].addEventListener('click', show_hidden);
}

function show_hidden(event) {
    const requests = event.target.nextElementSibling;

    requests.classList.toggle('show');
}