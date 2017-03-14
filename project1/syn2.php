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
	$startTags = array();
	$endTags = array();
	$arrayOfColors = array();
	$arrayOfSizes = array();
	$shiftnum = 0;
	$clrnum = 0;
	$sizenum = 0;
	

	$help = "IPP: Projekt - úloha SYN (Zvýraznění syntaxe):
optional parameters: 
	--format=\$path_to_file -> format file 
	--input=\$path_to_file -> input file
	--output=\$path_to_file -> output file
	--br -> EOL tag on each line of output";

	if ($argc > 5) {
		fwrite(STDERR, "Wrong format of arguments!\n");
		exit(1);
	}
	
	if ($argv[1] == "--help") {
		echo $help."\n";
		exit;
	}

	wrong_args_test();

	foreach (range(1, $argc) as $argnum) {

		if (substr($argv[$argnum], 0, 9) == "--format=") {
			$format_file = substr($argv[$argnum], 9, strlen($argv[$argnum]));
			$myformatfile = fopen($format_file, "r");

			if ($myformatfile == FALSE) {
				fwrite(STDERR, "Format file doesn't exist or error opening format file for reading.\n");
				exit(4);
			}
		}
	}
	
	foreach (range(1, $argc) as $argnum) {

		if (substr($argv[$argnum], 0, 8) == "--input=") {
			$input_file = substr($argv[$argnum], 8, strlen($argv[$argnum]));
			$myinputfile = fopen($input_file, "r");

			if ($myinputfile == FALSE) {
				fwrite(STDERR, "Input file does not exist or error opening input file for reading.\n");
				exit(2);
			}
			foreach (range(1, $argc) as $argnum) {

				if (substr($argv[$argnum], 0, 9) == "--output=") {
					$output_file = substr($argv[$argnum], 9, strlen($argv[$argnum]));
					$myoutputfile = fopen($output_file, "w");

					if ($myoutputfile == FALSE) {
						fwrite(STDERR, "Error opening input file for writing.\n");
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
					fwrite(STDERR, "Error opening input file for writing.\n");
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

 	function wrong_args_test() {
 		global $argc;
 		global $argv;
 			for($i=1; $i<$argc; ++$i) {
 				if ((substr($argv[$i], 0, 9) == "--format=") or
 				(substr($argv[$i], 0, 8) == "--input=") or
 				(substr($argv[$i], 0, 9) == "--output=") or
 				(substr($argv[$i], 0, 4) == "--br") or
 				(substr($argv[$i], 0, 6) == "--help")) {
 					continue;
 				}   	
 				else {
 					fwrite(STDERR, "Invalid argument '$argv[$i]'.\n");
 					exit(1);
 				}
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
				while(!feof($myformatfile)) {
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
 						if ($tab == FALSE) {
 							$regexp = $string;
 						}
 						$tab = TRUE;
 						$string = "";
 						continue;
 					}
 					elseif ((($char == ",") || ($char == "\n")) && ($tab == TRUE)) {
 						//echo $string."\n";
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
 					//echo $string."\n";
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
		global $arrayOfSizes;
		global $arrayOfColors;
		$output_array = array();
		$approvedChars = array();
		$repeat = FALSE;
		#$format_e = FALSE;
		$hexnum = FALSE;

		$count = 0;
		$overlay = FALSE;

			//print_r($arrayOfRules);
			//$overlay = is_overlayed($arrayOfRules, $inputContent);
				// print_r($arrayOfRules);
				// exit;
 				foreach ($arrayOfRules as $rule) {

 					$pattern = newPattern($arrayOfRules, $count);
 					echo $pattern."\n";
 					$count++;
 					foreach ($rule as $elem) {
		 			echo $elem."\n";
		 				
		 				 switch($elem) {

		 					case "bold":
								preg_match_all($pattern, $inputContent, $output_array);
			 						print_r($output_array);
			 						foreach($output_array as $array) {
			 							removeDuplicate($array);
			 							foreach ($array as $item) {
			 								//echo $item."\n";
			 								$inputContent = preg_replace("/".$item."/", "<b>".$item."</b>", $inputContent);
			 							}
			 						}
			 						if ($overlay == TRUE) {
			 							$inputContent = saveTag($inputContent, $elem);
			 						}
		 						break;

		 					case "italic":
		 					print_r($output_array);//berie aj tagy
		 						preg_match_all($pattern, $inputContent, $output_array);
								
			 						foreach($output_array as $array) {
			 							print_r($output_array);
			 							removeDuplicate($array);
			 							foreach ($array as $item) {
		 									$inputContent = preg_replace("/".$item."/", "<i>".$item."</i>", $inputContent);
			 							}
			 						}
			 						if ($overlay == TRUE) {
			 							$inputContent = saveTag($inputContent, $elem);
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
			 						if ($overlay == TRUE) {
			 							$inputContent = saveTag($inputContent, $elem);
			 						}
		 						break;

		 					case "teletype":
		 						preg_match_all($pattern, $inputContent, $output_array);
			 						foreach($output_array as $array) {
			 							removeDuplicate($array);
			 							foreach ($array as $item) {
		 									$inputContent = preg_replace("/".$item."/", "<tt>".$item."</tt>", $inputContent);
			 							}
			 						}
			 						if ($overlay == TRUE) {
			 							$inputContent = saveTag($inputContent, $elem);
			 						}
		 						break;

		 					default:
		 						echo $pattern."\n";
				 				if (!(substr($elem, 0, 5) == "size:") and !(substr($elem, 0, 6) == "color:")) {
			 						fwrite(STDERR, "Format table error: Nonexistent parameter '$elem'.\n");
		 							exit(4);	 						
								}
						}
						//$approvedChars = [];
		 				if (substr($elem, 0, 5) == "size:") {
		 					$sizeok = FALSE;
		 					$size = substr($elem, 5, strlen($elem));
		 					
		 					//print_r(range(1, 7));
		 					foreach (range(1, 7) as $value) {
		 						//echo $size."\n";
		 						//echo $value."\n";

		 						if ($size == $value) {
		 							$sizeok = TRUE;
		 						}
							}
							
							if ($sizeok != TRUE) {
		 						fwrite(STDERR, "Format table error: Invalid size '$size'.\n");
		 						exit(4);
		 					}				
		 					
							preg_match_all($pattern, $inputContent, $output_array);
								
			 						foreach($output_array as $array) {
			 							removeDuplicate($array);
			 							foreach ($array as $item) {
		 									$inputContent = preg_replace("/".$item."/", "<font size=".$size.">".$item."</font>", $inputContent);
			 							}
			 						}
			 						if ($overlay == TRUE) {
			 							$inputContent = saveTag($inputContent, $elem);
			 						}
			 						array_push($arrayOfSizes, $size);
						}
						
		 				elseif (substr($elem, 0, 6) == "color:") {
		 					$color = substr($elem, 6, strlen($elem));
		 					//echo $color."\n";
		 					$array_clr = str_split($color);
		 					$strlen_clr = strlen($color);
		 					//echo $strlen_clr."\n";
		 					
		 					for ($i=0; $i<strlen($color); ++$i) {
		 						//echo $array_clr[$i]."\n";
		 						foreach (range('A', 'F') as $char) {
		 							//echo $char."\n";
		 							if ($char == $array_clr[$i]) {
		 								$hexnum = TRUE;
		 								break;
		 							}
		 						}
		 						foreach (range(0, 9) as $value) {
		 							if ($value == $array_clr[$i]) {
		 								$hexnum = TRUE;
		 								break;
		 							}
		 						}
		 						
		 						if ($hexnum != TRUE) {
		 							fwrite(STDERR, "Format table error: Invalid color '$color'.\n");
		 							exit(4);
		 						}
		 					}
		 					preg_match_all($pattern, $inputContent, $output_array);
								
			 						foreach($output_array as $array) {
			 							removeDuplicate($array);
			 							foreach ($array as $item) {
		 									$inputContent = preg_replace("/".$item."/", "<font color=#".$color.">".$item."</font>", $inputContent);
			 							}
			 						}
			 						if ($overlay == TRUE) {
			 							$inputContent = saveTag($inputContent, $elem);
			 						}
			 						array_push($arrayOfColors, $color);
		 				} 		
		 			}
				}
				if ($overlay == TRUE) {	
					$inputContent = addSavedTags($inputContent);
					echo $inputContent."\n";
					exit;
				}
				//echo $inputContent."\n";
				//exit;
			}


	function newPattern($arrayOfRules, $count) {
		$num = 0;
		foreach ($arrayOfRules as $key => $value) {

			//echo $key."\n";
			if ($num == $count) {
				return $key;
			}
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

function saveTag($inputContent, $elem) {
	global $startTags;
	global $endTags;
	global $shiftnum;
	#$input = array();

	$input = str_split($inputContent);
	$elem = str_split($elem);
	
	$logsize = FALSE;
	$logcolor = FALSE;
	print_r($input);
	// exit;
	//print_r($input);
	for ($i=0; $i<count($input); ++$i) {
		if ($input[$i] == "<") {
			if ($input[$i+1] == "/") {

				switch ($input[$i+2]) {
					case 'b':
					echo "som v b\n";
						array_push($endTags, $i+$shiftnum);
						array_push($endTags, $elem[0]);
						unset_all($input, $i);
						$shiftnum += 4;
						break;
					case 'i':
						array_push($endTags, $i+$shiftnum);
						array_push($endTags, $elem[0]);
						unset_all($input, $i);
						$shiftnum += 4;
						break;
					case 'u':
						array_push($endTags, $i+$shiftnum);
						array_push($endTags, $elem[0]);
						unset_all($input, $i);
						$shiftnum += 4;
						break;
					case 't':
						array_push($endTags, $i+$shiftnum);
						array_push($endTags, $elem[0]);
						unset_all($input, $i);
						$shiftnum += 5;
						break;
					case 'f':
						// echo "som v case f\n";
						// print_r($input);
						array_push($endTags, $i+$shiftnum);
						array_push($endTags, $elem[0]);
						unset_all($input, $i);
						if ($logsize == TRUE) {
							$logsize = FALSE;
						}
						else if ($logcolor == TRUE) {
							$logcolor = FALSE;
						}
						$shiftnum += 7;
						// echo "som za unsetom end tagu\n";
						// print_r($input);
				}
				echo "shiftnum: ".$shiftnum."\n";
			}
			else {
				switch ($input[$i+1]) {
					case 'b':
						array_push($startTags, $i+$shiftnum);
						array_push($startTags, $elem[0]);
						unset_all($input, $i);
						$shiftnum += 3;
						break;
					case 'i':
						array_push($startTags, $i+$shiftnum);
						array_push($startTags, $elem[0]);
						unset_all($input, $i);
						$shiftnum += 3;
						break;
					case 'u':
						array_push($startTags, $i+$shiftnum);
						array_push($startTags, $elem[0]);
						unset_all($input, $i);
						$shiftnum += 3;
						break;
					case 't':
						array_push($startTags, $i+$shiftnum);
						array_push($startTags, $elem[0]);
						unset_all($input, $i);
						$shiftnum += 4;
						break;
					case 'f':
						if (($input[$i+6]) == 'c') {
							array_push($startTags, $i+$shiftnum);
							array_push($startTags, $elem[0]);
							unset_all($input, $i);
							$logcolor = TRUE;
							$shiftnum += 20;
						} 
						else if (($input[$i+6]) == 's') {
							array_push($startTags, $i+$shiftnum);
							array_push($startTags, $elem[0]);
							unset_all($input, $i);
							$logsize = TRUE;
							//echo "som za unsetom start tagu\n";
							//print_r($input);
							$shiftnum += 13;
						}
						break;
				}
			}
		}
		//echo $i."\n";
	}
	// print_r($startTags);
	// print_r($endTags);
	// print_r($input);
	//exit;
	
	$input = implode($input);
	//$input = str_split($input);

	//echo $input."\n";
	// exit;
	return $input;
}

function unset_all(&$input, $i) {
	echo "som v unsete\n";
	print_r($input);
	foreach ($input as $key => $value) {
		echo $value."\n";
		if ($value == '>') {
			for ($j=$i; $j<=$key; $j++) {
				unset($input[$j]);
			}
			break;
		}
	}
	$input = implode($input);
	$input = str_split($input);
	//print_r($input);
}


function addSavedTags($inputContent) {
	echo "som v addSavedTags\n";
	// global $arrayOfColors;
	// global $arrayOfSizes;
	global $startTags;
	global $endTags;
	// print_r($arrayOfColors);
	// print_r($arrayOfSizes);
	// exit;
	print_r($startTags);
	print_r($endTags);
	//$arrayOfColors = str_split($color);
	$len = strlen($inputContent);
	$input = str_split($inputContent);

	if (empty($startTags)) {
		return;
	}
	else {
		$numOfStartTags = count($startTags)/2;
		//echo $numOfStartTags."\n";
		//exit;
	}

	for ($i=0; $i<$numOfStartTags; $i++) {
		//print_r($input);
		// if ($startTags[$i] === "c") {
		// 	$hexnum++;
		// }
		addStartTag($input, $startTags);
		//echo "vypis input po start\n";
		//print_r($input);
		addEndTag($input, $endTags);
		//print_r($input);
		
		unset($startTags[0]);
		unset($startTags[1]);
		unset($endTags[0]);
		unset($endTags[1]);
		
		$startTags = implode(",", $startTags);
		$startTags = explode(",", $startTags);
		//print_r($startTags);
		
		$endTags = implode(",", $endTags);
		$endTags = explode(",", $endTags);
		//print_r($endTags);
	}
	//print_r($input);
	//print_r($input);
	$input = implode($input);
	//echo $input."\n";
	return $input;
}

function shift($index, $num, &$arrayOfChars) {

	//echo "som v shifte\n";
	//exit;
	//echo $index."\n";
	for ($j=0; $j<$num; $j++){
		$count = count($arrayOfChars);
		for ($i=$count-1; $i>=$index; $i--) {
			$arrayOfChars[$i+1] = $arrayOfChars[$i];

		}
		$arrayOfChars[$index] = "";			
	}
}

function is_overlayed($arrayOfRules, $inputContent) {

	$allPattern = array();
	$output_array = array();
	$results = array();
	$arrayOfResults = array();
	$arrayOfResults2 = array();
	$numOfKeys = 0;
	foreach ($arrayOfRules as $key => $value) {

		//echo $key."\n";
		array_push($allPattern, $key);
		$numOfKeys++;

	}
	//print_r($allPattern);

	foreach ($allPattern as $key => $value) {
		//echo $value."\n";
		preg_match_all($value, $inputContent, $output_array);
		foreach ($output_array as $key => $value) {
			foreach ($value as $key2 => $value2) {
				// echo $value2."\n";
				array_push($results ,$value2);
			}
		}
	}	
	//echo "results\n";
	//print_r($results);
	if (count($results) == 1) {
		return FALSE;
	}
	$count = count($results);
					
	foreach ($results as $key => $value) {
		//echo $value."\n";
		
		$arrayOfResults = explode(" ", $value);
		//print_r($arrayOfResults);
		
		if (empty($arrayOfResults2)) {
			$arrayOfResults2 = $arrayOfResults;
		}
	
	}

	for ($i=0; $i<count($arrayOfResults); ++$i) {
		for ($j=$i; $j<count($arrayOfResults2); ++$j) {
			if ($arrayOfResults[$i] == $arrayOfResults2[$j]) {
				//echo "nasiel som zhodu\n";
				return TRUE;
			}
		}
	}
	//echo "som za porovnavanim\n";
	return FALSE;
}

function addStartTag(&$input, $startTags) {
	global $arrayOfColors;
	global $arrayOfSizes;
	global $clrnum;
	global $sizenum;
	// print_r($arrayOfColors);
	// print_r($arrayOfSizes);

	echo "som v addStartTag\n";
	//print_r($input);
	
	// if (empty($startTags)) {
	// 	return;
	// }
	// else {
	// 	$numOfStartTags = count($startTags)/2;
	// }
	// print_r($startTags);
	//echo count($startTags)."\n";
	//exit;
	for ($i=0; $i<count($startTags); $i=$i+2) {
			
			if ($startTags[$i+1] === "b") {
				shift($startTags[$i], 3, $input);
				$input[$startTags[$i]] = "<";
				$input[$startTags[$i]+1] = $startTags[$i+1];
				$input[$startTags[$i]+2] = ">";
				break;
			}
			else if ($startTags[$i+1] === "i") {
					shift($startTags[$i], 3, $input);
					$input[$startTags[$i]] = "<";
					$input[$startTags[$i]+1] = $startTags[$i+1];
					$input[$startTags[$i]+2] = ">";
					break;
			}
			else if ($startTags[$i+1] === "u") {
					shift($startTags[$i], 3, $input);
					$input[$startTags[$i]] = "<";
					$input[$startTags[$i]+1] = $startTags[$i+1];
					$input[$startTags[$i]+2] = ">";
					break;
			}
			else if ($startTags[$i+1] === "t") {
					shift($startTags[$i], 4, $input);
					$input[$startTags[$i]] = "<";
					$input[$startTags[$i]+1] = $startTags[$i+1];
					$input[$startTags[$i]+2] = $startTags[$i+1];
					$input[$startTags[$i]+3] = ">";
					break;
			}
			else if ($startTags[$i+1] === "s") {
					echo "som v case s\n";
					shift($startTags[$i], 13, $input);
					$input[$startTags[$i]] = "<";
					$input[$startTags[$i]+1] = "f";
					$input[$startTags[$i]+2] = "o";
					$input[$startTags[$i]+3] = "n";
					$input[$startTags[$i]+4] = "t";
					$input[$startTags[$i]+5] = " ";
					$input[$startTags[$i]+6] = "s";
					$input[$startTags[$i]+7] = "i";
					$input[$startTags[$i]+8] = "z";
					$input[$startTags[$i]+9] = "e";
					$input[$startTags[$i]+10] = "=";
					$input[$startTags[$i]+11] = $arrayOfSizes[$sizenum];
					$input[$startTags[$i]+12] = ">";
					print_r($input);
					$sizenum++;
					break;
			}
			else if ($startTags[$i+1] === "c") {
					$hexnum = $arrayOfColors[$clrnum];
					//echo $hexnum."\n";
					$hexnum = str_split($hexnum);
					//print_r($hexnum);
					$clrnum++;
					shift($startTags[$i], 20, $input);
					$input[$startTags[$i]] = "<";
					$input[$startTags[$i]+1] = "f";
					$input[$startTags[$i]+2] = "o";
					$input[$startTags[$i]+3] = "n";
					$input[$startTags[$i]+4] = "t";
					$input[$startTags[$i]+5] = " ";
					$input[$startTags[$i]+6] = "c";
					$input[$startTags[$i]+7] = "o";
					$input[$startTags[$i]+8] = "l";
					$input[$startTags[$i]+9] = "o";
					$input[$startTags[$i]+10] = "r";
					$input[$startTags[$i]+11] = "=";
					$input[$startTags[$i]+12] = "#";
					$input[$startTags[$i]+13] = $hexnum[0];
					$input[$startTags[$i]+14] = $hexnum[1];
					$input[$startTags[$i]+15] = $hexnum[2];
					$input[$startTags[$i]+16] = $hexnum[3];
					$input[$startTags[$i]+17] = $hexnum[4];
					$input[$startTags[$i]+18] = $hexnum[5];
					$input[$startTags[$i]+19] = ">";
					break;
			}
	}

}

function addEndTag(&$input, $endTags) {
	echo "som v addEndTag\n";
	
	if (empty($endTags)) {
		return;
	}
	else {
		$numOfEndTags = count($endTags)/2;
		echo $numOfEndTags."\n";
	}
	//print_r($endTags);

	for ($i=0; $i<count($endTags); $i=$i+2) {
			// echo $i."\n";
			// echo $startTags[$i]."\n";
			// exit;
			if ($endTags[$i+1] === "b") {
				shift($endTags[$i], 4, $input);
					$input[$endTags[$i]] = "<";
					$input[$endTags[$i]+1] = "/";
					$input[$endTags[$i]+2] = $endTags[$i+1];
					$input[$endTags[$i]+3] = ">";
					break;
			}
			else if ($endTags[$i+1] === "i") {
					shift($endTags[$i], 4, $input);
					$input[$endTags[$i]] = "<";
					$input[$endTags[$i]+1] = "/";
					$input[$endTags[$i]+2] = $endTags[$i+1];
					$input[$endTags[$i]+3] = ">";
					break;
			}
			else if ($endTags[$i+1] === "u") {
					shift($endTags[$i], 4, $input);
					$input[$endTags[$i]] = "<";
					$input[$endTags[$i]+1] = "/";
					$input[$endTags[$i]+2] = $endTags[$i+1];
					$input[$endTags[$i]+3] = ">";
					break;
			}
			else if ($endTags[$i+1] === "t") {
					shift($endTags[$i], 5, $input);
					$input[$endTags[$i]] = "<";
					$input[$endTags[$i]+1] = "/";
					$input[$endTags[$i]+2] = $endTags[$i+1];
					$input[$endTags[$i]+3] = $endTags[$i+1];
					$input[$endTags[$i]+4] = ">";
					break;
			}
			else if ($endTags[$i+1] === "s") {
				echo "som v case s end\n";
					//print_r($input);
					
					shift($endTags[$i], 7, $input);
					//print_r($input);
					
					$input[$endTags[$i]] = "<";
					$input[$endTags[$i]+1] = "/";
					$input[$endTags[$i]+2] = "f";
					$input[$endTags[$i]+3] = "o";
					$input[$endTags[$i]+4] = "n";
					$input[$endTags[$i]+5] = "t";
					$input[$endTags[$i]+6] = ">";
					//print_r($input);
					
					break;
			}
			else if ($endTags[$i+1] === "c") {
					shift($endTags[$i], 7, $input);
					$input[$endTags[$i]] = "<";
					$input[$endTags[$i]+1] = "/";
					$input[$endTags[$i]+2] = "f";
					$input[$endTags[$i]+3] = "o";
					$input[$endTags[$i]+4] = "n";
					$input[$endTags[$i]+5] = "t";
					$input[$endTags[$i]+6] = ">";
					break;
			}
	}
}
?>