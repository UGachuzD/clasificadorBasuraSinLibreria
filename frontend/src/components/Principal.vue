<template>
  <v-container class="fill-height mx-auto">
    <v-responsive
      class="align-center fill-height mx-auto text-center"
      max-width="1000px"
    >
      <h1>CLASIFICADOR DE RESIDUOS</h1>
      <v-row justify="center">
        <!-- Centra las columnas horizontalmente -->
        <v-col cols="5">
          <v-card class="pa-6" width="400px" height="500px" variant="elevated" color="#F7F7FF">
            <v-card-title class="text-center"
              >Archivo BMP a clasificar:</v-card-title
            >
            <v-file-input
              v-model:="inputArchivo"
              label="Seleccionar"
              variant="outlined"
              @change="handleFileUpload"
            ></v-file-input>
            <!-- Campo para mostrar información -->
            <v-text-field
              v-model="clasificacionResiduo"
              label="Clasificación de residuo"
              readonly
            ></v-text-field>
            <!-- Botón para iniciar la clasificación -->
            <v-row justify="center">
              <v-btn
                color="primary"
                @click="clasificarResiduo"
                :disabled="!selectedImage"
                class="mr-4"
              >
                Clasificar
              </v-btn>
              <v-btn color="error" @click="limpiarCampos">Limpiar</v-btn>
            </v-row>
          </v-card>
        </v-col>
        <v-col cols="7">
          <v-card class="pa-6" max-width="600px" height="500px" variant="elevated" color="#F7F7FF">
            <v-card-title class="text-center"
              >Visualización de la imagen y su segmentación:</v-card-title
            >
            <v-carousel show-arrows="hover">
              <v-carousel-item
                :src="selectedImage"
                cover
                max-width="100%"
                max-height="80%"
              ></v-carousel-item>
              <v-carousel-item
                :src="'http://127.0.0.1:5000/imagen-segmentada/' + segmentedImage"
                cover
                max-width="100%"
                max-height="80%"
              ></v-carousel-item>
            </v-carousel>
          </v-card>
        </v-col>
      </v-row>
    </v-responsive>
  </v-container>
</template>

<script setup>
import { ref } from "vue";

const selectedImage = ref(""); // Variable para almacenar la imagen seleccionada
const clasificacionResiduo = ref(""); // Variable para almacenar la clasificación de residuo
const segmentedImage = ref(""); // Variable para almacenar el nombre del archivo de la imagen segmentada
const inputArchivo = ref(null); // Variable para almacenar el archivo seleccionado

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = (e) => {
    selectedImage.value = e.target.result;
  };

  reader.readAsDataURL(file);
};

const clasificarResiduo = async () => {
  const formData = new FormData();
  formData.append("file", await fetch(selectedImage.value).then((res) => res.blob()));

  try {
    const response = await fetch("http://127.0.0.1:5000/clasificar", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Error al clasificar la imagen");
    }

    const data = await response.json();
    clasificacionResiduo.value = data["Clasificación"];
    
    if (data['Imagen Segmentada']) {
      segmentedImage.value = data['Imagen Segmentada'];
    } else {
      console.error("La imagen segmentada no se pudo obtener.");
    }
  } catch (error) {
    console.error(error);
    clasificacionResiduo.value = "Error al clasificar la imagen";
  }
};

const limpiarCampos = () => {
  selectedImage.value = "";
  clasificacionResiduo.value = "";
  segmentedImage.value = "";
  inputArchivo.value = null;
};
</script>
