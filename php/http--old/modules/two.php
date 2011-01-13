<?php
	$classID = 'two';
	class two {
		function display() {
			echo 'This is #2';
		}
	}
	$classes[$classID] = new two();
	$titles[$classID] = 'Two';
?>