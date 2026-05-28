from flask import Blueprint
from flask import render_template, request

import sys
sys.path.append("src")

from model import logicaLiquidacion
from model import errores
from model import empleados

from controller import empleado_controller


# Crear un instancia de Flask que sera nuestra aplicacion
blueprint = Blueprint("vista_usuarios", __name__, "templates")

#Por cada ruta que vayamos a atender en el navegador, creamos una funcion en Python

@blueprint.route("/") #El decordador indica la ruta que llama a esta funcion
def ingresar_datos():
    return render_template("calculadora_ht.html")


@blueprint.route("/crear_tabla")
def crear_tabla():
    empleado_controller.controlador.crear_tabla()
    return 'Tabla creada exitosamente. <br><a href="/">Volver a la página principal</a>'


@blueprint.route("/buscar_ht")
def buscar_fecha():
    fecha_ingreso = request.args.get("fecha_ingreso")
    fecha_retiro = request.args.get("fecha_retiro")
    try:
        resultado = empleado_controller.controlador.buscar_por_fechas(fecha_ingreso, fecha_retiro)

        if resultado is None:
            return render_template("no_encontrado.html")
        else:
            return render_template("resultado_busqueda.html", resultado=resultado)

    except errores.ErrorFechaFormatoIncorrecto:
        return render_template("error_fecha.html")
    
    except errores.ErrorFechaIncorrecta:
        return render_template("error_fecha.html")
    

@blueprint.route("/buscar_ht")
def buscar_salario():
    fecha_ingreso = request.args.get("fecha_ingreso")
    fecha_retiro = request.args.get("fecha_retiro")
    try:
        resultado = empleado_controller.controlador.buscar_por_fechas(fecha_ingreso, fecha_retiro)

        if resultado is None:
            return render_template("no_encontrado.html")
        else:
            return render_template("resultado_busqueda.html", resultado=resultado)

    except errores.ErrorFechaFormatoIncorrecto:
        return render_template("error_fecha.html")
    
    except errores.ErrorFechaIncorrecta:
        return render_template("error_fecha.html")
    

@blueprint.route("/calcular_ht")
def calcular():
    cedula = request.args.get("cedula")
    fecha_ingreso = request.args.get("fecha_ingreso")
    fecha_retiro = request.args.get("fecha_retiro")
    salario = int(request.args.get("salario_mensual"))
    try:
        
        dias_trabajados = logicaLiquidacion.calcular_tiempo_trabajado_dias(fecha_ingreso, fecha_retiro)
        cesantias = logicaLiquidacion.calcular_cesantias(salario, dias_trabajados)
        intereses_cesantias = logicaLiquidacion.calcular_interes_cesantias(float(cesantias), dias_trabajados)
        vacaciones = logicaLiquidacion.calcular_vacaciones(salario, dias_trabajados)
        prima_servicios = logicaLiquidacion.calcular_prima_servicios(salario, dias_trabajados)
        pago_neto = logicaLiquidacion.calcular_pago_neto(float(cesantias), float(intereses_cesantias), float(vacaciones), float(prima_servicios))

        empleado_prueba = empleado_controller.empleados(
            cedula = cedula,
            fecha_ingreso = fecha_ingreso,
            fecha_salida = fecha_retiro,
            salario = salario,
            cesantias = f"{cesantias:.2f}",
            interes_cesantias = f"{intereses_cesantias:.2f}",
            prima_servicios = f"{prima_servicios:.2f}",
            vacaciones = f"{vacaciones:.2f}",
            pago_neto = f"{pago_neto:.2f}"   
        )

        empleado_controller.controlador.insertar(empleado_prueba)
    
        return render_template("calcular_ht.html", cedula= cedula, dias_trabajados=dias_trabajados, cesantias=round(cesantias, 2), intereses_cesantias=round(intereses_cesantias, 2), vacaciones=round(vacaciones, 2), prima_servicios=round(prima_servicios, 2), pago_neto=round(pago_neto, 2))
    
    except errores.ErrorFechaIncorrecta:
        return render_template("error_fecha.html")
    
    except errores.ErrorFechaFormatoIncorrecto:
        return render_template("error_fecha.html")

   



