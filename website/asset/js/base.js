function smooth_move_herf(para){
    var pos = $(para).offset().top - 30;
    $("html,body").animate({scrollTop: pos}, 1000); 
    return false;
}

function checkSearch() 
{   
    var search = document.getElementById('search');
    search.setCustomValidity("格式不正确哟，eg：'ac1205967'或者'带带我'");
}  