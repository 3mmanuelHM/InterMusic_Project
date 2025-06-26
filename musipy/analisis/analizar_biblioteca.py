import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
 
 class Analizador:
    
    def analizar_biblioteca_usuario(csv.path='biblioteca.csv', n_clusters=3):
        """
        Aplica K-Means a las canciones de la biblioteca del usuario.

        Parámetros:
        - csv_path: ruta al archivo CSV (por defecto: 'biblioteca.csv')
        - n_clusters: número de clústeres (por defecto: 3)

        Retorna:
        - DataFrame con canciones y su clúster asignado
        """
    
        try:
            df = pd.read_csv(csv_path)

            # Filtrar solo canciones válidas
            canciones = df[df["tipo"] == "cancion"].copy()
            canciones = canciones[["titulo", "duracion", "genero"]].dropna()

            if len(canciones) < n_clusters:
                print(f"[!] No hay suficientes canciones para agrupar en {n_clusters} clústeres.")
                return None

            # Codificar el género
            le = LabelEncoder()
            canciones["genero_cod"] = le.fit_transform(canciones["genero"])

            # Escalar características
            X = canciones[["duracion", "genero_cod"]]
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            # Aplicar K-Means
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            canciones["cluster"] = kmeans.fit_predict(X_scaled)

            print("[✓] Análisis completado.")
            return canciones

        except Exception as e:
            print(f"[Error] No se pudo realizar el análisis: {e}")
            return None