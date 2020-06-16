<?php
$clave= $_POST['PASS'];
$user= $_POST['USER'];


if (($clave == 'vita12358') && ($clave <> '') && ($clave <> null) )
 {
	 
	session_start();
    $_SESSION['YYY'] = "OK";
	$location="Location:home.php";
	header($location);
	
 } 
 
 else
 
 {
 echo 'CLAVE INCORRECTA';
 }
 
  ?>
   
   