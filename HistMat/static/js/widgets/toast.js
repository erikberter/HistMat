TITLE_INFORMATION = {
    'es' : 'Actualización Correcta',
    'en' : 'Correct Actualization',
    'eu' : 'Ez dakit euskera :C'
}

function load_toast(toast_text){
    $('.toast > .toast-body > p').text(toast_text);
    $('#toast-title').text(translate_text(TITLE_INFORMATION))
    $('.toast').toast({delay:2000});
    $('.toast').toast('show');
}