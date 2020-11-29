/**
 * **Summary**. Sends and AJAX request to the server to change the state of a book.
 * 
 * @param {string} book_state 
 * @param {string} book_slug 
 */
function send_book_state_change_ajax(book_state, book_slug){
    $.ajax({
        type: "POST",
        url: '/biblio/book_detail/'+book_slug+'/state_change',
        dataType:'json',
        data: { 
            book_state : book_state,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        success: function(result){
            $('#book_state_button').empty().append(book_state);
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
        url: pre_url+'/page_change',
        dataType:'json',
        data: { 
            act_page : act_page,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        success: function(result){
        },
        error: function(result) {
            result = false;
        }
    });
    return result;
}