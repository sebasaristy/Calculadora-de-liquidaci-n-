from flask import Flask
from flask import render_template
# Crear un instancia de Flask que sera nuestra aplicacion
app = Flask(__name__)

#Por cada ruta que vayamos a atender en el navegador, creamos una funcion en Python
@app.route("/") #El decordador indica la ruta que llama a esta funcion

def tim():
    return render_template("sexar_ht.html")


app.run(debug=True)