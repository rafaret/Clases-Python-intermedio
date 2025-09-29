from abc import ABC

class AparatoEncendible(ABC):
    def __init__(self):
        self.on_off = False

class Bombilla(AparatoEncendible):
    pass

class Ventilador(AparatoEncendible):
    pass

class Circuito:
    def __init__(self, aparato: AparatoEncendible):
        self.aparato = aparato  # Bombilla, ventilador, lavadora

    def click(self):
        self.aparato.on_off = not self.aparato.on_off

# Ejercicio
# Pacientes y Medicos que les administran Terapias

class Paciente:
    pass

class Medico:
    pass # Interactua con Pacientes!

class Terapia:
    pass  # Medicina farmacologica, medicina fisica, mediciona tradicional, etc...