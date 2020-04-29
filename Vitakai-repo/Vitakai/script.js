function home()
          {
		
				      document.location.href="home.php";
					
          }
function config()
          {
		
				      document.location.href="config.php";
					
          }
function costos()
          {
		
				      document.location.href="costos.php";
					
          }
function guardar()
          {
                     
            if ((document.mant.cantidad.value != '') && (document.mant.costo.value != '')) 
            {

           
                     if (confirm('Desea guardar?'))
                       {
                       document.mant.submit();
                       }
            }
            else
            {

                window.alert("Favor ingresar costo medio jornada y cantidad de personas");
            }
                    				   					
          }
