import unittest
import datetime
import sys
sys.path.append('src')
 
from controller.empleado_controller import controlador
from model.empleados import empleados
from model import errores

class Test_empleados(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        controlador.borrar_tabla()
        controlador.crear_tabla()



    def test_insertar_y_consultar_empleados_caso_normal_1(self):
        empleado_prueba = empleados(
            fecha_ingreso = "01/01/2026",
            fecha_salida = "31/12/2026",
            salario = 1_750_905,
            cesantias = 1_750_905,
            interes_cesantias = 210_109,
            prima_servicios = 1_750_905,
            vacaciones = 875_453,
            pago_neto = 4_587_371
        )

        controlador.insertar(empleado_prueba)

        empleado_buscado = controlador.buscar_salario(empleado_prueba.salario)
        
        self.assertTrue(empleado_prueba.is_equal(empleado_buscado))

    def test_insertar_y_consultar_empleado_caso_normal_2(self):
        empleado_prueba = empleados(
            fecha_ingreso = "01/01/2026",
            fecha_salida = "01/06/2026",
            salario = 3_501_810,
            cesantias = 1_459_088,
            interes_cesantias = 72_954,
            prima_servicios = 1_459_088,
            vacaciones = 729_544,
            pago_neto = 3_720_613
        )

        controlador.insertar(empleado_prueba)

        empleado_buscado = controlador.buscar_salario(empleado_prueba.salario)
        
        self.assertTrue(empleado_prueba.is_equal(empleado_buscado))
    
    def test_insertar_fecha_retiro_anterior_a_fecha_ingreso(self):
        fecha_ingreso = "28/03/2026"
        fecha_salida = "10/04/2025"

        empleado = empleados(fecha_ingreso = fecha_ingreso, fecha_salida = fecha_salida, salario = 1_750_905, cesantias = 0, interes_cesantias=0, vacaciones = 0, prima_servicios= 0, pago_neto=0)

        with self.assertRaises(errores.ErrorFechaIncorrecta):
            controlador.insertar(empleado)
    
    def test_insertar_fecha_inexistente(self):
        empleado = empleados(fecha_ingreso="32/04/2026", fecha_salida="1/05/2026", salario = 5_252_715, cesantias=0, interes_cesantias=0, vacaciones=0, prima_servicios=0, pago_neto=0)

        with self.assertRaises(errores.ErrorFechaFormatoIncorrecto):
            controlador.insertar(empleado)

    def test_buscar_fecha(self):
        empleado_prueba = empleados(
            fecha_ingreso = "01/08/2026",
            fecha_salida = "31/08/2026",
            salario = 5_050_000,
            cesantias = 420_833,
            interes_cesantias = 4_208,
            prima_servicios = 1_459_088,
            vacaciones = 210_417,
            pago_neto = 1_056_292
        )

        controlador.insertar(empleado_prueba)

        fecha_ingreso_buscada = controlador.buscar_por_fechas("01/08/2026", "31/08/2026")

        self.assertTrue(empleado_prueba.is_equal(fecha_ingreso_buscada))


        
if __name__ == "__main__":
    unittest.main()