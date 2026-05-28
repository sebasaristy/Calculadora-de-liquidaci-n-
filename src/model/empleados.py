import datetime

class empleados:
    def __init__(self, cedula: str, fecha_ingreso: datetime.date, fecha_salida: datetime.date, salario: int, cesantias: float = 0, interes_cesantias: float = 0, prima_servicios: float = 0, vacaciones: float = 0, pago_neto: float = 0):
        self.cedula = cedula
        self.fecha_ingreso = fecha_ingreso
        self.fecha_salida = fecha_salida
        self.salario = salario
        self.cesantias = cesantias
        self.interes_cesantias = interes_cesantias
        self.prima_servicios = prima_servicios
        self.vacaciones = vacaciones
        self.pago_neto = pago_neto
    
    def is_equal(self, otro) -> bool:
        assert (self.cedula == otro.cedula)
        assert (self.fecha_ingreso     ==    otro.fecha_ingreso)
        assert (self.fecha_salida      ==    otro.fecha_salida)
        assert (self.salario           ==    otro.salario)
        assert (self.cesantias         ==    otro.cesantias)
        assert (self.interes_cesantias ==    otro.interes_cesantias)
        assert (self.prima_servicios   ==    otro.prima_servicios)
        assert (self.vacaciones        ==    otro.vacaciones)
        assert (self.pago_neto         ==    otro.pago_neto)
        return True
    