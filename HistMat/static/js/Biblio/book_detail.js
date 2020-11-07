$(document).ready(function(e){
    let book_act_state = $("#book_state_button").attr('b_state');
    $("#book_state_button > option").each(function(){
        if($(this).val() == book_act_state)
            $(this).attr("selected","selected");
        
    });
});