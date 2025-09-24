import pytest

class Fruit:
    def __init__(self, name):
        self.name = name
        self.cubed = False

    def cube(self):
        self.cubed = True

class FruitSalad:
    def __init__(self, *fruit_bowl):
        self.fruit = fruit_bowl
        self._cube_fruit()

    def _cube_fruit(self):
        for fruit in self.fruit:
            fruit.cube()

# Arrange
@pytest.fixture
def fruit_bowl():
    lista_frutas = [Fruit("apple"), Fruit("banana")]  # Creamos unas frutas para la ensalada
    yield lista_frutas  # setUp
    del lista_frutas  # tearDown

def test_fruit_salad(fruit_bowl):
    # Act
    fruit_salad = FruitSalad(*fruit_bowl)  # Usamos esas frutas para crear una ensalada

    # Assert
    assert all(fruit.cubed for fruit in fruit_salad.fruit)  # Testeamos la ensalada (si tiene las frutas o no)