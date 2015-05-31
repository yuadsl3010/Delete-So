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
    
    getSearchs(u, p);
    $('input#search').val(u);
    $('button#submit').on('click', function(event) {
        event.preventDefault();
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

        getSearchs(u, p);
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

function reSearch(param) {
  smooth_move_herf('#features');
  var request = {
    QueryString : function(val){
      var uri = window.location.search;
      var re = new RegExp("" + val + "=([^\&\?]*)", "ig");
      return ((uri.match(re))?(uri.match(re)[0].substr(val.length+1)):null);
    }
  };
  var u = $('input#search').val();
  var p = parseInt(param.attr('data-page')) - 1;
  getSearchs(u, p);
}

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

function getSearchs(search, page)
{
    var url = "json/get_search_results/";

    $.post(url,
        {
            'search': search,
            'page': page,
        },
        function(json){
            if (!check_responds(json)) {
                return ;
            }

            var total = json.total;
            if (total == 0){
                $("#total").text("找到或者找不到，都是命运石之门的选择~");
                $("#resultSearch").html("");
            }
            else{
                document.getElementById("total").innerHTML = "共有" + total + "个结果：" + (page * 10 + 1) + "-" + (page * 10 + 10);
                var str = build_ac_comments(json.result);   
                /*$.each(json.result, function (index, content){
                    if (content.isDelete == 1){
                        str += '<div class="cell">\
                                  <div class="RightPost">\
                                    <h4>\
                                      <a href="' + 
                                      content.url + 
                                      '" target="_blank">' + 
                                        content.type + '-' + content.title + 
                                      '</a>\
                                    </h4>' + 
                                    '<h4>' + 
                                      '<span class="badge-info">#' + 
                                        content.layer + 
                                      '</span>&nbsp;\
                                      <b>' + content.userName + '</b>&nbsp;\
                                      <p>' + 
                                        rePrint(content.content) + 
                                      '</p>\
                                    </h4>\
                                  </div>\
                                </div>';
                    }
                    else{
                        str += '<div class="cell"><div class="Right">    <h2><a href="' + content.url + '" target="_blank">' + content.type + '-' + content.title + '</a></h2>' + '<h4>' + '<span class="badge-info">#' + content.layer + '</span>&nbsp;<b>' + content.userName + '</b>&nbsp;<small><i>' + content.postTime + '</i></smal></h4><p>' + rePrint(content.content) + '</p></div></div>';
                    }
                });*/

                str += $.MakePages({num: page + 1, count: total, size: 10, "long": 5}, 'home', 'reSearch');
                $("#resultSearch").html(str);
                //$('span.icon-mid').addClass('hidden');
            }
            
            smooth_move_herf("#news");
        }
    );
}
