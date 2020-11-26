/**
 * **Summary**. Filtering data used during the *send_book_lookup_ajax* function.
 */
var mycatalog_data = {
    "search_query" : "",
    "book_state" : "",
    "book_order" : "order-last-added"
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
            console.log(result);
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
            selected.push("#sortable-" + this.id.substring(3));
        }
    ); 
    
    var selected_id_string =  selected.join();

    $(selected_id_string).sortable({
        connectWith: ".connectedSortable",
        dropOnEmpty: true,
        receive: function( event, ui ) {
            let book_state = $(this).attr('shelf_name').trim();
            let book_slug = ui.item.attr('b_slug').trim();
            send_book_state_change_ajax(book_state, book_slug);
        }
    }).disableSelection();
}

/*
        MYCATALOG UTIL FUNCTIONS
*/

function send_book_state_request(elem){
    mycatalog_data["book_state"] = $("label[for=" + elem.id+"]").text().trim();
    send_book_lookup_ajax();
    $(elem).prop('checked',true);
}

function load_checked_filters(){
    $(".cb_filter_selector").each(function() {
        if(this.checked){
            delete_book_state_loaded_books(this);
            send_book_state_request(this);
        }else delete_book_state_loaded_books(this);
        
        refreshSortable();
    });
}

/*
        ONLOAD JQUERY
*/


$(document).ready(function() {
    
    /**
     *  **Summary**. On window load, check for default checked checkboxes.
     */
    load_checked_filters();

    $("input[type=radio][name=filter-order]").change(function(e){
        e.preventDefault();
        mycatalog_data["book_order"] = $(this).val();
        load_checked_filters();
    })

    /**
     * **Summary**. On change event for the book_shelf checkboxes in the filter section. 
     */
     /**
    $(".cb_filter_selector").change(function(e) {
        e.preventDefault();
        if(this.checked) send_book_state_request(this);
        else delete_book_state_loaded_books(this);
        
        refreshSortable();
    });
**/
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
        
        if($("#menu-toggle i.fa-angle-double-left").length>0)
            $("#menu-toggle i").removeClass('fa-angle-double-left').addClass("fa-angle-double-right");
        else
            $("#menu-toggle i").removeClass('fa-angle-double-right').addClass("fa-angle-double-left");
            
        
      });
      
});

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

var fab = new Vue({
    el: '#catalog-app',
    delimiters: ['[[', ']]'],
    data: {
        book_lists : {

        }
    },
    methods: {
        fab_action: function (event) {
            window.location = this.create_url;
        },
        load_books : function (book_state){
            axios.post(window.location.pathname, {
                book_state : book_state
            })
            .then(response => {
                this.book_lists[response.data.book_state] = {};
                this.book_lists[response.data.book_state].books = response.data.books;

                console.log("New book state " + response.data.book_state);
                console.log("books  " + this.book_lists[response.data.book_state].books.length);

                $('#container-'+response.data.book_state).remove();
                $('#book-to-add').append(result);
                
                refreshSortable();
            })
            .catch(error => {
                console.log(error)
            })
        }
    }
})