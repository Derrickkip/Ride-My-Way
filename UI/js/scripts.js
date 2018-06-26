"use strict";
const nav_toggler = document.querySelector('.jsnavbar__toggle');
const nav_links = document.querySelector('.jsnavbar__links');

function show_nav() {
    nav_links.classList.toggle('nav_show');
}

function show_user_modal(event) {
    user_modal.classList.toggle('modal__show');
}

function show_car_modal(event) {
    car_modal.classList.toggle('modal__show');
}


function show_hidden(event) {
    const requests = event.target.nextElementSibling;

    requests.classList.toggle('show');
}

function close_modal(event) {
    const parent_modal = event.target.parentNode.parentNode.parentNode;
    parent_modal.classList.toggle('modal__show');
}

nav_toggler.addEventListener('click', show_nav);

const acc = document.querySelectorAll('.js_accordion');

if (acc) {
    for (let i = 0; i < acc.length; i++) {
        acc[i].addEventListener('click', show_hidden);
    }
}

const modal = document.querySelectorAll('.modal');

const edit_user = document.querySelector('#edit_user');

const edit_car = document.querySelector('#edit_car');

const user_modal = document.querySelector('#user_modal');

const car_modal = document.querySelector('#car_modal');

const close = document.querySelectorAll('.close');

if (edit_user) {

    edit_user.addEventListener('click', show_user_modal);
}

if (edit_car) {

    edit_car.addEventListener('click', show_car_modal);

}

if (close) {

    for (let i = 0; i < close.length; i++) {
        close[i].addEventListener('click', close_modal);
    }
}

window.onclick = function() {
    for (let i = 0; i < modal.length; i++) {
        if (event.target == modal[i]) {
            modal[i].classList.toggle('modal__show');
        }
    }
}