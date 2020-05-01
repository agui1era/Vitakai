
import psycopg2
import datetime
import math 
import os

#funcin de consulta a la base de dadtos 
def getDB(sql_query):
    try:
        
        connection = psycopg2.connect(user = "postgres",
                                        password = "imagina12",
                                        host = "127.0.0.1",
                                        port = "5432",
                                        database = "thingsboard")

        print("Using Python variable in PostgreSQL select Query")
        cursor = connection.cursor()
        postgreSQL_select_Query = sql_query

        cursor.execute(postgreSQL_select_Query)
        bd_records = cursor.fetchall()
        for row in bd_records:
            print( "Query ok")

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)

    finally:
        # closing database connection
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed \n")
    try:
       
       out_query=row[0]

    except (Exception, psycopg2.Error) as error:
       out_query="QUERY ERROR"

    return out_query

#funcion de conversion de formato date to milis
def date_to_milis(date_string):

    #convert date to timestamp
    obj_date = datetime.datetime.strptime(date_string,"%d/%m/%Y %H:%M:%S")

    
    return str(math.trunc(obj_date.timestamp() * 1000))

#rendimientos de sacos x min
end_date = datetime.datetime.now()
str_end_date=end_date.strftime("%d/%m/%Y 22:00:00")
print(str_end_date)


only_start_str_date=end_date.strftime("%d/%m/%Y 06:00:00")
print(only_start_str_date)

#consultas a la base de datos
sql_str_10="SELECT SUM(long_v) FROM ts_kv WHERE ts >= " + date_to_milis(only_start_str_date)+" AND ts <= " + date_to_milis(str_end_date) + " AND key='Saco10K'"
sql_str_25="SELECT SUM(long_v) FROM ts_kv WHERE ts >= " + date_to_milis(only_start_str_date)+" AND ts <= " + date_to_milis(str_end_date) + " AND key='Saco25K'"
sql_cantidad_personas="SELECT long_v FROM ts_kv WHERE  key='Cantidad_personas_linea' ORDER BY ts ASC"
sql_costo_medio_jornada="SELECT long_v FROM ts_kv WHERE   key='Costo_medio_jornada' ORDER BY ts ASC"

sum_sacos10K=getDB(sql_str_10)
sum_sacos25K=getDB(sql_str_25)
cantidad_personas=getDB(sql_cantidad_personas)
costo_medio_jornada=getDB(sql_costo_medio_jornada)


if sum_sacos10K == None:
   sum_sacos10K="0"
if sum_sacos25K == None:
   sum_sacos25K="0"
   
if  (int(sum_sacos10K*10)== 0) and (int(sum_sacos25K*25)==0):
    
    result_total_pesos=0
      
else:
    result_total_pesos=str((cantidad_personas*costo_medio_jornada)/(int(sum_sacos10K*10)+int(sum_sacos25K*25)))

print("Kilos en sacos de 10K: "+str(sum_sacos10K*10))
print("Kilos en sacos de 25K: "+str(sum_sacos25K*25))
print("Cantidad de personas en la linea: "+str(cantidad_personas))
print("Costo medio jornada: "+str(costo_medio_jornada))
print("Costo del kilo procesado: "+str(result_total_pesos))

#envio datos a THB
os.system('curl -v -X POST -d "{\"Kilos_totales_sacos_10K": '+str(sum_sacos10K*10)+'}" iot.igromi.com:8080/api/v1/0nMihSqafQ5IT3Rqoysa/telemetry --header "Content-Type:application/json"')
os.system('curl -v -X POST -d "{\"Kilos_totales_sacos_25K": '+str(sum_sacos25K*25)+'}" iot.igromi.com:8080/api/v1/0nMihSqafQ5IT3Rqoysa/telemetry --header "Content-Type:application/json"')
os.system('curl -v -X POST -d "{\"Cost_kilo_total": '+str(result_total_pesos)+'}" iot.igromi.com:8080/api/v1/0nMihSqafQ5IT3Rqoysa/telemetry --header "Content-Type:application/json"')
