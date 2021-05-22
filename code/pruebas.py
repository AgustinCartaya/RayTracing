#!/usr/bin/env python
from polynomes import *
c0 = [-5,1]
c1 = [-1,1]
c2 = [-2,1]
c3 = [-3,1]
c4 = [-4,1]
c5 = [3,1]

# b = mult(mult( mult(mult(c1,c2),c3), c4),c0)
b = mult(c3,c5)
print(b)
c = racines(b)
print(c)
