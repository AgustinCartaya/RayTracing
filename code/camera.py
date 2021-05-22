from ray import Ray
from polynomes import interpole
from vector import Vector
from matrices import *
from point import Point
from color import Color


class Camera( object):
    """
    Camara encargada de lanzar los rayos para la creacion de la imagen
    """
    def __init__( self, o, look_at, size, aspr = 1, ctype = -1, background = Color(20,20,20), ox = Point(1,0,0), oy = Point(0,1,0) , oz = Point(0,0,1), hsizeworld = 5, soleil = Point(1,1,1)  ):
        """
        o: Point, posicion de la camara
        dir: Vector, look_at de la Camara
        width: int, amplitud horizontal de la Camara
        height: int, amplitud vertical de la camara
        ctype: int, tipo de camara (aun no implementado)
        aspr: float, acpect ratio Horizontal de la imagen

        """

        #cosas basicas
        self.o=o
        self.look_at = look_at
        self.dir = (look_at - o ).normalize()
        self.width = size[0]
        self.height = size[1]
        self.ctype = ctype
        self.background=background;

        #creacion de la pantaya y su tamno
        self.aspect_ratio = float(self.width) / self.height
        self.x0 = -aspr;
        self.x1 = aspr
        self.xstep = (self.x1 - self.x0) / (self.width - 1)
        self.y0 = -aspr / self.aspect_ratio
        self.y1 = aspr / self.aspect_ratio
        self.ystep = (self.y1 - self.y0) / (self.height - 1)
        print(self.y1)

        #camara del profesor
        self.ox= ox #vers la droite du spectateur
        self.oy= oy #regard du spectateur
        self.oz= oz #vertical du spectateur
        self.hsizeworld=hsizeworld
        self.hsizewin=size[0]
        self.soleil = soleil.normalize()


        #para la camara matricial
        if( self.dir.x == 0 ):
            self.teta = math.pi / 2
        else:
            self.teta = math.atan( self.dir.y / self.dir.x)

        if( self.dir.z == 0):
            self.rho = math.pi / 2
        else:
            self.rho = math.atan( math.sqrt(self.dir.y**2 + self.dir.x**2 )/ self.dir.z)


        self.mry = Matrix(  [  [ math.cos(self.teta), 0,math.sin(self.teta)],
                             [0,1,0],
                             [ -math.sin(self.teta), 0, math.cos(self.teta) ]
                           ])

        self.mrz = Matrix( [ [ math.cos(self.teta), -math.sin(self.teta), 0 ],
                             [ math.sin(self.teta), math.cos(self.teta), 0 ],
                             [0,0,1]
                             ])



        self.mr = self.mry.mult(self.mrz)



    def generate_ray( self, i, j):

        if self.ctype == 0:

            x = self.x0 + i* self.xstep
            y = self.y0 + j * self.ystep

            if  self.dir.z  == 0:
                z = 0
            else:
                z = self.dir.dot_product( self.o) - self.dir.x * x - self.dir.y * y
                z = z/ self.dir.z
            px = Point(x, y, z)
            # print(px)
            return Ray( self.o -px , self.dir)

        if self.ctype == 1:
            kx = interpole( 0., 0., self.hsizewin, self.hsizeworld, float(i))
            kz = interpole( 0., 0., self.hsizewin, self.hsizeworld, float(j))
            return Ray( Point(self.o.x + kx*self.ox.x + kz*self.oz.x,
            self.o.y + kx*self.ox.y + kz*self.oz.y,
            self.o.z + kx*self.ox.z + kz*self.oz.z),
            self.oy)

        if self.ctype == 2:
            x = 0
            y = self.x0 + j * self.xstep
            z = self.y0 + i * self.ystep
            P0 = Matrix( [[x], [y], [z]] )

            P1 = self.mr.mult(P0)

            prot = Point( P1.get(0,0), P1.get(1,0), P1.get(2,0))
            prot += self.o
            # print( prot.x, ", ", prot.y, ", ",prot.z )
            # print( self.dir.x, ", ", self.dir.y, ", ",self.dir.z )
            return Ray( prot , self.dir )

        if self.ctype == 3:
            x = self.x0 + i * self.xstep
            y = self.y0 + j * self.ystep
            desp = Vector(x, 0, y)
            return Ray( self.o - desp , self.look_at )

        x = self.x0 + i * self.xstep
        y = self.y0 + j * self.ystep
        return Ray(  self.dir  ,  Vector(x,y) - self.dir  )
