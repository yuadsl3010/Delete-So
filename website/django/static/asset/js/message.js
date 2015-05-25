function send_top_alert(type, msg){
	var top = '\
		<div id="notifications-top-center-tab">'
			+ msg + '\
		</div>';

	$('#notifications-top-center-tab').remove();
	$("#notifications-top-center").html();
	$("#notifications").append(top);
	$("#notifications-top-center-tab").addClass('animated ' + type + 'in');

	setTimeout(function() {
			$('#notifications-top-center-tab').removeClass();
			$('#notifications-top-center-tab').addClass('animated ' + type + 'out');
		},
		5000
	);
}

function send_bottom_alert(type, image, msg_top, msg_bot){
	var bottom = '\
		<div id="notifications-bottom-center-tab">\
			<div id="notifications-bottom-center-tab-avatar">'
				+ image + '\
			</div>\
			<div id="notifications-bottom-center-tab-right">\
				<div id="notifications-bottom-center-tab-right-title">'
					+ msg_top + '\
				</div>\
				<div id="notifications-bottom-center-tab-right-text">'
					+ msg_bot + '\
				</div>\
			</div>\
		</div>\
	';

	$("#notifications-bottom-center").html();
	$("#notifications-bottom-center").html(bottom);
	$('#notifications-bottom-center-tab').addClass('animated ' + type + 'in');

	setTimeout(function() {
			$('#notifications-bottom-center-tab').removeClass();
			$('#notifications-bottom-center-tab').addClass('animated ' + type + 'out');
    		$("#notifications-bottom-center").html();
		},
		5000
	);
}

function send_center_alert(data){
	var center = '\
		<div id="notifications-full">\
			<div id="notifications-full-close" class="close">\
				<span class="iconb" data-icon="&#xe20e;"></span>\
			</div>\
			<div id="notifications-full-icon">\
				<span class="iconb" data-icon="&#xe261;"></span>\
			</div>\
			<div id="notifications-full-text">\
				This is a large notification.\
				You can use this notification to display long warnings.\
				This type of notification is not suited for short warnings.\
				As an added bonus you have a big icon at the top.\
			</div>\
		</div>';
}

function send_warn(data)
{
	var image = '<img src="/static/asset/image/message/chuan.JPG" width="100" height="100"/>';
	var msg_bot = '';
	var type = 'bounce_';
	send_bottom_alert(type, image, data, msg_bot);
}

function send_ok(data) {
	var image = '<img src="/static/asset/image/message/chuan.JPG" width="100" height="100"/>';
	var msg_bot = '点击Github地址一起为网站添砖加瓦吧~';
	var type = 'bounce_';
	send_bottom_alert(type, image, data, msg_bot);
}

function send_info(data)
{
	var type = 'bounce_down_';
	send_top_alert(type, data);
}