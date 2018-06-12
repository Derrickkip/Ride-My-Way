const nav_toggler = document.querySelector('.navtoggle');
const nav_links = document.querySelector('.nav_pull_right');

nav_toggler.addEventListener('click', show_nav);

function show_nav() {
    nav_links.classList.toggle('nav_show');
}