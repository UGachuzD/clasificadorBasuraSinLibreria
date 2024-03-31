<template>
  <v-container class="fill-height">
    <v-responsive class="align-center fill-height mx-auto" max-width="1000">
      <v-card color="white" class="elevation-12" max-width="1000" height="500" outlined>
        <!-- Cambia el color de fondo a blanco -->
        <v-card-title class="text-center">CLASIFICADOR DE RESIDUOS</v-card-title>
        <v-container>
          <v-row justify="center"> <!-- Centra las columnas horizontalmente -->
            <v-col cols="5">
              <v-card class="pa-6" max-width="600" height="400" outlined>
                <v-card-title class="text-center">Archivo BMP a clasificar:</v-card-title>
                <v-file-input label="Seleccionar" variant="outlined" @change="handleFileUpload"></v-file-input>
                <!-- Campo para mostrar información -->
                <v-text-field v-model="clasificacionResiduo" label="Clasificación de residuo" readonly></v-text-field>
                <!-- Botón para iniciar la clasificación -->
                <v-btn color="primary" @click="clasificarResiduo" :disabled="!selectedImage">Clasificar</v-btn>
                <!-- Botón para limpiar campos -->
                <v-btn color="error" @click="limpiarCampos">Limpiar</v-btn>
              </v-card>
            </v-col>
            <v-col cols="7">
              <v-card class="pa-6" max-width="600" height="400" outlined>
                <v-card-title class="text-center">Visualización de la imagen:</v-card-title>
                <v-img :src="selectedImage" max-width="100%" max-height="90%"></v-img>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-responsive>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';

const selectedImage = ref(""); // Variable para almacenar la imagen seleccionada
const clasificacionResiduo = ref(""); // Variable para almacenar la clasificación de residuo

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
  formData.append('file', await fetch(selectedImage.value).then(res => res.blob()));

  try {
    const response = await fetch('http://127.0.0.1:5000/clasificar', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error('Error al clasificar la imagen');
    }

    const data = await response.json();
    clasificacionResiduo.value = data['Clasificación'];
  } catch (error) {
    console.error(error);
    clasificacionResiduo.value = "Error al clasificar la imagen";
  }
};

const limpiarCampos = () => {
  selectedImage.value = "";
  clasificacionResiduo.value = "";
};
</script>

<style scoped>
/* Estilos personalizados si es necesario */
</style>
