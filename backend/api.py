from flask import Flask, request, jsonify
from flask_cors import CORS 
import os

app = Flask(__name__)
CORS(app) 

def calcularProporcionesColores(datosImagen):
    totalPixeles = len(datosImagen) // 3
    rojo = 0
    amarillo = 0
    verde = 0
    negro = 0
    cafe = 0

    for i in range(0, len(datosImagen), 3):
        # El orden es BGR (Blue, Green, Red)
        if datosImagen[i] < 70 and datosImagen[i + 1] < 70 and datosImagen[i + 2] > 100:  # Amarillo
            amarillo += 1
        elif datosImagen[i + 2] > 100 and datosImagen[i + 1] < 100 and datosImagen[i] < 100:  # Rojo
            rojo += 1
        elif datosImagen[i + 1] > 100 and datosImagen[i] < 100 and datosImagen[i + 2] < 100:  # Verde
            verde += 1
        elif datosImagen[i] < 50 and datosImagen[i + 1] < 50 and datosImagen[i + 2] < 50:  # Negro
            negro += 1
        elif datosImagen[i] > 70 and datosImagen[i + 1] > 50 and datosImagen[i + 2] > 50:  # Café
            cafe += 1
        
    propRojo = rojo / totalPixeles * 100
    propAmarillo = amarillo / totalPixeles * 100
    propVerde = verde / totalPixeles * 100
    propNegro = negro / totalPixeles * 100
    propCafe = cafe / totalPixeles * 100

    return propRojo, propAmarillo, propVerde, propNegro, propCafe

def clasificarImagen(rutaImagen):
    with open(rutaImagen, 'rb') as imagen:
        # Leer la cabecera del archivo BMP
        encabezado = imagen.read(54)

        # Leer los datos de la imagen
        datosImagen = bytearray(imagen.read())

    propRojo, propAmarillo, propVerde, propNegro, propCafe = calcularProporcionesColores(datosImagen)

    response = {
        "Proporción de Rojo": f"{propRojo:.2f}%",
        "Proporción de Amarillo": f"{propAmarillo:.2f}%",
        "Proporción de Verde": f"{propVerde:.2f}%",
        "Proporción de Negro": f"{propNegro:.2f}%",
        "Proporción de Café": f"{propCafe:.2f}%"
    }

    # Clasificar la imagen
    if propRojo + propAmarillo + propVerde > 25:
        response["Clasificación"] = "La imagen es orgánica"
    elif propNegro > 20:
        response["Clasificación"] = "La imagen es de manejo especial o inorgánica no reciclable"
    elif propCafe > 20:
        response["Clasificación"] = "La imagen es inorgánica reciclable"
    else:
        response["Clasificación"] = "La imagen no puede ser clasificada con certeza"

    return response

@app.route('/clasificar', methods=['POST'])
def clasificar():
    if 'file' not in request.files:
        return jsonify({"error": "No se proporcionó ningún archivo"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No se seleccionó ningún archivo"}), 400

    filename = 'uploaded_image.bmp'
    file.save(filename)

    result = clasificarImagen(filename)
    os.remove(filename)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
