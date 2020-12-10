
TOAST_RESPONSE = {
    'book_page_change' : {
        'es' : 'Se ha cambiado la pagina correctamente',
        'en' : 'Page was correctly changed',
        'eu' : 'Pagina ondo aldatu da?'
    },
}




/**
 * **Summary**. Sends and AJAX request to the server to change the state of a book.
 * 
 * @param {string} book_state 
 * @param {string} book_slug 
 */
function send_book_state_change_ajax(book_state, book_slug){
    let book_state_s = book_state;
    $.ajax({
        type: "post",
        url: '/es/biblio/book_detail/'+book_slug+'/state_change',
        dataType:'json',
        data: { 
            book_state : book_state,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        success: function(result){
            $("#book_state_dropdown > option").each(function(){
                if($(this).val() == book_act_state)
                    $(this).attr("selected","selected");
            });
        },
        error: function(result) {
            alert('error');
        }
    });
}

/**
 * **Summary**. Sends and AJAX request to the server to change the page of a book.
 * 
 * @param {string} book_state 
 * @param {string} book_slug 
 */
function send_act_page_change_ajax(act_page, pre_url){
    var result = true;
    $.ajax({
        type: "POST",
        url: pre_url+'page_change',
        dataType:'json',
        data: { 
            act_page : act_page,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        success: function(result){
            var toast_text = translate_text(TOAST_RESPONSE['book_page_change']);
            load_toast(toast_text);
        },
        error: function(result) {
            result = false;
        }
    });
    return result;
}