// menu and menu mobile
const menuMobile = document.querySelector('.C-menu__span');
menuMobile.addEventListener('click', () => {
    const menuNav = document.querySelector('.C-menu__nav');

    if (menuMobile.textContent == 'menu') {
        menuMobile.textContent = 'close';
        menuNav.classList.remove('is_hidden');
    } else {
        menuMobile.textContent = 'menu';
        menuNav.classList.add('is_hidden');
    };
})

// animate scroll
const animeScroll = ()=>{
 
    const windowTop = window.scrollY + window.innerHeight * 0.75;
    
    const target = document.querySelectorAll('[data-anime]');
    
     target.forEach((element)=>{
      (windowTop) > element.offsetTop
      ? element.classList.add('animate') : element.classList.remove('animate')
     })
    }
    
window.addEventListener('scroll', animeScroll);
