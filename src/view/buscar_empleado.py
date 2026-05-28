import sys
sys.path.append("src")

from controller import empleado_controller
from model import errores

try:
    cedula_buscar = input("Cedula a buscar: ")

    resultado = empleado_controller.controlador.buscar_por_cedula(cedula_buscar)

    if resultado is None:
        print("No se encontró ningún empleado con esa cedula.")
    else:
        print(f"""
    Empleado encontrado:
    - Cedula:              {resultado.cedula}
    - Fecha ingreso:       {resultado.fecha_ingreso}
    - Fecha salida:        {resultado.fecha_salida}
    - Salario:             {resultado.salario}
    - Cesantías:           {resultado.cesantias}
    - Interés cesantías:   {resultado.interes_cesantias}
    - Vacaciones:          {resultado.vacaciones}
    - Prima servicios:     {resultado.prima_servicios}
    - Pago neto:           {resultado.pago_neto}
        """)



except Exception as e:
    print(f"Error inesperado: {e}")