#!/bin/php
<?php
	#Global variables init:
	$myoutputfile = "";
	$myinputfile = "";
	$myformatfile = "";
	$string = "";
	$regexp = "";
	$endOfLine = FALSE;
	//$overlap = FALSE;
	$arrayOfElem = array();
	$arrayOfRules = array();
	$arrayOfPattern = array();
	$startTagArray = array();
	$endTagArray = array();
	$shiftnum = 0;

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
		if (!empty($argv[$argnum])) {
			if (substr($argv[$argnum], 0, 9) == "--format=") {
				$format_file = substr($argv[$argnum], 9, strlen($argv[$argnum]));
				$myformatfile = fopen($format_file, "r");
				if ($myformatfile == FALSE) {
					fwrite(STDERR, "Format file doesn't exist or error opening format file for reading.\n");
					exit(4);
				}
			}
		}
	}
	
	foreach (range(1, $argc) as $argnum) {
		if (!empty($argv[$argnum])) {
			if (substr($argv[$argnum], 0, 8) == "--input=") {
				$input_file = substr($argv[$argnum], 8, strlen($argv[$argnum]));
				$myinputfile = fopen($input_file, "r");
				if ($myinputfile == FALSE) {
					fwrite(STDERR, "Input file does not exist or error opening input file for reading.\n");
					exit(2);
				}
				foreach (range(1, $argc) as $argnum) {
					if (!empty($argv[$argnum])) {
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
				}
				if ($myoutputfile == "") {
					$myoutputfile = fopen("php://stdout", "w");
					inToOut($myinputfile, $myoutputfile, $myformatfile, FALSE);
					break;
				}	
			}
		}
	}
	if ($myinputfile == "") {
		// echo "Enter your input: ";
		// $inputContent = trim(fgets(STDIN));
		foreach (range(1, $argc) as $argnum) {
			if (!empty($argv[$argnum])) {
				if (substr($argv[$argnum], 0, 9) == "--output=") {
					$output_file = substr($argv[$argnum], 9, strlen($argv[$argnum]));
					$myoutputfile = fopen($output_file, "w");
					if ($myoutputfile == FALSE) {
						fwrite(STDERR, "Error opening output file for writing.\n");
						exit(3);
					}
					echo "Enter your input: ";
					$inputContent = trim(fgets(STDIN));
					inToOut($inputContent, $myoutputfile, $myformatfile, TRUE);
					break;
				}
			}
		}
		if (($myoutputfile == "")) {
			echo "Enter your input: ";
			$inputContent = trim(fgets(STDIN));
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
 			if (!empty($argv[$argnum])) {
 				if (substr($argv[$argnum], 0, 4) == "--br") {
		 			$inputContent = preg_replace("/\n/", "<br />\n", $inputContent);
		 			break;
				}
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
			$overlapTestArray = array();
			$overlap = FALSE;

			$comment = FALSE;

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
	 						if ($tab == FALSE) {
	 							$regexp = $string;
	 							//echo $regexp."\n";
	 						}
	 						$tab = TRUE;
	 						$string = "";
	 						continue;
	 					}
	 					elseif ((($char == ",") || ($char == "\n")) && ($tab == TRUE)) {
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
		 			//echo $regexp."\n";
		 			//exit;
		 			// $pattern = "/".$regexp."/";
		 			//$pattern = $regexp;
		 			// $arrayOfRegex = str_split($regexp);
		 			// array_push($arrayOfRegex, "|[^(<|>)]");
		 			// $regexp = implode($arrayOfRegex);
		 			// echo $regexp."\n";
		 			//exit;

		 			$overlapTestRegex = $regexp;
		 			$overlapTestArray[$regexp] = $arrayOfElem;


		 			$pattern = "/(?!<[^>]*)".$regexp."(?![^<]*>)/";

		 			//$pattern = "/(?!<)".$regexp."(?!>)/";
		 			$arrayOfRules[$pattern] = $arrayOfElem;	
		 			//print_r($arrayOfElem);

				}
				$overlap = is_overlaped($overlapTestArray, $inputContent);
				
				addTag($arrayOfRules, $inputContent, $overlap);
			}
			else {
				$overlap = is_overlaped($overlapTestArray, $inputContent);
				addTag($arrayOfRules, $inputContent, $overlap);
			}
			
	}
		else {
			return;
		}
	}	
	function addTag($arrayOfRules, &$inputContent, $overlap) {
		//print_r($arrayOfRules);
		//exit;
		//global $overlap;
		global $startTagArray;
		global $endTagArray;
		$output_array = array();
		$approvedChars = array();
		$repeat = FALSE;
		#$format_e = FALSE;
		$hexnum = FALSE;
		$count = 0;
		// $overlap = is_overlaped($arrayOfRules, $inputContent);
	
				#hideElem($inputContent);
 				foreach ($arrayOfRules as $rule) {
 					//print_r($rule);
 					$pattern = newPattern($arrayOfRules, $count);
 					$count++;
 					foreach ($rule as $elem) {
		 				//echo $elem."\n";
		 				//echo $inputContent."\n";
		 				 switch($elem) {
		 					case "bold":
		 						$inputContent = preg_replace($pattern, "<b>$0</b>", $inputContent);
		 						if ($overlap) {
		 							$inputContent = saveTag($inputContent, $elem);
		 						}
		 						//echo "input content po save tag v bolde: ".$inputContent."\n";
								// preg_match_all($pattern, $inputContent, $output_array);
			 						
			 				// 		foreach($output_array as $array) {
			 				// 			//print_r($array);
			 				// 			//exit;
			 				// 			removeDuplicate($array);
			 				// 			//print_r($array);
			 							
			 				// 			foreach ($array as $item) {
			 				// 				$inputContent = preg_replace("/(?<!<)".$item."(?!>)/", "<b>".$item."</b>", $inputContent);
			 				// 			}
			 				// 			//echo $inputContent."\n";
			 				// 			//exit;
			 				// 		}
		 						break;
		 					case "italic":
		 					//echo "som v italic\n";
		 						$inputContent = preg_replace($pattern, "<i>$0</i>", $inputContent);
		 						
		 						if ($overlap) {
		 							//echo "som v overlap ".$inputContent."\n";
		 							$inputContent = saveTag($inputContent, $elem);
		 							//echo "input content po save tag v italic: ".$inputContent."\n";
		 						}// preg_match_all($pattern, $inputContent, $output_array);
									// //print_r($output_array);
									// //exit;
			 					// 	foreach($output_array as $array) {
			 					// 		removeDuplicate($array);
			 					// 		//print_r($array);
			 					// 		//najprv aplikovat element na pismeno, ktore ho oznacuje
			 					// 		foreach ($array as $item) {
		 						// 			//echo $item."\n";
		 						// 			$inputContent = preg_replace("/(?<!<)".$item."(?!>)/", "<i>".$item."</i>", $inputContent);
			 					// 		}
			 					// 	}
		 						break;
		 					case "underline":

		 						$inputContent = preg_replace($pattern, "<u>$0</u>", $inputContent);
		 						if ($overlap) {
		 							$inputContent = saveTag($inputContent, $elem);
		 						}
		 						// preg_match_all($pattern, $inputContent, $output_array);
								
			 					// 	foreach($output_array as $array) {
			 					// 		removeDuplicate($array);
			 					// 		//print_r($array);
			 							

			 					// 		foreach ($array as $item) {
		 						// 			$inputContent = preg_replace("/(?<!<)".$item."(?!>)/", "<u>".$item."</u>", $inputContent);
			 					// 		}
			 					// 	}
		 						break;
		 					case "teletype":
		 						
		 						$inputContent = preg_replace($pattern, "<tt>$0</tt>", $inputContent);
		 						
		 						if ($overlap) {
		 							$inputContent = saveTag($inputContent, $elem);
		 						}//preg_match_all($pattern, $inputContent, $output_array);
			 						// foreach($output_array as $array) {
			 						// 	//print_r($array);
			 						// 	removeDuplicate($array);
			 						// 	//print_r($array);
			 						// 	// usort($array, function($a, $b) {
			 						// 	// 	return strlen($b)-strlen($a);
			 						// 	// });
			 						// 	//print_r($array);
			 						// 	foreach ($array as $item) {
			 						// 		echo $item."\n";
		 							// 		//$inputContent = preg_replace("/(?!<)".$item."(?!>)/", "<tt>".$item."</tt>", $inputContent);
		 							// 		//$inputContent = preg_replace($pattern, "<tt>".$item."</tt>", $inputContent);
		 									
			 								
			 						// 		#(?!<[^>]*)Test(?![^<]*>)
			 						// 	}
			 							//echo $inputContent."\n";
			 						//}
		 						break;
		 					default:
		 						//echo $elem."\n";
		 						//echo substr($elem, 0, 5);
				 				if ((substr($elem, 0, 5) == "size:") or (substr($elem, 0, 6) == "color:") or ($elem == "")) {
			 						break;
			 					}
			 					else {
			 						fwrite(STDERR, "Format table error: Nonexistent parameter '$elem'.\n");
		 							exit(4);	 						
								}
						}
						//$approvedChars = [];
		 				if (substr($elem, 0, 5) == "size:") {
		 					$sizeok = FALSE;
		 					$size = substr($elem, 5, strlen($elem));
		 					// if ($size != range(1, 7)) {
		 					// 	fwrite(STDERR, "Format table error: Invalid size '$size'.\n");
		 					// 	exit(4);
		 					// }
		 					if (preg_match("/^[1-7]{1}$/", $size)) {
		 						$sizeok = TRUE;
		 					}
		 				// 	foreach (range(1, 7) as $value) {
		 				// 		//echo $size."\n";
		 				// 		//echo $value."\n";

		 				// 		if ($size == $value) {
		 				// 			$sizeok = TRUE;
		 				// 		}
							// }
							
							if ($sizeok != TRUE) {
		 						fwrite(STDERR, "Format table error: Invalid size '$size'.\n");
		 						exit(4);
		 					}	
		 					$inputContent = preg_replace($pattern, "<font size=".$size.">$0</font>", $inputContent);
		 					if ($overlap) {
		 							$inputContent = saveTag($inputContent, $elem);
		 					}
							// preg_match_all($pattern, $inputContent, $output_array);
								
			 			// 			foreach($output_array as $array) {
			 			// 				removeDuplicate($array);
			 			// 				foreach ($array as $item) {
		 				// 					$inputContent = preg_replace("/(?<!<|\/)".$item."/", "<font size=".$size.">".$item."</font>", $inputContent);
			 			// 				}
			 			// 			}
						}
		 				elseif (substr($elem, 0, 6) == "color:") {
		 					$colorok = FALSE;
		 					$color = substr($elem, 6, strlen($elem));
		 					#echo $color."\n";
		 					#exit;
		 				
		 					if (preg_match("/^[a-fA-F0-9]{6}$/", $color)) {
		 						$colorok = TRUE;
		 					} 

 							if ($colorok != TRUE) {
 								fwrite(STDERR, "Format table error: Invalid color '$color'.\n");
 								exit(4);	 						
		 					}
		 					//echo $color."\n";
		 					//echo $inputContent."\n";
				 			$inputContent = preg_replace($pattern, "<font color=#".$color.">$0</font>", $inputContent);
				 			if ($overlap) {
		 							$inputContent = saveTag($inputContent, $elem);
		 					}
		 					// preg_match_all($pattern, $inputContent, $output_array);
								
			 				// 		foreach($output_array as $array) {
			 				// 			removeDuplicate($array);
			 				// 			foreach ($array as $item) {
		 					// 				$inputContent = preg_replace("/(?<!<)".$item."/", "<font color=#".$color.">".$item."</font>", $inputContent);
			 				// 			}
			 				// 		}
		 				}
		 				//echo $inputContent."\n";
		 				// else {
		 				// 	fwrite(STDERR, "Format table error: Nonexistent parameter '$elem'.\n");
		 				// 	exit(4);
		 				// } 		
		 			}
		 			
					
				}
				//print_r($startTagArray);
		 			if ($overlap) {
		 				$inputContent = addSavedTags($inputContent);
		 			}
				 //print_r($startTagArray);
				// 	print_r($endTagArray);
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
				$char = "";
				$array = str_split($regexp);
				foreach ($array as $key => $value) {
					//echo $value."\n";
					if ($value == ".") {
						unset($array[$key]);
						$regexp = implode($array);
					}
				}
				//echo $regexp."\n";
				
				foreach ($array as $key => $value) {
					if ($value == "*") {
						$array[$key] = "+";
						$regexp = implode($array);
						//echo $regexp."\n";
					}
				}
				
				foreach ($array as $key => $value) {
					if ($value == "!") {
						$regexp = preg_replace("/!/", "[^", $regexp);
						$regexp = preg_replace("/.(?=(\+|$))/", "$0|<|>]", $regexp);
					}
				}

				foreach ($array as $key => $value) {
					//echo $value."\n";
					
					if ($value == "%") {
						if ($char == $value) {
							unset($array[$key]);
							$regexp = implode($array);
							//echo $regexp."\n";
							break;
						}
						//echo $regexp."\n";
					}
					$char = $value;
				}
				
			if (preg_match("/%s/", $regexp)) {
				if (preg_match("/!%s/", $regexp)) {
					$regexp = preg_replace("/!%s/", "[^\s]", $regexp);
				}
				$regexp = preg_replace("/%s/", "\s", $regexp);
			}

			if (preg_match("/%a/", $regexp)) {
				if (preg_match("/!%a/", $regexp)) {
					$regexp = preg_replace("/!%a/", "[^\S]", $regexp);
				}
				$regexp = preg_replace("/%a/", "\S", $regexp);
			}

			if (preg_match("/%d/", $regexp)) {
				if (preg_match("/!%d/", $regexp)) {
					$regexp = preg_replace("/!%d/", "[^0-9]", $regexp);
				}
				$regexp = preg_replace("/%d/", "[0-9]", $regexp);
			}

			if (preg_match("/%l/", $regexp)) {
				if (preg_match("/!%l/", $regexp)) {
					$regexp = preg_replace("/!%l/", "[^a-z]", $regexp);
				}
				$regexp = preg_replace("/%l/", "[a-z]", $regexp);
			}
				
			if (preg_match("/%L/", $regexp)) {
				if (preg_match("/!%L/", $regexp)) {
					$regexp = preg_replace("/!%L/", "[^A-Z]", $regexp);
				}
				$regexp = preg_replace("/%L/", "[A-Z]", $regexp);
			}
				
			if (preg_match("/%w/", $regexp)) {
				if (preg_match("/!%w/", $regexp)) {
					$regexp = preg_replace("/!%w/", "[^a-zA-Z]", $regexp);
				}
				$regexp = preg_replace("/%w/", "[a-zA-Z]", $regexp);
			}
			
			if (preg_match("/%W/", $regexp)) {
				if (preg_match("/!%W/", $regexp)) {
					$regexp = preg_replace("/!%W/", "[^a-zA-Z0-9]", $regexp);
				}
				$regexp = preg_replace("/%W/", "[a-zA-Z0-9]", $regexp);
			}
		
			if (preg_match("/%t/", $regexp)) {
				if (preg_match("/!%t/", $regexp)) {
					$regexp = preg_replace("/!%t/", "[^\t]", $regexp);
				}
				$regexp = preg_replace("/%t/", "\t", $regexp);
			}

			if (preg_match("/%n/", $regexp)) {
				if (preg_match("/!%n/", $regexp)) {
					$regexp = preg_replace("/!%s/", "[^\n]", $regexp);
				}
				$regexp = preg_replace("/%n/", "\n", $regexp);
			}
	}

