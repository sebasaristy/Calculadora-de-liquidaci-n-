
class Excepcion(Exception):
    pass

class ErrorSalarioNoEntero(Exception):
    """Se usa cuando el valor del salario es erroneo."""
    def __init__(self):
        super().__init__(f'El valor del salario es incorrecto. \n Ingrese un valor válido, evite letras o caracteres especiales.')

class ErrorSalarioMenorDeCero(Exception):
    """Se usa cuando el valor del salario es menor o igual a 0."""
    def __init__(self):
        super().__init__(f'El salario ingresado debe ser mayor a 0.\n Ingrese un valor válido, evite numero negativos.')

class ErrorFechaFormatoIncorrecto(Exception):
    """Se usa cuando el formato de la fecha está mal introducida"""
    """Se usa también cuando se ingresa una fecha de retiro anterior a la de ingreso."""
    def __init__(self):
        super().__init__(f'El formato de la fecha está mal introducido.\n Ingrese la fecha en el formato DD/MM/AAAA, evite letras o caracteres especiales.')
        
class ErrorFechaIncorrecta(Exception):
    """Se usa también cuando se ingresa una fecha de retiro anterior a la de ingreso."""
    """Se usa también cuando se ingresa una fecha inexistente."""
    def __init__(self):
        super().__init__(f'La fecha de retiro no puede ser anterior a la de ingreso o se ingreso una fecha inexistente.\n Ingrese una fecha de retiro válida, posterior a la fecha de ingreso.')