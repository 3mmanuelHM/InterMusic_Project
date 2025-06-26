import pandas as pd
from pathlib import Path

class AnalizarBiblioteca:
    @staticmethod
    def promedio_duracion_por_genero(csv_path='biblioteca.csv'):
        path = Path(csv_path)
        if not path.exists():
            print(f"❌ No se encontró el archivo: {csv_path}")
            return

        df = pd.read_csv(path)

        # Verificar que existan las columnas necesarias
        columnas_necesarias = {'tipo', 'genero', 'duracion'}
        if not columnas_necesarias.issubset(df.columns):
            print("❌ El archivo no contiene las columnas necesarias para el análisis.")
            return

        # Filtrar solo canciones con género y duración válidos
        canciones = df[df['tipo'].str.lower() == 'cancion'].copy()
        canciones = canciones.dropna(subset=['genero', 'duracion'])

        if canciones.empty:
            print("⚠️ No hay canciones válidas para analizar.")
            return

        # Agrupar por género y calcular promedio
        resultado = canciones.groupby("genero")["duracion"].mean().round(2)

        print("\n=== Promedio de duración por género ===")
        for genero, duracion in resultado.items():
            print(f"{genero}: {duracion} minutos")
