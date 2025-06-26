import pandas as pd
from pathlib import Path
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.cluster import KMeans
import joblib

class AnalizarBiblioteca:
    """
    Analiza la biblioteca de canciones del usuario mediante K-Means.
    """

    @staticmethod
    def analizar_biblioteca_usuario(
        csv_path: str | Path = "biblioteca.csv",
        n_clusters: int = 3,
        save_model: bool = False,
        modelo_dir: str | Path = "musipy/analisis/modelos_basicos"
    ) -> pd.DataFrame:
        """
        Aplica K-Means sobre las canciones de 'csv_path'.
        Devuelve un DataFrame con la columna 'cluster'.

        Parámetros
        ----------
        csv_path : str | Path
            Ruta al CSV con la biblioteca (por defecto 'biblioteca.csv').
        n_clusters : int
            Número de clústeres (default 3).
        save_model : bool
            Si True, guarda scaler + kmeans en 'modelo_dir'.
        modelo_dir : str | Path
            Carpeta donde se guardarán los modelos (si save_model=True).
        """
        csv_path = Path(csv_path)
        if not csv_path.exists():
            raise FileNotFoundError(f"No se encontró {csv_path}")

        df = pd.read_csv(csv_path)

        # Verificación mínima de columnas requeridas
        required_cols = {"tipo", "titulo", "duracion", "genero", "reproducciones"}
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"Faltan columnas necesarias: {missing}")

        # Filtrar canciones
        canciones = df[df["tipo"].str.lower() == "cancion"].copy()
        if len(canciones) < n_clusters:
            raise ValueError(f"No hay suficientes canciones ({len(canciones)}) para {n_clusters} clústeres.")

        # Codificar género (rápido).
        le = OneHotEncoder()
        canciones["genero_cod"] = le.fit_transform(canciones["genero"].fillna("desconocido"))

        # Seleccionar features
        X = canciones[["duracion", "reproducciones", "genero_cod"]]

        # Escalado
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # K-Means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
        canciones["cluster"] = kmeans.fit_predict(X_scaled)

        # Guardar modelos opcionalmente
        if save_model:
            modelo_dir = Path(modelo_dir)
            modelo_dir.mkdir(parents=True, exist_ok=True)
            joblib.dump(scaler,  modelo_dir / "scaler_biblioteca.joblib")
            joblib.dump(kmeans,  modelo_dir / "kmeans_biblioteca.joblib")
            joblib.dump(le,      modelo_dir / "labelencoder_genero.joblib")

        print("✅ Análisis completado.")
        return canciones
