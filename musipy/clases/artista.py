from typing import List

class Artista:
    def __init__(self, nombre: str, pais: str, fecha_inicio: str):
        self.nombre = nombre
        self.pais = pais
        self.fecha_inicio = fecha_inicio

    def __str__(self):
        return self.nombre

class Solista(Artista):
    def __init__(self, nombre: str, pais: str, fecha_inicio: str, apellido: str, fecha_nacimiento: str):
        super().__init__(nombre, pais, fecha_inicio)
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Banda(Artista):
    def __init__(self, nombre: str, pais: str, fecha_inicio: str, miembros: List[str]):
        super().__init__(nombre, pais, fecha_inicio)
        self.miembros = miembros
        self.cant_integrantes = len(miembros)

    def __str__(self):
        return f"{self.nombre} ({self.cant_integrantes} miembros)"