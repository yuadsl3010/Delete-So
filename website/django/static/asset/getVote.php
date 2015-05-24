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

	$uCid = $_GET['cid'];
	$uDo = $_GET["action"];

	$result = mysql_query("SELECT * FROM sijidb WHERE cid = '" . $uCid . "'");
	if ($row = mysql_fetch_array($result, MYSQL_ASSOC))
	{
		$person = $row["person"];
		$checkTime = $row["checkTime"];
	}

	if ($uDo != "get")
	{
		if ($uDo == "up")
		{
			$person = (int)$person + 1;
			$checkTime = strtotime($checkTime) + 72000;
		}
		else if($uDo == "down")
		{
			$person = (int)$person - 1;
			$checkTime = strtotime($checkTime) - 72000;
		}

		mysql_query("UPDATE sijidb SET person = '" . $person . "', checkTime = '" . date('y-m-d H:i:s', $checkTime) . "' WHERE cid = '" . $uCid . "'");
	}

	/*header("header('Content-type: text/json');");*/
    header("Access-Control-Allow-Origin:*");
	echo '{"person":[';
	echo json_encode($person);
	echo ']}';

	mysql_free_result($result); 
	//Close
	mysql_close($con);
	//echo '{"postTitle":' . json_encode($postTitle) . '"postContent":' . json_encode($postContent) . '"postUser":' . json_encode($postUser) . '"postTime":' . json_encode($postTime) . '}';
	//echo '{"postTitle":"1", "postContent":"2", "postUser":"3", "postTime":"4"}';
?>