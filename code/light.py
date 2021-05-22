from color import Color


class Light:
    """
    Clase que modela un punto de luz, en una posicion dada y con un color dado
    """

    def __init__(self, position, color=Color.from_hex("#FFFFFF")):
        self.position = position
        self.color = color
