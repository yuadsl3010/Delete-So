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
	
	$ip = get_client_ip(); 
	$type = $_GET['type'];
	$date = date('y-m-d H:i:s');
	$sql = "SELECT * FROM ip WHERE ip = '" . $ip . "'";
	$res = mysql_query($sql);
	$rows = mysql_fetch_array($res);
	if (empty($rows))
	{
		mysql_query("INSERT INTO ip (ip, time) VALUES ('" . $ip . "', '" . $date . "')");
		$res = mysql_query("SELECT * FROM access WHERE type = '" . $type . "'");
		$rows = mysql_fetch_array($res);
		mysql_query("UPDATE access SET count = '" . ((int)$rows['count'] + 1) . "' WHERE type = '" . $type . "'");
	}
	else
	{
		$time = strtotime($date) - strtotime($rows['time']);
		$minutes = $time / 60;
		if ($minutes > 1)
		{
			mysql_query("UPDATE ip SET time = '" . $date . "' WHERE ip = '" . $ip . "'");
			$res = mysql_query("SELECT * FROM access WHERE type = '" . $type . "'");
			$rows = mysql_fetch_array($res);
			mysql_query("UPDATE access SET count = '" . ((int)$rows['count'] + 1) . "' WHERE type = '" . $type . "'");
		}
	}

    header("Access-Control-Allow-Origin:*");
	mysql_free_result($result); 
	//Close
	mysql_close($con);

	function get_client_ip()
	{
	    foreach (array(
                'HTTP_CLIENT_IP',
                'HTTP_X_FORWARDED_FOR',
                'HTTP_X_FORWARDED',
                'HTTP_X_CLUSTER_CLIENT_IP',
                'HTTP_FORWARDED_FOR',
                'HTTP_FORWARDED',
                'REMOTE_ADDR') as $key) {
	        if (array_key_exists($key, $_SERVER)) {
	            foreach (explode(',', $_SERVER[$key]) as $ip) {
	                $ip = trim($ip);
	                if ((bool) filter_var($ip, FILTER_VALIDATE_IP,
	                                FILTER_FLAG_IPV4 |
	                                FILTER_FLAG_NO_PRIV_RANGE |
	                                FILTER_FLAG_NO_RES_RANGE)) {
	                    return $ip;
	                }
	            }
	        }
	    }
	    return null;
	}
?>