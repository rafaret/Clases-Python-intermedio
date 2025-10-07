from dataclasses import dataclass, field

@dataclass
class DataPipeline:
    data_sources: list = field(default_factory=list)
    transformations: list = field(default_factory=list)
    cache_enabled: bool = False
    cache: dict = field(default_factory=dict)
    batch_size: int = 0

class ConstructorDataPipeline:
    def __init__(self):
        self.pipeline = DataPipeline()
    
    def añadir_data_source(self, source: int | list[int]):
        if isinstance(source, list):
            self.pipeline.data_sources.extend(source)
        else:
            self.pipeline.data_sources.append(source)
        return self
    
    def transformation(self, func):
        self.pipeline.transformations.append(func)
        return self
    
    def activar_cache(self):
        self.pipeline.cache_enabled = True
        return self
    
    def tamaño(self, size: int):
        self.pipeline.batch_size = size
        return self
    
    def run(self):
        print("Ejecutando pipeline")
        for transform in self.pipeline.transformations:
            result = [transform(x) for x in self.pipeline.data]
        if self.pipeline.cache_enabled:
            self.pipeline.cache['datos'] = self.pipeline.data
        return result
    
    def reset(self):
        self.pipeline = DataPipeline()
        return self
    
    def construir(self) -> DataPipeline:
        return self.pipeline


def multiplicar_por_dos(x):
    return x * 2

def sumar_cinco(x):
    return x + 5

constructor = ConstructorDataPipeline()
pipeline = (constructor
            .añadir_data_source([1, 2, 3])
            .transformation(multiplicar_por_dos)
            .activar_cache()
            .tamaño(10)
            .construir())

print(pipeline)

# ---

from dataclasses import dataclass

@dataclass
class Query:
    select: str = ""
    from_clause: str = ""
    join: str = ""
    where: str = ""
    order_by: str = ""
    limit: str = ""

class ConstructorQuery:
    def __init__(self) -> None:
        self.query: Query = Query()
    
    def select(self, columnas: str) -> "ConstructorQuery":
        self.query.select = f"SELECT {columnas}"
        return self
    
    def from_table(self, tabla: str) -> "ConstructorQuery":
        self.query.from_clause = f"FROM {tabla}"
        return self
    
    def join(self, join_clause: str) -> "ConstructorQuery":
        self.query.join = f"JOIN {join_clause}"
        return self
    
    def where(self, condicion: str) -> "ConstructorQuery":
        self.query.where = f"WHERE {condicion}"
        return self
    
    def order_by(self, columna: str) -> "ConstructorQuery":
        self.query.order_by = f"ORDER BY {columna}"
        return self
    
    def limit(self, cantidad: int) -> "ConstructorQuery":
        self.query.limit = f"LIMIT {cantidad}"
        return self
    
    def construir(self) -> str:
        partes = [
            self.query.select,
            self.query.from_clause,
            self.query.join,
            self.query.where,
            self.query.order_by,
            self.query.limit
        ]
        query_sql = " ".join([parte for parte in partes if parte])
        return query_sql


# Uso
constructor = ConstructorQuery()
query1 = (constructor
          .select("id, nombre, email")
          .from_table("usuarios")
          .where("edad > 18")
          .order_by("nombre ASC")
          .limit(10)
          .construir())

print(query1)
print()

constructor2 = ConstructorQuery()
query2 = (constructor2
          .select("*")
          .from_table("pedidos")
          .join("usuarios ON pedidos.usuario_id = usuarios.id")
          .where("pedidos.estado = 'completado'")
          .order_by("pedidos.fecha DESC")
          .construir())

print(query2)

# ---

from abc import ABC, abstractmethod
from datetime import datetime

class TecnologiaMensajes(ABC):
    @abstractmethod
    def mandar_mensaje():  # Push, SMS, Teams, ...
        pass

class Notificacion(ABC):
    def __init__(self, sistemaMensajeria: TecnologiaMensajes):
        self.sistemaMensajeria = sistemaMensajeria  # SMS, HTTP, JSON, ...

    @abstractmethod
    def notificar():  # HelloWorlds, ShoppingCart, ...
        pass

