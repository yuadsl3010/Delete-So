<<<<<<< .mine
/**
 * Created by fanfan on 14-8-31.
 */
$(function(){
    $.ajax({
        url:"http://basiltest.duapp.com/asset/getComment.php",
        type:"GET",
        dataType:"json",
        beforeSend:function(){
            $("#content").append("Loading...")
        }
        }).done(function( json ) {
            $("#content").empty();
            buildDiv(json);
        })
        .fail(function( jqxhr, textStatus, error ) {
            $("#content").empty();
            var err = textStatus + ", " + error;
            console.log( "Request Failed: " + err );
            $("#content").append("Request Failed: " + err)
        });

});

function buildDiv(data){
    var arr=[["title1","comments1"],["title2","comments2"],["title3","comments3"],["title4","comments4"],["title5","comments5"]];
    var html="";
    var _footer='<tr></tr><tr><td colspan="2"></td><td class="title"><a href="javascript:" rel="nofollow">More</a></td></tr>';
    $.each(arr,function(ind,val){
        var _index=ind+1;
        var _title=data[val[0]][0];
        var _comments=data[val[1]];
        var _html='<div id='+ ind +'>'
            +'<div class="title">'+ '<h3 class="toggleComments" onclick="toggleComm($(this))">'+_index+'<small>&gt;</small>'+_title.type+' - '+_title.title+'</h3>'
            +'<p class="subtext pocket-inserted">'+' By <a href="javascript:">'+_title.up+'</a> | '+_title.time+' | <a target="_blank" href="http://'+_title.url+'#area-comment">评论'+_title.commentsN+'</a> '+' | 详见&gt; '+'<a class="comhead" target="_blank" href="http://'+_title.url+'">'+_title.url.match(/ac\d+$/)[0]+'</a>'+'</p></div>';
        html+=_html;
        var _commentSubHtml="";
        $.each(_comments,function(ind2,val2){
            _commentSubHtml+='<div class="author-comment last">'
                +'<span class="comhead"><a href="javascript:">'+val2.userName+'</a> | '+val2.postDate+'</span></div><br>'
                +'<div class="comment"><p>'+val2.content+'</p></div>';
        });
        var _commentHtml='<div class="comments hidden" id='+ ind +'-comments'+'>'
            +_commentSubHtml+'</div>';
        html+=_commentHtml;
    });
    $("#content").html(html+_footer);
}

function toggleComm(param) {
    var toggleDivId = 'div#'+param.parent().parent().attr('id')+'-comments';
    param.parent().parent().find(toggleDivId).toggleClass('hidden');
    param.stopPropagation();
}
=======
/**
 * Created by fanfan on 14-8-31.
 */
$(function(){

    $("#content").on("click",".toggleComments",function(e){
        var that=$(this);
        var thatCom=that.parent().parent().next().next().next();
        //that.parent().prev().find('.votearrow').css('transform','rotate(180deg)');
        if(thatCom.css("display")=="none"){
            thatCom.show(200).siblings('.comments').hide(100);
            $("#content tr").not('.comments').find('.votearrow').css('transform','rotate(0deg)');
            that.parent().prev().find('.votearrow').css('transform','rotate(180deg)');
        }else{
            thatCom.hide(100);
            that.parent().prev().find('.votearrow').css('transform','rotate(0deg)');
        }

    })

    $.ajax({
        url:"http://basiltest.duapp.com/asset/getComment.php",
        type:"GET",
        dataType:"json",
        beforeSend:function(){
            $("#content").append("<center>Loading...</center>")
        }
        }).done(function( json ) {
            $("#content").empty();
            bulidTable(json);
        })
        .fail(function( jqxhr, textStatus, error ) {
            $("#content").empty();
            var err = textStatus + ", " + error;
            console.log( "Request Failed: " + err );
            $("#content").append("Request Failed: " + err)
        });
});

function bulidTable(data){
    var arr=[["title1","comments1"],["title2","comments2"],["title3","comments3"],["title4","comments4"],["title5","comments5"]]
    var html="";
    var _footer='<tr style="height:10px"></tr><tr><td colspan="2"></td><td class="title"><a href="javascript:" rel="nofollow">More</a></td></tr>';
    $.each(arr,function(ind,val){
        var _index=ind+1;
        var _title=data[val[0]][0];
        var _comments=data[val[1]];
        var _html='<tr><td align="right" valign="middle" class="title">'+_index+'.</td>'
            +'<td><center><a href="javascript:"><div class="votearrow" title="upvote"></div></a><span></span></center></td>'
            +'<td class="title"><a href="index-new.html#'+val[0]+'" class="toggleComments" id="'+val[0]+'">'+_title.type+' - '+_title.title+'</a><span class="comhead"> (<a target="_blank" href="http://'+_title.url+'">'+_title.url.match(/ac\d+$/)[0]+'</a>) </span></td></tr>'
            +'<tr><td colspan="2"></td>'
            +'<td class="subtext pocket-inserted"><span>'+_title.click+' 点击</span> by <a href="javascript:">'+_title.up+'</a> '+_title.time+' | <a target="_blank" href="http://'+_title.url+'#area-comment">'+_title.commentsN+' 评论</a></td></tr>'
            +'<tr style="height:5px"></tr>';
        html+=_html;

        var _commentSubHtml="";
        $.each(_comments,function(ind2,val2){
            _commentSubHtml+='<tr><td><img src="asset/image/post/s.gif" height="1" width="0" style="height:1px;width:0px;"></td><td valign="top"><center><a href="javascript:"><div class="votearrow" title="upvote"></div></a><span></span></center></td><td class="default"><div style="margin-top:1px; margin-bottom:-10px; "><span class="comhead"><a href="javascript:">'+val2.userName+'</a> | <a href="javascript:">'+val2.postDate+'</a></span></div><br>'
                +'<span class="comment"><p style="color:#000">'+val2.content+'</p></span></td></tr>';
        })

        var _commentHtml='<tr class="comments"><td colspan="2"></td><td><table border="0"><tbody>'+_commentSubHtml+_commentSubHtml+_commentSubHtml+'</tbody></table></td></tr>';

        html+=_commentHtml;
    });

    $("#content").append(html+_footer);

};



>>>>>>> .r217
