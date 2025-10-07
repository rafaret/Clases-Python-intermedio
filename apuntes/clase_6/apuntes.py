from time import sleep
import functools

CACHE = {}

# def cache(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         global CACHE
#         key: tuple = (func.__name__, args, tuple(kwargs.items()))  # Key para la cache
#         if args in CACHE:  # Si args ESTA en cache...
#             return CACHE[key]  # ...me das lo de la cache
#         resultado = func(*args, **kwargs)  # Si NO esta en cache, hay que evaluar!
#         CACHE[key] = resultado  # Guardamos resultado en cache
#         return resultado
#     return wrapper


# @cache
# def sumar(a, b):
#     sleep(1)
#     return a + b

# # ---

# class Cache:
#     def __init__(self, func: callable):
#         functools.update_wrapper(self, func)
#         self.func = func
    
#     def __call__(self, *args, **kwargs):
#         key = (self.func.__name__, args, tuple(kwargs.items()))
#         if key in CACHE:
#             print(f"Desde caché: {args}")
#             return CACHE[key]
        
#         print(f"Calculando: {args}")
#         resultado = self.func(*args)
#         CACHE[key] = resultado
#         return resultado


# @Cache
# def restar(a, b):
#     sleep(1)
#     return a + b

# ---

# Fabrica de profesionales

# 1. Profesionales
from abc import ABC, abstractmethod

class Persona(ABC):
    def __init__(self, nombre: str):
        self.nombre = nombre

class Desarrollador(Persona):
    def desarrollar(self):
        print(f"Soy {self.nombre} y me dedico a desarrollar")

class Medico(Persona):
    def curar(self):
        print(f"Soy {self.nombre} y me dedico a curar")

class Profesor(Persona):
    def educar(self):
        print(f"Soy {self.nombre} y me dedico a enseñar Python!")

def fabrica_con_estrategia(tipo: str, nombre: str):
    if tipo == "dev":
        return Desarrollador(nombre)
    elif tipo == "doc":
        return Medico(nombre)
    elif tipo == "teacher":
        return Profesor(nombre)
    else:
        raise ValueError(f"Tipo desconocido: {tipo}")

def fabrica_con_inyeccion(trabajador: Persona, nombre: str):
    return trabajador(nombre)

# ---

class FabricaInterfaz(ABC):
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def crear(self):
        ...

class FabricaConEstrategia:
    def __init__(self):
        self._estrategias = {
            "dev": Desarrollador,
            "doc": Medico,
            "teacher": Profesor
        }

    def crear(self, tipo: str, nombre: str) -> Persona:
        try:
            clase = self._estrategias[tipo]
            return clase(nombre)
        except KeyError:
            raise ValueError(f"Tipo desconocido: {tipo}")

# *******************

class FabricaConInyeccion:
    def __init__(self, clase_persona: Persona):
        self.clase_persona = clase_persona

    def crear(self, nombre: str) -> Persona:
        return self.clase_persona(nombre)
    
    def cambiar_clase(self, clase_nueva: Persona):
        self.clase_persona = clase_nueva

# ---

class Fabrica:
    @staticmethod
    def crear(trabajador: Persona, nombre: str) -> Persona:
        return trabajador(nombre)
 
 # ---

metodo = "push"

class Transporte(ABC):
    def __init__(self, coste):
        self.coste = coste

    @abstractmethod
    def transportar():
        ...

class Bici(Transporte):
    def __init__(self, coste):
        super().__init__(coste)
        self.velocidad = 20  # km/h

    def transportar(self):
        print("Estoy utilizando una bici")

class Bus(Transporte):
    def __init__(self, coste):
        super().__init__(coste)
        self.velocidad = 60  # km/h

    def transportar(self):
        print("Estoy utilizando un bus publico")

class Taxi(Transporte):
    def __init__(self, coste):
        super().__init__(coste)
        self.velocidad = 100  # km/h

    def transportar(self):
        print("Estoy utilizando un VTC")

class AlgoritmoTransporte:
    def __init__(self, coste):
        self.estrategia = self.elegir_estrategia(coste)

    @staticmethod
    def elegir_estrategia(coste):  # Estrategia
        if coste >= 100:
            return Taxi(coste)
        elif 100 > coste >= 10:
            return Bus(coste)
        elif 10 > coste:
            return Bici(coste)
        else:
            raise ValueError("Ese coste es raro raro")
        
    def utilizar_transporte(self):
        self.estrategia.transportar()
