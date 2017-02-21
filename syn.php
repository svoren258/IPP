#!/bin/php
<?php

	#Global variables init:
	$myoutputfile = "";
	$myinputfile = "";
	$myformatfile = "";
	$string = "";
	$regexp = "";
	$endOfLine = FALSE;
	$arrayOfElem = array();

	$help = "IPP: Projekt - úloha SYN (Zvýraznění syntaxe)";

	if ($argc > 5) {
		fwrite(STDERR, "Wrong format of parameters!\n");
		exit(1);
	}
	
	if ($argv[1] == "--help") {
		echo $help."\n";
		exit;
	}

	foreach (range(1, $argc) as $argnum) {
		if (substr($argv[$argnum], 0, 9) == "--format=") {
			$format_file = substr($argv[$argnum], 9, strlen($argv[$argnum]));
			$myformatfile = fopen($format_file, "r");
			if ($myformatfile == FALSE) {
				fwrite(STDERR, "Format file doesn't exist or error by opening format file for reading.\n");
				exit(4);
			}
		}
	}
	
	foreach (range(1, $argc) as $argnum) {
		if (substr($argv[$argnum], 0, 8) == "--input=") {
			$input_file = substr($argv[$argnum], 8, strlen($argv[$argnum]));
			$myinputfile = fopen($input_file, "r");
			if ($myinputfile == FALSE) {
				fwrite(STDERR, "Input file doesn't exist or error by opening input file for reading.\n");
				exit(2);
			}
			foreach (range(1, $argc) as $argnum) {
				if (substr($argv[$argnum], 0, 9) == "--output=") {
					$output_file = substr($argv[$argnum], 9, strlen($argv[$argnum]));
					$myoutputfile = fopen($output_file, "w");
					if ($myoutputfile == FALSE) {
						fwrite(STDERR, "Output file doesn't exist or error by opening input file for writing.\n");
						exit(3);
					}
					inToOut($myinputfile, $myoutputfile, $myformatfile, FALSE);
					break;
				}
			}
			if ($myoutputfile == "") {
				$myoutputfile = fopen("php://stdout", "w");
				inToOut($myinputfile, $myoutputfile, $myformatfile, FALSE);
				break;
			}	
		}
	}

	if ($myinputfile == "") {
		$inputContent = trim(fgets(STDIN));
		foreach (range(1, $argc) as $argnum) {
			if (substr($argv[$argnum], 0, 9) == "--output=") {
				$output_file = substr($argv[$argnum], 9, strlen($argv[$argnum]));
				$myoutputfile = fopen($output_file, "w");
				if ($myoutputfile == FALSE) {
					fwrite(STDERR, "Output file doesn't exist or error by opening input file for writing.\n");
					exit(3);
				}
					
				inToOut($inputContent, $myoutputfile, $myformatfile, TRUE);
				break;
					
			}
		}
		if (($myoutputfile == "")) {
			$myoutputfile = fopen("php://stdout", "w");
			inToOut($inputContent, $myoutputfile, $myformatfile, TRUE);
		}			
 	}
			
 	function endTag(&$inputContent) {
 		global $argc;
 		global $argv;

 		foreach (range(1, $argc) as $argnum) {	
			if (substr($argv[$argnum], 0, 4) == "--br") {
		 		$inputContent = preg_replace("/\n/", "<br />\n", $inputContent);
		 		break;
			}
		}
	}

	closeFiles($myinputfile, $myoutputfile, $myformatfile);


	function inToOut($myinputfile, $myoutputfile, $myformatfile, $stdin) {

		if ($stdin == FALSE) {
			while(!feof($myinputfile)) {
 	 			$inputContent = fgets($myinputfile);
 	 			echo $inputContent."\n";
 	 			endTag($inputContent);
 	 			regexpSetting($myformatfile, $inputContent);
 	 			fwrite($myoutputfile, $inputContent);
 	 		}
		}
		elseif ($stdin == TRUE) {
			endTag($myinputfile);
			regexpSetting($myformatfile, $myinputfile);
 	 		fwrite($myoutputfile, $myinputfile);
		}	
	}


	function closeFiles($myinputfile, $myoutputfile, $myformatfile) {
		if ($myinputfile != "") {
			fclose($myinputfile);	
		} 
		#pred uzavretim suboru prechadzam na dalsi riadok
		fwrite($myoutputfile, "\n");
		fclose($myoutputfile);
		if ($myformatfile != "") {
			fclose($myformatfile);
		}
	}
	
	function regexpSetting($myformatfile, &$inputContent) {
		//spracovanie formatovacieho suboru a regularnych vyrazov//

		if ($myformatfile != "") {

			global $string;
			global $regexp;
			global $endOfLine;
			global $arrayOfElem;
			// $output_array = array();
			
			#$elements = implode(" ", $arrayOfElem);
			if ((empty($arrayOfElem) == true) and ($regexp == "")) {
				while(!feof($myformatfile)){
				echo "som vo while\n";
				$tab = FALSE;
				
				$line = fgets($myformatfile);
				echo $line."\n";
				$arrayOfChars = str_split($line);
				
				if ($arrayOfChars[strlen($line)-1] != "\n") {
					array_push($arrayOfChars, "\n");		
				}
 					
				foreach ($arrayOfChars as $char) {

 					if ($char == "\t") {
 						$tab = TRUE;
 						$regexp = $string;
 						$string = "";
 						#echo $regexp."\n";
 						continue;
 					}
 					elseif (($char == ",") || ($char == "\n")) {
 						array_push($arrayOfElem, $string);
 						$string = "";
 						continue;
 					}
 					elseif ($char == " "){;
 						if ($tab == FALSE) {
 							#echo "som v ife v ktorom nemam byt\n";
 							$string .= $char;
 						}
 						continue;
 					}
 					$string .= $char;
 					#echo $string."\n";
 				}
			 
 			#echo $regexp." regexp\n";
 			
 			$pattern = "/".$regexp."/";

 			addTag($arrayOfElem, $pattern, $inputContent);
		}
			}
			else {
				$pattern = "/".$regexp."/";
				addTag($arrayOfElem, $pattern, $inputContent);
			}
			
	}
		else {
			return;
		}
	}	


	function addTag($arrayOfElem, $pattern, &$inputContent) {
		$output_array = array();
		foreach ($arrayOfElem as $elem) {
 				echo $elem."\n";
 				 switch($elem) {
 					case "bold":
 						preg_match($pattern, $inputContent, $output_array);
 						foreach($output_array as $item) {

 							$inputContent = preg_replace($pattern, "<b>".$item."</b>", $inputContent);
 							#echo $inputContent."\n";
 						}
 						break;

 					case "italic":
 						echo $inputContent."\n";
 						echo $pattern."\n";
 						preg_match($pattern, $inputContent, $output_array);
 						
 						foreach($output_array as $item) {
 							#echo $item."\n";
 							#echo $inputContent."\n";
 							$inputContent = preg_replace($pattern, "<i>".$item."</i>", $inputContent);
 							#echo $inputContent."\n";
 						}
 						break;

 					case "underline":
 						preg_match($pattern, $inputContent, $output_array);
 						foreach($output_array as $item) {
 							$inputContent = preg_replace($pattern, "<u>".$item."</u>", $inputContent);
 						}
 						break;

 					case "teletype":
 						preg_match($pattern, $inputContent, $output_array);
 						foreach($output_array as $item) {
 							$inputContent = preg_replace($pattern, "<tt>".$item."</tt>", $inputContent);
 						}
 						break;
				}
 				if (substr($elem, 0, 5) == "size:") {
 					$size = substr($elem, 5, strlen($elem));
					preg_match($pattern, $inputContent, $output_array);
 					foreach($output_array as $item) {
 						$inputContent = preg_replace($pattern, "<font size=".$size.">".$item."</font>", $inputContent);
 					}
				}
 				elseif (substr($elem, 0, 6) == "color:") {
 					$color = substr($elem, 6, strlen($elem));
 					preg_match($pattern, $inputContent, $output_array);
 					foreach($output_array as $item) {
 						$inputContent = preg_replace($pattern, "<font color=#".$color.">".$item."</font>", $inputContent);
 					}
 				}
 			}
	}
?>