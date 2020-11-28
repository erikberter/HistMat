$(document).ready(function(e){

    let book_slug = $("#book_slug").val();
    let book_act_state = $("#book_state_button").attr('b_state');

    $("#book_state_dropdown > option").each(function(){
        if($(this).val() == book_act_state)
            $(this).attr("selected","selected");
        
    });

    $("#book_state_dropdown > option").click(function(){
        send_book_state_change_ajax(this.value, book_slug);
    })

    $("input[name='rating_v']").click( function(){
        $("#star-rating").submit();
    })
    $("#set-act-page").keypress(function(e){
        if(e.which == 13){
            let act_page = $(this).val();
            send_act_page_change_ajax(act_page, $(this).attr('b_slug'));
            $("#set-act-page").attr("placeholder", act_page);
            $("#set-act-page").val("");
        }
    });

});