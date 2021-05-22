from vector import Vector


class Color(Vector):
    """
    Clase que modela una triada de colores de forma RGB
    Example: <80, 30, 240>
            R = 80
            G = 30
            B = 240
    """

    @classmethod
    def from_hex(cls, hexcolor="#000000"):
        """
        Metodo de clase que convierte un color en formato WEB a RGB

        Parameters:
            hexcolor: String, color en formato WEB, example: #32CCCC

        Return:
            col: Color, color en formato RGB <R,G,B>
        """
        x = int(hexcolor[1:3], 16) / 255.0
        y = int(hexcolor[3:5], 16) / 255.0
        z = int(hexcolor[5:7], 16) / 255.0
        return cls(x, y, z)
