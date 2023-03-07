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
try {
    const animeScroll = ()=>{
    
        const windowTop = window.scrollY + window.innerHeight * 0.75;
        
        const target = document.querySelectorAll('[data-anime]');
        
        target.forEach((element)=>{
        (windowTop) > element.offsetTop
        ? element.classList.add('animate') : element.classList.remove('animate')
        })
        }

        window.addEventListener('scroll', animeScroll);
} catch(error) {
}

// modal animated for gallery
try {
    (()=>{
        const images = document.querySelectorAll('.C-gallery__image');
        let modal = document.querySelector('.C-modal');
        let modalImage = document.querySelector('.C-modal__image');
        const button = document.querySelector('.C-modal__button');

        images.forEach((element)=>{
            element.addEventListener("click", ()=>{
                let srcVal = element.getAttribute('src');
                modalImage.setAttribute('src', srcVal);
                modal.classList.toggle('C-modal__is_active');
            })
        })

        button.addEventListener("click", ()=>{
            modal.classList.toggle('C-modal__is_active');
        })
    })();
} catch(error) {
}

// button service delete
try {
    (()=>{
        const buttonDelete = document.querySelectorAll('.C-services_view_delete');

        buttonDelete.forEach((element)=>{
            element.addEventListener('submit', (event)=>{
                event.preventDefault();

                const toConfirm = confirm('Deseja realmente deletar o serviço?');

                if (toConfirm) {
                    element.submit();
                }
            })
        })
    })();
} catch(error) {
};
