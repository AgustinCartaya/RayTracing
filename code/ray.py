class Ray:
    """
    Clase que modela un rayo
    El rayo esta caracterizado por tener una posicion y una direccion
    """

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalize()
