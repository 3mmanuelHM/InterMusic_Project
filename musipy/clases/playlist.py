import datetime
from typing import List
from musipy.clases.multimedia import Multimedia


class Playlist:
    def __init__(self, nombre: str, creador: str):
        self.nombre = nombre
        self.creador = creador
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d")
        self.elementos: List[Multimedia] = []

    def agregar_elemento(self, multimedia: Multimedia):
        self.elementos.append(multimedia)
        return f"'{multimedia.titulo}' agregado a la playlist '{self.nombre}'"

    def eliminar_elemento(self, indice: int):
        if 0 <= indice < len(self.elementos):
            elemento = self.elementos.pop(indice)
            return f"'{elemento.titulo}' eliminado de la playlist"
        return "Índice inválido"

    def reproducir_playlist(self):
        print(f"\nReproduciendo playlist: {self.nombre}")
        for i, elemento in enumerate(self.elementos, 1):
            print(f"{i}. {elemento.reproducir()}")

    def mostrar_elementos(self):
        if not self.elementos:
            print("\nLa playlist está vacía")
            return

        print(f"\nElementos en '{self.nombre}':")
        for i, elemento in enumerate(self.elementos, 1):
            print(f"{i}. {elemento}")

    def __str__(self):
        return f"📋 {self.nombre} (Creada por: {self.creador}, {len(self.elementos)} elementos)"