<?php
	//Open DB
	$dbname = 'deleteso';
	$host = 'rdsnqvfianubnan.mysql.rds.aliyuncs.com';
	$port = 3306;
	$user = 'deleteso';
	$pwd = 'deletepassso';

	//连接数据库 
	$con = @mysql_connect("{$host}:{$port}", $user, $pwd, true);
	if (!$con)
	{
		die('数据库连接失败！</br>错误原因：' . mysql_error());
	}

	//选定数据库 
	mysql_select_db($dbname, $con);

	$result = mysql_query("SELECT * FROM status WHERE name = 'acfunstart'");
	if ($row = mysql_fetch_array($result, MYSQL_ASSOC))
	{
		$start = $row['status'];
	}

	$result = mysql_query("SELECT * FROM status WHERE name = 'acfunend'");
	if ($row = mysql_fetch_array($result, MYSQL_ASSOC))
	{
		$end = $row['status'];
	}

	$result = mysql_query("SELECT * FROM status WHERE name = 'acrefresh'");
	if ($row = mysql_fetch_array($result, MYSQL_ASSOC))
	{
		$acrefresh = $row['status'];
	}

	if (date('y-m-d H:i:s') - strtotime() > 900)
		$status = "异常";
	else if (strtotime($end) - strtotime($start) > 900)
		$status = "异常";
	else if (strtotime($end) - strtotime($start) < -900)
		$status = "异常";
	else
		$status = "正常";

	$result = mysql_query("SELECT COUNT(*) AS total FROM (SELECT * FROM accomments WHERE siji = 1) AS a LIMIT 1");
	if ($row = mysql_fetch_array($result, MYSQL_ASSOC))
	{
		$siji = $row['total'];
	}

	$result = mysql_query("SELECT COUNT(*) AS total FROM (SELECT * FROM accomments WHERE isDelete = 1) AS a LIMIT 1");
	if ($row = mysql_fetch_array($result, MYSQL_ASSOC))
	{
		$isDelete = $row['total']; 
	}

	$result = mysql_query("SELECT COUNT(*) AS total FROM commentdb");
	if ($row = mysql_fetch_array($result, MYSQL_ASSOC))
	{
		$comments = $row['total'];
	}
	
	/*header("header('Content-type: text/json');");*/
    header("Access-Control-Allow-Origin:*");
	echo '{"status":';
	echo json_encode($status);
	echo ',"start":';
	echo json_encode($start);
	echo ',"end":';
	echo json_encode($end);
	echo ',"acrefresh":';
	echo json_encode($acrefresh);
	echo ',"isDelete":';
	echo json_encode($isDelete);
	echo ',"siji":';
	echo json_encode($siji);
	echo ',"comments":';
	echo json_encode($comments);
	echo '}';

	mysql_free_result($result); 
	//Close
	mysql_close($con);
	//echo '{"postTitle":' . json_encode($postTitle) . '"postContent":' . json_encode($postContent) . '"postUser":' . json_encode($postUser) . '"postTime":' . json_encode($postTime) . '}';
	//echo '{"postTitle":"1", "postContent":"2", "postUser":"3", "postTime":"4"}';
?>