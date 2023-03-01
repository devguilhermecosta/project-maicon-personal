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


// animate gallery
(()=>{
    const imageContainer = document.querySelectorAll('.glass_image');

    const body = document.querySelector('.C-body');

    imageContainer.forEach((element)=>{
        element.addEventListener('click', ()=>{
            
            let d = document.createElement('div');
            let image = element.parentElement.lastElementChild;
           
                d.classList.add('is_back');
                image.classList.add('full_page');
                d.appendChild(image);
                body.appendChild(d);
                console.log('abri');

                image.addEventListener("click", ()=>{
                    image.classList.remove('full_page');
                    image.classList.add('is_hidden');
                    d.classList.remove('is_back');
                    d.classList.add('is_hidden');
                })
             
        });
    })
})();


// (()=>{
//     const imageAnimated = document.querySelector('.full_page');
//     imageAnimated.addEventListener("click", ()=>{
//         console.log('cliquei');
//     })
// })();