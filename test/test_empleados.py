import unittest
import datetime
import sys
sys.path.append('src')
 
from controller.empleado_controller import controlador
from model.empleados import empleados

class Test_empleados(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        controlador.borrar_tabla()
        controlador.crear_tabla()



    def test_insertar_y_consultar_empleados(self):
        empleado_prueba = empleados(
            fecha_ingreso = datetime.date(2026, 1, 1),
            fecha_salida = datetime.date(2026, 12, 31),
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

        
if __name__ == "__main__":
    unittest.main()