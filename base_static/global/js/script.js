// menu and menu mobile
try {
    const menuMobile = document.querySelector('.C-menu__span');
    menuMobile.addEventListener('click', () => {
        const menuNav = document.querySelector('.C-menu__nav');
        const menuButton = document.querySelector('.C-menu__button');

        if (menuMobile.textContent == 'close') {
            menuMobile.textContent = 'menu_open';
            menuNav.classList.add('is_hidden');
            menuButton.classList.remove('C-menu__button__is_fixed');
        } else {
            menuMobile.textContent = 'close';
            menuNav.classList.remove('is_hidden');
            menuButton.classList.add('C-menu__button__is_fixed');
        };
    })
} catch(error){}

// menu control after clicking the link
(()=>{
    try {
        const menuLink = document.querySelectorAll('.C-menu__link');
        const menuNav = document.querySelector('.C-menu__nav');
        const menuButton = document.querySelector('.C-menu__button');
        const menuMobile = document.querySelector('.C-menu__span');

        menuLink.forEach((element)=>{
            element.addEventListener("click", ()=>{
                menuNav.classList.toggle('is_hidden');
                menuButton.classList.toggle('C-menu__button__is_fixed');
                menuMobile.textContent = 'menu_open';
            })
        })
    } catch(error){}
})()

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

// function for delete object
function deleteObject(className, message) {
    const buttonDelete = document.querySelectorAll(className);

    buttonDelete.forEach((element)=>{
        element.addEventListener('submit', (event)=>{
            event.preventDefault();

            const toConfirm = confirm(message);

            if (toConfirm) {
                element.submit();
            }
        })
    })
}

// function delete object
function deleteObject(className, message) {
    const buttonDelete = document.querySelectorAll(className);
    
    buttonDelete.forEach((element)=>{
        element.addEventListener('submit', (event)=>{
            event.preventDefault();

            const toConfirm = confirm(message);

            if (toConfirm) {
                element.submit();
            }
        })
    })
}

// button service delete
try {
    const deleteService = deleteObject('.C-service__delete', 'Deseja realmente deletar o serviço?');
    deleteService();
} catch(error) {
}

// button image delete
try {
    const deleteImage = deleteObject('.C-image__delete', 'Deseja realmente deletar a imagem?');
    deleteImage();
} catch(error) {
}