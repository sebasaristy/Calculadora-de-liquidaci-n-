from flask import Flask
from flask import render_template, request
import sys
sys.path.append("src")

from model import logicaLiquidacion
from model import errores
# Crear un instancia de Flask que sera nuestra aplicacion
app = Flask(__name__)

#Por cada ruta que vayamos a atender en el navegador, creamos una funcion en Python

@app.route("/") #El decordador indica la ruta que llama a esta funcion
def ingresar_datos():
    return render_template("calculadora_ht.html")

@app.route("/calcular_ht")
def calcular():
    fecha_ingreso = request.args.get("fecha_ingreso")
    fecha_retiro = request.args.get("fecha_retiro")
    salario = int(request.args.get("salario_mensual"))
    try:
        
        dias_trabajados = logicaLiquidacion.calcular_tiempo_trabajado_dias(fecha_ingreso, fecha_retiro)
        cesantias = logicaLiquidacion.calcular_cesantias(salario, dias_trabajados)
        intereses_cesantias = logicaLiquidacion.calcular_interes_cesantias(cesantias, dias_trabajados)
        vacaciones = logicaLiquidacion.calcular_vacaciones(salario, dias_trabajados)
        prima_servicios = logicaLiquidacion.calcular_prima_servicios(salario, dias_trabajados)
        pago_neto = logicaLiquidacion.calcular_pago_neto(cesantias, intereses_cesantias, vacaciones, prima_servicios)
        
        return render_template("calcular_ht.html", dias_trabajados=dias_trabajados, cesantias=cesantias, intereses_cesantias=intereses_cesantias, vacaciones=vacaciones, prima_servicios=prima_servicios, pago_neto=pago_neto)
    
    except errores.ErrorFechaIncorrecta:
        return render_template("error_fecha.html")

app.run(debug=True)