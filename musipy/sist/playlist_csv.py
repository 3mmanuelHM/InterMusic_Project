import csv
import os
from musipy.clases.multimedia import Cancion, Podcast
from musipy.clases.playlist import Playlist
from musipy.clases.genero import Genero
from musipy.clases.artista import Solista, Banda

CARPETA_PLAYLISTS = "playlist_exportadas"
os.makedirs(CARPETA_PLAYLISTS, exist_ok=True)

def guardar_playlist_csv(playlist: Playlist):
    nombre_archivo = f"{playlist.nombre.replace(' ', '_')}.csv"
    ruta = os.path.join(CARPETA_PLAYLISTS, nombre_archivo)

    with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["tipo", "titulo", "duracion", "artista", "extra", "reproducciones"])

        for item in playlist.elementos:
            tipo = "Cancion" if isinstance(item, Cancion) else "Podcast"
            artista = str(item.artista)
            extra = item.album if tipo == "Cancion" else item.categoria
            escritor.writerow([
                tipo,
                item.titulo,
                item.duracion,
                artista,
                extra,
                item.contador_reproducciones
            ])

def exportar_todas_las_playlists(playlists):
    for p in playlists:
        guardar_playlist_csv(p)

def cargar_playlist_csv(nombre_archivo, biblioteca_usuario):
    ruta = os.path.join(CARPETA_PLAYLISTS, nombre_archivo)
    playlist = Playlist(nombre_archivo.replace(".csv", ""), "importada")

    if not os.path.exists(ruta):
        return playlist

    with open(ruta, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            tipo = fila["tipo"]
            titulo = fila["titulo"]
            duracion = float(fila["duracion"])
            artista_str = fila["artista"]
            extra = fila["extra"]
            reproducciones = int(fila["reproducciones"])

            elemento = next((e for e in biblioteca_usuario if e.titulo == titulo and str(e.artista) == artista_str), None)
            if elemento:
                elemento.contador_reproducciones = reproducciones
                playlist.agregar_elemento(elemento)

    return playlist