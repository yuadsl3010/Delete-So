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
	$sql = "SELECT * FROM(SELECT * FROM accomments WHERE height > 10 AND height < 30 LIMIT 50) AS A ORDER BY rand() LIMIT 5";
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

	//$sql = "SELECT * FROM storedb WHERE cid = '" . $row1['cid'] . "'";
	$sql1 = "SELECT * FROM accommentsstore WHERE cid = " . $row1['cid'] . " LIMIT 50";
	$sql2 = "SELECT * FROM accommentsstore WHERE cid = " . $row2['cid'] . " LIMIT 50";
	$sql3 = "SELECT * FROM accommentsstore WHERE cid = " . $row3['cid'] . " LIMIT 50";
	$sql4 = "SELECT * FROM accommentsstore WHERE cid = " . $row4['cid'] . " LIMIT 50";
	$sql5 = "SELECT * FROM accommentsstore WHERE cid = " . $row5['cid'] . " LIMIT 50";

	$acMsgSQL = mysql_query("SELECT * FROM accommentsinfo WHERE id = " . $row1['acid']);
	$acMsg = mysql_fetch_array($acMsgSQL, MYSQL_ASSOC);
	$row1['url'] = $acMsg['url'];
	$row1['type'] = $acMsg['type'];
	$row1['title'] = $acMsg['title'];
	$row1['up'] = $acMsg['up'];
	$row1['postTime'] = $acMsg['postTime'];
	$result = mysql_query($sql1);
	while ($store1 = mysql_fetch_row($result, MYSQL_ASSOC))
	{
		$store1['content'] = str_replace('u003cbr/u003e', '</br>', $store1['content']);
		$store1['content'] = preg_replace("/(\[img(.*?)\])/", "</br><img src=\"", $store1['content']);
		$store1['content'] = preg_replace("/(\[\/img(.*?)\])/", "\"></br>", $store1['content']);

		while (($i = strpos($store1['content'], "[emot")) > -1)
		{
			$j = strpos($store1['content'], "/]") + 2 - $i;
			$limit = substr($store1['content'], $i);
			$k = strpos($limit, ",");
			$emojType = substr($limit, $k - 3, 3);
			$emojNum = substr($limit, $k + 1, 2);
			$store1['content'] = substr_replace($store1['content'], "<img src=\"asset/image/emoj/" . $emojType . "/" . $emojNum . ".gif\">", $i, $j);
		}

		$store1['content'] = preg_replace("/(\[(.*?)\])/", "", $store1['content']);
		$objs1[] = $store1;
	}

	$acMsgSQL = mysql_query("SELECT * FROM accommentsinfo WHERE id = " . $row2['acid']);
	$acMsg = mysql_fetch_array($acMsgSQL, MYSQL_ASSOC);
	$row2['url'] = $acMsg['url'];
	$row2['type'] = $acMsg['type'];
	$row2['title'] = $acMsg['title'];
	$row2['up'] = $acMsg['up'];
	$row2['postTime'] = $acMsg['postTime'];
	$result = mysql_query($sql2);
	while ($store2 = mysql_fetch_row($result, MYSQL_ASSOC))
	{
		$store2['content'] = str_replace('u003cbr/u003e', '</br>', $store2['content']);
		$store2['content'] = preg_replace("/(\[img(.*?)\])/", "</br><img src=\"", $store2['content']);
		$store2['content'] = preg_replace("/(\[\/img(.*?)\])/", "\"></br>", $store2['content']);

		while (($i = strpos($store2['content'], "[emot")) > -1)
		{
			$j = strpos($store2['content'], "/]") + 2 - $i;
			$limit = substr($store2['content'], $i);
			$k = strpos($limit, ",");
			$emojType = substr($limit, $k - 3, 3);
			$emojNum = substr($limit, $k + 1, 2);
			$store2['content'] = substr_replace($store2['content'], "<img src=\"asset/image/emoj/" . $emojType . "/" . $emojNum . ".gif\">", $i, $j);
		}

		$store2['content'] = preg_replace("/(\[(.*?)\])/", "", $store2['content']);
		$objs2[] = $store2;
	}

	$acMsgSQL = mysql_query("SELECT * FROM accommentsinfo WHERE id = " . $row3['acid']);
	$acMsg = mysql_fetch_array($acMsgSQL, MYSQL_ASSOC);
	$row3['url'] = $acMsg['url'];
	$row3['type'] = $acMsg['type'];
	$row3['title'] = $acMsg['title'];
	$row3['up'] = $acMsg['up'];
	$row3['postTime'] = $acMsg['postTime'];
	$result = mysql_query($sql3);
	while ($store3 = mysql_fetch_row($result, MYSQL_ASSOC))
	{
		$store3['content'] = str_replace('u003cbr/u003e', '</br>', $store3['content']);
		$store3['content'] = preg_replace("/(\[img(.*?)\])/", "</br><img src=\"", $store3['content']);
		$store3['content'] = preg_replace("/(\[\/img(.*?)\])/", "\"></br>", $store3['content']);

		while (($i = strpos($store3['content'], "[emot")) > -1)
		{
			$j = strpos($store3['content'], "/]") + 2 - $i;
			$limit = substr($store3['content'], $i);
			$k = strpos($limit, ",");
			$emojType = substr($limit, $k - 3, 3);
			$emojNum = substr($limit, $k + 1, 2);
			$store3['content'] = substr_replace($store3['content'], "<img src=\"asset/image/emoj/" . $emojType . "/" . $emojNum . ".gif\">", $i, $j);
		}

		$store3['content'] = preg_replace("/(\[(.*?)\])/", "", $store3['content']);
		$objs3[] = $store3;
	}

	$acMsgSQL = mysql_query("SELECT * FROM accommentsinfo WHERE id = " . $row4['acid']);
	$acMsg = mysql_fetch_array($acMsgSQL, MYSQL_ASSOC);
	$row4['url'] = $acMsg['url'];
	$row4['type'] = $acMsg['type'];
	$row4['title'] = $acMsg['title'];
	$row4['up'] = $acMsg['up'];
	$row4['postTime'] = $acMsg['postTime'];
	$result = mysql_query($sql4);
	while ($store4 = mysql_fetch_row($result, MYSQL_ASSOC))
	{
		$store4['content'] = str_replace('u003cbr/u003e', '</br>', $store4['content']);
		$store4['content'] = preg_replace("/(\[img(.*?)\])/", "</br><img src=\"", $store4['content']);
		$store4['content'] = preg_replace("/(\[\/img(.*?)\])/", "\"></br>", $store4['content']);

		while (($i = strpos($store4['content'], "[emot")) > -1)
		{
			$j = strpos($store4['content'], "/]") + 2 - $i;
			$limit = substr($store4['content'], $i);
			$k = strpos($limit, ",");
			$emojType = substr($limit, $k - 3, 3);
			$emojNum = substr($limit, $k + 1, 2);
			$store4['content'] = substr_replace($store4['content'], "<img src=\"asset/image/emoj/" . $emojType . "/" . $emojNum . ".gif\">", $i, $j);
		}

		$store4['content'] = preg_replace("/(\[(.*?)\])/", "", $store4['content']);
		$objs4[] = $store4;
	}

	$acMsgSQL = mysql_query("SELECT * FROM accommentsinfo WHERE id = " . $row5['acid']);
	$acMsg = mysql_fetch_array($acMsgSQL, MYSQL_ASSOC);
	$row5['url'] = $acMsg['url'];
	$row5['type'] = $acMsg['type'];
	$row5['title'] = $acMsg['title'];
	$row5['up'] = $acMsg['up'];
	$row5['postTime'] = $acMsg['postTime'];
	$result = mysql_query($sql5);
	while ($store5 = mysql_fetch_row($result, MYSQL_ASSOC))
	{
		$store5 = rePrint($store5);
		$objs5[] = $store5;
	}

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