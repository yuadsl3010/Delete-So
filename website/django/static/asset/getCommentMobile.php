<?php
	//Open DB
	$dbname = 'pGgdVFbDzjYgLilljcoQ';
	$host = 'sqld.duapp.com';
	$port = 4050;
	$user = 'e17atet3Z28uWYUW1PZ8Olff';
	$pwd = 'Rin0l7x5KUlMKstqiLX82DDOTYaWrXbz';

	//连接数据库 
	$con = @mysql_connect("{$host}:{$port}", $user, $pwd, true);
	if (!$con)
	{
		die('数据库连接失败！</br>错误原因：' . mysql_error());
	}

	//选定数据库 
	mysql_select_db($dbname, $con);

	//执行SQL语句(查询) 
	$sql = "SELECT * FROM (SELECT * FROM commentsVIP WHERE person = '1' ORDER BY checkTime DESC LIMIT 500) AS T ORDER BY rand() LIMIT 1";
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

	$row = mysql_fetch_row($result, MYSQL_ASSOC);
	$row['content'] = preg_replace("/(\[(.*?)\])/", '', str_replace('u003cbr/u003e', '</br>', $row['content']));

	$obj = array();

	//$sql = "SELECT * FROM storedb WHERE cid = '" . $row1['cid'] . "'";
	$sql = "SELECT * FROM storedb WHERE cid = '" . $row['cid'] . "'";

	$result = mysql_query($sql);
	while ($store = mysql_fetch_row($result, MYSQL_ASSOC))
	{
		$store['content'] = preg_replace("/(\[(.*?)\])/", '', str_replace('u003cbr/u003e', '</br>', $store['content']));
		$obj[] = $store;
	}

	/*header("header('Content-type: text/json');");*/
    header("Access-Control-Allow-Origin:*");
	echo '{"title1":[';
	echo json_encode($row);
	echo '],"comments1":';
	echo json_encode($obj);
	echo '}';

	mysql_free_result($result); 
	//Close
	mysql_close($con);
	//echo '{"postTitle":' . json_encode($postTitle) . '"postContent":' . json_encode($postContent) . '"postUser":' . json_encode($postUser) . '"postTime":' . json_encode($postTime) . '}';
	//echo '{"postTitle":"1", "postContent":"2", "postUser":"3", "postTime":"4"}';
?>