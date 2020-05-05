
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import xlsxwriter
import time
import psycopg2
import datetime
import math 
import os
import smtplib 
import logging



#convert date to timestamp
def date_to_milis(date_string):

    obj_date = datetime.datetime.strptime(date_string,"%d/%m/%Y %H:%M:%S")
    
    return str(math.trunc(obj_date.timestamp() * 1000))

#metodod e consulta a BD 
def getDB(sql_query):

    try:
        
        connection = psycopg2.connect(user = "postgres",
                                        password = "imagina12",
                                        host = "127.0.0.1",
                                        port = "5432",
                                        database = "thingsboard")

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

def escribir_log(cadena):

    logging.basicConfig(filename='vitakai.log',level=logging.DEBUG)

    end_date = datetime.datetime.now()
    str_date=end_date.strftime("%d/%m/%Y %H:%M:%S")
    logging.info(str_date+": "+cadena)
    print(str_date+": "+cadena)

    return 0

end_date = datetime.datetime.now()
begin_date = end_date  - datetime.timedelta(days=1)
str_start_date=begin_date.strftime("%d/%m/%Y 6:00:00")
str_end_date=begin_date.strftime("%d/%m/%Y 22:00:00")


str_t8=begin_date.strftime("%d/%m/%Y 8:00:00")
str_t13=begin_date.strftime("%d/%m/%Y 13:00:00")
str_t14=begin_date.strftime("%d/%m/%Y 14:00:00")
str_t18=begin_date.strftime("%d/%m/%Y 18:00:00")


print("Inicio sumatoria de kilos procesados: "+str_start_date)
print("Final sumatoria de kilos procesados: "+str_end_date)

#consultas a la base de datos
sql_str_10="SELECT SUM(long_v) FROM ts_kv WHERE ts >= " + date_to_milis(str_start_date)+" AND ts <= " + date_to_milis(str_end_date) + " AND key='Saco10K'"
sql_str_25="SELECT SUM(long_v) FROM ts_kv WHERE ts >= " + date_to_milis(str_start_date)+" AND ts <= " + date_to_milis(str_end_date) + " AND key='Saco25K'"
sql_str_dentenciones="SELECT SUM(long_v) FROM ts_kv WHERE ts >= " + date_to_milis(str_start_date)+" AND ts <= " + date_to_milis(str_end_date) + " AND key='Detencion_20_minutos'"
#sql_str_10_avg="SELECT AVG(long_v) FROM ts_kv WHERE ts >= " + date_to_milis(str_start_date)+" AND ts <= " + date_to_milis(str_end_date) + " AND key='Saco10KxMin' AND ((ts >= " + date_to_milis(str_t8) + " AND ts <= " + date_to_milis(str_t13) + ") OR ( ts >= " + date_to_milis(str_t14) + " AND ts <= " + date_to_milis(str_t18)+"))" 
#sql_str_25_avg="SELECT AVG(long_v) FROM ts_kv WHERE ts >= " + date_to_milis(str_start_date)+" AND ts <= " + date_to_milis(str_end_date) + " AND key='Saco25KxMin' AND ((ts >= " + date_to_milis(str_t8) + " AND ts <= " + date_to_milis(str_t13) + ") OR ( ts >= " + date_to_milis(str_t14) + " AND ts <= " + date_to_milis(str_t18)+"))" 
sql_cantidad_personas="SELECT long_v FROM ts_kv WHERE  key='Cantidad_personas_linea' ORDER BY ts ASC"
sql_costo_medio_jornada="SELECT long_v FROM ts_kv WHERE   key='Costo_medio_jornada' ORDER BY ts ASC"

print(sql_str_dentenciones)

sum_sacos10K=getDB(sql_str_10)
sum_sacos25K=getDB(sql_str_25)
sum_detenciones=getDB(sql_str_dentenciones)
cantidad_personas=getDB(sql_cantidad_personas)
costo_medio_jornada=getDB(sql_costo_medio_jornada)



if sum_sacos10K == None:
   sum_sacos10K="0"
if sum_sacos25K == None:
   sum_sacos25K="0"
if sum_detenciones== None:
   sum_detenciones="0"
   
if  (int(sum_sacos10K*10)== 0) and (int(sum_sacos25K*25)==0):
    
    result_total_pesos=0
      
else:
    result_total_pesos=str((cantidad_personas*costo_medio_jornada)/(int(sum_sacos10K*10)+int(sum_sacos25K*25)))

avg_sacos10K=int(sum_sacos10K)/540
avg_sacos25K=int(sum_sacos25K)/540


print("Kilos en sacos de 10K: "+str(sum_sacos10K*10))
print("Kilos en sacos de 25K: "+str(sum_sacos25K*25))
print("Cantidad de personas en la linea: "+str(cantidad_personas))
print("Costo medio jornada: "+str(costo_medio_jornada))
print("Costo del kilo procesado: "+str(result_total_pesos))
print("Promedio rendimiento 10K: "+str(avg_sacos10K))
print("Promedio rendimiento 25K: "+str(avg_sacos25K))
print("Denciones en minutos: "+str(sum_detenciones))


