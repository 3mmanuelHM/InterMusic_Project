from typing import Dict
from musipy.clases.genero import Genero
from musipy.clases.artista import Artista

class Multimedia:
    def __init__(self, titulo: str, duracion: float, artista: Artista):
        self.titulo = titulo
        self.duracion = duracion
        self.artista = artista
        self.contador_reproducciones = 0
        
    def to_dict(self) -> Dict:
        """Convierte el objeto en un diccionario serializable a CSV."""
        raise NotImplementedError  # implementado en subclases 
    
    @staticmethod
    def from_dict(data: Dict) -> "Multimedia":
        """Devuelve Cancion o Podcast según el campo 'tipo'."""
        if data["tipo"] == "cancion":
            from musipy.clases.multimedia import Cancion  # import diferido
            return Cancion.from_dict(data)
        else:
            from musipy.clases.multimedia import Podcast
            return Podcast.from_dict(data)   

    def reproducir(self):
        self.contador_reproducciones += 1
        return f"Reproduciendo: {self.titulo} - {self.artista}"

class Cancion(Multimedia):
    def __init__(self, titulo: str, duracion: float, artista: Artista,
                 letra: str, album: str, genero: Genero):
        super().__init__(titulo, duracion, artista)
        self.letra = letra
        self.album = album
        self.genero = genero

    def __str__(self):
        return f"🎵 {self.titulo} - {self.artista} | Álbum: {self.album} | Género: {self.genero.nombre}"
    
    def to_dict(self):
        return {
            "tipo": "cancion",
            "titulo": self.titulo,
            "duracion": self.duracion,
            "artista": self.artista.__str__(),
            "letra": self.letra,
            "album": self.album,
            "genero": self.genero.nombre
        }

    @staticmethod
    def from_dict(data):
        from musipy.clases.genero import Genero
        from musipy.clases.artista import Artista
        # Nota: se recrea un Artista/Genero básico solo con el nombre
        artista = Artista(data["artista"], "NA", "NA")
        genero = Genero(data["genero"], "")
        return Cancion(data["titulo"], float(data["duracion"]), artista,
                       data["letra"], data["album"], genero)

class Podcast(Multimedia):
    def __init__(self, titulo: str, duracion: float, artista: Artista,
                 descripcion: str, categoria: str):
        super().__init__(titulo, duracion, artista)
        self.descripcion = descripcion
        self.categoria = categoria

    def __str__(self):
        return f"🎙 {self.titulo} - {self.artista} | Categoría: {self.categoria}"
    
    def to_dict(self):
        return {
            "tipo": "podcast",
            "titulo": self.titulo,
            "duracion": self.duracion,
            "artista": self.artista.__str__(),
            "descripcion": self.descripcion,
            "categoria": self.categoria
        }

    @staticmethod
    def from_dict(data):
        from musipy.clases.artista import Artista
        artista = Artista(data["artista"], "NA", "NA")
        return Podcast(data["titulo"], float(data["duracion"]), artista,
                       data["descripcion"], data["categoria"])