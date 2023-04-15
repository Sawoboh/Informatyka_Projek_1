# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 21:05:43 2023

@author: Sawob
"""
import numpy as np
from math import *
import argparse


def Np(f,a,e2):
    N = a / np.sqrt(1 - e2*np.sin(f)**2)
    return(N)


def hirvonen(X,Y,Z,a,e2):
    p = np.sqrt(X**2 + Y**2)
    f = np.arctan(Z/(p * (1 - e2)))
    while True:
        N = Np(f,a,e2)
        h = (p / np.cos(f)) - N
        fp = f
        f = np.arctan(Z / (p * (1 - e2 * (N / (N+h)))))
        if np.abs(fp - f) < (0.000001/206265):
            break
    l = np.arctan2(Y,X)
    return(f,l,h)


def flh2XYZ(f,l,h,a,e2):
    N = Np(f,a,e2)
    X = (N + h) * np.cos(f) * np.cos(l)
    Y = (N + h) * np.cos(f) * np.sin(l)
    Z = (N * (1 - e2) + h) * np.sin(f)
    return(X,Y,Z)


def get_dXYZ(xa, ya, za, xb, yb, zb):
    dXYZ = [xb-xa, yb-ya, zb-za]
    return(dXYZ)


def Rneu(f, l):
    R = np.array([[-np.sin(f)*np.cos(l), -np.sin(l), np.cos(f)*np.cos(l)],
                  [-np.sin(f)*np.sin(l),  np.cos(l), np.cos(f)*np.sin(l)],
                  [np.cos(f),             0,         np.sin(f)          ]])
    return(R)


def XYZ2neu(dX, f, l):
    R = Rneu(f,l)
    return(R.T @ dX)


def GK(f,l,l0,a,e2):
    a2 = a**2
    b2 = a2 * (1 - e2)
    e_2 = (a2 - b2)/b2
    dl = l - l0
    dl2 = dl**2
    dl4 = dl**4
    t = tan(f)
    t2 = t**2
    t4 = t**4
    n2 = e_2 * (cos(f)**2)
    n4 = n2 ** 2
    N = Np(f,a,e2)
    e4 = e2**2
    e6 = e2**3
    A0 = 1 - (e2/4) - ((3*e4)/64) - ((5*e6)/256)
    A2 = (3/8) * (e2 + e4/4 + (15*e6)/128)
    A4 = (15/256) * (e4 + (3*e6)/4)
    A6 = (35*e6)/3072
    sigma = a * ((A0 * f) - A2 * sin(2*f) + A4 * sin(4*f) - A6 * sin(6*f))
    xgk = sigma + ((dl**2)/2) * N * sin(f) * cos(f) * (1 + ((dl**2)/12)*(cos(f)**2)*(5 - t2 + 9 * n2 + 4 * n4) + (dl4/360) * (cos(f)**4)*(61 - (58 * t2) + t4 + (270 * n2) - (330 * n2 * t2)))
    ygk = dl * N * cos(f) * (1 + (dl2/6) * (cos(f)**2) * (1 - t2 + n2) + (dl4/120) * (cos(f)**4) * (5 - (18 * t2) + t4 + (14 * n2) - 58 * n2 * t2))
    return(xgk,ygk)


def GK2PL92(xgk,ygk):
    x_92 = xgk * 0.9993 - 5300000
    y_92 = ygk * 0.9993 + 500000
    return(x_92, y_92)


def GK2PL00(xgk,ygk,l0):
    strefa = int(l0 * 180/pi)/3
    x_00 = xgk * 0.999923
    y_00 = ygk * 0.999923 + strefa * 1000000 + 500000
    return(x_00, y_00)


def PoleProstokata(BokProstokata, PodstawaProstokata):
    Pole = BokProstokata * PodstawaProstokata
    return(Pole)


parser = argparse.ArgumentParser(description="Policz pole prostokąta")
parser.add_argument("-h" "--BokProstokata", type=int, help="Podaj bok Prostokata")
parser.add_argument("-r" "--PodstawaProstokata", type=int, help="Podaj podstawe Prostokata")
args = parser.parse_args()

#args: NameSpace = parser.parse_args()

if __name__ == "__main__":
    print(PoleProstokata(args.BokProstokata, args.PodstawaProstokata))

    
    a_GRS80 = 6378137.000
    e2_GRS80 = 0.00669438002290


    a_kras = 6378245.000
    e2_kras = 0.00669342162296


    a_WGS84 = 6378137.000
    e2_WGS84 = 0.00669437999013