#fechas para crear el informe del dia anterior

end_date = datetime.datetime.now()
str_end_date=end_date.strftime("%d-%m-%Y")
begin_date = end_date  - datetime.timedelta(days=1)
str_begin_date=begin_date.strftime("%d-%m-%Y")
print("Fecha de data del informe: "+str_begin_date)


#Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('/home/Informe_producion-costos_VITAKAI_IoT_'+str_begin_date+'.xlsx')
worksheet = workbook.add_worksheet()


bold = workbook.add_format({'bold': True})
cell_format = workbook.add_format({'bold': True, 'font_color': 'red'})
cell_format2 = workbook.add_format({'bold': True, 'font_color': 'red'})
cell_format.set_font_size(14)
cell_format3 = workbook.add_format({'bold': True, 'font_color': 'green'})
cell_format3.set_font_size(14)


currency_format = workbook.add_format({'num_format': '$#'})

# Write a total using a formula.
worksheet.write(1, 1,'INFORME DE PRODUCIÓN DEL DÍA '+ str_begin_date, cell_format3)
worksheet.write(5, 1,'Kilos en sacos de 10K:',bold)
worksheet.write(5, 7, int(sum_sacos10K*10))
worksheet.write(7, 1,'Promedio de rendimiento Sacos de 10K x Minuto:',bold)
worksheet.write(7, 7, round(avg_sacos10K,2))
worksheet.write(9, 1,'Kilos en sacos de 25K:',bold)
worksheet.write(9, 7, int(sum_sacos25K*25))
worksheet.write(11, 1,'Promedio de rendimiento Sacos de 25K x Minuto:',bold)
worksheet.write(11, 7, round(avg_sacos25K,2))
worksheet.write(13, 1,'Costo x kilo procesado:',bold)
worksheet.write(13, 7, float(result_total_pesos),currency_format)
worksheet.write(15, 1,'*Cantidad de personas en la linea:',bold)
worksheet.write(15, 7, int(cantidad_personas))
worksheet.write(17, 1,'*Costo medio de la jornada:',bold)
worksheet.write(17, 7,float(costo_medio_jornada),currency_format)
worksheet.write(19, 1,'Detenciones en minutos:',bold)
worksheet.write(19, 7,int(sum_detenciones))
worksheet.write(23, 1,'*Se considera los datos ingresados en la web de configuración en el cálculo',cell_format2)

workbook.close()


fromaddr = "notificaciones@igromi.com"
# instance of MIMEMultipart 
msg = MIMEMultipart() 

# storing the senders email address 
msg['From'] = fromaddr 

# storing the receivers email address 


# storing the subject 
msg['Subject'] = "Informe IoT de producción y costos "+str_begin_date+"."

# string to store the body of the mail 
body = "Se adjunta informe IoT de producción y costos "+str_begin_date+"."

# attach the body with the msg instance 
msg.attach(MIMEText(body, 'plain')) 

# open the file to be sent 
filename = 'Informe_producion-costos_VITAKAI_IoT_'+str_begin_date+'.xlsx'
attachment = open('/home/Informe_producion-costos_VITAKAI_IoT_'+str_begin_date+'.xlsx', "rb") 

# instance of MIMEBase and named as p 
p = MIMEBase('application', 'octet-stream') 

# To change the payload into encoded form 
p.set_payload((attachment).read()) 

# encode into base64 
encoders.encode_base64(p) 

p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 

# attach the instance 'p' to instance 'msg' 
msg.attach(p) 

# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 

# start TLS for security 
s.starttls() 

# Authentication 
s.login(fromaddr, "imagina12") 

# Converts the Multipart msg into a string 
text = msg.as_string() 

# sending the mail 
msg['To'] = "aguileraelectro@gmail.com",
s.sendmail(fromaddr,"aguileraelectro@gmail.com", text)
escribir_log("email sent to aguileraelectro@gmail.com")

time.sleep(10)

msg['To'] = "victor.ruz@igromi.com"
s.sendmail(fromaddr, "victor.ruz@igromi.com", text) 

time.sleep(10)

msg['To'] = "carlos.castillo@igromi.com"
s.sendmail(fromaddr, "carlos.castillo@igromi.com", text) 

time.sleep(10)

msg['To'] = "armorales@vitakai.com"
s.sendmail(fromaddr, "armorales@vitakai.com", text) 

time.sleep(10)

msg['To'] = "cgonzalez@vitakai.com"
s.sendmail(fromaddr, "cgonzalez@vitakai.com", text) 

time.sleep(10)

msg['To'] = "spinto@vitakai.com"
s.sendmail(fromaddr, "spinto@vitakai.com", text) 

# terminating the session 
s.quit() 

