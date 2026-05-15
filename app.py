from flask import Flask
from flask import render_template
# Crear un instancia de Flask que sera nuestra aplicacion
app = Flask(__name__)

#Por cada ruta que vayamos a atender en el navegador, creamos una funcion en Python
@app.route("/") #El decordador indica la ruta que llama a esta funcion

def hola():
    #Lo que la funcion retorne, llega en el cuerpo HTML al navegador
    return "<strong><h1>Hola Mundo</h1></strong>"
@app.route("/clase")
def hola_clase():
    return "<strong><h1>Hola Clase</h1></strong>"

@app.route("/tim")
def tim():
    return render_template("hola.html")


app.run(debug=True)