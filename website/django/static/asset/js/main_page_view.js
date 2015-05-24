/**
 * Created by fanfan on 14-8-31.
 * Editored by yuzhenchuan, guyaxian
 */

$(function(){
    var url = "json/refresh_main_page_view/";
    $.get(url,
        function(json){
            $("#content").empty();
            buildDiv(json);
        }
    );
});

function buildDiv(data){
    var arr = [["title1","comments1"],["title2","comments2"],["title3","comments3"],["title4","comments4"],["title5","comments5"]];
    var html = "";
    var _header = '<div class="box text-center">';
    var _header_welcome = '<h2>最新被删评论</h2>';
    var _header_foot = '</div>';
    var _footer = '';//'<h4 class="title"><a href="javascript:" rel="nofollow" onclick="refreshComm();return false">更多热评...</a></h4>' + _header_foot;
    html = _header + _header_welcome;
    html = html + build_ac_comments(data.contents_view);
    $("#content").html(html+_footer);
}

function toggleComm(param) {
    var toggleDivId = 'div#'+param.parent().parent().attr('id')+'-comments';
    param.parent().parent().find(toggleDivId).toggleClass('hidden');
    param.stopPropagation();

}

function refreshComm(){
    $("#content").empty();
    $.ajax({
        url:"http://www.delete.so/asset/getComment.php",
        type:"GET",
        dataType:"json",
        beforeSend:function(){
            $("#content").append('<p id ="loading">热评正在加载...</p>');
            $('p#loading').animate({opacity: 0.1}, {duration: 3000});
        }
    }).done(function( json ) {
            $("#content").empty();
            buildDiv(json);
            
    }).fail(function( jqxhr, textStatus, error ) {
            var err = textStatus + ", " + error;
            console.log( "Request Failed: " + err );
            $("#content").empty().append("Request Failed: " + err)
    });
    $('#cancel-button').click();
}
