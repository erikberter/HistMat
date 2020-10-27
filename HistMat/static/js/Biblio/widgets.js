

var catalog_data_s = {
    "book_state" : "",
    "book_pk" : ""
}
function convertToSlug(Text)
{
    return Text
        .toLowerCase()
        .replace(/ /g,'_')
        ;
}

function send_change_state_ajax(){
    $.ajax({
        type: "POST",
        url: "/biblio/catalog/state_change",
        dataType:'json',
        data: { 
            book_state : catalog_data_s['book_state'],
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            book_pk : catalog_data_s['book_pk']
        },
        success: function(result) {
            $('.book_state_button[b_id='+ catalog_data_s['book_pk']+']').empty().append(catalog_data_s['book_state']);
        },
        error: function(result) {
            alert('error');
        }
    }); 
}


$(document).on('click', '.book_state_form_field', function(e){ 
    e.preventDefault();
    catalog_data_s['book_state'] = convertToSlug($(this).val());
    catalog_data_s['book_pk'] = $(this).attr('b_id');
    send_change_state_ajax();
});

