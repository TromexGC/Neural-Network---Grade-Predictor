import pandas as pd
import os
import sys


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
    Save_Data("alumno_materia.csv", {'legajo': 1001, 'id_materia': 1, 'asistencia': 90, 'horas_semanales': 10})
    Save_Data("alumno_materia.csv", {'legajo': 1001, 'id_materia': 2, 'asistencia': 85, 'horas_semanales': 8})
    Save_Data("alumno_materia.csv", {'legajo': 1002, 'id_materia': 1, 'asistencia': 95, 'horas_semanales': 12})
    Save_Data("alumno_materia.csv", {'legajo': 1002, 'id_materia': 3, 'asistencia': 88, 'horas_semanales': 9})
    Save_Data("alumno_materia.csv", {'legajo': 1003, 'id_materia': 1, 'asistencia': 80, 'horas_semanales': 6})
    Save_Data("alumno_materia.csv", {'legajo': 1003, 'id_materia': 4, 'asistencia': 75, 'horas_semanales': 5})
    Save_Data("alumno_materia.csv", {'legajo': 1004, 'id_materia': 2, 'asistencia': 92, 'horas_semanales': 10})
    Save_Data("alumno_materia.csv", {'legajo': 1004, 'id_materia': 3, 'asistencia': 85, 'horas_semanales': 7})
    Save_Data("alumno_materia.csv", {'legajo': 1005, 'id_materia': 3, 'asistencia': 78, 'horas_semanales': 6})
    Save_Data("alumno_materia.csv", {'legajo': 1005, 'id_materia': 4, 'asistencia': 82, 'horas_semanales': 8})


    # === Agregar notas por alumno y materia ===
    Save_Data("notas.csv", {'legajo': 1001, 'id_materia': 1, 'nota': 85, 'fecha': '2023-05-10', 'dificultad': 'Media'})
    Save_Data("notas.csv", {'legajo': 1001, 'id_materia': 2, 'nota': 78, 'fecha': '2023-05-12', 'dificultad': 'Alta'})
    Save_Data("notas.csv", {'legajo': 1002, 'id_materia': 1, 'nota': 92, 'fecha': '2023-05-11', 'dificultad': 'Media'})
    Save_Data("notas.csv", {'legajo': 1002, 'id_materia': 3, 'nota': 88, 'fecha': '2023-05-13', 'dificultad': 'Baja'})
    Save_Data("notas.csv", {'legajo': 1003, 'id_materia': 1, 'nota': 75, 'fecha': '2023-05-10', 'dificultad': 'Media'})
    Save_Data("notas.csv", {'legajo': 1003, 'id_materia': 4, 'nota': 80, 'fecha': '2023-05-14', 'dificultad': 'Alta'})
    Save_Data("notas.csv", {'legajo': 1004, 'id_materia': 2, 'nota': 89, 'fecha': '2023-05-12', 'dificultad': 'Alta'})
    Save_Data("notas.csv", {'legajo': 1004, 'id_materia': 3, 'nota': 84, 'fecha': '2023-05-13', 'dificultad': 'Baja'})
    Save_Data("notas.csv", {'legajo': 1005, 'id_materia': 3, 'nota': 77, 'fecha': '2023-05-13', 'dificultad': 'Baja'})
    Save_Data("notas.csv", {'legajo': 1005, 'id_materia': 4, 'nota': 83, 'fecha': '2023-05-14', 'dificultad': 'Alta'})


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