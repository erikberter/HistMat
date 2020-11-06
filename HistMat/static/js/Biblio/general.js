/**
 * **Summary**. Sends and AJAX request to the server to change the state of a book.
 * 
 * @param {string} book_state 
 * @param {string} book_slug 
 */
function send_book_state_change_ajax(book_state, book_slug){
    $.ajax({
        type: "POST",
        url: '/biblio/catalog/'+book_slug+'/state_change',
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