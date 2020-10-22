
var mybooks_data = {
    "search_book" : "",
    "book_state" : "reading",
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
            book_order : mybooks_data["book_order"]
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
        mybooks_data["book_state"] = $(this).attr('name');
        $(".btn_filter_selector").removeClass("active");
        $(this).addClass("active");
        $('#catalog_book_title').empty().append($(this).val());
        send_mybook_ajax();
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