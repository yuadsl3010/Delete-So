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
  var u = request.QueryString("search");
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
            var total = json.total;
            if (total == "0"){
                $("#total").text("很遗憾，我性能都调上去了还是看不到，这就是命。。。如果这种情况经常出现，请留言反馈");
            }
            else{
                document.getElementById("total").innerHTML = "共找到" + total + "条结果：" + (page * 10 + 1) + "-" + (page * 10 + 10);
                var str = "";   
                $.each(json.result, function (index, content){
                    if (content.isDelete == 1){
                        str += '<div class="cell"><div class="RightPost"><h2><a href="' + content.url + '" target="_blank">' + content.type + '-' + content.title + '</a></h2>' + '<h4>' + '<span class="badge-info">#' + content.layer + '</span>&nbsp;<b>' + content.up + '</b>&nbsp;<small><i>' + content.postTime + '</i></small></h4><p>' + content.content + '</p></div></div>';
                    }
                    else{
                        str += '<div class="cell"><div class="Right">    <h2><a href="' + content.url + '" target="_blank">' + content.type + '-' + content.title + '</a></h2>' + '<h4>' + '<span class="badge-info">#' + content.layer + '</span>&nbsp;<b>' + content.up + '</b>&nbsp;<small><i>' + content.postTime + '</i></smal></h4><p>' + content.content + '</p></div></div>';
                    }
                });

                str += $.MakePages({num: page + 1, count: total, size: 10, "long": 5}, 'home', 'reSearch');
                $("#resultSearch").html(str);
                $('span.icon-mid').addClass('hidden');
            }
        }
    );
}