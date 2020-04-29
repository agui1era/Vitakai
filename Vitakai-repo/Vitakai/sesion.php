<?php
$clave= $_POST['PASS'];
$user= $_POST['USER'];

$conexion = mysql_connect( "localhost", "root", "U7L1xSOU9rqMVQNt" ) or die ("No se ha podido conectar al servidor de Base de datos");

$query = "SELECT * FROM zadmin_vitakai.usuarios WHERE user='".$user."' ;";     // Esta linea hace la consulta 

//echo $query;

$result = mysql_query($query);

while ($row=mysql_fetch_array($result))
{ 
$clave_bd =$row['pass'];
};

//echo $clave_bd ;

if (($clave == $clave_bd) && ($clave <> '') && ($clave <> null) )
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
   
   