from dataclasses import field, asdict, astuple, dataclass, replace, make_dataclass
import pytest

@dataclass
class Config:
    nombre_app: str         # Nombre visible de la aplicación
    entorno: str            # 'producción', 'desarrollo', 'test'
    debug: bool             # Activar modo debug/logs extendidos
    puerto: int             # Puerto de escucha del servidor
    base_datos_url: str     # URL de conexión a la base de datos
 
    def como_dict(self):
        """
        Devuelve la configuración como diccionario.
        Útil para exportar a JSON, YAML o logs.
        """
        return asdict(self)
 
    @classmethod
    def desde_dict(cls, datos: dict):
        return cls(**datos)

# ---

def filtrar_nombres(nombres, patron):
    for nombre in nombres:
        if not nombre.lower().startswith(patron.lower()):
            yield nombre

nombres = [
    "Alejandro","Ana", "ANA", "Luis", "Maria", "ana", "Valentina", "Santiago", "Isabella", "Mateo", "Camila",
    "Sebastián", "Lucía", "Diego", "Mariana", "Daniel", "Sara",
    "Julián", "Emma", "Gabriel", "Victoria", "Luis", "Antonella",
    "Carlos", "Paula", "Miguel", "Natalia", "Andrés", "Renata",
    "Fernando", "Elena", "Juan", "Mía", "Pablo", "Antonella",
    "Ricardo", "Olivia", "Tomás", "Sofía", "Héctor", "Valeria",
    "Álvaro", "Camila", "Javier", "Martina"
]

def test_contador_nombres():
    nombres2 = ["Ana", "ANA", "Luis", "Maria", "ana"]
    
    resultado = contador_nombres(nombres2)
    assert resultado == {"ana": 3, "luis": 4, "maria": 5}
    
    resultado = contador_nombres([])
    assert resultado == {}
    
    resultado = contador_nombres(["Pedro", "Carlos"])
    assert resultado == {"pedro": 5, "carlos": 6}

def contador_nombres(nombres):
    return {nombre.lower(): len(nombre) for nombre in set(nombres)}

# ---

class Nido:
    def __init__(self, huevos: int, especie: str):
        self.huevos = huevos if huevos >= 0 else 0
        self.especie = especie

    def __str__(self):
        return f"Nido de {self.especie}"
    
    def __bool__(self):
        return self.huevos > 0
    
    def __add__(self, other):
        if isinstance(other, int):
            self.huevos + other
        elif isinstance(other, Nido):
            self.huevos + other.huevos
        
    def __radd__(self, other):
        if self.especie == other.especie:
            return self.huevos + other.huevos
        else:
            raise TypeError("Los nidos son de especies distintas")
        
    def __iadd__(self, other):
        if self.especie == other.especie:
            return self.huevos + other.huevos
        else:
            raise TypeError("Los nidos son de especies distintas")
        
    def __sub__(self, other):
        if self.especie == other.especie:
            return self.huevos - other.huevos
        else:
            raise TypeError("Los nidos son de especies distintas")
        
    def __rsub__(self, other):
        if self.especie == other.especie:
            return other.huevos - self.other
        else:
            raise TypeError("Los nidos son de especies distintas")
        
    def __iasub__(self, other):
        if self.especie == other.especie:
            return self.huevos - other.huevos
        else:
            raise TypeError("Los nidos son de especies distintas")
        
    def __eq__(self, other):
        return self.huevos == other.huevos
    
    def __ge__(self, other):
        return self.huevos >= other.huevos
    
    def __gt__(self, other):
        return self.huevos > other.huevos
    
    def __le__(self, other):
        return self.huevos <= other.huevos
    
    def __lt__(self, other):
        return self.huevos < other.huevos
    
    def __invert__(self):
        self.huevos = 0

    def __pos__(self):
        self.huevos += 1

    def __neg__(self):
        self.huevos -= 1

    def __len__(self):
        return self.huevos

nido1 = Nido(12, "gallina")
nido2 = Nido(10, "avestruz")

print(len(nido1))


# ---

@pytest.fixture
def datos_controlados() -> tuple[list[int], list[str]]:
    random.seed(42)
    numeros = generar_lista_numeros()
    nombres = generar_nombres_aleatorios()
    return numeros, nombres

def test_asociacion_aleatoria(datos_controlados):
    numeros, nombres = datos_controlados
    asociaciones = asociar_nombres_a_numeros(nombres, numeros)

    assert len(numeros) == 10
    assert len(nombres) == 10
    assert len(asociaciones) == 10
    assert all(isinstance(key, str) and len(key) == 5 for key in asociaciones.keys())
    assert all(isinstance(value, int) and 1 <= value <= 100 for value in asociaciones.values())



import random
import string

def generar_lista_numeros(cantidad: int=10, minimo: int=1, maximo: int=100):
     return [random.randint(minimo, maximo) for _ in range(cantidad)]

def generar_nombres_aleatorios(cantidad=10, longitud=5):
    return [''.join(random.choices(string.ascii_lowercase, k=longitud)) for _ in range(cantidad)]

def asociar_nombres_a_numeros(nombres: list[str], numeros: list[int]) -> dict[str, int]:
    return {nombre: numero for nombre, numero in zip(nombres, numeros)}
 
 # ---

