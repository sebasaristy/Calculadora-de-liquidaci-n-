import psycopg2

from model.empleados import empleados


class controlador:
    
    def insertar(empleado: empleados):
        coneccion = psycopg2.connect(database="calculadora_liquidacion_qjii" , user="admin" , password="5UGfOj4KELdPGu3vJgc74cE5aiMB3cVT" , host="dpg-d7uv3g3eo5us73ddtga0-a.oregon-postgres.render.com" , port="5432" )

        cursor = coneccion.cursor()

        sql = f""" INSERT INTO empleados (fecha_ingreso, fecha_salida, salario) VALUES ({empleado.fecha_ingreso}, {empleado.fecha_salida}, {empleado.salario}) """
        
        cursor.execute(sql) 

        coneccion.commit()

    def buscar(salario: int):
        coneccion = psycopg2.connect(database="calculadora_liquidacion_qjii" , user="admin" , password="5UGfOj4KELdPGu3vJgc74cE5aiMB3cVT" , host="dpg-d7uv3g3eo5us73ddtga0-a.oregon-postgres.render.com" , port="5432" )

        cursor = coneccion.cursor()

        sql = f""" SELECT * FROM empleados WHERE salario = {salario} """
        cursor.execute(sql)
        resultado = cursor.fetchone()
        cursor.close()
        coneccion.close()
        return resultado