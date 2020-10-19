
var catalog_data = {
    "search_book" : "",
    "book_self" : "public",
    "book_order" : "last_added"
}

$(document).ready(function(){
    $('#catalog_book_title').empty().append("Public");
    send_catalog_ajax();
});

function send_catalog_ajax(){
    $.ajax({
        type: "POST",
        url: "/biblio/catalog",
        data: { 
            search_book : catalog_data["search_book"],
            book_self : catalog_data["book_self"],
            book_order : catalog_data["book_order"]
        },
        success: function(result) {
            
            $('#catalog_book_window').empty();
            $('#catalog_book_window').append(result);
            
        },
        error: function(result) {
            alert('error');
        }
    }); 
}



$(document).ready(function() {
    $(".btn_filter_selector").click(function(e) {
        e.preventDefault();
        catalog_data["book_self"] = $(this).attr('name');
        $('#catalog_book_title').empty().append($(this).val());
        send_catalog_ajax();
    });
    $('#exampleFormControlInput1').keypress(function(e){
        e.preventDefault();
        if(e.which == 13){
            catalog_data["search_book"] =  $('#exampleFormControlInput1').val();
            send_catalog_ajax();
        }
    });
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
      });
});