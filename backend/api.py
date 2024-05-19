from flask import Flask, request, jsonify, send_file
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

def segmentar(ruta_imagen, colores_segmentar):
    with open(ruta_imagen, "rb") as f:
        # Leer la cabecera del archivo BMP
        header = f.read(54)

        # Obtener dimensiones de la imagen
        ancho = int.from_bytes(header[18:22], byteorder='little')
        alto = int.from_bytes(header[22:26], byteorder='little')

        # Crear un nuevo archivo BMP para almacenar la imagen segmentada
        imagen_segmentada = bytearray()
        
        # Iterar sobre cada fila de píxeles de la imagen original
        for _ in range(alto):
            # Iterar sobre cada píxel de la fila actual
            for _ in range(ancho):
                # Leer el color del píxel en formato BGR
                blue = int.from_bytes(f.read(1), byteorder='little')
                green = int.from_bytes(f.read(1), byteorder='little')
                red = int.from_bytes(f.read(1), byteorder='little')

                # Verificar si el color está dentro de alguno de los rangos de la lista colores_segmentar
                color_en_rango = False
                for color_min, color_max in colores_segmentar:
                    if color_min[0] <= red <= color_max[0] and \
                       color_min[1] <= green <= color_max[1] and \
                       color_min[2] <= blue <= color_max[2]:
                        color_en_rango = True
                        break

                # Si el color está dentro de algún rango, escribirlo en la imagen segmentada
                if color_en_rango:
                    imagen_segmentada.extend([blue, green, red])
                else:
                    # Si no está en la lista, poner negro en la imagen segmentada
                    imagen_segmentada.extend([255, 255, 255])

    return header + imagen_segmentada

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

    print(response)

    # Clasificar la imagen
    if propRojo + propAmarillo + propVerde > 15:
        response["Clasificación"] = "La imagen es orgánica"
        # Segmentar la imagen en rojo, amarillo y verde
        colores_segmentar = [
            ((150, 0, 0), (255, 100, 100)),     # Rango de colores rojos
            ((0, 150, 0), (100, 255, 100)),     # Rango de colores verdes
            ((150, 150, 0), (255, 255, 100))    # Rango de colores amarillos
        ]
    elif propNegro > 20:
        response["Clasificación"] = "La imagen es de manejo especial o inorgánica no reciclable"
        # Segmentar la imagen en negro
        colores_segmentar = [((0, 0, 0), (50, 50, 50))]  # Rango de colores negros
    elif propCafe > 20:
        response["Clasificación"] = "La imagen es inorgánica reciclable"
        # Segmentar la imagen en café
        colores_segmentar = [
            ((80, 50, 0), (150, 100, 50)),   # Rango de colores cafés
            ((0, 0, 0), (50, 50, 50))        # Rango de colores negros
        ]  
    else:
        response["Clasificación"] = "La imagen no puede ser clasificada con certeza"
        return response

    # Segmentar la imagen
    imagen_segmentada = segmentar(rutaImagen, colores_segmentar)

    # Guardar la imagen segmentada en un nuevo archivo
    with open("imagenSegmentadaColores.bmp", "wb") as archivo_segmentado:
        archivo_segmentado.write(imagen_segmentada)

    response["Imagen Segmentada"] = "imagenSegmentadaColores.bmp"

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

@app.route('/imagen-segmentada/<nombre_archivo>')
def obtener_imagen_segmentada(nombre_archivo):
    # Devuelve la imagen segmentada solicitada al frontend
    return send_file("imagenSegmentadaColores.bmp", mimetype='image/bmp')


if __name__ == '__main__':
    app.run(debug=True)
