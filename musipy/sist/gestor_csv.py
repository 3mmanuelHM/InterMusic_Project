import csv
import os
from typing import List
from musipy.clases.multimedia import Cancion, Multimedia, Podcast
from musipy.clases.playlist import Playlist

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
                
                
    @staticmethod
    def exportar_playlist(playlist, ruta="playlist_exportadas"):
        if not os.path.exists(ruta):
            os.makedirs(ruta)
        
        nombre_archivo = f"playlist_{playlist.nombre.replace(' ', '_')}.csv"
        path_completo = os.path.join(ruta, nombre_archivo)
        
        with open(path_completo, mode='w', newline='', encoding='utf-8') as file:
            fieldnames =[
                "titulo", "duración", "artista", "tipo", 
                "album", "genero", "descripción", "categoría"
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for item in playlist.elementos:
                fila = {
                    "titulo": item.titulo,
                    "duracion": item.duracion,
                    "artista": str(item.artista),
                    "tipo": "Cancion" if isinstance(item, Cancion) else "Podcast",
                    "album": item.album if isinstance(item, Cancion) else "",
                    "genero": item.genero.nombre if isinstance(item, Cancion) else "",
                    "descripcion": item.descripcion if isinstance(item, Podcast) else "",
                    "categoria": item.categoria if isinstance(item, Podcast) else ""
                }
                writer.writerow(fila)
        
        return path_completo
    
    @staticmethod
    def importar_canciones(ruta_csv: str) -> List[Multimedia]:
        """
        Lee un CSV (mismo formato que canciones_predeterminadas.csv)
        y devuelve objetos Cancion o Podcast listos para usar.
        """
        with open(ruta_csv, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [Multimedia.from_dict(row) for row in reader]
        
    @staticmethod
    def importar_playlist_csv(ruta_csv: str,
                              creador: str = "Importada") -> Playlist:
        """
        Convierte un CSV exportado por el sistema en un objeto Playlist.
        El nombre se deduce del archivo; si viene 'playlist_Mi_Playlist.csv'
        => 'Mi Playlist'.
        """
        base = os.path.basename(ruta_csv)
        nombre_playlist = os.path.splitext(base)[0].replace("playlist_", "")
        nombre_playlist = nombre_playlist.replace("_", " ")

        playlist = Playlist(nombre_playlist, creador)

        with open(ruta_csv, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                item = Multimedia.from_dict({
                    "tipo": "cancion" if row["tipo"].lower() == "cancion" else "podcast",
                    "titulo": row["titulo"],
                    "duracion": row["duracion"],
                    "artista": row["artista"],
                    "letra": row.get("letra", ""),
                    "album": row.get("album", ""),
                    "genero": row.get("genero", ""),
                    "descripcion": row.get("descripcion", ""),
                    "categoria": row.get("categoria", "")
                })
                playlist.agregar_elemento(item)
        return playlist

