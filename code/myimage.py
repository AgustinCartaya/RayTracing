from PIL import Image

class MyImage:

    """
    Clase encargada de crear la imagen resultante por el renderizado de la escena
    contiene todos los pixeles obtenidos por el motore de renderizado
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.internal_img = Image.new("RGB", (width,height))

    def set_pixel(self, x, y, px):
        """
        agrega un pixe en la posicion x,y de la matriz de pixeles de la imagen,
        el pixel debe de venir normalizado, este luego se pasara al rango 0-255

        Parameters:
            x = int, fila
            y = list, columna
            px = float,  pixel correspondiente a la posicion x,y de la matriz de la imagen (0 =<px =< 1, pueden haber excepciones)
        """
        def to_byte(c):
            return round(max(min(c * 255, 255), 0))

        self.internal_img.putpixel((x,y), ( to_byte( px.x), to_byte( px.y), to_byte( px.z)))

    def save_image(self, name = "test.png"):
        """
        crea la imagen de la matriz de pixeles y la guarda en el repertorio actual,

        Parameters:
            name: String, nombre y extension de la imagen example: "test.png"
        """
        self.internal_img.save(name)
