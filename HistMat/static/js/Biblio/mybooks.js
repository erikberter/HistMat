
var mybooks_data = {
    "search_book" : "",
    "book_state" : "",
    "book_order" : "last_added"
}


$(document).ready(function(){
    $('#catalog_book_title').empty().append("Reading");
    $('.btn_filter_selector[value=Reading]').addClass("active");
    send_mybook_ajax();
});

function send_mybook_ajax(){
    $.ajax({
        type: "POST",
        url: "/biblio/mybooks",
        data: { 
            search_book : mybooks_data["search_book"],
            book_state : mybooks_data["book_state"],
            book_order : mybooks_data["book_order"],
            csrfmiddlewaretoken: window.CSRF_TOKEN
        },
        success: function(result) {
            $('#book-to-add').append(result);
            
        },
        error: function(result) {
            alert('error');
        }
    }); 
}

function refreshSortable(){
    var selected = [];
        $('.cb_filter_selector:checked').each(function() {
            selected.push("#Sortable" + $(this).val());
        });
        alert(selected.join());
$(selected.join() ).sortable({
        connectWith: ".connectedSortable",
        receive: function( event, ui ) {
            let book_state = $(this).attr('shelf_name');
            let bookPK = ui.item.attr('b_id');
            
            $.ajax({
                type: "POST",
                url: "/biblio/catalog/state_change",
                dataType:'json',
                data: { 
                    book_state : book_state,
                    csrfmiddlewaretoken: '{{ csrf_token }}',
                    book_pk : bookPK
                },
                error: function(result) {
                    alert('error');
                }
            });
        }
        }).disableSelection();
    
}

$(document).ready(function() {
    
    $(".cb_filter_selector").change(function(e) {
        e.preventDefault();
        
        if(this.checked) {
            mybooks_data["book_state"] = $(this).val();
            send_mybook_ajax();
            $(this).prop('checked',true);
        }else{
            $('#Container'+$(this).val()).remove();
            $(this).prop('checked',false);
        }
        refreshSortable();
        //$('#catalog_book_title').empty().append($("label[for="+$(this).attr("id") + "]").text());
        
    });
    $('#exampleFormControlInput1').keypress(function(e){
        if(e.which == 13){
            mybooks_data["search_book"] =  $('#exampleFormControlInput1').val();
            send_mybook_ajax();
        }
    });
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
      });
    
      
});