#!/bin/php
<?php
	$help = "Napoveda";
	if ($argv[1] === "--help") {
		echo $help."\n";
	}
	elseif (substr($argv[1], 0, 9) === "--format=") {
		$filename = substr($argv[1], 9, strlen($argv[1]));
		echo $filename."\n";
	}
	else {
		echo $argv[0]."\n";
	}
?>