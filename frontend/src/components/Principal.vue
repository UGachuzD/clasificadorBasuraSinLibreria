<template>
<<<<<<< HEAD
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
            </v-carousel>
          </v-card>
        </v-col>
      </v-row>
=======
  <v-container class="fill-height">
    <v-responsive class="align-center fill-height mx-auto" max-width="1000">
      <v-card color="white" class="elevation-12" max-width="1000" height="500" outlined>
        <v-card-title class="text-center">CLASIFICADOR DE RESIDUOS</v-card-title>
        <v-container>
          <v-row justify="center">
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
>>>>>>> cff0f5d41582757e243619c4880b8d013f69a06e
    </v-responsive>
  </v-container>
</template>

<script setup>
import { ref } from "vue";

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
  formData.append(
    "file",
    await fetch(selectedImage.value).then((res) => res.blob())
  );

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
</style>
