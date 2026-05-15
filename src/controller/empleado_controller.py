import psycopg2

from model.empleados import empleados
import secret_config 


class controlador:
    def obtener_cursor():
        coneccion = psycopg2.connect(database=secret_config.PGDATABASE , user=secret_config.PGUSER , password=secret_config.PGPASSWORD , host=secret_config.PGHOST , port=secret_config.PGPORT )

        cursor = coneccion.cursor()

        return cursor

    def insertar(empleado: empleados):
        cursor = controlador.obtener_cursor()

        sql = f""" INSERT INTO empleados (fecha_ingreso, fecha_salida, salario, cesantias, interes_cesantias, vacaciones, prima_servicios, pago_neto) VALUES ('{empleado.fecha_ingreso}', '{empleado.fecha_salida}', {empleado.salario}, {empleado.cesantias}, {empleado.interes_cesantias}, {empleado.vacaciones}, {empleado.prima_servicios}, {empleado.pago_neto}) """
        
        cursor.execute(sql) 

        cursor.connection.commit()

    def buscar_salario(salario: int) -> empleados:
        cursor = controlador.obtener_cursor()

        consulta = f""" SELECT fecha_ingreso, fecha_salida, salario, cesantias, interes_cesantias, vacaciones, prima_servicios, pago_neto
            FROM public.empleados WHERE salario = 1750905; """
        
        cursor.execute(consulta)

        fila = cursor.fetchone()
        saldo = empleados(fecha_ingreso=fila[0], fecha_salida=fila[1], salario=fila[2], cesantias=fila[3], interes_cesantias=fila[4], vacaciones=fila[5], prima_servicios=fila[6], pago_neto=fila[7])

        return saldo