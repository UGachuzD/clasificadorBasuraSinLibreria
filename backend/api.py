from flask import Flask, request, jsonify
from flask_cors import CORS  # Importar la extensión CORS
import os

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas en la aplicación

def calcular_proporcion_colores(datosImagen):
    total_pixeles = len(datosImagen) // 3
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
        
    prop_rojo = rojo / total_pixeles * 100
    prop_amarillo = amarillo / total_pixeles * 100
    prop_verde = verde / total_pixeles * 100
    prop_negro = negro / total_pixeles * 100
    prop_cafe = cafe / total_pixeles * 100

    return prop_rojo, prop_amarillo, prop_verde, prop_negro, prop_cafe

def clasificar_imagen(imagen_path):
    with open(imagen_path, 'rb') as imagen:
        # Leer la cabecera del archivo BMP
        encabezado = imagen.read(54)

        # Leer los datos de la imagen
        datosImagen = bytearray(imagen.read())

    prop_rojo, prop_amarillo, prop_verde, prop_negro, prop_cafe = calcular_proporcion_colores(datosImagen)

    response = {
        "Proporción de Rojo": f"{prop_rojo:.2f}%",
        "Proporción de Amarillo": f"{prop_amarillo:.2f}%",
        "Proporción de Verde": f"{prop_verde:.2f}%",
        "Proporción de Negro": f"{prop_negro:.2f}%",
        "Proporción de Café": f"{prop_cafe:.2f}%"
    }

    # Clasificar la imagen
    if prop_rojo + prop_amarillo + prop_verde > 25:
        response["Clasificación"] = "La imagen es orgánica"
    elif prop_negro > 20:
        response["Clasificación"] = "La imagen es de manejo especial o inorgánica no reciclable"
    elif prop_cafe > 20:
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

    result = clasificar_imagen(filename)
    os.remove(filename)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
