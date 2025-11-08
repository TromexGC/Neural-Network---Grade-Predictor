import pandas as pd
import numpy as np
import os
import sys
import subprocess
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential  #type: ignore
from tensorflow.keras.layers import Dense, Input #type: ignore
from tensorflow.keras.initializers import GlorotUniform #type: ignore
from tensorflow.keras.callbacks import EarlyStopping #type: ignore

def entrenar_modelo(df_notas, df_alumno_materia):
    """
    Entrena un modelo neuronal para predecir la nota esperada
    (entre 0 y 100) según asistencia y horas de estudio.
    """
    # 1. Fusionamos datos
    datos = df_notas.merge(df_alumno_materia, on=["legajo", "id_materia"])

    # 2. Seleccionamos variables de entrada (X) y salida (y)
    X = datos[["asistencia", "horas_semanales"]]
    y = datos["nota"]

    X_np = X.values
    # 3. Normalizamos los datos de entrada (X)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_np)

    # 4. Dividimos entre entrenamiento y prueba (Usamos random_state=42 para reproducibilidad)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    # 5. Normalizamos las notas (y) de 0-100 a 0-1, ya que usaremos la activación Sigmoide
    y_train_scaled = y_train / 100.0
    # No necesitamos el y_test_scaled para el entrenamiento, pero lo dejamos por consistencia

    # 6. Creamos el modelo (Arquitectura para regresión limitada de 0-100)
    model = Sequential([
        Input(shape=(X_np.shape[1],)),

        Dense(8, activation="relu",
            kernel_initializer=GlorotUniform(seed=42)),
        Dense(4, activation="relu"),
        Dense(1, activation="sigmoid") 
    ])

    model.compile(optimizer="adam", loss="mean_squared_error")

    early_stop = EarlyStopping(
        monitor='loss', patience=20, restore_best_weights=True
    )

    # 7. Entrenamos el modelo con el target escalado y_train_scaled
    # Aumentamos epochs para un mejor ajuste con pocos datos
    model.fit(X_train, y_train_scaled, epochs=200, batch_size=16, verbose=0, callbacks=[early_stop])

    # 8. Devolvemos el modelo y el scaler
    return model, scaler


def predecir(modelo, scaler, asistencia, horas):
    """
    Predice la nota esperada de un alumno.
    """
    entrada = np.array([[asistencia, horas]]) 
    entrada_escalada = scaler.transform(entrada)
    
    prediccion_0_1 = modelo.predict(entrada_escalada, verbose=0)
    
    # Multiplicamos por 100 para obtener el rango 0-100
    nota_predicha = prediccion_0_1[0][0] * 100 
    
    # Aseguramos que la nota esté estrictamente entre 0 y 100
    nota_final = np.clip(nota_predicha, 0, 100) 
    
    return round(float(nota_final), 2)


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