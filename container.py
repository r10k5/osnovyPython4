import numpy
from scipy import optimize


class Container:
    def __init__(self, material, emkost, koeffC):
        self.material = material
        self.emkost = emkost
        self.koeffC = koeffC


class ContainerCircleSquare(Container):
    def __init__(self, material, emkost, koeffC):
        super().__init__(material, emkost, koeffC)
        self.__Ropt = 0
        self.__Hopt = 0
        self.__FFmin = 0
        self.__ropt = 0

    @property
    def R(self):
        return self.__Ropt

    @property
    def H(self):
        return self.__Hopt

    @property
    def F(self):
        return self.__FFmin

    @property
    def r(self):
        return self.__ropt

    def __str__(self):
        return f'{self.material}(V={self.emkost}, c={self.koeffC}, R={self.__Ropt}, H={self.__Hopt}, F={self.__FFmin}, r={self.__ropt})'

    def __fradius_outer(self, h):
        return numpy.sqrt(self.emkost / (numpy.pi * h))

    def __fsurface(self, h):
        R = self.__fradius_outer(h)
        r = self.koeffC * R
        a2 = r / numpy.sqrt(2)

        return 2 * ((numpy.pi * R ** 2) - a2) + 2 * numpy.pi * R * h + 4 * a2

    def __tabulation(self, hn, h0, hk, n):
        h_step = (hk - hn) / n
        h = h0
        while h < hk:
            yield h, self.__fsurface(h)
            h += h_step

    def optimizaciya(self):
        h0 = self.emkost ** (1 / 3)
        hn = h0 / 3
        hk = 2 * h0
        self.__Hopt = optimize.fmin(self.__fsurface, h0)[0]
        self.__Ropt = self.__fradius_outer(self.__Hopt)
        self.__ropt = self.koeffC * self.__Ropt
        self.__FFmin = self.__fsurface(self.__Hopt)

        H_list = []
        F_H = []

        for (H, F) in self.__tabulation(hn, h0, hk, 50):
            H_list.append(H)
            F_H.append(F)

        return H_list, F_H

