import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

class AnalizarKmeans:
    @staticmethod
    def aplicar_kmeans(csv_path='biblioteca.csv', n_clusters=3):
        try:
            df = pd.read_csv(csv_path)
        except FileNotFoundError:
            print(f"No se encontró el archivo {csv_path}")
            return None

        # Filtrar solo canciones válidas
        canciones = df[df['tipo'].str.lower() == 'cancion'].copy()
        canciones = canciones.dropna(subset=['genero', 'duracion'])

        if canciones.empty:
            print("No hay canciones válidas para analizar.")
            return None

        # Codificar género como número
        le = LabelEncoder()
        canciones['genero_cod'] = le.fit_transform(canciones['genero'])

        # Aplicar KMeans
        X = canciones[['duracion', 'genero_cod']]
        modelo = KMeans(n_clusters=n_clusters, random_state=0, n_init=10)
        canciones['cluster'] = modelo.fit_predict(X)

        # Asignar nombres a los clusters (puedes cambiar esto)
        nombres_clusters = {
            0: "Grupo A",
            1: "Grupo B",
            2: "Grupo C"
        }
        canciones['grupo_musical'] = canciones['cluster'].map(nombres_clusters)

        # Mostrar tabla
        print(f"Análisis K-Means aplicado con {n_clusters} clusters.")
        print(canciones[['titulo', 'genero', 'duracion', 'grupo_musical']])

        # Graficar
        plt.figure(figsize=(8, 6))
        plt.scatter(canciones['duracion'], canciones['genero_cod'],
                    c=canciones['cluster'], cmap='viridis', s=50)
        plt.xlabel('Duración (minutos)')
        plt.ylabel('Género codificado')
        plt.title('Agrupación de Canciones por K-Means')
        plt.grid(True)
        plt.show()

        return canciones[['titulo', 'genero', 'duracion', 'grupo_musical']]
