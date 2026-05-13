import datetime

class empleados:
    def __init__(self, fecha_ingreso: datetime.date, fecha_salida: datetime.date, salario: int, cesantias: float = 0, interes_cesantias: float = 0, prima_servicios: float = 0, vacaciones: float = 0, pago_neto: float = 0):
        self.fecha_ingreso = fecha_ingreso
        self.fecha_salida = fecha_salida
        self.salario = salario
        self.cesantias = cesantias
        self.interes_cesantias = interes_cesantias
        self.prima_servicios = prima_servicios
        self.vacaciones = vacaciones
        self.pago_neto = pago_neto
    
    