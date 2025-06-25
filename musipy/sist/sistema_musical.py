from musipy.clases.artista import Banda, Solista
from musipy.clases.genero import Genero
from musipy.clases.multimedia import Cancion, Podcast
from musipy.clases.playlist import Playlist
from musipy.clases.usuario import Usuario
from musipy.sist.gestor_csv import GestorCSV


class SistemaMusical:
    def __init__(self):
        self.usuario_actual = None
        self.generos_disponibles = []
        self.artistas_registrados = []
        
    def _cargar_biblioteca(self):
        if self.usuario_actual:
            self.usuario_actual.biblioteca = GestorCSV.cargar_biblioteca()

    def _guardar_biblioteca(self):
        if self.usuario_actual:
            GestorCSV.guardar_biblioteca(self.usuario_actual.biblioteca)    

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

        print("\n🎧 BIENVENIDO AL SISTEMA MUSICAL INTERACTIVO 🎧")
        nombre = input("Por favor, ingresa tu nombre: ")
        self.usuario_actual = Usuario(nombre)
        self._cargar_biblioteca() 
        print(f"\n¡Hola, {nombre}! ¿Qué te gustaría hacer hoy?")

        self.menu_principal()
        
        self._guardar_biblioteca()

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
                self._guardar_biblioteca()
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
            print("3. Volver al menú principal")

            opcion = input("Selecciona una opción (1-3): ")

            if opcion == "1":
                self.agregar_cancion()
            elif opcion == "2":
                self.agregar_podcast()
            elif opcion == "3":
                break
            else:
                print("Opción no válida. Intenta de nuevo.")

    def menu_playlists(self):
        while True:
            print("\n--- MIS PLAYLISTS ---")
            self.usuario_actual.mostrar_playlists()
            print("\nOpciones:")
            print("1. Crear nueva playlist")
            print("2. Gestionar playlist existente")
            print("3. Volver al menú principal")

            opcion = input("Selecciona una opción (1-3): ")

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
        duracion = float(input("Duración en minutos (ej. 3.5): "))

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

    def agregar_podcast(self):
        print("\n--- AGREGAR NUEVO PODCAST ---")
        titulo = input("Título del podcast: ")
        duracion = float(input("Duración en minutos (ej. 45.0): "))

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