class Scene:
    
    """Contiene toda la informacion necesaria de una escena, utilizada
        por el motor de renderizado para crear la imagen resultante. contiene:
            -camara
            -luces
            -objetos"""

    def __init__(self, camera, objects, lights):
        self.camera = camera
        self.objects = objects
        self.lights = lights
