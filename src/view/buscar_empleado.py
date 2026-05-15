import sys
sys.path.append("src")

from controller import empleado_controller
from model import errores

try:
    fecha_ingreso = input("Fecha ingreso a buscar (DD/MM/AAAA): ")
    fecha_salida = input("Fecha salida a buscar (DD/MM/AAAA): ")

    resultado = empleado_controller.controlador.buscar_por_fechas(fecha_ingreso, fecha_salida)

    if resultado is None:
        print("No se encontró ningún empleado con esas fechas.")
    else:
        print(f"""
    Empleado encontrado:
    - Fecha ingreso:       {resultado.fecha_ingreso}
    - Fecha salida:        {resultado.fecha_salida}
    - Salario:             {resultado.salario}
    - Cesantías:           {resultado.cesantias}
    - Interés cesantías:   {resultado.interes_cesantias}
    - Vacaciones:          {resultado.vacaciones}
    - Prima servicios:     {resultado.prima_servicios}
    - Pago neto:           {resultado.pago_neto}
        """)

except errores.ErrorFechaFormatoIncorrecto:
    print("Error: Una de las fechas ingresadas tiene un formato incorrecto. Use DD/MM/AAAA.")

except errores.ErrorFechaIncorrecta:
    print("Error: La fecha de salida no puede ser anterior a la fecha de ingreso.")

except Exception as e:
    print(f"Error inesperado: {e}")