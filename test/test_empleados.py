import unittest
import datetime
import sys
sys.path.append('src')
 
from controller.empleado_controller import controlador
from model.empleados import empleados

class Test_empleados(unittest.TestCase):

    def test_insertar_y_consultar_empleados(self):
        empleado_prueba = empleados(
            fecha_ingreso='2024-2-1',
            fecha_salida='2024-5-1',
            salario=2000000
        )

        controlador.insertar(empleado_prueba)

        buscado_empleado = controlador.buscar(2000000)

        self.assertEqual(empleado_prueba.salario, buscado_empleado.salario)