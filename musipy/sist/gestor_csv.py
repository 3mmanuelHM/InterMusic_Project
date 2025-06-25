import csv
from typing import List
from musipy.clases.multimedia import Multimedia

class GestorCSV:
    """
    Guarda y carga la biblioteca completa del usuario.
    Cada fila representa una Cancion o Podcast.
    """
    @staticmethod
    def guardar_biblioteca(biblioteca: List[Multimedia],
                           ruta: str = "biblioteca.csv") -> None:
        if not biblioteca:     # nada que guardar
            return
        with open(ruta, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=biblioteca[0].to_dict().keys())
            writer.writeheader()
            for item in biblioteca:
                writer.writerow(item.to_dict())

    @staticmethod
    def cargar_biblioteca(ruta: str = "biblioteca.csv") -> List[Multimedia]:
        try:
            with open(ruta, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return [Multimedia.from_dict(fila) for fila in reader]
        except FileNotFoundError:
            return []  # primera ejecución, no hay archivo
    
    @staticmethod
    def filtrar_nuevas(biblioteca, ruta_dataset):
        existentes = set()
        try:
            with open(ruta_dataset, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existentes.add((row["titulo"].lower(), row["artista"].lower()))
        except FileNotFoundError:
            pass

        return [
            item for item in biblioteca
            if (item.titulo.lower(), str(item.artista).lower()) not in existentes
        ]

    @staticmethod
    def agregar_al_dataset(canciones, ruta_dataset):
        if not canciones:
            return
        with open(ruta_dataset, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=canciones[0].to_dict().keys())
            # No escribimos encabezado en modo append
            for item in canciones:
                writer.writerow(item.to_dict())

