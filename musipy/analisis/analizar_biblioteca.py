import pandas as pd
import matplotlib.pyplot as plt
import os

def analizar_top_generos():
    ruta_csv = os.path("biblioteca_canciones.csv")

    if not os.path.exists(ruta_csv):
        print(f"No se encontró el archivo: {ruta_csv}")
        return

    df = pd.read_csv(ruta_csv)

    if 'genero' not in df.columns or 'reproducciones' not in df.columns:
        print("El CSV no contiene las columnas necesarias ('genero', 'reproducciones')")
        return

    if df.empty:
        print("El archivo está vacío.")
        return

    df['reproducciones'] = pd.to_numeric(df['reproducciones'], errors='coerce').fillna(0).astype(int)
    top_generos = df.groupby("genero")["reproducciones"].sum().sort_values(ascending=False)

    if top_generos.empty:
        print("No hay datos suficientes para graficar.")
        return

    # Imprimir en consola los datos
    print("\n🎧 Top de Géneros por Reproducciones:")
    print(top_generos.to_string())

    # Mostrar gráfico
    plt.figure(figsize=(10, 5))
    top_generos.plot(kind="bar", color="skyblue")
    plt.title("🎶 Top Géneros por Reproducciones")
    plt.xlabel("Género")
    plt.ylabel("Total de Reproducciones")
    plt.xticks(rotation=45)
    plt.grid(axis="y")
    plt.tight_layout()
    plt.show()

