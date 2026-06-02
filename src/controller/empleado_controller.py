import psycopg2

import sys
sys.path.append("src")

import os
# Sube dos niveles: controller -> src -> raíz del proyecto
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from model import logicaLiquidacion
import secret_config
from model.empleados import empleados
import secret_config 


class controlador:

    def crear_tabla():
        cursor = controlador.obtener_cursor()

        with open("sql/crear_empleados.sql","r") as archivo:
            sql = archivo.read()

        cursor.execute(sql)
        cursor.connection.commit()

    def borrar_tabla():
        cursor = controlador.obtener_cursor()
        
        with open("sql/borrar_empleados.sql","r") as archivo:
            sql = archivo.read()
        
        cursor.execute(sql)
        cursor.connection.commit()

    def obtener_cursor():
        coneccion = psycopg2.connect(database=secret_config.PGDATABASE , user=secret_config.PGUSER , password=secret_config.PGPASSWORD , host=secret_config.PGHOST , port=secret_config.PGPORT )

        cursor = coneccion.cursor()

        return cursor

    
    def insertar(empleado: empleados):
        cursor = controlador.obtener_cursor()

        fecha_ingreso_bd = logicaLiquidacion.convertir_fecha(empleado.fecha_ingreso).strftime("%Y-%m-%d")
        fecha_salida_bd = logicaLiquidacion.convertir_fecha(empleado.fecha_salida).strftime("%Y-%m-%d")
        
        logicaLiquidacion.validar_rango_fechas(logicaLiquidacion.convertir_fecha(empleado.fecha_ingreso), logicaLiquidacion.convertir_fecha(empleado.fecha_salida))
        
        sql = f""" INSERT INTO empleados (cedula, fecha_ingreso, fecha_salida, salario, cesantias, interes_cesantias, vacaciones, prima_servicios, pago_neto) 
                VALUES ('{empleado.cedula}', '{fecha_ingreso_bd}', '{fecha_salida_bd}', {empleado.salario}, {empleado.cesantias}, {empleado.interes_cesantias}, {empleado.vacaciones}, {empleado.prima_servicios}, {empleado.pago_neto}) """
        
        cursor.execute(sql)
        cursor.connection.commit()

    def buscar_salario(salario: int) -> empleados:
        cursor = controlador.obtener_cursor()

        consulta = f""" SELECT cedula,fecha_ingreso, fecha_salida, salario, cesantias, interes_cesantias, vacaciones, prima_servicios, pago_neto
            FROM public.empleados WHERE salario = {salario}; """
        
        cursor.execute(consulta)

        fila = cursor.fetchone()
        saldo = empleados(cedula=fila[0], fecha_ingreso=fila[1].strftime("%d/%m/%Y"), fecha_salida=fila[2].strftime("%d/%m/%Y"), salario=fila[3], cesantias=fila[4], interes_cesantias=fila[5], vacaciones=fila[6], prima_servicios=fila[7], pago_neto=fila[8])

        return saldo
    
    def buscar_por_fechas(fecha_ingreso: str, fecha_salida: str) -> empleados:
        cursor = controlador.obtener_cursor()

        # Convierte DD/MM/AAAA → AAAA-MM-DD para PostgreSQL
        fecha_ingreso_bd = logicaLiquidacion.convertir_fecha(fecha_ingreso).strftime("%Y-%m-%d")
        fecha_salida_bd = logicaLiquidacion.convertir_fecha(fecha_salida).strftime("%Y-%m-%d")

        consulta = f"""SELECT cedula, fecha_ingreso, fecha_salida, salario, cesantias, interes_cesantias, vacaciones, prima_servicios, pago_neto
                    FROM public.empleados 
                    WHERE fecha_ingreso = '{fecha_ingreso_bd}' AND fecha_salida = '{fecha_salida_bd}';"""

        cursor.execute(consulta)
        fila = cursor.fetchone()

        saldo = empleados(cedula=fila[0], fecha_ingreso=fila[1].strftime("%d/%m/%Y"), fecha_salida=fila[2].strftime("%d/%m/%Y"), salario=fila[3], cesantias=fila[4], interes_cesantias=fila[5], vacaciones=fila[6], prima_servicios=fila[7], pago_neto=fila[8])

        return saldo
    
    def buscar_por_cedula(cedula: str) -> empleados:
        cursor = controlador.obtener_cursor()

        consulta = f"""SELECT cedula, fecha_ingreso, fecha_salida, salario, cesantias, interes_cesantias, vacaciones, prima_servicios, pago_neto
                    FROM public.empleados 
                    WHERE cedula = '{cedula}';"""

        cursor.execute(consulta)
        fila = cursor.fetchone()

        saldo = empleados(cedula=fila[0], fecha_ingreso=fila[1].strftime("%d/%m/%Y"), fecha_salida=fila[2].strftime("%d/%m/%Y"), salario=fila[3], cesantias=fila[4], interes_cesantias=fila[5], vacaciones=fila[6], prima_servicios=fila[7], pago_neto=fila[8])

        return saldo