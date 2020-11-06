function convertToSlug(Text){
    return Text
        .toLowerCase()
        .replace(/ /g,'_')
        ;
}


$(document).ready(function(){ 
    $('#book_state_dropdown > div > input').click(function(e){
        e.preventDefault();
        
        book_state = convertToSlug($(this).val());
        book_slug = $("#book_state_button").attr('b_slug');

        send_book_state_change_ajax(book_state, book_slug);
            
    });
});

