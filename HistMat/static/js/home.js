$(document).ready(function(){
    $(".home_action").each(function(i){
        $(this).delay(100*i).show("slide", { direction: "left" }, 1000);
    });
});