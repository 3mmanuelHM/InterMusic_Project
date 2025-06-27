from typing import Dict
from musipy.clases.genero import Genero
from musipy.clases.artista import Artista

class Multimedia:
    def __init__(self, titulo: str, duracion: float, artista: Artista):
        self.titulo = titulo
        self.duracion = duracion
        self.artista = artista
        self.contador_reproducciones = 0

    def reproducir(self):
        self.contador_reproducciones += 1
        return f"Reproduciendo: {self.titulo} - {self.artista}"

    def __str__(self):
        return f"{self.titulo} - {self.artista} ({self.duracion} min) | Reproducciones: {self.contador_reproducciones}"

class Cancion(Multimedia):
    def __init__(self, titulo: str, duracion: float, artista: Artista,
                 letra: str, album: str, genero: Genero):
        super().__init__(titulo, duracion, artista)
        self.letra = letra
        self.album = album
        self.genero = genero

    def __str__(self):
        return f"{self.titulo} - {self.artista} | Álbum: {self.album} | Género: {self.genero.nombre} | Reproducciones: {self.contador_reproducciones}"

class Podcast(Multimedia):
    def __init__(self, titulo: str, duracion: float, artista: Artista,
                 descripcion: str, categoria: str):
        super().__init__(titulo, duracion, artista)
        self.descripcion = descripcion
        self.categoria = categoria

    def __str__(self):
        return f"{self.titulo} - {self.artista} | Categoría: {self.categoria} | Reproducciones: {self.contador_reproducciones}"