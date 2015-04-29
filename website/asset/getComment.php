<?php
	//Open DB
	$dbname = 'deleteso';
	$host = 'rdsnqvfianubnan.mysql.rds.aliyuncs.com';
	$port = 3306;
	$user = 'deleteso';
	$pwd = 'deletepassso';

	//连接数据库 
	$con = mysql_connect("{$host}:{$port}", $user, $pwd, true);
	if (!$con)
	{
		die('数据库连接失败！</br>错误原因：' . mysql_error());
	}

	//选定数据库 
	mysql_select_db($dbname, $con);

	//执行SQL语句(查询) 
	$sql = "SELECT * FROM accomments WHERE isDelete = 1 ORDER BY checkTime DESC LIMIT 5";
	$result = mysql_query($sql);
	if (!$result)
	{
		die('数据库连接失败！</br>错误原因：' . mysql_error());
	} 
	
	// $post = array();
	// $i = 0;
	// while ($row = mysql_fetch_array($result, MYSQL_ASSOC))
	// {
	// 	$objs[] = $obj;
	// 	$postTitle = $obj->title;
	// 	$postContent = $obj->content;
	// 	$postUser = $obj->userName;
	// 	$postTime = $obj->postDate;
	// 	$post[$i] = $row;
	// 	$i++;
	// }

	$row1 = mysql_fetch_row($result, MYSQL_ASSOC);
	$row2 = mysql_fetch_row($result, MYSQL_ASSOC);
	$row3 = mysql_fetch_row($result, MYSQL_ASSOC);
	$row4 = mysql_fetch_row($result, MYSQL_ASSOC);
	$row5 = mysql_fetch_row($result, MYSQL_ASSOC);

	$row1 = rePrint($row1);
	$row2 = rePrint($row2);
	$row3 = rePrint($row3);
	$row4 = rePrint($row4);
	$row5 = rePrint($row5);

	$objs1 = array();
	$objs2 = array();
	$objs3 = array();
	$objs4 = array();
	$objs5 = array();

	$acMsgSQL = mysql_query("SELECT * FROM accommentsinfo WHERE id = " . $row1['acid']);
	$acMsg = mysql_fetch_array($acMsgSQL, MYSQL_ASSOC);
	$row1['url'] = $acMsg['url'];
	$row1['type'] = $acMsg['type'];
	$row1['title'] = $acMsg['title'];
	$row1['up'] = $acMsg['up'];
	$row1['postTime'] = $acMsg['postTime'];
	$result = mysql_query($sql1);
	$store1 = rePrint($row1);
	$objs1[] = $store1;

	$acMsgSQL = mysql_query("SELECT * FROM accommentsinfo WHERE id = " . $row2['acid']);
	$acMsg = mysql_fetch_array($acMsgSQL, MYSQL_ASSOC);
	$row2['url'] = $acMsg['url'];
	$row2['type'] = $acMsg['type'];
	$row2['title'] = $acMsg['title'];
	$row2['up'] = $acMsg['up'];
	$row2['postTime'] = $acMsg['postTime'];
	$result = mysql_query($sql2);
	$store2 = rePrint($row2);
	$objs2[] = $store2;

	$acMsgSQL = mysql_query("SELECT * FROM accommentsinfo WHERE id = " . $row3['acid']);
	$acMsg = mysql_fetch_array($acMsgSQL, MYSQL_ASSOC);
	$row3['url'] = $acMsg['url'];
	$row3['type'] = $acMsg['type'];
	$row3['title'] = $acMsg['title'];
	$row3['up'] = $acMsg['up'];
	$row3['postTime'] = $acMsg['postTime'];
	$result = mysql_query($sql3);
	$store3 = rePrint($row3);
	$objs3[] = $store3;

	$acMsgSQL = mysql_query("SELECT * FROM accommentsinfo WHERE id = " . $row4['acid']);
	$acMsg = mysql_fetch_array($acMsgSQL, MYSQL_ASSOC);
	$row4['url'] = $acMsg['url'];
	$row4['type'] = $acMsg['type'];
	$row4['title'] = $acMsg['title'];
	$row4['up'] = $acMsg['up'];
	$row4['postTime'] = $acMsg['postTime'];
	$result = mysql_query($sql4);
	$store4 = rePrint($row4);
	$objs4[] = $store4;

	$acMsgSQL = mysql_query("SELECT * FROM accommentsinfo WHERE id = " . $row5['acid']);
	$acMsg = mysql_fetch_array($acMsgSQL, MYSQL_ASSOC);
	$row5['url'] = $acMsg['url'];
	$row5['type'] = $acMsg['type'];
	$row5['title'] = $acMsg['title'];
	$row5['up'] = $acMsg['up'];
	$row5['postTime'] = $acMsg['postTime'];
	$result = mysql_query($sql5);
	$store5 = rePrint($row5);
	$objs5[] = $store5;

	/*header("header('Content-type: text/json');");*/
    header("Access-Control-Allow-Origin:*");
	echo '{"title1":[';
	echo json_encode($row1);
	echo '],"comments1":';
	echo json_encode($objs1);
	echo ',"title2":[';
	echo json_encode($row2);
	echo '],"comments2":';
	echo json_encode($objs2);
	echo ',"title3":[';
	echo json_encode($row3);
	echo '],"comments3":';
	echo json_encode($objs3);
	echo ',"title4":[';
	echo json_encode($row4);
	echo '],"comments4":';
	echo json_encode($objs4);
	echo ',"title5":[';
	echo json_encode($row5);
	echo '],"comments5":';
	echo json_encode($objs5);
	echo '}';

	mysql_free_result($result); 
	//Close
	mysql_close($con);
	//echo '{"postTitle":' . json_encode($postTitle) . '"postContent":' . json_encode($postContent) . '"postUser":' . json_encode($postUser) . '"postTime":' . json_encode($postTime) . '}';
	//echo '{"postTitle":"1", "postContent":"2", "postUser":"3", "postTime":"4"}';
?>

<?php
function rePrint($row)
{
	$row['content'] = str_replace('u003cbr/u003e', '</br>', $row['content']);
	$row['content'] = preg_replace("/(\[img(.*?)\])/", "</br><img src=\"", $row['content']);
	$row['content'] = preg_replace("/(\[\/img(.*?)\])/", "\"></br>", $row['content']);

	while (($i = strpos($row['content'], "[emot")) > -1)
	{
		$j = strpos($row['content'], "/]") + 2 - $i;
		$limit = substr($row['content'], $i);
		$k = strpos($limit, ",");
		$emojType = substr($limit, $k - 3, 3);
		$emojNum = substr($limit, $k + 1, 2);
		$row['content'] = substr_replace($row['content'], "<img src=\"asset/image/emoj/" . $emojType . "/" . $emojNum . ".gif\">", $i, $j);
	}

	$row['content'] = preg_replace("/(\[(.*?)\])/", "", $row['content']);
	return $row;
}
?>