class SMS(TecnologiaMensajes):
    def __init__(self, numero_telefono: int):
        self.numero_telefono = numero_telefono  # property de validacion

    def mandar_mensaje(self, body: str, *args):
        print(f"Se ha mandado desde {self.numero_telefono} el mensaje:\n\n{body}")

class Email(TecnologiaMensajes):
    def __init__(self, cuenta_email: str):  # usuario y contraseña!
        self.cuenta_email = cuenta_email  # property de validacion

    def mandar_mensaje(self, body: str, asunto: str = "Asunto generico"):
        print(f"Se ha mandado desde {self.cuenta_email} el mensaje:\n\n<h1>{asunto}</h1>\n<p>{body}</p>")

class Welcome(Notificacion):
    def __init__(self, sistemaMensajeria):
        super().__init__(sistemaMensajeria)

    def notificar(self, mensaje: str):
        self.sistemaMensajeria.mandar_mensaje(mensaje)

class Factura(Notificacion):
    def __init__(self, sistemaMensajeria, fecha: datetime = datetime.now()):
        super().__init__(sistemaMensajeria)
        self.fecha = fecha

    def notificar(self, mensaje: str, contexto: str):
        self.sistemaMensajeria.mandar_mensaje(mensaje, contexto)
        print("Factura almacenada en base de datos")


Factura(SMS(666666666)).notificar("Mañana tienes que hacer el pago", "Pago de mañana")

# ---

from abc import ABC, abstractmethod

# FORMATO DEL DATO (parte 1 del puente)
class FormatoDato(ABC):
    @abstractmethod
    def serializar(self, datos: dict) -> str:
        pass

class JSON(FormatoDato):
    def serializar(self, datos: dict) -> str:
        import json
        return json.dumps(datos)

class Bin(FormatoDato):
    def serializar(self, datos: dict) -> str:
        return str(datos).encode("utf-8").hex()

class HTTP(FormatoDato):
    def serializar(self, datos: dict) -> str:
        lineas = []
        for clave, valor in datos.items():
            linea = f"{clave}: {valor}"
            lineas.append(linea)
        return "\n".join(lineas)


# TIPO DE CONEXIÓN (parte 2 del puente)
class Conexion(ABC):
    def __init__(self, formato: FormatoDato):
        self.formato = formato

    @abstractmethod
    def enviar(self, datos: dict):
        pass

class GoogleDrive(Conexion):
    def enviar(self, datos: dict):
        contenido = self.formato.serializar(datos)
        print(f"[GoogleDrive] Subiendo archivo con contenido:\n{contenido}")

class HttpTransport(Conexion):
    def enviar(self, datos: dict):
        contenido = self.formato.serializar(datos)
        print(f"[HTTP] Realizando solicitud POST con datos:\n{contenido}")

class WebSocket(Conexion):
    def enviar(self, datos: dict):
        contenido = self.formato.serializar(datos)
        print(f"[WebSocket] Transmitiendo mensaje:\n{contenido}")

# Ejemplo de uso del patrón Bridge

datos = {"usuario": "miguel", "accion": "login", "estado": "ok"}

# Enviar por WebSocket en formato JSON
conexion1 = WebSocket(JSON())
conexion1.enviar(datos)

# Enviar por GoogleDrive en formato Binario
conexion2 = GoogleDrive(Bin())
conexion2.enviar(datos)

# Enviar por HTTP en formato HTTP 
conexion3 = HttpTransport(HTTP())
conexion3.enviar(datos)

# ---

class Conexion(ABC):
    @abstractmethod
    def conectar(self) -> str:
        pass

class WebSocket(Conexion):
    def conectar(self) -> str:
        return "Conectando por WebSocket"

class REST(Conexion):
    def conectar(self) -> str:
        return "Conectando por REST"

class S3(Conexion):
    def conectar(self) -> str:
        return "Conectando por S3"

class Formato(ABC):
    @abstractmethod
    def serializar(self, dato: str) -> str:
        pass

