import psycopg2
import datetime
import math 
import os

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
       out_query="ERROR"

    return out_query

def date_to_milis(date_string):

    #convert date to timestamp
    obj_date = datetime.datetime.strptime(date_string,"%d/%m/%Y %H:%M:%S")

    
    return str(math.trunc(obj_date.timestamp() * 1000))


#veo si ha pasado un saco en 20 min

end_date = datetime.datetime.now()
str_end_date=end_date.strftime("%d/%m/%Y %H:%M:%S")
print(str_end_date)
begin_date = end_date  - datetime.timedelta(seconds=1200)
str_begin_date=begin_date.strftime("%d/%m/%Y %H:%M:%S")
print(str_begin_date)


#horario laboral


str_t8=end_date.strftime("%d/%m/%Y 8:00:00")

str_t13=end_date.strftime("%d/%m/%Y 13:00:00")

str_t14=end_date.strftime("%d/%m/%Y 14:00:00")

str_t18=end_date.strftime("%d/%m/%Y 18:00:00")

str_t5=end_date.strftime("%d/%m/%Y 20:00:00")



sql_str_det="SELECT key FROM ts_kv WHERE ts >= " + date_to_milis(str_begin_date)+" AND ts <= " + date_to_milis(str_end_date) + " AND (key = 'Detencion_20_minutos' OR key = 'Saco10K' OR key = 'Saco20K') AND ((ts >= " + date_to_milis(str_t8) + " AND ts <= " + date_to_milis(str_t13) + ") OR ( ts >= " + date_to_milis(str_t14) + " AND ts <= " + date_to_milis(str_t18)+"))" 


print(sql_str_det)
result_det=str(getDB(sql_str_det))
print(result_det)

#registro una detención si no hay registros de nuevos sacos u otras detenciones

#if result_det == "ERROR" and (((date_to_milis(str_t1) >= date_to_milis(str_end_date)) and (date_to_milis(str_t2) <= date_to_milis(str_end_date)) ) or ((date_to_milis(str_t3) >= date_to_milis(str_end_date)) and (date_to_milis(str_t4) <= date_to_milis(str_end_date)))) :

if result_det == "ERROR":
    os.system('curl -v -X POST -d "{\"Detencion_20_minutos\": 20}" http://localhost:8080/api/v1/0nMihSqafQ5IT3Rqoysa/telemetry --header "Content-Type:application/json"')

