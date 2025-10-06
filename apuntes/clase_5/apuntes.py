from dataclasses import field, asdict, astuple, dataclass, replace, make_dataclass

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
