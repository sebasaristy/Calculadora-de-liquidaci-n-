import datetime

class empleados:
    def __init__(self, fecha_ingreso: datetime.date, fecha_salida: datetime.date, salario: int):
        self.fecha_ingreso = fecha_ingreso
        self.fecha_salida = fecha_salida
        self.salario = salario
    
    