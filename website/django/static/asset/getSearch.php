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

	$search = $_GET['search'];
	$page = $_GET['page'];
	$result = array();
	if ($search != '')
	{
		if ($page == '')
			$page = 0;
		else
			$page = (int)$page;

		if (strcmp($search, "带带我") == 0)
		{
			$totalRes = mysql_query("SELECT COUNT(*) AS total FROM accomments WHERE siji = 1 LIMIT 1");
			$res = mysql_query("SELECT * FROM (SELECT * FROM accomments WHERE siji = 1) as t ORDER BY checkTime DESC LIMIT " . $page * 10 . ", 10");
			if ($row = mysql_fetch_array($totalRes, MYSQL_ASSOC))
			{
				$total = $row['total'];
			}

			while ($row = mysql_fetch_array($res, MYSQL_ASSOC))
			{
				$acMsgSQL = mysql_query("SELECT * FROM accommentsinfo WHERE id = " . $row['acid']);
				$acMsg = mysql_fetch_array($acMsgSQL, MYSQL_ASSOC);
				$row['url'] = $acMsg['url'];
				$row['type'] = $acMsg['type'];
				$row['title'] = $acMsg['title'];
				$row['up'] = $acMsg['up'];
				$row['postTime'] = $acMsg['postTime'];

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
				$result[] = $row;
			}
		}
		else
		{
			if (strpos($search, 'ac') > -1)
			{
				$search = substr($search, 2);
			}

			if (strpos($search, ' ') > 0)
			{
				$acid = substr($search, 0, strpos($search, ' '));
				$layer = substr($search, strpos($search, ' ') + 1);
				setRefresh($acid);
				$totalRes = mysql_query("SELECT COUNT(*) AS total FROM accomments WHERE layer = " . $layer . " AND acid = " . $acid . " AND isDelete = 1 LIMIT 1");
				$res = mysql_query("SELECT * FROM accomments WHERE layer = " . $layer . " AND acid = " . $acid . " AND isDelete = 1 " . "LIMIT " . $page * 10 . ", 10");
			}
			else
			{
				$acid = $search;
				setRefresh($acid);
				$totalRes = mysql_query("SELECT COUNT(*) AS total FROM accomments WHERE acid = " . $acid . " AND isDelete = 1 LIMIT 1");
				$res = mysql_query("SELECT * FROM accomments WHERE acid = " . $acid . " AND isDelete = 1 " . "LIMIT " . $page * 10 . ", 10");
			}

			if ($row = mysql_fetch_array($totalRes, MYSQL_ASSOC))
			{
				$total = $row['total'];
			}

			while ($row = mysql_fetch_array($res, MYSQL_ASSOC))
			{
				$acMsgSQL = mysql_query("SELECT * FROM accommentsinfo WHERE id = " . $row['acid']);
				$acMsg = mysql_fetch_array($acMsgSQL, MYSQL_ASSOC);
				$row['url'] = $acMsg['url'];
				$row['type'] = $acMsg['type'];
				$row['title'] = $acMsg['title'];
				$row['up'] = $acMsg['up'];
				$row['postTime'] = $acMsg['postTime'];
				
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
				$result[] = $row;
			}
		}
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

	function setRefresh($acid)
	{
		$date = date('y-m-d H:i:s');
		mysql_query("INSERT INTO acrefresh(id, createTime, status) VALUES ('" . $acid . "', '" . $date . "', '0')");
	}
?>