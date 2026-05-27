from flask import Flask
from flask import render_template, request

import sys
sys.path.append("src")

from model import logicaLiquidacion
from model import errores
from model import empleados

from controller import empleado_controller

from view.web import vista_usuarios

# Crear un instancia de Flask que sera nuestra aplicacion
app = Flask(__name__)

app.register_blueprint(vista_usuarios.blueprint)

if __name__ == '__main__':
    app.run(debug=True)