class Bombilla:
    def __init__(self):
        self.on_off = False  # Empieza apagada

class Circuito:
    def __init__(self):
        self.bombilla = Bombilla()

    def click(self):
        self.bombilla.on_off = False if self.bombilla.on_off else True
