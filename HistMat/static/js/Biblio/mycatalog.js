/**
 * **Summary**. Filtering data used during the *send_book_lookup_ajax* function.
 */
var mycatalog_data = {
    "search_query" : "",
    "book_state" : "",
    "book_order" : "last_added"
}

/*
        AJAX FUNCTIONS
*/

/**
 * **Summary**. Sends AJAX request to the server to get a HTML with the books inside
 * 
 * **Description**. Sends the server an AJAX request with the filters used inside the query. 
 *              The filters sent are based on the input in the left-side filtering panel.
 */
function send_book_lookup_ajax(){
    $.ajax({
        type: "POST",
        url: "/biblio/mycatalog",
        data: { 
            search_query : mycatalog_data["search_query"],
            book_state : mycatalog_data["book_state"],
            book_order : mycatalog_data["book_order"],
            csrfmiddlewaretoken: window.CSRF_TOKEN
        },
        success: function(result) {
            $('#book-to-add').append(result);
            refreshSortable();
        },
        error: function(result) {
            alert('error');
        }
    }); 
}

/*
        JQUERY UI FUNCTIONS
*/

/**
 * **Summary**. Refreshes the Sortable div.
 * 
 * **Description**. Creates a list of id's with all checked checkboxes in the filter sections
 *              and then makes the whole list of *div's* connected lists so one can drag 
 *              and drop between them.
 */
function refreshSortable(){
    var selected = [];
    $('.cb_filter_selector:checked').each(
        function() {
            selected.push("#Sortable" + $(this).val());
        }
    ); 
    
    var selected_id_string =  selected.join();

    $(selected_id_string).sortable({
        connectWith: ".connectedSortable",
        dropOnEmpty: true,
        receive: function( event, ui ) {
            let book_state = $(this).attr('shelf_name');
            let book_slug = ui.item.attr('b_slug');
            
            send_book_state_change_ajax(book_state, book_slug);
        }
    }).disableSelection();
}

/*
        MYCATALOG UTIL FUNCTIONS
*/

function send_book_state_request(elem){
    mycatalog_data["book_state"] = $(elem).val();
    send_book_lookup_ajax();
    $(elem).prop('checked',true);
}

function delete_book_state_loaded_books(elem){
    $('#Container'+$(elem).val()).remove();
    $(elem).prop('checked',false);
}

/*
        ONLOAD JQUERY
*/


$(document).ready(function() {
    
    /**
     * **Summary**. On change event for the book_shelf checkboxes in the filter section. 
     */
    $(".cb_filter_selector").change(function(e) {
        e.preventDefault();
        
        if(this.checked) send_book_state_request(this);
        else delete_book_state_loaded_books(this);
        
        refreshSortable();
    });

    /**
     * **Summary**. KeyPress event listener for the enter key on the search bar.
     */
    $('#exampleFormControlInput1').keypress(function(e){
        if(e.which == 13){
            mycatalog_data["search_query"] =  $('#exampleFormControlInput1').val();
            send_book_lookup_ajax();
        }
    });

    /**
     * **Summary**. On click listener for the filter menu toggle button.
     */
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
      });
    

    // On page loaded script
    // Sends the basic book_shelf to load
      
})