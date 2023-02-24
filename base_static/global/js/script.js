// animate scroll

const target = document.querySelectorAll('[data-anime]');
const animationClass = 'animate';

function animeScroll() {
    const windowTop = window.scrollY + (window.innerHeight * 0.75);
    
    target.forEach(function(element) {
        ((windowTop) > element.offsetTop) ?
            element.classList.add(animationClass):element.classList.remove('animate');
            console.log(element, element.offsetTop)
    });
}

animeScroll();
window.addEventListener('scroll', animeScroll);