function removeDuplicate(&$array) {
	$count = count($array);
	for ($i=0; $i < $count; $i++) {
		for ($j=$i+1; $j < $count; $j++){
			if (isset($array[$i]) and isset($array[$j])) {
				if ($array[$i] == $array[$j]) {
					unset($array[$i]);
				}
			}
		}
	}		
}

function saveTag($inputContent, $elem) {
	global $startTagArray;
	global $endTagArray;
	//echo "som v saveTag\n";
	//echo $inputContent."\n";
	$inputArray = str_split($inputContent);
	//print_r($inputArray);
	//global $shiftnum;

	switch ($elem) {
		case 'bold':
			for ($i=0; $i<count($inputArray); ++$i) {
				//echo $inputArray[$i]."\n";
				 if ($inputArray[$i] === "<") {
					if ($inputArray[$i+1] === "/") {

						array_push($endTagArray, $i);
						array_push($endTagArray, $elem[0]);
						unset_all($inputArray, $i);
						
					}
					else {
						array_push($startTagArray, $i);
						array_push($startTagArray, $elem[0]);
						unset_all($inputArray, $i);
						
				 	}
				}
			}
			break;

		case 'italic':
			for ($i=0; $i<count($inputArray); ++$i) {
				//echo $inputArray[$i]."\n";
				 if ($inputArray[$i] === "<") {
					if ($inputArray[$i+1] === "/") {

						array_push($endTagArray, $i);
						array_push($endTagArray, $elem[0]);
						unset_all($inputArray, $i);
						
					}
					else {
						array_push($startTagArray, $i);
						array_push($startTagArray, $elem[0]);
						unset_all($inputArray, $i);
				 		
				 	}
				}
			}
			break;
	}
	// print_r($startTagArray);
	// print_r($endTagArray);
	// print_r($inputArray);
	$inputContent = implode($inputArray);
	//echo $inputContent."\n";
	return $inputContent;
}

