import csv
from musipy.clases.artista import Banda, Solista
from musipy.clases.genero import Genero
from musipy.clases.multimedia import Cancion, Podcast
from musipy.clases.playlist import Playlist
from musipy.clases.usuario import Usuario
from musipy.sist.gestor_csv import (
    guardar_canciones_csv,
    cargar_canciones_csv,
    guardar_podcasts_csv,
    cargar_podcasts_csv
)
from musipy.sist.playlist_csv import (
    guardar_playlist_csv,
    exportar_todas_las_playlists,
    cargar_playlist_csv
)
import os

from musipy.analisis.analizar_biblioteca import analizar_top_generos, clustering_con_silueta

class SistemaMusical:
    def __init__(self):
        self.usuario_actual = None
        self.generos_disponibles = []
        self.artistas_registrados = []

    def registrar_generos_predeterminados(self):
        self.generos_disponibles = [
            Genero("Pop", "Música popular comercial"),
            Genero("Rock", "Música rock en todas sus variantes"),
            Genero("Electrónica", "Música creada con instrumentos electrónicos"),
            Genero("Reggaeton", "Música urbana originaria de Puerto Rico"),
            Genero("Indie", "Música independiente"),
            Genero("Jazz", "Música jazz con improvisaciones"),
            Genero("Clásica", "Música clásica tradicional")
        ]

    def registrar_artistas_predeterminados(self):
        self.artistas_registrados = [
            Solista("Taylor", "EEUU", "2006", "Swift", "1989-12-13"),
            Solista("Bad", "Puerto Rico", "2018", "Bunny", "1994-03-10"),
            Banda("Coldplay", "Reino Unido", "1996", ["Chris Martin", "Jonny Buckland"]),
            Solista("Dua", "Reino Unido", "2015", "Lipa", "1995-08-22"),
            Banda("Imagine Dragons", "EEUU", "2008", ["Dan Reynolds", "Wayne Sermon"])
        ]

    def iniciar_sistema(self):
        self.registrar_generos_predeterminados()
        self.registrar_artistas_predeterminados()

        print("\n BIENVENIDO AL SISTEMA MUSICAL INTERACTIVO ")
        nombre = input("Por favor, ingresa tu nombre: ")
        self.usuario_actual = Usuario(nombre)
        print(f"\n¡Hola, {nombre}! ¿Qué te gustaría hacer hoy?")
        canciones_cargadas = cargar_canciones_csv(self.generos_disponibles, self.artistas_registrados)
        for c in canciones_cargadas:
            self.usuario_actual.agregar_a_biblioteca(c)
            
        podcasts_cargados = cargar_podcasts_csv(self.artistas_registrados)
        for p in podcasts_cargados:
            self.usuario_actual.agregar_a_biblioteca(p)

        self.menu_principal()

    def menu_principal(self):
        while True:
            print("\n--- MENÚ PRINCIPAL ---")
            print("1. Gestionar mi biblioteca musical")
            print("2. Gestionar mis playlists")
            print("3. Buscar música")
            print("4. Salir del sistema")

            opcion = input("Selecciona una opción (1-4): ")

            if opcion == "1":
                self.menu_biblioteca()
            elif opcion == "2":
                self.menu_playlists()
            elif opcion == "3":
                self.buscar_musica()
            elif opcion == "4":
                print("\n¡Gracias por usar el sistema musical! Hasta pronto.")
                break
            else:
                print("Opción no válida. Por favor, intenta de nuevo.")

    def menu_biblioteca(self):
        while True:
            print("\n--- MI BIBLIOTECA ---")
            self.usuario_actual.mostrar_biblioteca()
            print("\nOpciones:")
            print("1. Agregar nueva canción")
            print("2. Agregar nuevo podcast")
            print("3. Reproducir elemento")
            print("4. Importar canciones desde CSV externo")
            print("5. Analizar Biblioteca")
            print("6. Volver al menú principal")

            opcion = input("Selecciona una opción (1-6): ")

            if opcion == "1":
                self.agregar_cancion()
            elif opcion == "2":
                self.agregar_podcast()
            elif opcion == "3":
                self.reproducir_elemento_biblioteca()
            elif opcion == "4":
                archivo = input("Nombre del archivo CSV externo (con .csv): ")
                self.cargar_canciones_csv_externo(archivo)
                guardar_canciones_csv([c for c in self.usuario_actual.biblioteca if isinstance(c, Cancion)])
            elif opcion == "5":
                analizar_top_generos()
                clustering_con_silueta()
            elif opcion == "6":
                break
            else:
                print("Opción no válida. Intenta de nuevo.")
    
    def cargar_canciones_csv_externo(self, ruta: str):
        with open(ruta, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                nombre_csv = row['artista'].strip().lower()

                # Intentar buscar por nombre exacto (para Solista: nombre + apellido, para Banda: nombre)
                artista_encontrado = None
                for a in self.artistas_registrados:
                    if isinstance(a, Solista):
                        nombre_completo = f"{a.nombre} {a.apellido}".strip().lower()
                    else:
                        nombre_completo = a.nombre.strip().lower()

                    if nombre_completo == nombre_csv:
                        artista_encontrado = a
                        break

                # Si no se encuentra, se registra nuevo artista
                if not artista_encontrado:
                    print(f"\nEl artista '{row['artista']}' no está registrado.")
                    tipo = input("¿Es un solista (S) o una banda (B)? ").upper()
                    nombre = row['artista']
                    pais = input("País de origen: ")
                    fecha_inicio = input("Fecha de inicio (AAAA-MM-DD): ")

                    if tipo == "S":
                        apellido = input("Apellido: ")
                        fecha_nacimiento = input("Fecha de nacimiento (AAAA-MM-DD): ")
                        artista_encontrado = Solista(nombre, pais, fecha_inicio, apellido, fecha_nacimiento)
                    elif tipo == "B":
                        miembros = input("Miembros de la banda (separados por coma): ").split(",")
                        artista_encontrado = Banda(nombre, pais, fecha_inicio, [m.strip() for m in miembros])
                    else:
                        print("Tipo inválido. Se omite la canción.")
                        continue

                    self.artistas_registrados.append(artista_encontrado)

                genero_encontrado = next((g for g in self.generos_disponibles if g.nombre.lower() == row['genero'].strip().lower()), None)
                if not genero_encontrado:
                    print(f"\nEl género '{row['genero']}' no está registrado.")
                    descripcion = input("Descripción del género: ")
                    genero_encontrado = Genero(row['genero'], descripcion)
                    self.generos_disponibles.append(genero_encontrado)

                cancion = Cancion(
                    titulo=row['titulo'],
                    duracion=float(row['duracion']),
                    artista=artista_encontrado,
                    letra=row['letra'],
                    album=row['album'],
                    genero=genero_encontrado
                )
                cancion.contador_reproducciones = int(row['reproducciones'])
                self.usuario_actual.agregar_a_biblioteca(cancion)

        print("\nImportación de canciones completada con éxito.")


    def menu_playlists(self):
        while True:
            print("\n--- MIS PLAYLISTS ---")
            self.usuario_actual.mostrar_playlists()
            print("\nOpciones:")
            print("1. Crear nueva playlist")
            print("2. Gestionar playlist existente")
            print("3. Exportar todas las playlists")
            print("4. Importar playlist desde CSV")
            print("5. Volver al menú principal")

            opcion = input("Selecciona una opción (1-5): ")

            if opcion == "1":
                nombre = input("Ingresa el nombre de la nueva playlist: ")
                playlist = self.usuario_actual.crear_playlist(nombre)
                print(f"Playlist '{playlist.nombre}' creada exitosamente!")
            elif opcion == "2":
                if not self.usuario_actual.playlists:
                    print("No tienes playlists para gestionar.")
                    continue

                print("\nSelecciona una playlist:")
                for i, playlist in enumerate(self.usuario_actual.playlists, 1):
                    print(f"{i}. {playlist}")

                try:
                    seleccion = int(input("Ingresa el número de playlist: ")) - 1
                    if 0 <= seleccion < len(self.usuario_actual.playlists):
                        self.gestionar_playlist(self.usuario_actual.playlists[seleccion])
                    else:
                        print("Número de playlist inválido.")
                except ValueError:
                    print("Por favor ingresa un número válido.")
            elif opcion == "3":
                exportar_todas_las_playlists(self.usuario_actual.playlists)
                print("Playlists exportadas exitosamente en la carpeta 'playlist_exportadas'.")
            elif opcion == "4":
                archivo = input("Nombre del archivo CSV (con .csv): ")
                playlist = cargar_playlist_csv(archivo, self.usuario_actual.biblioteca)
                self.usuario_actual.playlists.append(playlist)
                print(f"Playlist '{playlist.nombre}' importada exitosamente.")
            elif opcion == "5":
                break
            else:
                print("Opción no válida. Intenta de nuevo.")

    def gestionar_playlist(self, playlist: Playlist):
        while True:
            print(f"\nGESTIONANDO PLAYLIST: {playlist.nombre}")
            playlist.mostrar_elementos()
            print("\nOpciones:")
            print("1. Agregar elemento de mi biblioteca")
            print("2. Eliminar elemento")
            print("3. Reproducir playlist")
            print("4. Volver al menú de playlists")

            opcion = input("Selecciona una opción (1-4): ")

            if opcion == "1":
                self.agregar_elemento_a_playlist(playlist)
            elif opcion == "2":
                self.eliminar_elemento_de_playlist(playlist)
            elif opcion == "3":
                playlist.reproducir_playlist()
                guardar_canciones_csv([c for c in self.usuario_actual.biblioteca if isinstance(c, Cancion)])
            elif opcion == "4":
                break
            else:
                print("Opción no válida. Intenta de nuevo.")

    def agregar_elemento_a_playlist(self, playlist: Playlist):
        if not self.usuario_actual.biblioteca:
            print("Tu biblioteca está vacía. Agrega música primero.")
            return

        print("\nSelecciona un elemento de tu biblioteca:")
        self.usuario_actual.mostrar_biblioteca()

        try:
            seleccion = int(input("Ingresa el número del elemento a agregar: ")) - 1
            if 0 <= seleccion < len(self.usuario_actual.biblioteca):
                elemento = self.usuario_actual.biblioteca[seleccion]
                print(playlist.agregar_elemento(elemento))
            else:
                print("Número de elemento inválido.")
        except ValueError:
            print("Por favor ingresa un número válido.")

    def eliminar_elemento_de_playlist(self, playlist: Playlist):
        if not playlist.elementos:
            print("La playlist está vacía.")
            return

        playlist.mostrar_elementos()

        try:
            seleccion = int(input("Ingresa el número del elemento a eliminar: ")) - 1
            resultado = playlist.eliminar_elemento(seleccion)
            print(resultado)
        except ValueError:
            print("Por favor ingresa un número válido.")

    def agregar_cancion(self):
        print("\n--- AGREGAR NUEVA CANCIÓN ---")
        titulo = input("Título de la canción: ")
        try:
            duracion = float(input("Duración en minutos (ej. 3.5): "))
            if duracion <= 0:
                print("La duración debe ser positiva.")
                return
        except ValueError:
            print("Duración inválida.")
            return

        print("\nArtistas disponibles:")
        for i, artista in enumerate(self.artistas_registrados, 1):
            print(f"{i}. {artista}")
        print(f"{len(self.artistas_registrados)+1}. Registrar nuevo artista")

        try:
            seleccion = int(input("Selecciona un artista: "))
            if 1 <= seleccion <= len(self.artistas_registrados):
                artista = self.artistas_registrados[seleccion-1]
            elif seleccion == len(self.artistas_registrados)+1:
                artista = self.registrar_nuevo_artista()
                if not artista:
                    return
            else:
                print("Selección inválida")
                return
        except ValueError:
            print("Por favor ingresa un número válido.")
            return

        letra = input("Letra de la canción (opcional, presiona Enter para omitir): ")
        album = input("Álbum al que pertenece: ")

        print("\nGéneros disponibles:")
        for i, genero in enumerate(self.generos_disponibles, 1):
            print(f"{i}. {genero.nombre}")

        try:
            seleccion = int(input("Selecciona un género: ")) - 1
            if 0 <= seleccion < len(self.generos_disponibles):
                genero = self.generos_disponibles[seleccion]
            else:
                print("Selección inválida")
                return
        except ValueError:
            print("Por favor ingresa un número válido.")
            return

        cancion = Cancion(titulo, duracion, artista, letra, album, genero)
        print(self.usuario_actual.agregar_a_biblioteca(cancion))
        guardar_canciones_csv([c for c in self.usuario_actual.biblioteca if isinstance(c, Cancion)])

    def agregar_podcast(self):
        print("\n--- AGREGAR NUEVO PODCAST ---")
        titulo = input("Título del podcast: ")
        try:
            duracion = float(input("Duración en minutos (ej. 45.0): "))
            if duracion <= 0:
                print("La duración debe ser positiva.")
                return
        except ValueError:
            print("Duración inválida.")
            return

        print("\nArtistas disponibles:")
        for i, artista in enumerate(self.artistas_registrados, 1):
            print(f"{i}. {artista}")
        print(f"{len(self.artistas_registrados)+1}. Registrar nuevo artista")

        try:
            seleccion = int(input("Selecciona un artista: "))
            if 1 <= seleccion <= len(self.artistas_registrados):
                artista = self.artistas_registrados[seleccion-1]
            elif seleccion == len(self.artistas_registrados)+1:
                artista = self.registrar_nuevo_artista()
                if not artista:
                    return
            else:
                print("Selección inválida")
                return
        except ValueError:
            print("Por favor ingresa un número válido.")
            return

        descripcion = input("Descripción del podcast: ")
        categoria = input("Categoría (ej. Tecnología, Ciencia, Entretenimiento): ")

        podcast = Podcast(titulo, duracion, artista, descripcion, categoria)
        print(self.usuario_actual.agregar_a_biblioteca(podcast))
        guardar_podcasts_csv([p for p in self.usuario_actual.biblioteca if isinstance(p, Podcast)])

    def registrar_nuevo_artista(self):
        print("\n--- REGISTRAR NUEVO ARTISTA ---")
        tipo = input("¿Es un solista (S) o una banda (B)? ").upper()

        nombre = input("Nombre: ")
        pais = input("País de origen: ")
        fecha_inicio = input("Fecha de inicio (AAAA-MM-DD): ")

        if tipo == "S":
            apellido = input("Apellido: ")
            fecha_nacimiento = input("Fecha de nacimiento (AAAA-MM-DD): ")
            artista = Solista(nombre, pais, fecha_inicio, apellido, fecha_nacimiento)
        elif tipo == "B":
            miembros = input("Nombres de los miembros (separados por coma): ").split(',')
            miembros = [m.strip() for m in miembros]
            artista = Banda(nombre, pais, fecha_inicio, miembros)
        else:
            print("Tipo de artista no válido")
            return None

        self.artistas_registrados.append(artista)
        print(f"Artista '{artista}' registrado exitosamente!")
        return artista

    def buscar_musica(self):
        print("\n--- BUSCAR MÚSICA ---")
        termino = input("Ingresa término de búsqueda (título, artista o álbum): ").lower()

        resultados = []
        for item in self.usuario_actual.biblioteca:
            if (termino in item.titulo.lower() or
                termino in str(item.artista).lower() or
                (isinstance(item, Cancion) and termino in item.album.lower())):
                resultados.append(item)

        if resultados:
            print("\nResultados de búsqueda:")
            for i, item in enumerate(resultados, 1):
                print(f"{i}. {item}")
        else:
            print("\nNo se encontraron resultados para tu búsqueda.")

    def reproducir_elemento_biblioteca(self):
        if not self.usuario_actual.biblioteca:
            print("Tu biblioteca está vacía.")
            return

        self.usuario_actual.mostrar_biblioteca()

        try:
            seleccion = int(input("Selecciona el número del elemento a reproducir: ")) - 1
            if 0 <= seleccion < len(self.usuario_actual.biblioteca):
                item = self.usuario_actual.biblioteca[seleccion]
                print(item.reproducir())
                if isinstance(item, Cancion):
                     guardar_canciones_csv([c for c in self.usuario_actual.biblioteca if isinstance(c, Cancion)])
                elif isinstance(item, Podcast):
                    guardar_podcasts_csv([p for p in self.usuario_actual.biblioteca if isinstance(p, Podcast)])
                print(f"Reproducciones: {item.contador_reproducciones}")
            else:
                print("Número inválido.")
        except ValueError:
            print("Por favor ingresa un número válido.")