import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

from sklearn.cluster import KMeans
from sklearn.discriminant_analysis import StandardScaler
from sklearn.metrics import silhouette_score

def analizar_top_generos():
    ruta_csv = os.path.join("biblioteca_canciones.csv")

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
    plt.title("Top Géneros por Reproducciones")
    plt.xlabel("Género")
    plt.ylabel("Total de Reproducciones")
    plt.xticks(rotation=45)
    plt.grid(axis="y")
    plt.tight_layout()
    plt.show()

def clustering_con_silueta():
    ruta_csv = os.path.join("biblioteca_canciones.csv")

    if not os.path.exists(ruta_csv):
        print("No se encontró el archivo de canciones.")
        return

    df = pd.read_csv(ruta_csv)

    if df.empty or 'duracion' not in df.columns or 'reproducciones' not in df.columns:
        print("El archivo no tiene las columnas necesarias o está vacío.")
        return

    df['duracion'] = pd.to_numeric(df['duracion'], errors='coerce').fillna(0)
    df['reproducciones'] = pd.to_numeric(df['reproducciones'], errors='coerce').fillna(0)

    X = df[['duracion', 'reproducciones']].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    range_n_clusters = range(2, 10)
    silhouette_avgs = []

    kmeans_kwargs = {
        "init": "random",
        "n_init": 10,
        "max_iter": 300,
        "random_state": 42,
    }

    for n_clusters in range_n_clusters:
        kmeans = KMeans(n_clusters=n_clusters, **kmeans_kwargs)
        kmeans.fit(X_scaled)
        score = silhouette_score(X_scaled, kmeans.labels_)
        silhouette_avgs.append(score)

    # Graficar coeficiente de silueta
    plt.figure(figsize=(8, 4))
    plt.plot(range_n_clusters, silhouette_avgs, marker='o', color='blue')
    plt.title("Coeficientes de Silueta para diferentes valores de k")
    plt.xlabel("Número de clusters (k)")
    plt.ylabel("Coeficiente de Silueta Promedio")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Elegir el mejor k
    best_k = range_n_clusters[np.argmax(silhouette_avgs)]
    kmeans_final = KMeans(n_clusters=best_k, **kmeans_kwargs)
    labels = kmeans_final.fit_predict(X_scaled)

    # Graficar clustering final
    plt.figure(figsize=(6, 5))
    plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=labels, cmap='rainbow')
    plt.xlabel('Duración (escalada)')
    plt.ylabel('Reproducciones (escaladas)')
    plt.title(f'Clusters K-Means (k óptimo = {best_k})')
    plt.grid(True)
    plt.tight_layout()
    plt.show()