from typing import List
from musipy.clases.multimedia import Multimedia
from musipy.clases.playlist import Playlist

class Usuario:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.playlists: List[Playlist] = []
        self.biblioteca: List[Multimedia] = []

    def crear_playlist(self, nombre: str):
        nueva_playlist = Playlist(nombre, self.nombre)
        self.playlists.append(nueva_playlist)
        return nueva_playlist

    def agregar_a_biblioteca(self, multimedia: Multimedia):
        for item in self.biblioteca:
            if item.titulo == multimedia.titulo and item.artista == multimedia.artista:
                return f"'{multimedia.titulo}' ya está en tu biblioteca"
        self.biblioteca.append(multimedia)
        return f"'{multimedia.titulo}' agregado a tu biblioteca"

    def mostrar_playlists(self):
        if not self.playlists:
            print("\nNo tienes playlists creadas")
            return

        print("\nTus playlists:")
        for i, playlist in enumerate(self.playlists, 1):
            print(f"{i}. {playlist}")

    def mostrar_biblioteca(self):
        if not self.biblioteca:
            print("\nTu biblioteca está vacía")
            return

        print("\nTu biblioteca musical:")
        for i, item in enumerate(self.biblioteca, 1):
            print(f"{i}. {item}")