function addSavedTags(&$inputContent) {
	global $startTagArray;
	global $endTagArray;
	//print_r($startTagArray);
	
	$shiftnum = 0;
	$inputArray = str_split($inputContent);
	for ($i=0; $i<count($startTagArray); $i=$i+2) {
		$inputArray = addStartTags($inputArray, $shiftnum, $i);
		$inputContent = implode($inputArray);
		$inputArray = str_split($inputContent);
		$shiftnum += 3;
	}
	//echo $inputContent."\n";
	for ($i=0; $i<count($endTagArray); $i=$i+2) {
		$inputArray = addEndTags($inputArray, $shiftnum, $i);
		$inputContent = implode($inputArray);
		$inputArray = str_split($inputContent);
		$shiftnum += 4;
	}
	//echo $inputContent."\n";
	//exit;
	return $inputContent;
}

function shift($index, $num, &$arrayOfChars) {
	for ($j=0; $j<$num; $j++){
		$count = count($arrayOfChars);
		for ($i=$count-1; $i>=$index; $i--) {
			$arrayOfChars[$i+1] = $arrayOfChars[$i];

		}
		$arrayOfChars[$index] = "";			
	}

}

function addStartTags(&$inputArray, $shiftnum, $i) {
	global $startTagArray;
	switch ($startTagArray[$i+1]) {
			case 'b':
				shift($startTagArray[$i]+$shiftnum, 3, $inputArray);
				$inputArray[$startTagArray[$i]+$shiftnum] = "<";
				$inputArray[$startTagArray[$i]+1+$shiftnum] = $startTagArray[$i+1];
				$inputArray[$startTagArray[$i]+2+$shiftnum] = ">";
				break;
			
			case 'i':
			//echo "som v case i\n";
				shift($startTagArray[$i]+$shiftnum, 3, $inputArray);
				$inputArray[$startTagArray[$i]+$shiftnum] = "<";
				$inputArray[$startTagArray[$i]+1+$shiftnum] = $startTagArray[$i+1];
				$inputArray[$startTagArray[$i]+2+$shiftnum] = ">";
				break;
		}
	return $inputArray;
}

