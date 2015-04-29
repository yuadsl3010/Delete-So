<?php
	function clear_word($contents)
	{
		// 载入词典，成功返回一个 Trie_Filter 资源句柄，失败返回 NULL  
		return $contents;
		
		if ($contents == '')
		{
			return '';
		}

		$file = trie_filter_load('./word-filter.dic');  
		// 检测文本中是否含有词典中定义的敏感词(假设敏感词设定为：‘敏感词’)  
		$res = trie_filter_search($file, $contents);
		var_dump($res);
		if (empty($res) == false)
		{
			trie_filter_free($file); //最后别忘记调用free
			return '';
		}

		//$res1 = trie_filter_search_all($file, $str1);  // 一次把所有的敏感词都检测出来
		//$res2 = trie_filter_search($file, $str2);// 每次只检测一个敏感词  
		trie_filter_free($file); //最后别忘记调用free
		return $contents;
	}
?>

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

	$page = $_GET['page'];
	$uName = $_GET['userName'];
	$uContents = $_GET['contents'];
	$uCid = $_GET['cid'];
	$date = date('y-m-d H:i:s');

	$uContents = clear_word($uContents);
	if ($uContents == '')
	{
		$uName = '';
	}

	if ($uName != '')
	{
		if (strcmp($uCid, "0") != 0)
		{
			mysql_query("INSERT INTO comment2db(cid, userName, contents, postDate) VALUES('" . $uCid . "', '" . $uName . "', '" . $uContents . "', '" . $date . "')");
			mysql_query("UPDATE commentdb SET sortDate = '" . $date . "' WHERE cid = '" . $uCid . "'");
		}
		else
		{
			mysql_query("INSERT INTO commentdb(userName, contents, sortDate, postDate) VALUES('" . $uName . "', '" . $uContents . "', '" . $date . "', '" . $date . "')");
		}
	}

	if ($page == '')
		$page = 0;
	else
		$page = (int)$page;
	
	$totalRes = mysql_query("SELECT COUNT(*) AS total FROM commentdb");
	$res = mysql_query("SELECT * FROM commentdb ORDER BY sortDate DESC LIMIT " . ($page * 10) . ", 10");
	//执行SQL语句(查询) 

	$result = array();
	if ($row = mysql_fetch_array($totalRes, MYSQL_ASSOC))
	{
		$total = $row['total'];
	}

	while ($row = mysql_fetch_array($res, MYSQL_ASSOC))
	{
		$cid = $row["cid"];
		$tmpResult = mysql_query("SELECT * FROM comment2db WHERE cid = '" . $cid . "'");
		$tmpComment = array();
		while ($comments = mysql_fetch_array($tmpResult, MYSQL_ASSOC))
		{
			$tmpComment[] = $comments;
		}

		$row["comment2"] = $tmpComment;
		$result[] = $row;
	}

	/*header("header('Content-type: text/json');");*/
    header("Access-Control-Allow-Origin:*");
	echo '{"total":[';
	echo json_encode($total);
	echo '],"result":';
	echo json_encode($result);
	echo '}';

	mysql_free_result($result); 
	//Close
	mysql_close($con);
	//echo '{"postTitle":' . json_encode($postTitle) . '"postContent":' . json_encode($postContent) . '"postUser":' . json_encode($postUser) . '"postTime":' . json_encode($postTime) . '}';
	//echo '{"postTitle":"1", "postContent":"2", "postUser":"3", "postTime":"4"}';
?>