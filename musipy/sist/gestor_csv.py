import csv
import os
from musipy.clases.multimedia import Cancion, Podcast
from musipy.clases.artista import Artista, Solista, Banda
from musipy.clases.genero import Genero

RUTA_CANCIONES = "biblioteca_canciones.csv"
RUTA_PODCASTS = "biblioteca_podcasts.csv"

def guardar_canciones_csv(canciones):
    with open(RUTA_CANCIONES, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([
            "titulo", "duracion", "artista_tipo", "artista_nombre", "artista_apellido",
            "artista_pais", "artista_inicio", "letra", "album", "genero", "reproducciones"
        ])
        for c in canciones:
            tipo = "Solista" if isinstance(c.artista, Solista) else "Banda"
            apellido = c.artista.apellido if isinstance(c.artista, Solista) else ""
            escritor.writerow([
                c.titulo,
                c.duracion,
                tipo,
                c.artista.nombre,
                apellido,
                c.artista.pais,
                c.artista.fecha_inicio,
                c.letra,
                c.album,
                c.genero.nombre,
                c.contador_reproducciones
            ])

def cargar_canciones_csv(generos, artistas):
    canciones = []
    if not os.path.exists(RUTA_CANCIONES):
        return canciones

    with open(RUTA_CANCIONES, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            titulo = fila["titulo"]
            duracion = float(fila["duracion"])
            tipo = fila["artista_tipo"]
            nombre = fila["artista_nombre"]
            apellido = fila["artista_apellido"]
            pais = fila["artista_pais"]
            inicio = fila["artista_inicio"]
            letra = fila["letra"]
            album = fila["album"]
            genero_nombre = fila["genero"]
            reproducciones = int(fila["reproducciones"])

            artista = next((a for a in artistas if a.nombre == nombre and str(a) == (nombre + " " + apellido).strip()), None)
            if not artista:
                if tipo == "Solista":
                    artista = Solista(nombre, pais, inicio, apellido, "2000-01-01")
                else:
                    artista = Banda(nombre, pais, inicio, [nombre])
                artistas.append(artista)

            genero = next((g for g in generos if g.nombre == genero_nombre), None)
            if not genero:
                genero = Genero(genero_nombre, "")
                generos.append(genero)

            cancion = Cancion(titulo, duracion, artista, letra, album, genero)
            cancion.contador_reproducciones = reproducciones
            canciones.append(cancion)

    return canciones

def guardar_podcasts_csv(podcasts):
    with open(RUTA_PODCASTS, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([
            "titulo", "duracion", "artista_tipo", "artista_nombre", "artista_apellido",
            "artista_pais", "artista_inicio", "descripcion", "categoria", "reproducciones"
        ])
        for p in podcasts:
            tipo = "Solista" if isinstance(p.artista, Solista) else "Banda"
            apellido = p.artista.apellido if isinstance(p.artista, Solista) else ""
            escritor.writerow([
                p.titulo,
                p.duracion,
                tipo,
                p.artista.nombre,
                apellido,
                p.artista.pais,
                p.artista.fecha_inicio,
                p.descripcion,
                p.categoria,
                p.contador_reproducciones
            ])

def cargar_podcasts_csv(artistas):
    podcasts = []
    if not os.path.exists(RUTA_PODCASTS):
        return podcasts

    with open(RUTA_PODCASTS, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            titulo = fila["titulo"]
            duracion = float(fila["duracion"])
            tipo = fila["artista_tipo"]
            nombre = fila["artista_nombre"]
            apellido = fila["artista_apellido"]
            pais = fila["artista_pais"]
            inicio = fila["artista_inicio"]
            descripcion = fila["descripcion"]
            categoria = fila["categoria"]
            reproducciones = int(fila["reproducciones"])

            artista = next((a for a in artistas if a.nombre == nombre and str(a) == (nombre + " " + apellido).strip()), None)
            if not artista:
                if tipo == "Solista":
                    artista = Solista(nombre, pais, inicio, apellido, "2000-01-01")
                else:
                    artista = Banda(nombre, pais, inicio, [nombre])
                artistas.append(artista)

            podcast = Podcast(titulo, duracion, artista, descripcion, categoria)
            podcast.contador_reproducciones = reproducciones
            podcasts.append(podcast)

    return podcasts

