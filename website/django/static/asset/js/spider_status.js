$(document).ready(function(){
    //get_spider_status();
});

function get_spider_status() {
    var url = "json/get_spider_speed/";
    $.get(url, function(json){
            var spider_status = json.status;
            var spider_speed = json.speed;
            var text = "";

            if (spider_status == 'alive')
            {
                text = "当前评论分析速度：" + spider_speed + "条/秒";
            }
            else
            {
                text = "悲剧啦！爬虫已经当机，请呼叫小川进行修复吧！";
            }
            
            send_info(text);
        }
    );
}