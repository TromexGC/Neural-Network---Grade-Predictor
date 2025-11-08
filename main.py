import os
# BLOQUE PARA SUPRIMIR ADVERTENCIAS DE TENSORFLOW Y KERAS
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # Suprime mensajes informativos y warnings


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


import tensorflow as tf
tf.get_logger().setLevel('ERROR') # Solo muestra errores graves

from tensorflow.keras.models import Sequential  #type: ignore
from tensorflow.keras.layers import Dense   #type: ignore




import datasetMethods as dm
import ui

try:
    # Crear datasets si no existen
    dm.Create_Dataset("alumnos.csv", [
        "legajo",
        "nombre",
        "edad",
        "genero"
        ])
    dm.Create_Dataset("materias.csv", [
        "id_materia",
        "nombre"
        ])
    dm.Create_Dataset("notas.csv", [
        "legajo",
        "id_materia",
        "nota",
        "fecha",
        "dificultad"])
    dm.Create_Dataset("alumno_materia.csv", [
        "legajo",
        "id_materia",
        "asistencia",
        "horas_semanales"])
    
    # Agregar datos iniciales para pruebas
    dm.CrearDatosPrincipio()
    

    # Iniciar la interfaz de usuario
    ui.mostrar_menu()

except Exception as e:
    print(f"Error: {e}")