function addEndTags(&$inputArray, $shiftnum, $i) {
	global $endTagArray;
	switch ($endTagArray[$i+1]) {
			case 'b':
				shift($endTagArray[$i]+$shiftnum, 4, $inputArray);
				$inputArray[$endTagArray[$i]+$shiftnum] = "<";
				$inputArray[$endTagArray[$i]+1+$shiftnum] = "/";
				$inputArray[$endTagArray[$i]+2+$shiftnum] = $endTagArray[$i+1];
				$inputArray[$endTagArray[$i]+3+$shiftnum] = ">";
				break;
			
			case 'i':
			//echo "som v case i\n";
				shift($endTagArray[$i]+$shiftnum, 4, $inputArray);
				$inputArray[$endTagArray[$i]+$shiftnum] = "<";
				$inputArray[$endTagArray[$i]+1+$shiftnum] = "/";
				$inputArray[$endTagArray[$i]+2+$shiftnum] = $endTagArray[$i+1];
				$inputArray[$endTagArray[$i]+3+$shiftnum] = ">";
				break;
		}
	return $inputArray;
}

function unset_all(&$input, $i) {
	//echo "som v unsete\n";
	//print_r($input);
	foreach ($input as $key => $value) {
		//echo $value."\n";
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

function is_overlaped($array, $inputContent) {
	$regexArray = array();
	//print_r($array);
	foreach ($array as $key => $underarray) {
		array_push($regexArray, $key);
		
		// foreach ($underarray as $underkey => $value) {
		// 	echo $value."\n";
		// }
	}
	//print_r($regexArray);
	for ($i=0; $i<count($regexArray); ++$i) {
		$array1 = explode(" ", $regexArray[$i]);
		if (($i+1) == count($regexArray)) {
			break;
		}
		$array2 = explode(" ", $regexArray[$i+1]);	
		for ($j=0; $j<count($array1); ++$j) {
			//echo $array1[$j]." array1\n";
			for ($k=0; $k<count($array2); ++$k) {
			//	echo $array2[$k]." array2\n";
				if ($array1[$j] == $array2[$k]) {
					return TRUE;
				}
			}
		}
	}
	return FALSE;
}
?>