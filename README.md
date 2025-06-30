# InterMusic_Project
Desarrollo del proyecto para la materia de Desarrollo de Aplicaciones de Análisis de Datos, por Hernández Mendoza Emmanuel y Báez López Julio Alberto

InterMusic es un sistema interactivo hecho en Python para gestionar, reproducir y analizar bibliotecas musicales. Permite registrar canciones, podcasts y playlists, así como realizar análisis exploratorios sobre los datos usando técnicas de agrupamiento y estadísticas.

---

## Requisitos

Asegúrate de tener Python 3.8+ instalado. Luego, instala las dependencias necesarias con:

```bash
pip install -r requirements.txt

```

para ejecutar el sistema estando en la capeta InterMusic_Project ejecutar

python main.py

## Documentación del funcionamiento

El sistema **InterMusic** está organizado siguiendo principios de programación orientada a objetos y modularización. A continuación se describe el funcionamiento interno por componentes:

### Estructura general
- `main.py`: punto de entrada. Despliega el menú y ejecuta las opciones principales.
- `musipy/`: paquete que contiene toda la lógica del sistema.

### 🔍 Paquetes internos

#### `musipy/clases/`
Contiene las clases principales del modelo:
- `artista.py`: define la clase `Artista` con solista y banda como clases que heredan
- `genero.py`: clase `Genero`, describe el tipo de contenido musical.
- `multimedia.py`: clase base `Multimedia` para representar canciones y podcasts, ambas clases que heredan de multimedia.
- `playlist.py`: clase `Playlist` para agrupar contenidos.
- `usuario.py`: clase `Usuario`

#### `musipy/sist/`
Lógica del sistema:
- `sistema_musical.py`: contiene la clase `SistemaMusical`, la cual gestiona las operaciones principales (agregar canciones, reproducir, etc.).
- `gestor_csv.py`: contiene funciones para leer y escribir en archivos CSV. Se encarga de la persistencia de la biblioteca musical. Se encuentra también `playlist_csv` con el mismo proposito pero para playlist

#### `musipy/analisis/`
Módulos de análisis con aprendizaje automático:
- `analizar_biblioteca.py`: contiene funciones para realizar clustering sobre las canciones.

---

### Flujo de ejecución

1. El usuario ejecuta `main.py`, lo cual despliega un menú.
2. Cada opción del menú invoca métodos del `SistemaMusical`.
3. Al agregar o reproducir contenido, se actualiza el archivo `biblioteca.csv` a través del `gestor_csv`.
4. Si el usuario selecciona la opción de análisis, se aplica `KMeans` y se grafica el resultado.

---

### Persistencia

Todos los cambios (nuevas canciones, reproducciones, playlists) se guardan automáticamente en:
- `biblioteca.csv`: canciones y podcasts.
- Archivos CSV individuales para cada playlist.


