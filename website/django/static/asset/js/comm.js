/**
 * Created by 先哥 on 2014/8/17.
 *
 */

function showComment(page) {
    var url = "json/refresh_ds_comments/";
    $.post(url,
        {
            'page': page,
        }, 
        function(json){
            var str = "";
            var comment_date = "";
            var comment2_date = "";
            total = json.total;
            $.each(json.result, function (index, content) {
                comment_date = JSON.stringify(content.postDate).replace(/T/gm, ' ').replace(/"/gm, '');
                str += '<div class="author_comment">' + '<label id="' + (index + 1) + '" style="display:none">' + content.cid + '</label>'+ "<span class=\"badge badge-info\">#" + (index + 1) + '</span>&nbsp;' +'<a class="name">' + content.userName + '</a>' + "<span class='time'>" + comment_date + "</span>"+'<span class="area-tool-comment"><a class="btn-quote" onclick="quoteComm($(this))">[回复]</a></span>';
                str += '<div class="content-comment">' + content.contents + "</div>";
                $.each(content.comment2, function (index2, content2) {
                    comment2_date = JSON.stringify(content2.postDate).replace(/T/gm, ' ').replace(/"/gm, '');
                    str += '<div class="author_comment last"><a class="name"> &nbsp;' + content2.userName + '</a>' + "<span class='time'>" + comment2_date + "</span>"  + '<span class="area-tool-comment"><a class="btn-quote" onclick="quoteComm($(this))">[回复]</a></span>'+'<div class="content-comment">' + content2.contents + "</div></div>";
                });

                str += "</div>";
            });

            str += $.noteMakePages({num: page + 1, count: total, size: 10, "long": 5});
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
        alert("请不要空评论就发送好么？");
        ue.focus();
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
            alert("发送成功，欢迎留言建议和想法~");
        }
    );

    showComment(0);
}


function quoteComm(param) {
    var posMsg;
    UE.getEditor('editor').setContent('');
    $('#goComment1').remove();
    $('button#send-button').addClass('hidden');
    var area, content, editor, shadow;
    var hotDiv = '<div id="goComment1" class="hotComment1 panel-footer">';
    hotDiv += '</div>';
    param.parent().parent().find('div.content-comment:first').after(hotDiv);
    area = $("#goComment");
    shadow = $("#goComment1");
    $("button#cancel-button, #item-editor-shadow, button#send-button-1").removeClass("hidden");
    shadow.css({height: 357});
    area.css({width: shadow.width() + 2});
    area.css({display: "block", position: "absolute", left: shadow.offset().left, top: shadow.offset().top}).animate({opacity: 1});

    area.on('click', 'button#send-button-1', function (e){
        e.stopPropagation();
        if (!UE.getEditor('editor').getContent()){
            return false;
        }
        else {
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
                width: 950
            });
            sendComment({
                textMsg: contentMsg, 
                nameMsg: $("#nameInput").val().replace(/\s/g, ""), 
                posMsg: posMsg
            });
            smooth_move_herf('#contact');
            area.off('click', 'button#send-button-1');
            //location.reload();
        }
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
            width:950
        });
        $('button#send-button').removeClass('hidden');
        UE.getEditor('editor').setContent('');
        area.off('click', 'button#cancel-button');
    });
    /*
    area.delegate('button#send-button-1', 'click', function (e){
        e.stopPropagation();
        if (!UE.getEditor('editor').getContent()){
            return false;
        }
        else {
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
                width: 950
            });
            sendComment({
                textMsg: contentMsg, 
                nameMsg: $("#nameInput").val().replace(/\s/g, ""), 
                posMsg: posMsg
            });
            smooth_move_herf('#contact');
            area.undelegate();
            //location.reload();
        }
    });

    area.delegate('button#cancel-button', 'click', function (e){
        e.stopPropagation();
        $(this).addClass('hidden');
        $('button#send-button-1').addClass('hidden');
        $('#goComment1').remove();
        area.css({
            position:"relative",
            top:0,
            left:0,
            width:950
        });
        $('button#send-button').removeClass('hidden');
        UE.getEditor('editor').setContent('');
        area.undelegate();
    });*/

    //param.stopPropagation();
}

function reNote(param) {
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

(function() {
  $.noteMakePages = function(param) {
    var f, i, p, _i, _j, _ref, _ref1, _ref2, _ref3;
    f = {num: 1, count: 0, size: 10, "long": 5};
    if (param) {
        $.extend(f, param)
    }

    p = {total: f.totalPage || Math.ceil(f.count / f.size), num: f.num};
    if (p.total > 1) {
        p.fore = p.num !== 1 ? '<a href=\"#contact\"> <span class="pager pager-fore" onclick="reNote($(this))" data-page="' + (p.num - 1) + '">' + '上一页' + '</span></a>' : "";
        p.hind = p.num !== p.total ? '<a href=\"#contact\"> <span class="pager pager-hind" onclick="reNote($(this))" data-page="' + ((p.num | 0) + 1) + '">' + '下一页' + '</span></a>' : "";
        p.last = p.num !== p.total ? '<a href=\"#contact\"> <span class="pager pager-first" onclick="reNote($(this))" data-page="' + p.total + '">' + '最末' + '</span></a>' : "";
        p.first = p.num !== 1 ? '<a href=\"#contact\"> <span class="pager pager-last" onclick="reNote($(this))" data-page="' + 1 + '">' + '最初' + '</span></a>' : "";
        p.here = '<span class="pager pager-here active" data-page="' + p.num + '">' + p.num + "</span>";
        p.fores = "";
        for (i = _i = _ref = p.num - 1, _ref1 = p.num - f.long; _i > _ref1; i = _i += -1) {
            if (i >= 1) {
                p.fores = '<a href=\"#contact\"> <span class="pager pager-hinds" onclick="reNote($(this))" data-page="' + i + '">' + i + "</span></a>" + p.fores
            }
        }
        p.hinds = "";
        for (i = _j = _ref2 = p.num + 1, _ref3 = p.num + f.long; _j < _ref3; i = _j += 1) {
            if (i <= p.total) {
                p.hinds += '<a href=\"#contact\"> <span class="pager pager-fores" onclick="reNote($(this))" data-page="' + i + '">' + i + "</span></a>"
            }
        }
        p.html = '<div id="' + (f.id || "") + '" class="area-pager ' + (f["class"] || "") + '">' + (f.before || "") + p.first + p.fore + p.fores + p.here + p.hinds + p.hind + p.last + '<span class="hint">当前位置：' + (!f.addon ? p.num : '<input class="ipt-pager" type="number" value="' + p.num + '" data-max="' + p.total + '">') + "/" + p.total + "页" + (f.addon ? '<button class="btn mini btn-pager">跳页</button>' : "") + "</span>" + (f.after || "") + '<span class="clearfix"></span> </div>'
    } else {
        p.html = "";
    }

    return p.html;
  };
}).call(this);

$(document).ready(function(){
    $('button#send-button').on('click',function(){
        sendComment({textMsg:UE.getEditor('editor').getContent(),nameMsg: $("#nameInput").val().replace(/\s/g, "")})
        UE.getEditor('editor').setContent("");
    });
    //
    UE.getEditor('editor');
    //
    $('div#item-editor-shadow,button.btn-right,button#send-button-1').addClass('hidden');
    //
});