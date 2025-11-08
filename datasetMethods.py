import pandas as pd
import os
import sys
import subprocess
import random as rnd


def Create_Dataset(nombre, columnas):
    """
    Crea un nuevo dataset CSV con las columnas especificadas.
    """
    try:
        df = pd.DataFrame(columns=columnas)
        df.to_csv(nombre, index=False)
    except Exception as e:
        print(f"Error al crear el dataset: {e}")

def Save_Data(nombre, data):
    """
    Guarda datos nuevos en un CSV existente.
    Si los datos se pasan como diccionario, los convierte en DataFrame.
    """
    try:
        # Si data es un diccionario, convertirlo a DataFrame
        if isinstance(data, dict):
            data = pd.DataFrame([data])
        
        df = pd.read_csv(nombre)
        df = pd.concat([df, data], ignore_index=True)
        df.to_csv(nombre, index=False)

    except Exception as e:
        print(f"Error al guardar los datos: {e}")

def CrearDatosPrincipio():
    """
    Agrega datos iniciales a los datasets para pruebas.
    """
    # Alumnos
    Save_Data("alumnos.csv", {'legajo': 1001, 'nombre': 'Juan Pérez', 'edad': 22, 'genero': 'M'})
    Save_Data("alumnos.csv", {'legajo': 1002, 'nombre': 'Ana Gómez', 'edad': 21, 'genero': 'F'})
    Save_Data("alumnos.csv", {'legajo': 1003, 'nombre': 'Facundo López', 'edad': 20, 'genero': 'M'})
    Save_Data("alumnos.csv", {'legajo': 1004, 'nombre': 'Camila Torres', 'edad': 23, 'genero': 'F'})
    Save_Data("alumnos.csv", {'legajo': 1005, 'nombre': 'Martín Ruiz', 'edad': 19, 'genero': 'M'})

    # Materias
    Save_Data("materias.csv", {'id_materia': 1, 'nombre': 'Programación'})
    Save_Data("materias.csv", {'id_materia': 2, 'nombre': 'Matemática'})
    Save_Data("materias.csv", {'id_materia': 3, 'nombre': 'Bases de Datos'})
    Save_Data("materias.csv", {'id_materia': 4, 'nombre': 'Física'})


    # Relación alumno–materia (asistencia y horas semanales)

    for alumno in range(1001, 1006):
        for materia in range(1, 5):
            asistencia = rnd.randint(70, 100)
            horas_semanales = rnd.randint(5, 12)
            Save_Data("alumno_materia.csv", {'legajo': alumno, 'id_materia': materia, 'asistencia': asistencia, 'horas_semanales': horas_semanales})
    

    # === Agregar notas por alumno y materia ===

    for alumno in range(1001, 1006):
        for materia in range(1, 5):
            for i in range(1, 10):  # 10 notas por materia
                nota = rnd.randint(40, 100)
                fecha = f"2023-{rnd.randint(1, 12)}-{rnd.randint(10, 20)}"
                dificultad = rnd.choice(['Baja', 'Media', 'Alta'])
                Save_Data("notas.csv", {'legajo': alumno, 'id_materia': materia, 'nota': nota, 'fecha': fecha, 'dificultad': dificultad})


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