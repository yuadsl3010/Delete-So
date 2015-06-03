$(window).scroll(refresh_nav);

function smooth_move_herf(para){
    var pos = $(para).offset().top - 80;
    $("html,body").animate({scrollTop: pos}, 500); 
    return false;
}

function checkSearch() 
{   
    var search = document.getElementById('search');
    search.setCustomValidity("格式不正确哟，eg：'ac1205967'或者'带带我'");
}  

function getCookie(name){  
    var cookieValue = null;  
    if (document.cookie && document.cookie != '') {  
        var cookies = document.cookie.split(';');  
        for (var i = 0; i < cookies.length; i++) {  
            var cookie = cookies[i].trim();  
            // Does this cookie string begin with the name we want?  
            if (cookie.substring(0, name.length + 1) == (name + '=')) {  
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));  
                break;  
            }  
        }  
    }  
    return cookieValue;  
}  

//从cookie中获取token
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method){
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url){
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

//django规定前端在POST的时候必须带上csrf的token
$.ajaxSetup({
    beforeSend: function(xhr, settings){
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

//从json中解析ac的评论
function build_ac_comments(data) {
    var html = "";
    $.each(data, function(ind, val){
        var _index = ind + 1;
        var _html = '<div class="cell" id=' + ind + '>'
            + '<div class="title">'
            + '<h3>' + _index + ' ' + val.type + ' - ' + val.title + '</h3>'
            + '<div style="padding-left: 25px"><p class="subtext pocket-inserted">' + 'UP主 <a href="javascript:">' + val.up + '</a> | ' + val.postTime + ' | 详见&gt; ' + '<a class="comhead" target="_blank" href="' + val.url + '">ac' + val.acid + '</a>'+'</p></div></div>';
        html += _html;
        html += '<div class="RightPost">' + '<h4><span class="badge-info">#' + val.layer + '</span>&nbsp;<b>' + val.userName + '</b>&nbsp</h4>' + '<div class="text-show-view"><p>' + rePrint(val.content) + '</p></div></div>';
        html += '</div>';
    });
    
    return html;
}
/*
error code:
    0: OK
    1: Invalid Params
*/
//服务器返回消息
function check_responds(json) {
    result = false;
    switch (json.status) {
    case 0:
        if (json.message != undefined) {
            send_warn(json.message);
        }

        result = true;
        break;
    case 1:
        if (json.message != undefined) {
            send_warn(json.message);
        }
        else {
            send_warn("参数校验错误！");
        }

        break;
    default:
        //BUG_ON
        break;
    }

    return result;
}

//将图片代码替换成图片
function rePrint(contents){
	//先将img图片替换成url
	contents = contents.replace(/u003cbr\/u003e/gm, "</br>");
	contents = contents.replace(/(\[img(.*?)\])/gm, "</br><img src=\"");
	contents = contents.replace(/(\[\/img(.*?)\])/gm, "\"></br>");

	//再将emoj表情替换成url
	var i = 0, j = 0, k = 0;
	var limit = "", emoj_type = "", emoj_num = "", left = "", right = "";
	while ((i = contents.indexOf("[emot")) > -1)
	{
		j = contents.indexOf("/]") + 2;
		left = contents.substr(0, i);
		limit = contents.substr(i, j - i);
		right = contents.substr(j, contents.length - j);
		k = limit.indexOf(",");
		emoj_type = limit.substr(k - 3, 3);
		emoj_num = limit.substr(k + 1, 2);
		contents = left;
		contents += "<img class=\"emotion\" src=\"/static/asset/image/emoj/";
		contents += emoj_type;
		contents += "/";
		contents += emoj_num;
		contents += ".gif\">";
		contents += right;
	}

	contents = contents.replace(/(\[(.*?)\])/gm, "");
	return contents;
}

(function() {
  $.MakePages = function(param, back_tag, call_back) {
    var f, i, p, _i, _j, _ref, _ref1, _ref2, _ref3;
    f = {num: 1,count: 0,size: 10,"long": 5};
    if (param) {
        $.extend(f, param)
    }
    p = {total: f.totalPage || Math.ceil(f.count / f.size),num: f.num};
    if (p.total > 1) {
        p.fore = p.num !== 1 ? '<a href=\"#' + back_tag + '\"> <span class="pager pager-fore" onclick="' + call_back + '($(this))" data-page="' + (p.num - 1) + '">' + '上一页' + '</span></a>' : "";
        p.hind = p.num !== p.total ? '<a href=\"#' + back_tag + '\"> <span class="pager pager-hind" onclick="' + call_back + '($(this))" data-page="' + ((p.num | 0) + 1) + '">' + '下一页' + '</span></a>' : "";
        p.last = p.num !== p.total ? '<a href=\"#' + back_tag + '\"> <span class="pager pager-first" onclick="' + call_back + '($(this))" data-page="' + p.total + '">' + '最末' + '</span></a>' : "";
        p.first = p.num !== 1 ? '<a href=\"#' + back_tag + '\"> <span class="pager pager-last" onclick="' + call_back + '($(this))" data-page="' + 1 + '">' + '最初' + '</span></a>' : "";
        p.here = '<span class="pager pager-here active" data-page="' + p.num + '">' + p.num + "</span>";
        p.fores = "";
        for (i = _i = _ref = p.num - 1, _ref1 = p.num - f.long; _i > _ref1; i = _i += -1) {
            if (i >= 1) {
                p.fores = '<a href=\"#' + back_tag + '\"> <span class="pager pager-hinds" onclick="' + call_back + '($(this))" data-page="' + i + '">' + i + "</span></a>" + p.fores
            }
        }
        p.hinds = "";
        for (i = _j = _ref2 = p.num + 1, _ref3 = p.num + f.long; _j < _ref3; i = _j += 1) {
            if (i <= p.total) {
                p.hinds += '<a href=\"#' + back_tag + '\"> <span class="pager pager-fores" onclick="' + call_back + '($(this))" data-page="' + i + '">' + i + "</span></a>"
            }
        }
        p.html = '<div id="' + (f.id || "") + '" class="area-pager ' + (f["class"] || "") + '">' + (f.before || "") + p.first + p.fore + p.fores + p.here + p.hinds + p.hind + p.last + '<span class="hint">当前位置：' + (!f.addon ? p.num : '<input class="ipt-pager" type="number" value="' + p.num + '" data-max="' + p.total + '">') + "/" + p.total + "页" + (f.addon ? '<button class="btn mini btn-pager">跳页</button>' : "") + "</span>" + (f.after || "") + '<span class="clearfix"></span> </div>'
    } else {
        p.html = "";
    }
    return p.html;
  };
}).call(this);

// Bar
function refresh_nav(){
    var
        navbar_dynamic  = $('.navbar-dynamic'),
        subNav          = $('.sub-nav'),
        subNavWrapper   = $('.sub-nav-wrapper'),
        scroll_position = $(document).scrollTop(),
        top_bar_height  = navbar_dynamic.height();
        wrapper_offset  = subNavWrapper.offset().top,
        travel_distance  = wrapper_offset - top_bar_height;


    if (scroll_position > 5){
        navbar_dynamic.removeClass('navbar-top-logo');
        navbar_dynamic.addClass('navbar-bar-logo');

        top_bar_height  = navbar_dynamic.height();
    } else {
        navbar_dynamic.removeClass('navbar-bar-logo');
        navbar_dynamic.addClass('navbar-top-logo');
    }

    if (scroll_position > travel_distance) {
        subNav.addClass('fixed');
        subNav.css('top', top_bar_height + "px");
    } else {
        subNav.removeClass('fixed');
    }
}

jQuery(function($) {
    $(document).ready( function() {
        //enabling stickUp on the '.navbar-wrapper' class
        $(document).ready( function() {
            //为 '.navbar-wrapper' class 启用stickUp插件
            $('.sub-nav-wrapper').stickUp({
                parts: {
                    0: 'news',
                    1: 'comments',
                    2: 'support',
                    3: 'share',
                },
                itemClass: 'menuItem',
                itemHover: 'active'
            });
        });
    });
});

(function() {

// Create a safe reference to the Underscore object for use below.
var _ = function(obj) {
    if (obj instanceof _) return obj;
    if (!(this instanceof _)) return new _(obj);
    this._wrapped = obj;
};
// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.
_.debounce = function(func, wait, immediate) {
    var timeout, result;
    return function() {
        var context = this, args = arguments;
        var later = function() {
            timeout = null;
            if (!immediate) result = func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) result = func.apply(context, args);
        return result;
    };
};
// Variables used throughout the functions below
var scrollPosition = $(document).scrollTop();

// Update scrollPosition on window scroll
$(window).scroll(_.debounce(function() {
    scrollPosition = $(document).scrollTop();
}, 10));


function hoverTiles() {
    var
    tiles              = $('#share-tiles'),
    tile               = $('#share-tiles li'),
    text               = $('#share-tiles small.tile-description')
    activeTile         = $('#share-tiles li.active'),
    activeText         = $('#share-tiles li.active small.tile-description'),
    activeTileHeight   = activeTile.outerHeight(true),
    activeTextWidth    = activeText.width();

    tiles.height(activeTileHeight);
    text.width(activeTextWidth);

    tile.hover(function() {
        tile.addClass('inactive');
        tile.removeClass('active');
        $(this).addClass('active');       
    }, function(){
//tile.removeClass('active');
//tile.removeClass('inactive');
})
}

$(document).ready(function() {
    hoverTiles();
})
})()