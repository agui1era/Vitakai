<?php

include("verificar_sesion.php");

?> 

<html>
<meta charset="UTF-8">
	  <head>
	 	<script src="script.js">		
	    </script>
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">

		<!-- Optional theme -->
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">
		
		<b><title> CONFIGURACIÓN COSTOS</title></b>
		<br>
		
	  </head>
	      <body>
		  <div class="container ">
            <span class="text-success"><h2>Configuración Costos</h2></span><br>
						
						<form name="mant" method="post" action="http://iot.igromi.com:5000/save-config">
								
                        <pre><dt><h4>Cantidad de pesonas en la línea</h4></dt></pre><br>
						<input name="cantidad" size="50" placeholder="ej: 8"   type="number" /><br><br>
						<pre><dt><h4>Costo promedio jornada:</h4></dt></pre></dt> <br>
                        <input name="costo"  size="50" placeholder="ej: 15000"  type="number" /><br><br>
                        <pre><b><h4> Extensión de 2 horas extras</h4></b></pre><br>
						
						<div class="checkbox">
						<label><input type="checkbox" value="">Lunes</label>
						</div>
						<div class="checkbox">
						<label><input type="checkbox" value="">Martes</label>
						</div>
						<div class="checkbox">
						<label><input type="checkbox" value="">Miércoles</label>
						</div>
						<div class="checkbox">
						<label><input type="checkbox" value="">Jueves</label>
						</div>
						<div class="checkbox">
						<label><input type="checkbox" value="">Viernes</label>
						</div><br>
						
						
									
						<input type="button" class="btn btn btn-success btn-lg" value="GUARDAR" onClick="guardar()" >&nbsp;&nbsp;&nbsp;
						<input type="button" class="btn btn btn-success btn-lg" value="Ir a Home" onClick="home()" >
						</form>
												
		
		</body>
		</div>
	</html>