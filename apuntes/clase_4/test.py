from apuntes import Bombilla, Ventilador, Circuito
from apuntes import AparatoEncendible
from apuntes import Paciente, Medico, Terapia

def test_circuito():
    ventilador = Ventilador()
    mi_circuito = Circuito(ventilador)

    assert mi_circuito.aparato.on_off is False

    mi_circuito.click()
    assert mi_circuito.aparato.on_off is True

    mi_circuito.click()
    assert mi_circuito.aparato.on_off is False

def test_cambio_aparato():
    ventilador = Ventilador()
    mi_circuito = Circuito(ventilador)
    mi_circuito.click()  # Encendemos
    assert mi_circuito.aparato.on_off is True
    bombilla = Bombilla()
    mi_circuito.aparato = bombilla
    mi_circuito.click()  # Encendemos
    assert mi_circuito.aparato.on_off is True

def test_cambio_nuevo_aparato():
    class MandoTele(AparatoEncendible):
        pass

    mando = MandoTele()
    mi_circuito = Circuito(mando)
    assert mi_circuito.aparato.on_off is False
    mi_circuito.click()
    assert mi_circuito.aparato.on_off is True

# Hay que completar un poco este test!

paciente = Paciente()
medico = Medico()
terapia = Terapia()

def test_paciente():
    assert paciente.nombre == "Juan"
