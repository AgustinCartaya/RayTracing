#!/usr/bin/env python
"""Projet Info3A RayTracing By Agustin CARTAYA """
import argparse
import importlib
import os

from engine import RenderEngine
from scene import Scene

from color import Color
from light import Light
from material import *
from point import Point
from objects import *
from vector import Vector
from camera import Camera



co=Point(0,-1,0)
look_at = Point(0,0,0)
aspect_ratio = 1
c_type = -1

droite=  Vector(1.,0.,0.)
regard=  Vector(0.,1.,0.)
vertical= Vector(0.,0.,1.)



"""
Aqui colocamos las caracteristicas de la scena
-estrictemanete necesario
    -Una camara
    -nombre de la imagen que sera guardada
    -dimensiones de la imagen
-opcional
    -luces
    -objetos
"""
WIDTH = 200
HEIGHT = 200
RENDER_IMG = "Example0-1.png"
# CAMERA = Camera( Point(0, 6, 0), Vector(0, -1, 0), WIDTH, HEIGHT, 0, 10 )
#CAMERA = Camera( Point(1,1,1), Vector(0,0,0), WIDTH, HEIGHT, 0, 2 )
CAMERA=Camera( Point(0,-1,0), Point(0,0,0), (WIDTH, HEIGHT), 2, 2)

OBJECTS = [
    # Plane(Point(0,-25,0), Vector(0,1,0), ChequeredMaterial( reflection=0)),
    Sphere(Point(0,0,0),1,  Material( Color.from_hex("#00FFFF"), reflection=0 ) ),
    Sphere(Point(0, -.2, 0), 1,  ChequeredMaterial() )

]

LIGHTS = [


     Light(Point(1.5,-.5,-10), Color.from_hex("#FFFFFF")),
    Light(Point(-0.5,-10.5,-10), Color.from_hex("#E6E6E6")),
    Light(Point(1.5,-.5,10), Color.from_hex("#FFFFFF")),
    Light(Point(-0.5,10.5,10), Color.from_hex("#E6E6E6"))

]




""" Fin de las caracteristicas de la escena """


def main():
    """
    Metodo inicial del projecto:
        inicializacion de la escena, del motor de renderizado y de la imagen a renderizar
    """

    scene = Scene(CAMERA, OBJECTS, LIGHTS)
    engine = RenderEngine()
    image = engine.render(scene)
    image.save_image( RENDER_IMG )


if __name__ == "__main__":
    main()
