<?php
	session_start();
	$titles = array();
	$classes = array();
	$nl = "\n";
	
	function showNavigation() {
		global $titles, $classes, $nl;
		$dh = opendir('modules');
		while (($file = readdir($dh)) !== false) {
			$safeext = '.php';
			$l = strlen($file);
			if (strpos($file, $safeext) == $l - strlen($safeext) && $l > strlen($safeext)) {
				//it's a .php file!
				include_once 'modules/'.$file;
			}
		}
		closedir($dh);
		foreach ($titles as $key=>$val) {
			echo '<a href="?module='.$key.'">'.$titles[$key].'</a> '.$nl;
		}
	}
	
	function executeModule($module) {
		global $titles, $classes, $nl;
		$classes[$module]->display();
	}
	
	showNavigation();
	if (isset($_GET['module'])) {
		executeModule($_GET['module']);
	}
	
?>