from apuntes import Bombilla, Circuito

mi_circuito = Circuito()

def test_circuito():
    # Bombilla empieza apagada
    assert mi_circuito.bombilla.on_off is False
    # Encendemos bombilla
    mi_circuito.encender()
    assert mi_circuito.bombilla.on_off is True
    # Apagamos bombilla
    mi_circuito.apagar()
    assert mi_circuito.bombilla.on_off is False
