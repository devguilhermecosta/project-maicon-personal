const menuMobile = document.querySelector('.c-header__nav_menu_mobile').addEventListener("click", controlMenu)

function controlMenu() {
    const navMenuUl = document.querySelector('.c-header__ul');
    const navMenu = document.querySelector('.c-header__nav');
    const iconMenu = document.querySelector('.c-header__nav_menu_mobile');

    if (navMenuUl.classList.contains('is_closed')) {
        navMenuUl.classList.remove('is_closed');
        navMenuUl.classList.add('is_open');
        navMenu.style.width = '150px';
        iconMenu.style.right = '150px';
        iconMenu.textContent = 'close';
    } else {
        navMenuUl.classList.remove('is_open');
        navMenuUl.classList.add('is_closed');
        navMenu.style.width = '5px';
        iconMenu.style.right = '5px';
        iconMenu.textContent = 'menu';
    };
};

(function() {
    const menuLink = document.querySelectorAll('.c-header__link');

    for (const link of menuLink) {
        link.addEventListener("click", controlMenu);
    }
})();

(function() {
    const benefitIntro = document.querySelectorAll('.c-main__benefit');

    for (const benefit of benefitIntro) {
        if (benefit.classList.contains('is_left')) {
            benefit.style.left = 0;
            benefit.style.opacity = 1;
        } else if (benefit.classList.contains('is_right'))
            benefit.style.right = 0;
            benefit.style.opacity = 1;
        };
})();