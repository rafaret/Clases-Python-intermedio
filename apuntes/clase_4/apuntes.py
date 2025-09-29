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

