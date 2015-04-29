/**
 * Created by fanfan on 14-8-31.
 * Editored by guyaxian21@163.com
 */
$(function(){
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
            showComment(0);
    }).fail(function( jqxhr, textStatus, error ) {
            var err = textStatus + ", " + error;
            console.log( "Request Failed: " + err );
            $("#content").empty().append("Request Failed: " + err)
    });

});

function buildDiv(data){
    var arr=[["title1","comments1"],["title2","comments2"],["title3","comments3"],["title4","comments4"],["title5","comments5"]];
    var html="";
    var _header = '<div class="box">';
    var _header_welcome = '<div class="header">最新被删评论</div>';
    var _header_foot = '</div>';
    var _footer='<h4 class="title"><a href="javascript:" rel="nofollow" onclick="refreshComm();return false">更多热评...</a></h4>' + _header_foot;
    html = _header + _header_welcome;
    $.each(arr,function(ind,val){
        var _index=ind+1;
        var _title=data[val[0]][0];
        var _comments0=data[val[0]][0];
        var _comments=data[val[1]];
        var _html='<div class="cell" id=' + ind + '>'
            +'<div class="title">'
            +'<h3 class="toggleComments" onclick="toggleComm($(this))">'+_index+'<small>&gt;</small>'+_title.type+' - '+_title.title+'</h3>'
            +'<div style="padding-left: 25px"><p class="subtext pocket-inserted">'+'By <a href="javascript:">'+_title.up+'</a> | '+_title.postTime+' | <a target="_blank" href="http://'+_title.url+'#area-comment">评论'+_title.height+'</a> '+' | 详见&gt; '+'<a class="comhead" target="_blank" href="'+_title.url+'">ac'+_title.acid+'</a>'+'</p></div></div>';
        html += _html;
        html += '<div class="RightPost">' + '<h4><span class="badge-info">#' + _title.layer + '</span>&nbsp;<b>' + _title.userName + '</b>&nbsp</h4>' + '<p>' + _title.content + '</p></div>';
        //下面这段代码是做楼层叠加的，首页现在要展示被删评论，所以现在不需要了
        /*
        var _commentSubHtml="";
        $.each(_comments,function(ind2,val2){
            _commentSubHtml+='<div class ="comments">';
            _commentSubHtml+='<div class="author-comment add">'
                +'<span class="comhead"><a href="javascript:">' + val2.layer + 'L by ' + val2.userName+'</a></span></div>'
                +'<div class="comment add"><p>'+val2.content+'</p>'
                +'</div>';
        });
        $.each(_comments,function(){
            _commentSubHtml += '</div>';
        });
        var _commentHtml='<div class="hidden" style="margin-left:25px" id='+ ind +'-comments'+'>'
            +_commentSubHtml+'</div>';
        html += _commentHtml;*/
        html += '</div>';
    });
    $("#content").html(html+_footer);
    $('h3.toggleComments').hover(function () {
        $(this).attr({"title":'点击展开 | 收起热评'})
        }, function () {
            $(this).removeAttr('title')
        }
    );
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
