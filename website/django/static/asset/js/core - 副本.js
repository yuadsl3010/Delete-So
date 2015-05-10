$(document).ready(function(){
    var request = {
                QueryString : function(val){
                  var uri = window.location.search;
                  var re = new RegExp("" + val + "=([^\&\?]*)", "ig");
                  return ((uri.match(re))?(uri.match(re)[0].substr(val.length+1)):null);
                }
    };
    var u = request.QueryString("search");
    var p = request.QueryString("page");
    if (p == ""){
       p = 0;
    }
    
    getComments(u, p);
    $('button#submit').on('click', function () {
         var searchText = $('input#search').val();
         var request = {
            QueryString : function(val){
              var uri = window.location.search;
              var re = new RegExp("" + val + "=([^\&\?]*)", "ig");
              return ((uri.match(re))?(uri.match(re)[0].substr(val.length+1)):null);
            }
         };
          var u = searchText;
          var p = request.QueryString("page");
          if (p == ""){
               p = 0;
          }
      
          getComments(u, p);
    });

    $('div#features').hover(function(){
        $('span.icon-mid').removeClass('hidden')
    },function(){
        $('span.icon-mid').addClass('hidden')
    })
});

function close_ad(param)
{
    param.parent().addClass('hidden');
}

function reComm(param) {
  smooth_move_herf('#features');
  var request = {
    QueryString : function(val){
      var uri = window.location.search;
      var re = new RegExp("" + val + "=([^\&\?]*)", "ig");
      return ((uri.match(re))?(uri.match(re)[0].substr(val.length+1)):null);
    }
  };
  var u = request.QueryString("search");
  var p = parseInt(param.attr('data-page')) - 1;
  getComments(u, p);
}

(function() {
  $.commMakePages = function(param) {
    var f, i, p, _i, _j, _ref, _ref1, _ref2, _ref3;
    f = {num: 1,count: 0,size: 10,"long": 5};
    if (param) {
        $.extend(f, param)
    }
    p = {total: f.totalPage || Math.ceil(f.count / f.size),num: f.num};
    if (p.total > 1) {
        p.fore = p.num !== 1 ? '<a href=\"#home\"> <span class="pager pager-fore" onclick="reComm($(this))" data-page="' + (p.num - 1) + '">' + '上一页' + '</span></a>' : "";
        p.hind = p.num !== p.total ? '<a href=\"#home\"> <span class="pager pager-hind" onclick="reComm($(this))" data-page="' + ((p.num | 0) + 1) + '">' + '下一页' + '</span></a>' : "";
        p.last = p.num !== p.total ? '<a href=\"#home\"> <span class="pager pager-first" onclick="reComm($(this))" data-page="' + p.total + '">' + '最末' + '</span></a>' : "";
        p.first = p.num !== 1 ? '<a href=\"#home\"> <span class="pager pager-last" onclick="reComm($(this))" data-page="' + 1 + '">' + '最初' + '</span></a>' : "";
        p.here = '<span class="pager pager-here active" data-page="' + p.num + '">' + p.num + "</span>";
        p.fores = "";
        for (i = _i = _ref = p.num - 1, _ref1 = p.num - f.long; _i > _ref1; i = _i += -1) {
            if (i >= 1) {
                p.fores = '<a href=\"#home\"> <span class="pager pager-hinds" onclick="reComm($(this))" data-page="' + i + '">' + i + "</span></a>" + p.fores
            }
        }
        p.hinds = "";
        for (i = _j = _ref2 = p.num + 1, _ref3 = p.num + f.long; _j < _ref3; i = _j += 1) {
            if (i <= p.total) {
                p.hinds += '<a href=\"#home\"> <span class="pager pager-fores" onclick="reComm($(this))" data-page="' + i + '">' + i + "</span></a>"
            }
        }
        p.html = '<div id="' + (f.id || "") + '" class="area-pager ' + (f["class"] || "") + '">' + (f.before || "") + p.first + p.fore + p.fores + p.here + p.hinds + p.hind + p.last + '<span class="hint">当前位置：' + (!f.addon ? p.num : '<input class="ipt-pager" type="number" value="' + p.num + '" data-max="' + p.total + '">') + "/" + p.total + "页" + (f.addon ? '<button class="btn mini btn-pager">跳页</button>' : "") + "</span>" + (f.after || "") + '<span class="clearfix"></span> </div>'
    } else {
        p.html = "";
    }
    return p.html;
  };
}).call(this);

$(document).ready(function () {
        $('.dropdown').each( function() {
    $(this).hover(
            function () {
      //show its submenu
      $( this ).find( '.navbar-top-li-dropdown' ).fadeIn();
        },
        function () {
      //hide its submenu
        $( this ).find( '.navbar-top-li-dropdown' ).hide();
        }
      );
  });
});

function getComments(search, page)
{
    var url = "asset/getSearch.php?search=" + search + "&page=" + page;
    $.getJSON(url, function(json){
          //1
          var total = json.total[0];
          if (total == "0"){
             $("#total").text("没有找到？没有关系，我已对搜索系统做出了重大升级，请一个小时之后再来找找看吧");
          }
          else{
              document.getElementById("total").innerHTML = "共找到" + json.total[0] + "条结果：" + (p * 10 + 1) + "-" + (p * 10 + 10);
              var str = "";
              $.each(json.result, function(index, content) {
                  if (content.isDelete == 1) {
                      str += '<div class="cell"><div class="RightPost"><h2><a href="' + content.url + '" target="_blank">' + content.type + '-' + content.title + '</a></h2>' + '<h4>' + '<span class="badge-info">#' + content.layer + '</span>&nbsp;<b>' + content.up + '</b>&nbsp;<small><i>' + content.postTime + '</i></small></h4><p>' + content.content + '</p></div></div>';
                  }
                  else {
                      str += '<div class="cell"><div class="Right">    <h2><a href="' + content.url + '" target="_blank">' + content.type + '-' + content.title + '</a></h2>' + '<h4>' + '<span class="badge-info">#' + content.layer + '</span>&nbsp;<b>' + content.up + '</b>&nbsp;<small><i>' + content.postTime + '</i></smal></h4><p>' + content.content + '</p></div></div>';
                  }
              });

              str += $.commMakePages({num: p + 1,count: total,size: 10,"long": 5});
          }
    });  
}