class JSON(Formato):
    def serializar(self, dato: str) -> str:
        return f'{{"data": "{dato}"}}'

class HTTP(Formato):
    def serializar(self, dato: str) -> str:
        return f"HTTP/1.1\nBody: {dato}"

class Binario(Formato):
    def serializar(self, dato: str) -> str:
        return f"[BINARIO] {bin(ord(dato[0]))}"

class Transportador:
    def __init__(self, conexion: Conexion, formato: Formato) -> None:
        self.conexion = conexion
        self.formato = formato
    
    def enviar(self, dato: str) -> None:
        print(f"{self.conexion.conectar()}")
        print(f"Formato: {self.formato.serializar(dato)}\n")


print("WebSocket + JSON")
transportador1 = Transportador(WebSocket(), JSON())
transportador1.enviar("Hola")

print("REST + HTTP")
transportador2 = Transportador(REST(), HTTP())
transportador2.enviar("Datos")

print("S3 + Binario")
transportador3 = Transportador(S3(), Binario())
transportador3.enviar("A")

# ---

# Legacy

class LegacyImageLib:
    def load(self, path: str):
        self.width = len(path) + 1
        self.height = max(1, len(path) // 2)

class NewImageLib:
    class S3_picture:
        def __init__(self, name):
            self.name = name

        def get_info(self):
            return {"width": len(self.name) + 2, "height": 10}

    def query_image(self, name):
        return NewImageLib.S3_picture(name)

# Clase Adaptador
class ImageAdapter:
    def __init__(self, libreria_imagen):
        self.lib = libreria_imagen

    def load(self, name: str) -> dict[str, int]:
        if isinstance(self.lib, LegacyImageLib):
            data = self._load_legacy(name=name)
            return {"width": data[0], "height": data[1]}
        if isinstance(self.lib, NewImageLib):
            return self._load_new(name=name)

    def _load_legacy(self, *, name: str) -> tuple[int, int]:
        self.lib.load(name)
        return self.lib.width, self.lib.height

    def _load_new(self, *, name: str) -> dict[str, int]:
        image = self.lib.query_image(name)
        info = image.get_info()
        return info

if __name__ == "__main__":
    legacy = LegacyImageLib()
    new = NewImageLib()
 
    loader = ImageAdapter(new)
 
    img = loader.load("ejemplo.png")
    print(img, f"ancho - {img["width"]}", f"alto - {img["height"]}")

# ---

# Librería Legacy 
class LegacyImageLib:
    def load(self, path: str):
        self.width = len(path) + 1
        self.height = max(1, len(path) // 2)

# Librería New
class NewImageLib:
    class S3_picture:
        def __init__(self, name):
            self.name = name

        def get_info(self):
            return {"width": len(self.name) + 2, "height": 10}

    def query_image(self, name):
        return self.S3_picture(name)

# Clase Imagen (estructura común)
class Imagen:
    def __init__(self, width: int, height: int, path: str):
        self.width = width
        self.height = height
        self.path = path

# Adaptador 
class ImageAdapter:
    def __init__(self, lib):
        self.lib = lib

    def load(self, path: str) -> Imagen:
        if isinstance(self.lib, LegacyImageLib):
            self.lib.load(path)
            return Imagen(self.lib.width, self.lib.height, path)

        elif isinstance(self.lib, NewImageLib):
            picture = self.lib.query_image(path)
            info = picture.get_info()
            return Imagen(info["width"], info["height"], path)
        else:
            raise TypeError("Librería no compatible")


# *** Ejemplo de uso ***

if __name__ == "__main__":
    legacy = LegacyImageLib()
    new = NewImageLib()

    loader1 = ImageAdapter(legacy)
    img1 = loader1.load("foto_legacy.png")
    print(f"Legacy -> width: {img1.width}, height: {img1.height}, path: {img1.path}")

    loader2 = ImageAdapter(new)
    img2 = loader2.load("foto_new.png")
    print(f"New -> width: {img2.width}, height: {img2.height}, path: {img2.path}")

