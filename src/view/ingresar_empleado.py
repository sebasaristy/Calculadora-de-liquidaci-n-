import sys
sys.path.append("src")

from controller import empleado_controller
from model import logicaLiquidacion
from model.empleados import empleados
import datetime

try: 
    empleado = empleados(cedula = "", fecha_ingreso="",fecha_salida="",salario=0,cesantias=0,interes_cesantias=0,prima_servicios=0, vacaciones = 0, pago_neto = 0)

    empleado.cedula = input("Cedula: ")
    empleado.fecha_ingreso = input("Fecha ingreso (DD/MM/AAAA): ")
    empleado.fecha_salida = input("Fecha salida (DD/MM/AAAA): ")
    empleado.salario = int(input("SMMLV: "))

    dias = logicaLiquidacion.calcular_tiempo_trabajado_dias(empleado.fecha_ingreso, empleado.fecha_salida)

    empleado.cesantias = logicaLiquidacion.calcular_cesantias(empleado.salario, dias)
    empleado.interes_cesantias = logicaLiquidacion.calcular_interes_cesantias(empleado.cesantias, dias)
    empleado.vacaciones = logicaLiquidacion.calcular_vacaciones(empleado.salario, dias)
    empleado.prima_servicios = logicaLiquidacion.calcular_prima_servicios(empleado.salario, dias)
    empleado.pago_neto = logicaLiquidacion.calcular_pago_neto(empleado.cesantias, empleado.interes_cesantias, empleado.vacaciones, empleado.prima_servicios)

    empleado_controller.controlador.insertar(empleado)

    print(f"Empleado registrado exitosamente")

except Exception as e:
    print(f"Ocurrio un error al registrar el empleado")
    print (str(e))