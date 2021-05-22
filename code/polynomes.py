import math
import random

def plus(a,b):

    """
    Hace la suma de dos polinomios
    sumando componente a componente

    Parameters:
        a = list, polinomio a
        b = list, polinomio b

    Return:
        c: list, resultante de la suma polinomial de a y b

    Example:
        a = [0,5,2,3]
        b = [2,4,3,5]
        c = a+b = [2,9,5,8]
    """
    res =[0 for i in range( max( len(a),len(b)))]
    for i in range( max( len(a),len(b)) ):
        if i >= len(a):
            res[i] = b[i]
        elif i >= len(b):
            res[i] = a[i]
        else:
            res[i] = a[i]+b[i]
    return res

def mult(a,b):
    """
    Hace la multiplicacion de dos polinomios

    Parameters:
        a = list, polinomio a
        b = list, polinomio b

    Return:
        c: list, resultante de la multiplicacion polinomial de a y b

    Example:
        a = [0,5,2,3]
        b = [2,4,3,5]

        c = a * b = [0,10,24,29,43,19,15]
    """
    res = [0 for i in range( len(a)+len(b)-1)]
    for i in range( len(a) ):
        for j in range( len(b) ):
            res[i+j] += a[i]*b[j]
    return res

def opp(a):
    """
    Devuelve el polinomio a multiplicafo por (-1)

    Parameters:
        a = list, polinomio a

    Return:
        c: list, resultante de la multiplicacion escalar de cada elemento de a por (-1)


    Example:
        a = [0,-5,2,3]

        c = a * (-1) = [0,5,-2,-3]
    """
    res = []
    for i in a:
        res.append( -i )
    return res

def coeff(a, i):
    """
    Devuelve el coefficiente i del polinimio a (si este existe)

    Parameters:
        a: lits, polinomio a
        i: int, posicion del coeficiente en el polinomio

    Return:
        c: float, coeficiente en la posicion i de p
        c: None, si el coeficiente no es encontrado

    Example:
        a = [0,-5,2,3]
        i = 2

        c = 2
    """
    if i>=0 and i<len(a):
        return a[i]
    return None

def evaluate(a, t):
    """
    Evalua una t danda en el polinomio a

    Parameters:
        a: lits, polinomio a
        t: float, valor de t en el polinomio

    Return:
        c: float, resultado de evaluar t en el polinomio

    Example:
        a = [0,-5,2,3]
        t = 2

        c = 0*t + (-5)*t + 2*t^2 + 3*t^3 = 22
    """

    res = 0
    for i in range( len(a) ):
        res = res + a[i] * (t**i)
    return res


def c(n,k):
    """
    Calcula el coeficiente binomial del conjunto n, en k

    Parameters:
        k: float, elementos a escojer en el conjunto
        n: float, conjunto de n elementos

    Return:
        c: int, cantidad de formas de escojer k elementos en n

    Example
        c(2,0) = 1
        c(2,1) = 2
        c(2,2) = 1

    """
    if n<k:
        return 0
    if n == k or k == 0:
        return 1
    if k == 1:
        return n
    return c(n-1, k-1)+c(n-1, k)



def casteljau(v):
    """
    Ejecuta el algoritmo de casteljeau

    Parameters:
        v: list, lista a descomponer

    Return:
        c: list, liasta que contiene 2 sublistas, resultado del algoritmo de casteljau

    Example
        v = [0,4,16]

        c = [[0,2,6],[6,10,16]]
    """
    res = [[],[]]

    def internal(v):
        res[0].append(v[0])
        res[1].append(v[-1])
        if len(v) == 1:
            return
        vn =[]
        for i in range(len(v)-1):
            vn.append(( v[i]+ v[i+1]) /2)

        internal(vn)

    internal(v)
    #invertir lista 1 antes de enviarla
    return [res[0], res[1][::-1]]


#desde aqui no entiendo
def tobernstein(a):
    """
    convierte un polinomio a de la base canonica a la base de berstein

    Parameters:
        a: list, polinomio en la base canonica

    Return:
        b: list, polinomio en la base de berstein

    Example
        a = [0,0,10]

        b = [0,0,10]
    """
    ret = [0 for x in range(len(a))]
    d = len(a) -1
    for k in range(len(a)):
        temp = []
        for i in range(len(a)):
            temp.append(a[k]* (c(i, k)/c(d, k)))
        ret = [ret[x]+temp[x] for x in range(len(ret))]
    return ret


def solve(epsilon, tab, t1, t2, sol):
    """
    Encuentra las raices del polinomio en la base de berstein
    """
    if 0 < min(tab) or 0>max(tab):
        return sol
    if t2-t1 < epsilon:
        return ((t1+t2)/2, None)
    tab1, tab2 = casteljau(tab)
    b1 = solve(epsilon, tab1, t1, (t1+t2)/2, sol)
    b2 = solve(epsilon, tab2, (t1+t2)/2, t2, sol)
    return cons(b1, b2)


def cons(c1, c2):
    if c1 == None:
        return c2
    if c2 == None:
        return c1
    (hd, qu) = c1
    return cons(qu, (hd, c2))

def mymap(func, lst):
    if lst == None:
        return None
    (hd, qu) = lst
    return (func(hd), mymap(func, qu))

def racines(p):
    p1 = p[::-1]
    p1 = tobernstein(p1)
    roots = solve(1e-8,p1, 0, 1, None)
    return  mymap((lambda x: 1./x), roots)


def hd( q ):
    if q is not None:
        m = []
        while True:
            m.append(q[0])
            q = q[1]
            if q is None:
                break
            if q[1] is None:
                m.append(q[0])
                break
        return min(m)
    return None

def interpole( x1, y1, x2, y2, x) :
    # x=x1 -> y=y1
    # x=x2 -> y=y2
    x1, y1, x2, y2, x= float(x1), float(y1), float( x2), float(y2), float(x)
    return (x-x2)/(x1-x2)*y1 + (x-x1)/(x2-x1)*y2

def normalize3(x):
    (a,b,c) = (x[0], x[1], x[2])
    (a,b,c)=(float(a),float(b),float(c))
    n=math.sqrt(a*a+b*b+c*c)
    if 0.==n:
        return (0.,0.,0.)
    else:
        return (a/n, b/n, c/n)