def calculadora(n1: int, n2: int, operacion: callable):
    return operacion(n1, n2)  # No cambia!

def suma(n1, n2):
    return n1 + n2

def resta(n1, n2):
    return n1 -n2

resultado = calculadora(10, 20, lambda n1, n2: n1 * n2)
print(resultado)

# ---

# Crear una Playlist con Canciones, y que esa playlist se pueda tratar como una lista
import pytest

class Cancion:
    def __init__(self, nombre:str, artista:str, estilo:str, duracion:float):
        self.nombre = nombre
        self.artista = artista
        self.estilo = estilo
        self.duracion = duracion


class Playlist:
    def __init__(self, nombre):
        self.nombre = nombre
        self.canciones = []

    def añadirCancion(self, cancion: Cancion):
        self.canciones.append(cancion)

    def __getitem__(self, indice: int):
        return self.canciones[indice]
    
    def __setitem__(self, indice: int, cancion: Cancion):
        self.canciones[indice] = cancion
    
    def __len__(self):
        return len(self.canciones)
    
    def __iter__(self):
        return iter(self.canciones)
    
c = Cancion("Wonderwall", "Oasis", "Rock", 2.30)
p = Playlist("MiMusica")


@pytest.fixture
def playlist():
    return Playlist("MiMusica")

@pytest.fixture
def cancion():
    return Cancion("Wonderwall", "Oasis", "Rock", 2.30)

@pytest.fixture
def cancion_distinta():
    return Cancion("River Flows in You", "Yiruma", "Piano", 6.66)

def test_nombre(playlist):
    assert playlist.nombre == "MiMusica"

def test_añadir_cancion(cancion, playlist):
    p = playlist
    p.añadirCancion(cancion)
    assert p[0].nombre == "Wonderwall"
    assert p[0].artista == "Oasis"
    assert p[0].estilo == "Rock"
    assert p[0].duracion == 2.30

def test_cambiar_cancion(cancion, playlist, cancion_distinta):
    p = playlist
    p.añadirCancion(cancion)
    p[0] = cancion_distinta
    assert p[0].nombre != "Wonderwall"
    assert p[0].artista != "Oasis"
    assert p[0].estilo != "Rock"
    assert p[0].duracion != 2.30
    assert p[0].nombre == "River Flows in You"
    assert p[0].artista == "Yiruma"
    assert p[0].estilo == "Piano"
    assert p[0].duracion == 6.66

def test_tamaño_playlist(playlist, cancion):
    playlist.añadirCancion(cancion)
    assert len(playlist) == 1

def test_iterar_playlist(playlist, cancion):
    c2 = Cancion("Wonderwall2", "Oasis2", "Rock22", 2.30)
    playlist.añadirCancion(cancion)
    playlist.añadirCancion(c2)

    cancion = playlist.canciones[0]

    p = list(playlist)  # Esto llama a __iter__ automáticamente

    assert len(p) == 2
    assert p[0].artista == "Oasis"
    assert p[0].estilo == "Rock"
    assert p[1].artista == "Oasis2"
    assert p[1].estilo == "Rock22"

def test_pertenencia_cancion(playlist, cancion, cancion_distinta):
    playlist.añadirCancion(cancion)
    assert cancion_distinta not in playlist
    assert cancion in playlist


def validar_contraseña(contraseña, *funciones: list[callable]):
    resultados = []
    for funcion in funciones:
        resultado.append(funcion(contraseña))
    return all(resultados)  # Solo True si TODAS las validaciones son correctas

f = lambda x: lambda y: lambda z: x**2 + y**2 + z**2 + 1
f(1)(2)(3)

def f(x: int) -> callable:
    def inner_y(y: int) -> callable:
        def inner_z(z: int) -> int:
            return x**2 + y**2 + z**2 + 1
        return inner_z
    return inner_y

def nombre_decorador(func):  # Decorador
    def wrapper(*args, **kwargs):
        ...  # logica del decorador
        return func(*args, **kwargs)  # Ojo evaluada!
    return wrapper  #Ojo no evaluada! (closure)

from time import time, sleep

def tiempo(func):
    def wrapper(*args, **kwargs):
        inicio = time()
        resultado = func(*args, **kwargs)
        fin = time()
        print(f"{func.__name__} ha tardado {fin - inicio}")
        return resultado
    return wrapper

@tiempo
def sumar(n1, n2):
    return n1 + n2

import unittest

HISTORIAL = []  # TESTEAMOS ESTO
def historial(func):
    def wrapper(*args, **kwargs):
        HISTORIAL.append(func.__name__)
        resultado = func(*args, **kwargs)
        return resultado
    return wrapper

@historial
def saludar(nombre):
    return f"Buenas tarde{nombre}"
 
class TestDecorador(unittest.TestCase):

    @historial
    def funcion_de_test(n1):
        return n1 +1
    funcion_de_test(1)

    def test_historial(self):
        self.assertEqual(HISTORIAL, ["funcion_de_test"], f'{HISTORIAL} es lo que tengo, deberia ser ["funcion_de_test"]')


def nombre_decorador(args):
    def decorador(func):
        def wrapper(*args, **kwargs):
            ...
            return func(*args, **kwargs)
        return wrapper
    return decorador

@saluda_a_funcion("Juan")
def sumar(n1, n2):
    return n1 + n2

print(sumar(12, 44))