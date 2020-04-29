
import psycopg2
import datetime
import math 
import os

#función de consulta a la base de dadtos 
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
str_end_date=end_date.strftime("%d/%m/%Y %H:%M:%S")
print(str_end_date)
begin_date = end_date  - datetime.timedelta(seconds=60)
str_begin_date=begin_date.strftime("%d/%m/%Y %H:%M:%S")
print(str_begin_date)


#horarios para considerar en el conteo de sacos

only_str_end_date=end_date.strftime("%d/%m/%Y 23:00:00")
print(only_str_end_date)

only_start_str_date=end_date.strftime("%d/%m/%Y 06:00:00")
print(only_start_str_date)

#consultas a la base de datos
sql_str_10="SELECT SUM(long_v) FROM ts_kv WHERE ts >= " + date_to_milis(str_begin_date)+" AND ts <= " + date_to_milis(str_end_date) + " AND key='Saco10K' AND ts >="+ date_to_milis(str_begin_date)+" AND ts <= " + date_to_milis(str_end_date)
sql_str_25="SELECT SUM(long_v) FROM ts_kv WHERE ts >= " + date_to_milis(str_begin_date)+" AND ts <= " + date_to_milis(str_end_date) + " AND key='Saco25K' AND ts >="+ date_to_milis(str_begin_date)+" AND ts <= " + date_to_milis(str_end_date)


print(sql_str_10)
result_10=str(getDB(sql_str_10))

print(sql_str_25)
result_25=str(getDB(sql_str_25))

print(result_10)
print(result_25)

#envio datos a THB
if result_10 != "None":
    os.system('curl -v -X POST -d "{\"Saco10KxMin\": '+result_10+'}" iot.igromi.com:8080/api/v1/0nMihSqafQ5IT3Rqoysa/telemetry --header "Content-Type:application/json"')
else:
    os.system('curl -v -X POST -d "{\"Saco10KxMin\": 0}" iot.igromi.com:8080/api/v1/0nMihSqafQ5IT3Rqoysa/telemetry --header "Content-Type:application/json"')

if result_25!= "None":
    os.system('curl -v -X POST -d "{\"Saco25KxMin\": '+result_25+'}" iot.igromi.com:8080/api/v1/0nMihSqafQ5IT3Rqoysa/telemetry --header "Content-Type:application/json"')
else:
    os.system('curl -v -X POST -d "{\"Saco25KxMin\": 0}" iot.igromi.com:8080/api/v1/0nMihSqafQ5IT3Rqoysa/telemetry --header "Content-Type:application/json"')


