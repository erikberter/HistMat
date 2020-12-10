$(document).ready(function(e){

    let book_slug = $("#book_slug").val();
    let book_act_state = $("#book_state_dropdown").attr('b_state');

    $("#book_state_dropdown > option").each(function(){
        if($(this).val() == book_act_state)
            $(this).attr("selected","selected");
        
    });

    $("#book_state_dropdown").change(function(){
        send_book_state_change_ajax(this.value, book_slug);
        location.reload(); 
    });

    $("input[name='rating_v']").click( function(){
        $("#star-rating").submit();
    });
    $("#set-act-page").keypress(function(e){
        if(e.which == 13){
            let act_page = $(this).val();
            if(!$.isNumeric(act_page)){
                $( "#set-act-page" ).effect( "shake" , { direction: "up", times: 4, distance: 5});
                return;
            }else if(parseInt(act_page) > parseInt($("#npage").text()) || parseInt(act_page) < 0){
                $( "#set-act-page" ).effect( "shake" , { direction: "up", times: 4, distance: 5});
                return;
            }

            var result = send_act_page_change_ajax(act_page, window.location.pathname);
            if(result){
                $("#act-page").text(act_page);
                $("#act-page").fadeOut(300, function() {
                    $(this).text(act_page).fadeIn(300);
                 });
                $(this).val("");
                $(this).effect("highlight", {color: '#aaffaa' }, 1200);
            }else{
                alert("Error on the server side. Please reload and try again later.");
            }
            
            
        }
    });

});