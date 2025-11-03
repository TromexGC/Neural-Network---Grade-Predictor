# ui.py
import os
import sys
import subprocess
import platform
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential  #type: ignore
from tensorflow.keras.layers import Dense   #type: ignore

# BLOQUE PARA SUPRIMIR ADVERTENCIAS DE TENSORFLOW Y KERAS
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # Suprime mensajes informativos y warnings
import tensorflow as tf
tf.get_logger().setLevel('ERROR') # Solo muestra errores graves

import datasetMethods as dm
import predictor as pr

lista_predicciones = []


def limpiar_consola():
    """Limpia la consola según el sistema operativo."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def mostrar_menu():
    while True:
        try:
            print("****************************************************")
            print("*           SISTEMA DE GESTION ACADEMICA           *")
            print("****************************************************")
            print("*  1. Registrar nueva materia                      *")
            print("*  2. Registrar nuevo alumno                       *")
            print("*  3. Asociar alumno a materia                     *")
            print("*  4. Registrar calificación de alumno             *")
            print("*  5. Predecir rendimiento académico               *")
            print("*  6. Visualizar materias registradas              *")
            print("*  7. Visualizar alumnos registrados               *")
            print("*  8. Visualizar notas registradas                 *")
            print("*  9. Salir del sistema                            *")
            print("****************************************************")
            opcion = int(input("Seleccione una opción (1-9): ").strip())
            if 1 <= opcion <= 9:
                if opcion == 1:
                    limpiar_consola()
                    registrar_materia()
                    pausar()
                elif opcion == 2:
                    limpiar_consola()
                    registrar_alumno()
                    pausar()
                elif opcion == 3:
                    limpiar_consola()
                    asociar_alumno_materia()
                    pausar()
                elif opcion == 4:
                    limpiar_consola()
                    asociar_nota()
                    pausar()
                elif opcion == 5:
                    limpiar_consola()
                    predecir_nota()
                    pausar()
                elif opcion == 6:
                    limpiar_consola()
                    visualizar_materias()
                    pausar()
                elif opcion == 7:
                    limpiar_consola()
                    visualizar_alumnos()
                    pausar()
                elif opcion == 8:
                    limpiar_consola()
                    visualizar_notas()
                    pausar()
                elif opcion == 9:
                    guardar_predicciones()
                    print("Saliendo del sistema. ¡Hasta luego!")
                    pausar()
                    limpiar_consola()
                    break
            else:
                print("Opción fuera de rango. Intente nuevamente.")
        except ValueError:
            print("Ingrese un número válido.")
        finally:
            limpiar_consola()

def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input("\nPresione Enter para continuar...")


def registrar_materia():    #1. Registrar nueva materia
    """
    Permite registrar una nueva materia en el dataset 'materias.csv'.
    Verifica que no haya duplicados (sin importar mayúsculas/minúsculas).
    """
    materias_df = pd.read_csv("materias.csv")

    # Pedir nombre de la materia
    nombre = input("Ingrese el nombre de la nueva materia: ").strip().title()

    # Verificar si ya existe (sin distinguir mayúsculas/minúsculas)
    if nombre.lower() in materias_df["nombre"].str.lower().values:
        print(f"La materia '{nombre}' ya existe en el sistema.")
        return
    
    # Calcular el próximo ID (si está vacío, arranca en 1)
    nuevo_id = materias_df["id_materia"].max() + 1 if not materias_df.empty else 1

    # Crear registro nuevo
    nueva_materia = {"id_materia": nuevo_id, "nombre": nombre}
    dm.Save_Data("materias.csv", nueva_materia)

    print(f"Materia '{nombre}' registrada con éxito (ID: {nuevo_id}).")

def registrar_alumno():   #2. Registrar nuevo alumno
    """
    Permite registrar un nuevo alumno en el dataset 'alumnos.csv'.
    Verifica que no haya duplicados por legajo.
    """
    alumnos_df = pd.read_csv("alumnos.csv")

    # Pedir datos del alumno
    legajo = alumnos_df["legajo"].max() + 1 if not alumnos_df.empty else 1000

    nombre = input("Ingrese el nombre completo del alumno: ").strip().title()
    edad = int(input("Ingrese la edad del alumno: ").strip())
    genero = input("Ingrese el género del alumno (M/F/O): ").strip().upper()

    # Crear registro nuevo
    nuevo_alumno = {
        "legajo": legajo,
        "nombre": nombre,
        "edad": edad,
        "genero": genero
    }
    dm.Save_Data("alumnos.csv", nuevo_alumno)

    print(f"Alumno '{nombre}' registrado con éxito (Legajo: {legajo}).")

def asociar_alumno_materia():   #3. Asociar alumno a materia
    """
    Permite asociar un alumno a una materia en el dataset 'alumno_materia.csv'.
    """
    alumnos_df = pd.read_csv("alumnos.csv")
    materias_df = pd.read_csv("materias.csv")
    alumno_materia_df = pd.read_csv("alumno_materia.csv")

    # Pedir legajo y nombre de materia
    legajo = int(input("Ingrese el legajo del alumno: ").strip())
    nombre_materia = input("Ingrese el nombre de la materia: ").strip().capitalize()

    # Verificar existencia del alumno
    if legajo not in alumnos_df["legajo"].values:
        print(f"El legajo {legajo} no corresponde a ningún alumno registrado.")
        return

    # Verificar existencia de la materia
    materia_data = materias_df[materias_df["nombre"].str.lower() == nombre_materia.lower()]
    if materia_data.empty:
        print(f"La materia '{nombre_materia}' no está registrada.")
        return
    id_materia = materia_data["id_materia"].iloc[0]

    # Pedir datos de asistencia y horas semanales
    asistencia = float(input("Ingrese el porcentaje de asistencia del alumno (0-100): ").strip())
    horas_semanales = float(input("Ingrese las horas semanales de estudio del alumno: ").strip())

    # Crear registro nuevo
    nueva_asociacion = {
        "legajo": legajo,
        "id_materia": id_materia,
        "asistencia": asistencia,
        "horas_semanales": horas_semanales
    }
    dm.Save_Data("alumno_materia.csv", nueva_asociacion)

    print(f"Alumno (Legajo: {legajo}) asociado a la materia '{nombre_materia}' con éxito.")


def asociar_nota():    #4. Registrar calificación de alumno
    """
    Permite registrar una calificación de un alumno en el dataset 'notas.csv'.
    """
    alumnos_df = pd.read_csv("alumnos.csv")
    materias_df = pd.read_csv("materias.csv")
    notas_df = pd.read_csv("notas.csv")

    # Pedir legajo y nombre de materia
    legajo = int(input("Ingrese el legajo del alumno: ").strip())
    nombre_materia = input("Ingrese el nombre de la materia: ").strip().capitalize()

    # Verificar existencia del alumno
    if legajo not in alumnos_df["legajo"].values:
        print(f"El legajo {legajo} no corresponde a ningún alumno registrado.")
        return

    # Verificar existencia de la materia
    materia_data = materias_df[materias_df["nombre"].str.lower() == nombre_materia.lower()]
    if materia_data.empty:
        print(f"La materia '{nombre_materia}' no está registrada.")
        return
    id_materia = materia_data["id_materia"].iloc[0]

    # Pedir datos de la nota
    nota = float(input("Ingrese la nota obtenida por el alumno (0-100): ").strip())
    fecha = input("Ingrese la fecha de la calificación (YYYY-MM-DD): ").strip()
    dificultad = input("Ingrese la dificultad percibida por el alumno (Baja/Media/Alta): ").strip().capitalize()

    # Crear registro nuevo
    nueva_nota = {
        "legajo": legajo,
        "id_materia": id_materia,
        "nota": nota,
        "fecha": fecha,
        "dificultad": dificultad
    }
    dm.Save_Data("notas.csv", nueva_nota)

    print(f"Calificación registrada con éxito para el alumno (Legajo: {legajo}) en la materia '{nombre_materia}'.")


def predecir_nota():        #5. Predecir rendimiento académico
    """
    Permite predecir la nota esperada de un alumno según su asistencia y horas de estudio.
    """
    try:
        alumnos_df = pd.read_csv("alumnos.csv")
        materias_df = pd.read_csv("materias.csv")
        alumno_materia_df = pd.read_csv("alumno_materia.csv")

        # 1. Pedir inputs
        legajo = int(input("Ingrese el legajo del alumno: ").strip())
        nombre_materia = input("Ingrese el nombre de la materia: ").strip().capitalize()


        # 2. Obtener nombre del alumno y verificar que exista
        alumno_data = alumnos_df[alumnos_df['legajo'] == legajo]

        if alumno_data.empty:
            print(f"Error: El legajo {legajo} no corresponde a ningún alumno registrado.")
            return
            
        nombre_alumno = alumno_data['nombre'].iloc[0] # Obtenemos el nombre del alumno


        # 3. Obtener id_materia
        materia_data = materias_df[materias_df['nombre'].str.lower() == nombre_materia.lower()]
        
        if materia_data.empty:
            print(f"Error: La materia '{nombre_materia}' no está registrada.")
            return

        id_materia = materia_data["id_materia"].iloc[0]

        # 4. Obtener asistencia y horas para el alumno/materia específicos
        datos_alumno = alumno_materia_df[
            (alumno_materia_df["legajo"] == legajo) & 
            (alumno_materia_df["id_materia"] == id_materia)
        ]

        if datos_alumno.empty:
            print(f"Error: El legajo {legajo} no está asociado a la materia {nombre_materia}.")
            return

        asistencia = datos_alumno["asistencia"].iloc[0]
        horas = datos_alumno["horas_semanales"].iloc[0]

        print("Aguarde un momento, se está realizando la predicción...")

        # 5. Entrenar y predecir
        notas_df = pd.read_csv("notas.csv")
        modelo, scaler = pr.entrenar_modelo(notas_df, alumno_materia_df)

        nota_predicha = pr.predecir(modelo, scaler, asistencia, horas)

        lista_predicciones.append(f"Legajo: {legajo}, Alumno: {nombre_alumno}, Materia: {nombre_materia}, Nota Predicha: {nota_predicha:.2f}")

        print(f"\n--- Resultado de la Predicción ---")
        print(f"Alumno: {nombre_alumno}, Legajo: {legajo}, Materia: {nombre_materia}")
        print(f"Porcentaje de asistencia: {asistencia}%, Horas de estudio por semana: {horas}")
        print(f"La nota que se predice para el alumno es: {nota_predicha}")

    except ValueError:
        print("Por favor, ingrese un legajo numérico y asegúrese de que la materia sea válida.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def visualizar_materias(): #6. Visualizar materias registradas
    """Muestra las materias registradas en el sistema."""
    materias_df = pd.read_csv("materias.csv")
    print("\n--- Materias Registradas ---")
    print(materias_df.to_string(index=False))

def visualizar_alumnos():  #7. Visualizar alumnos registrados
    """Muestra los alumnos registrados en el sistema."""
    alumnos_df = pd.read_csv("alumnos.csv")
    print("\n--- Alumnos Registrados ---")
    print(alumnos_df.to_string(index=False))

def visualizar_notas():    #8. Visualizar notas registradas
    """Muestra las notas registradas en el sistema."""
    notas_df = pd.read_csv("notas.csv")
    print("\n--- Notas Registradas ---")
    print(notas_df.to_string(index=False))

def guardar_predicciones():
    """Guarda las predicciones realizadas en un archivo de texto."""
    if lista_predicciones:
        with open("predicciones.txt", "w") as f:
            for linea in lista_predicciones:
                f.write(linea + "\n")
        print("Predicciones guardadas en 'predicciones.txt'.")
    else:
        print("No hay predicciones para guardar.")



if __name__ == "__main__":      # Redirige la ejecución a main.py si se ejecuta este archivo directamente
    
    script_actual = os.path.basename(sys.argv[0])

    if script_actual != "main.py":
        print("-------------------------------------------------------")
        print(f"   ADVERTENCIA: Se intentó ejecutar '{script_actual}' directamente.")
        print("    Redirigiendo la ejecución a 'main.py'...")
        print("-------------------------------------------------------")

        try:
            # Encuentra la ruta al intérprete de Python
            python_executable = sys.executable
            
            # Ejecuta el archivo principal (main.py)
            subprocess.run([python_executable, "main.py"])

        except FileNotFoundError:
            print("\nERROR: No se pudo encontrar el intérprete de Python o 'main.py'.")