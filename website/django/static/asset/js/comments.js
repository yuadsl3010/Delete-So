/**
 * Created by yuzhenchuan on 2015/5/12.
 *
 */

function showComment(page) {
    var url = "json/refresh_ds_comments/";
    //$("#ds_comments").html("");
    $.get(url,
        {
            'page': page,
        }, 
        function(json){
            var str = "";
            var comment_date = "";
            var comment2_date = "";
            var total = json.total;
            $.each(json.result, function (index, content){
                comment_date = JSON.stringify(content.postDate).replace(/T/gm, ' ').replace(/"/gm, '');
                str += '<div class="author_comment">' + '<label id="' + (index + 1) + '" style="display:none">' + content.cid + '</label>'+ "<span class=\"badge badge-info\">#" + (index + 1) + '</span>&nbsp;' +'<a class="name">' + content.userName + '</a>' + "<span class='time'>" + comment_date + "</span>"+'<span class="area-tool-comment"><a class="btn-quote" onclick="quoteComm($(this))">[回复]</a></span>';
                str += '<div class="content-comment">' + content.contents + "</div>";
                $.each(content.comment2, function (index2, content2){
                    comment2_date = JSON.stringify(content2.postDate).replace(/T/gm, ' ').replace(/"/gm, '');
                    str += '<div class="author_comment last"><a class="name"> &nbsp;' + content2.userName + '</a>' + "<span class='time'>" + comment2_date + "</span>"  + '<span class="area-tool-comment"><a class="btn-quote" onclick="quoteComm($(this))">[回复]</a></span>'+'<div class="content-comment">' + content2.contents + "</div></div>";
                });

                str += "</div>";
            });

            str += $.MakePages({num: page + 1, count: total, size: 10, "long": 5}, 'contact', 'reComm');
            $("#ds_comments").html(str);
        }
    );
}

function sendComment(param){
    var url = "json/refresh_ds_comments/";
    var textMsg = param.textMsg;
    var posMsg = param.posMsg || '0';
    var nameMsg = param.nameMsg;
    if (!textMsg){
        send_warn("<span>留言失败!</span></br>请不要空评论就发送好么？");
        return false;
    }

    if (nameMsg == ""){
        nameMsg = "匿名用户";
    }

    $.post(url,
        {
            'username': nameMsg,
            'content': textMsg,
            'position': posMsg,
        },
        function(json){
            var status = json.status;
            showComment(0);
            if (status == 'bad word!')
            {
                send_warn("<span>留言失败!</span></br>留言包含敏感词！");
            }
            else
            {
                send_ok("<span>留言成功!</span></br>欢迎提出建议和想法~");
            }
        }
    );
}


function quoteComm(param) {
    var posMsg;
    var width_bak = 0;
    UE.getEditor('editor').setContent('');
    $('#goComment1').remove();
    $('button#send-button').addClass('hidden');
    var area, content, editor, shadow;
    var hotDiv = '<div id="goComment1" class="hotComment1 panel-footer">';
    hotDiv += '</div>';
    param.parent().parent().find('div.content-comment:first').after(hotDiv);
    area = $("#goComment");
    width_bak = area.width();
    shadow = $("#goComment1");
    $("button#cancel-button, #item-editor-shadow, button#send-button-1").removeClass("hidden");
    shadow.css({height: 357});
    area.css({width: shadow.width() + 2});
    area.css({display: "block", position: "absolute", left: shadow.offset().left, top: shadow.offset().top + 30}).animate({opacity: 1});

    area.on('click', 'button#send-button-1', function (e){
        e.stopPropagation();
        posMsg = param.parent().parent().find('label').text() || param.parent().parent().parent().find('label').text();
        contentMsg = UE.getEditor('editor').getContent();
        UE.getEditor('editor').setContent('');

        $('button#cancel-button, #send-button-1').addClass('hidden');
        $('#goComment1').remove();
        $('button#send-button').removeClass('hidden');
        area.css({
            position: "relative",
            top: 0, 
            left: 0, 
            width: width_bak
        });
        sendComment({
            textMsg: contentMsg, 
            nameMsg: $("#nameInput").val().replace(/\s/g, ""), 
            posMsg: posMsg
        });
        smooth_move_herf('#contact');
        area.off('click', 'button#send-button-1');
        //location.reload();
    });

    area.on('click', 'button#cancel-button', function (e){
        e.stopPropagation();
        $(this).addClass('hidden');
        $('button#send-button-1').addClass('hidden');
        $('#goComment1').remove();
        area.css({
            position:"relative",
            top:0,
            left:0,
            width: width_bak
        });
        $('button#send-button').removeClass('hidden');
        UE.getEditor('editor').setContent('');
        area.off('click', 'button#cancel-button');
    });
}

function reComm(param) {
    smooth_move_herf('#contact');
    var request = {
        QueryString : function(val){
            var uri = window.location.search;
            var re = new RegExp("" + val + "=([^\&\?]*)", "ig");
            return ((uri.match(re))?(uri.match(re)[0].substr(val.length+1)):null);
        }
    };

    var p = parseInt(param.attr('data-page')) - 1;
    showComment(p);
}

$(document).ready(function(){
    $('button#send-button').on('click',function(){
        sendComment({
            textMsg:UE.getEditor('editor').getContent(),
            nameMsg: $("#nameInput").val().replace(/\s/g, "")
        });
        UE.getEditor('editor').setContent("");
    });
    //
    UE.getEditor('editor');
    //
    $('div#item-editor-shadow,button.btn-right,button#send-button-1').addClass('hidden');
    //

    showComment(0);
});