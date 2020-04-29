from flask import Flask,request
from flask import render_template
import os
app = Flask(__name__)


@app.route('/save-config',methods=['POST', 'GET'])
def savepost():
    if request.method=='POST':
       cantidad=request.form['cantidad']
       costo=request.form['costo']
       os.system('curl -v -X POST -d "{\"Cantidad_personas_linea\": '+cantidad+'}" iot.igromi.com:8080/api/v1/0nMihSqafQ5IT3Rqoysa/telemetry --header "Content-Type:application/json"')
       os.system('curl -v -X POST -d "{\"Costo_medio_jornada": '+costo+'}" iot.igromi.com:8080/api/v1/0nMihSqafQ5IT3Rqoysa/telemetry --header "Content-Type:application/json"')

       return render_template('Servidor_configuracion.html', cantidad=cantidad,costo=costo)
    else:
        return "<h2>Error</h2>"

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000) 
