import unittest
import datetime
import sys
sys.path.append('src')
 
from controller.empleado_controller import controlador
from model.empleados import empleados

class Test_empleados(unittest.TestCase):

    def test_insertar_y_consultar_empleados(self):
        empleado_prueba = empleados(
            fecha_ingreso = datetime.date(2020, 1, 1),
            fecha_salida = datetime.date(2021, 1, 1),
            salario = 2000000,
            cesantias = 100000,
            interes_cesantias = 5000,
            prima_servicios = 150000,
            vacaciones = 20000,
            pago_neto = 2150000
        )

        controlador.insertar(empleado_prueba)

        

        self.assertEqual(empleado_prueba.salario, 2000000)

        
if __name__ == "__main__":
    unittest.main()