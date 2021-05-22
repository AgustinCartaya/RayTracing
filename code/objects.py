from dags import *
import polynomes
from math import sqrt

from color import Color
from material import *
from point import Point
from vector import Vector

class Obj(object):
    """Clase padre de todos los objetos que se pueden mostrar en la scena"""
    def __init__( self):
        " "


class Prim(Obj):
    """
    Clase padre de todos los objetos primitivos
    defindos por funciones matematicas conocidas
    """

    def __init__( self, fonc_xyz, material):
        self.fonc=fonc_xyz
        self.material = material

    def intersects( self, rayon):
        """
        devuelve el/los punto(s) de intercepcion del objeto con el rayo
        calculando las raices del rayo (linea en R3) y el objeto en si
        (cuerpo 3D representado pr una formula matematica en X,Y,Z)
        aun tengo dudas de como se calculan las raices!!!

        Parameters
            rayon: Vector, rayo a interceptar el objeto

        Return
            link: linked-list, devuelve las raices de la intercepcion

        Example (3,(2,(1,None)))

        """

        dico = { "x": Nb(rayon.origin.x) + Nb(rayon.direction.x)*Var("t"),
        "y": Nb(rayon.origin.y) + Nb(rayon.direction.y)*Var("t"),
        "z": Nb(rayon.origin.z) + Nb(rayon.direction.z)*Var("t")}
        expression_en_t=self.fonc.evalsymb( dico )
        pol_t = expression_en_t.topolent()
        return racines( pol_t)

    def normal( self, P):
        """
        Devuelve el vector normal del objeto en el punto P
        calculado a partir de las derivadas parciales

        Parameters
            P: Point, punto dode se va a calcular el vector normal en el objeto

        Return
            N: Vector, vector normal en el punto p del objeto

        """
        fx=self.fonc.derivee("x")
        fy=self.fonc.derivee("y")
        fz=self.fonc.derivee("z")
        dico={"x":P.x , "y": P.y , "z":P.z}
        (a,b,c)= ( fx.eval( dico), fy.eval( dico), fz.eval( dico))
        normal = Vector(a,b,c).normalize()
        return normal

class Sphere(Prim):

    """
    Modela una esfera creada a partir de su centro y su radio cuya ecuacion es la siguiente
    E = X^2 + Y^2 + Z^2 = r^2


    """

    def __init__( self, origin, r, material):
        Prim.__init__( self, Sphere.ecuation([origin,r]), material)
        self.origin = origin
        self.r = r

    @staticmethod
    def ecuation(args):
        (cx,cy,cz,r) = (args[0].x,args[0].y,args[0].z, args[1])
        x=Var("x")
        y=Var("y")
        z=Var("z")
        return (x-Nb(cx))*(x-Nb(cx)) + (y-Nb(cy))*(y-Nb(cy)) + (z-Nb(cz))*(z-Nb(cz)) - Nb(r*r)

    def intersects(self, ray):
        """
        sobre escritura del metodo intersects de la clase padre, para optimizar el tiempo
        de renderizado de este tipo de objetos.
        utiliza la ecuacion simplificada de la intercepcion de la esphera y el rayo.
        devuelve el primer punto interceptado por el rayo (aquel punto que es el mas cercano a la camara).

        Parameters
            rayon: Vector, rayo a interceptar el objeto

        Return
            link: linked-list, devuelve las raices de la intercepcion

        """

        sphere_to_ray = ray.origin - self.origin
        # a = 1
        b = 2 * ray.direction.dot_product(sphere_to_ray)
        c = sphere_to_ray.dot_product(sphere_to_ray) - self.r * self.r
        discriminant = b * b - 4 * c

        if discriminant >= 0:
            dist = (-b - sqrt(discriminant)) / 2
            if dist > 0:

                return (dist,None)
        return None

    def normal(self, P):
        """
        sobre escritura del metodo normal de la clase padre
        ya que el vector normal de un punto p en una esfera s
        tiene la misma direccio y sentido al vector que va desde el origen de la esfera
        hasta el punto p

        Parameters
            P: Point, punto dode se va a calcular el vector normal en el objeto

        Return
            N: Vector, vector normal en el punto p del objeto

        """


        return (P - self.origin).normalize()

class Plane(Prim):

    def __init__( self, origin, n, material):
        Prim.__init__( self, Plane.ecuation([origin,n]), material)
        self.origin = origin
        self.n = n.normalize()

    @staticmethod
    def ecuation(args):
        (ox,oy,oz) = (args[0].x,args[0].y,args[0].z)
        (nx,ny,nz) = (args[1].x,args[1].y,args[1].z)
        x=Var("x")
        y=Var("y")
        z=Var("z")
        return ( Nb(nx) * (x-Nb(ox))+  Nb(ny)*(y-Nb(oy)) +  Nb(nz)*(z-Nb(oz)) )

    def intersects(self, ray):

        down = self.n.x * ray.direction.x  + self.n.y * ray.direction.y + self.n.z *ray.direction.z
        if( down == 0):
            return (None)
        up = self.n.x * ( self.origin.x - ray.origin.x) + self.n.y * ( self.origin.y - ray.origin.y) + self.n.z * ( self.origin.z - ray.origin.z)
        return  (up/down,None)

    def normal(self, P):
        return self.n



class Tore(Prim):

    def __init__( self,  r, R, material):
        Prim.__init__( self, Tore.ecuation([r,R]), material)
        self.r = r
        self.R = R

    @staticmethod
    def ecuation(args):
        (r, R) = (args[0],args[1])
        x=Var("x")
        y=Var("y")
        z=Var("z")
        tmp=x*x+y*y+z*z+Nb(R*R-r*r)
        return tmp*tmp- Nb(4.*R*R)*(x*x+z*z)

class Steiner2(Prim):

    def __init__( self, material):
        Prim.__init__( self, Steiner2.ecuation(None), material)

    @staticmethod
    def ecuation(args):
        x=Var("x")
        y=Var("y")
        z=Var("z")
        return (x * x * y * y - x * x * z * z + y * y * z * z - x * y * z)

class Steiner4(Prim):

    def __init__( self, material):
        Prim.__init__( self, Steiner4.ecuation(None), material)

    @staticmethod
    def ecuation(args):
        x=Var("x")
        y=Var("y")
        z=Var("z")
        return y * y - Nb( 2.) * x * y * y - x * z * z + x * x * y * y + x * x * z * z - z * z * z * z

class Hyperboloide_2nappes(Prim):

    def __init__( self, material):
        Prim.__init__( self, Hyperboloide_2nappes.ecuation(None), material)

    @staticmethod
    def ecuation(args):
        x=Var("x")
        y=Var("y")
        z=Var("z")
        return Nb(0.) - (z * z - (x * x + y * y + Nb(0.1)))




class Hyperboloide_1nappe(Prim):

    def __init__( self, material):
        Prim.__init__( self, Hyperboloide_1nappe.ecuation(None), material)

    @staticmethod
    def ecuation(args):
        x=Var("x")
        y=Var("y")
        z=Var("z")
        return Nb(0.) - (z * z - (x * x + y * y - Nb(0.1)))




class Roman(Prim):

    def __init__( self, material):
        Prim.__init__( self, Roman.ecuation(None), material)

    @staticmethod
    def ecuation(args):
        x=Var("x")
        y=Var("y")
        z=Var("z")
        return ( x * x * y * y + x * x * z * z + y * y * z * z - Nb(2.) * x * y * z)
