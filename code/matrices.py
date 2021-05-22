#!/usr/bin/env python
import math
import random

class MatrixError(Exception):
    def __init__(self, message = "Matrix error"):
        self.message = message

class Matrix:

    def __init__(self, ilist = [[]], row = 2, col = 2,  fill = 0, rdm = False, min_value = 0, max_value = 10):
        if ilist == [[]]:
            self.ilist = [ [ fill if rdm == False else random.randint(min_value,max_value) for i in range(col)] for i in range(row)]
        elif Matrix.valid_matrix(ilist):
            self.ilist = ilist

    def row_num(self):
        return len(self.ilist)

    def col_num(self):
        return len(self.ilist[0])

    def row (self, n):
        if n < 0 or n > self.row_num():
            return None
        return self.ilist[n]

    def col (self, n):
        if n < 0 or n > self.col_num():
            return None
        _t = []
        for i in range(self.col_num()):
            _t.append([ self.ilist[i][n]])
        return _t

    def get(self, r, c):
        # print("r: ", r, " c: ", c)
        return self.ilist[r][c]

    def minsq(self):
        return min(  self.row_num(),  self.col_num())

    def multiple(self, alph):
        res = []
        for i in range ( self.row_num() ):
            res.append([])
            for j in range ( self.row_num() ):
                res[i].append( self.get(i,j) * alph )
        return Matrix(res)

    def sum(self, m):
        if m.row_num() != self.row_num() or m.col_num() != self.col_num():
            return None
        res = []
        for i in range(0, self.row_num()):
            res.append([])
            for j in range(0, self.col_num() ):
                res[i].append( self.get(i,j) + m.get(i,j))
        return Matrix(res)

    def mult(self, m):

        if self.col_num()  != m.row_num():
            return None
        res = [ [ 0 for i in range( m.col_num() ) ]  for i in range( self.row_num() ) ]
        temp = 0
        for i in range( self.row_num() ):
            for j in range( m.col_num() ):
                for k in range( m.row_num() ):
                    # print("i: ", i, " k: ", k, " j: ", j)
                    temp = temp + self.get(i,k) * m.get(k,j)
                res[i][j] = temp
                temp = 0
        return Matrix(res)


    def T (self):
        res = [[0 for i in range( self.row_num() )]for i in range( self.col_num() )]
        minPiv = self.minsq()

        for i in range( minPiv ):
            for j in range(i, self.col_num() ):
                res[j][i] = self.get(i,j)
            for j in range(i+1, self.row_num() ):
                res[i][j] = self.get(j,i)

        return ( Matrix(res) )

    @staticmethod
    def valid_matrix( m ):
        if not isinstance(m, list):
            raise MatrixError("parametter is not a list")
            return False

        if not isinstance(m[0], list):
            raise MatrixError("parametter is a vector")
            return False

        col0 = len(m[0])
        for i in range ( 1, len(m) ):
            if col0 != len(m[i]):
                raise MatrixError("list has no the same col numbers")
                return False

        return True

# a = [[1,2,3],[0,1,2],[3,2,1]]
# b = [[1],[2],[3]]
# a = Matrix(a)
# b = Matrix(b)
# c = a.mult(b)
# #
# print(c.ilist)

#print(transMatx( a))
