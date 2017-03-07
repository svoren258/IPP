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
	$arrayOfRules = array();
	$arrayOfPattern = array();

	$help = "IPP: Projekt - úloha SYN (Zvýraznění syntaxe):
optional parameters: 
	--format=\$path_to_file -> format file 
	--input=\$path_to_file -> input file
	--output=\$path_to_file -> output file
	--br -> EOL tag on each line of output";

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
				fwrite(STDERR, "Error by opening input file for reading.\n");
				exit(2);
			}
			foreach (range(1, $argc) as $argnum) {

				if (substr($argv[$argnum], 0, 9) == "--output=") {
					$output_file = substr($argv[$argnum], 9, strlen($argv[$argnum]));
					$myoutputfile = fopen($output_file, "w");

					if ($myoutputfile == FALSE) {
						fwrite(STDERR, "Error by opening input file for writing.\n");
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
		echo "Enter your input: ";
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
 			if (empty($inputContent)){
 				return;
 			}
 			$arrayOfChars = str_split($inputContent);
 			if ($arrayOfChars[strlen($inputContent)-1] != "\n") {
					array_push($arrayOfChars, "\n");		
				}
			$inputContent = implode($arrayOfChars);

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
 	 			//echo $inputContent."\n";
 	 			regexpSetting($myformatfile, $inputContent);
 	 			endTag($inputContent);
 	 			fwrite($myoutputfile, $inputContent);
 	 		}
		}
		elseif ($stdin == TRUE) {
			regexpSetting($myformatfile, $myinputfile);
 	 		endTag($myinputfile);
 	 		fwrite($myoutputfile, $myinputfile);
		}	
	}


	function closeFiles($myinputfile, $myoutputfile, $myformatfile) {
		if ($myinputfile != "") {
			fclose($myinputfile);	
		} 

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
			global $arrayOfRules;
			global $arrayOfPattern;

			if (empty($arrayOfRules)) {
				while(!feof($myformatfile)){
				$arrayOfElem = array();
				$regexp = "";
				$tab = FALSE;
				
				$line = fgets($myformatfile);
				$arrayOfChars = str_split($line);

				
				if ($arrayOfChars[strlen($line)-1] != "\n") {
					array_push($arrayOfChars, "\n");		
				}
 					
				foreach ($arrayOfChars as $char) {
 					if ($char == "\t") {

 						$tab = TRUE;
 						$regexp = $string;

 						$string = "";
 						continue;
 					}
 					elseif (($char == ",") || ($char == "\n")) {
 						array_push($arrayOfElem, $string);
 						$string = "";
 						continue;
 					}
 					elseif ($char == " "){;
 						if ($tab == FALSE) {
 							$string .= $char;
 						}
 						continue;
 					}
 					$string .= $char;
 				}

			
 			regexpSettings($regexp);
 			$pattern = "/".$regexp."/";
 			$arrayOfRules[$pattern] = $arrayOfElem;	
		}
		
		addTag($arrayOfRules, $inputContent);
			}
			else {
				addTag($arrayOfRules, $inputContent);
			}
			
	}
		else {
			return;
		}
	}	


	function addTag($arrayOfRules, &$inputContent) {
		$output_array = array();
		$approvedChars = array();
		$repeat = FALSE;
		$count = 0;
				#hideElem($inputContent);
 				foreach ($arrayOfRules as $rule) {
 					//print_r($rule);
 					$pattern = newPattern($arrayOfRules, $count);
 					$count++;
 					foreach ($rule as $elem) {
		 				//echo $elem."\n";
		 				
		 				 switch($elem) {

		 					case "bold":

								preg_match_all($pattern, $inputContent, $output_array);
			 						
			 						foreach($output_array as $array) {
			 							removeDuplicate($array);
			 							foreach ($array as $item) {
			 								$inputContent = preg_replace("/".$item."/", "<b>".$item."</b>", $inputContent);
			 							}
			 						}
		 						break;

		 					case "italic":

		 						preg_match_all($pattern, $inputContent, $output_array);
								
			 						foreach($output_array as $array) {
			 							removeDuplicate($array);
			 							foreach ($array as $item) {
		 									$inputContent = preg_replace("/".$item."/", "<i>".$item."</i>", $inputContent);
			 							}
			 						}
		 						break;

		 					case "underline":
		 						preg_match_all($pattern, $inputContent, $output_array);
								
			 						foreach($output_array as $array) {
			 							removeDuplicate($array);
			 							foreach ($array as $item) {
		 									$inputContent = preg_replace("/".$item."/", "<u>".$item."</u>", $inputContent);
			 							}
			 						}
		 						break;

		 					case "teletype":
		 						preg_match_all($pattern, $inputContent, $output_array);
								//print_r($output_array);
								// print_r($output_array);
			 						foreach($output_array as $array) {
			 							removeDuplicate($array);
			 							foreach ($array as $item) {
			 								#echo $item."\n";
		 									$inputContent = preg_replace("/".$item."/", "<tt>".$item."</tt>", $inputContent);
			 								#echo $inputContent."\n";
			 							}
			 						}
		 						break;
						}
						//$approvedChars = [];
		 				if (substr($elem, 0, 5) == "size:") {
		 					$size = substr($elem, 5, strlen($elem));
		 			
							preg_match_all($pattern, $inputContent, $output_array);
								
			 						foreach($output_array as $array) {
			 							removeDuplicate($array);
			 							foreach ($array as $item) {
		 									$inputContent = preg_replace("/".$item."/", "<font size=".$size.">".$item."</font>", $inputContent);
			 							}
			 						}
						}

		 				elseif (substr($elem, 0, 6) == "color:") {
		 					
		 					$color = substr($elem, 6, strlen($elem));
		 					preg_match_all($pattern, $inputContent, $output_array);
								
			 						foreach($output_array as $array) {
			 							removeDuplicate($array);
			 							foreach ($array as $item) {
		 									$inputContent = preg_replace("/".$item."/", "<font color=#".$color.">".$item."</font>", $inputContent);
			 							}
			 						}
		 				}	 		
		 			}
				}
			}


	function newPattern($arrayOfRules, $count) {
		$num = 0;
		while($array = current($arrayOfRules)){
 			$pattern = key($arrayOfRules);
 			
 			if ($num == $count) {
 				return $pattern;
 			}
 			next($arrayOfRules);
 			$num++;
 		}
	}

	function regexpSettings(&$regexp) {
		switch ($regexp) {
			case "%s":
				$regexp = "\s";
				break;
			
			case "%a":
				$regexp = "\S";
				break;

			case "%d":
				$regexp = "[0-9]";
				break;

			case "%l":
				$regexp = "[a-z]";
				break;

			case "%L":
				$regexp = "[A-Z]";
				break;

			case "%w":
				$regexp = "[a-zA-Z]";
				break;

			case "%W":
				$regexp = "[a-zA-Z0-9]";
				break;

			case "%t":
				$regexp = "\t";
				break;

			case "%n":
				$regexp = "\n";
				break;

			default:
				break;
		}
	}

function removeDuplicate(&$array) {
	$count = count($array);
	for ($i=0; $i < $count; $i++) {
		for ($j=$i+1; $j < $count; $j++){
			if ($array[$i] == $array[$j]) {
				unset($array[$i]);
			}
		}
	}		
}

// function hideElem($inputContent) {
// 	$words = array();
// 	$words = explode(space(), $inputContent);
// 	print_r($words);
// 	exit;
// }

// function space() {
// 	$string = 
// 	return $string;
// }
?>