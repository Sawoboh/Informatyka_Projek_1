# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 21:05:43 2023

@author: Sawob
"""
import numpy as np
from math import *
import argparse

class Transformacje:
    
    
    def __init__(self, model: str="WGS84"):
        if model == "WGS84":
            self.a = 6378137.000
            self.e2 = 0.00669437999013
        elif model == "GRS80":
            self.a = 6378137.000
            self.e2 = 0.00669438002290
        elif model == "Krasowski":
            self.a = 6378245.000
            self.e2 = 0.00669342162296
        else:
            raise NotImplementedError(f"{model}  jest nieobsługiwalną elipsoidą - przykładowe elipsoidy WGS84, GRS80, Krasowski.")


    def get_np(self, f):
        N = self.a / np.sqrt(1 - self.e2 * np.sin(f)**2)
        return(N)
    
    
    def hirvonen(self, X, Y, Z):
        p = np.sqrt(X**2 + Y**2)
        f = np.arctan(Z/(p * (1 - self.e2)))
        while True:
            N = Transformacje.get_np(self, f)
            h = (p / np.cos(f)) - N
            fp = f
            f = np.arctan(Z / (p * (1 - self.e2 * (N / (N+h)))))
            if np.abs(fp - f) < (0.000001/206265):
                break
        l = np.arctan2(Y, X)
        return(f,l,h)

    
    def flh2XYZ(self, f, l, h):
        N = Transformacje.get_np(self, f)
        X = (N + h) * np.cos(f) * np.cos(l)
        Y = (N + h) * np.cos(f) * np.sin(l)
        Z = (N * (1 - self.e2) + h) * np.sin(f)
        return(X,Y,Z)
    
    
    def get_dXYZ(xa, ya, za, xb, yb, zb):
        dXYZ = [xb-xa, yb-ya, zb-za]
        return(dXYZ)
    
    
    def rneu(f, l):
        R = np.array([[-np.sin(f)*np.cos(l), -np.sin(l), np.cos(f)*np.cos(l)],
                      [-np.sin(f)*np.sin(l),  np.cos(l), np.cos(f)*np.sin(l)],
                      [np.cos(f),             0,         np.sin(f)          ]])
        return(R)
    
    
    def xyz2neu(f, l, xa, ya, za, xb, yb, zb):
        dX = Transformacje.get_dXYZ(xa, ya, za, xb, yb, zb)
        R = Transformacje.rneu(f,l)
        return(R.T @ dX)
    
    
    def GK(self, f, l, l0):
        a2 = self.a**2
        b2 = a2 * (1 - self.e2)
        e_2 = (a2 - b2)/b2
        dl = l - l0
        dl2 = dl**2
        dl4 = dl**4
        t = tan(f)
        t2 = t**2
        t4 = t**4
        n2 = e_2 * (cos(f)**2)
        n4 = n2 ** 2
        N = Transformacje.Np(self, f)
        e4 = self.e2**2
        e6 = self.e2**3
        A0 = 1 - (self.e2/4) - ((3*e4)/64) - ((5*e6)/256)
        A2 = (3/8) * (self.e2 + e4/4 + (15*e6)/128)
        A4 = (15/256) * (e4 + (3*e6)/4)
        A6 = (35*e6)/3072
        sigma = self.a * ((A0 * f) - A2 * sin(2*f) + A4 * sin(4*f) - A6 * sin(6*f))
        xgk = sigma + ((dl**2)/2) * N * sin(f) * cos(f) * (1 + ((dl**2)/12)*(cos(f)**2)*(5 - t2 + 9 * n2 + 4 * n4) + (dl4/360) * (cos(f)**4)*(61 - (58 * t2) + t4 + (270 * n2) - (330 * n2 * t2)))
        ygk = dl * N * cos(f) * (1 + (dl2/6) * (cos(f)**2) * (1 - t2 + n2) + (dl4/120) * (cos(f)**4) * (5 - (18 * t2) + t4 + (14 * n2) - 58 * n2 * t2))
        return(xgk,ygk)
    
    
    def flh2PL92(self, f, l, h):
        
        if l > 25.5 and l < 13.5:
            raise NotImplementedError(f"{l} ten południk nie jest obsługiwany przez układ współrzędnych płaskich PL2000")
            
        if f > 55 and f < 48.9:
            raise NotImplementedError(f"{f} ten równoleżnik nie jest obsługiwany przez układ współrzędnych płaskich PL2000")
            
        f = np.radians(f)
        l = np.radians(l)
        a2 = self.a**2
        b2 = a2 * (1 - self.e2)
        e_2 = (a2 - b2)/b2
        l0 = np.radians(19)
        dl = l - l0
        dl2 = dl**2
        dl4 = dl**4
        t = np.tan(f)
        t2 = t**2
        t4 = t**4
        n2 = e_2 * (np.cos(f)**2)
        n4 = n2 ** 2
        N = Transformacje.get_np(self, f)
        e4 = self.e2**2
        e6 = self.e2**3
        A0 = 1 - (self.e2/4) - ((3*e4)/64) - ((5*e6)/256)
        A2 = (3/8) * (self.e2 + e4/4 + (15*e6)/128)
        A4 = (15/256) * (e4 + (3*e6)/4)
        A6 = (35*e6)/3072
        sigma = self.a * ((A0 * f) - A2 * np.sin(2*f) + A4 * np.sin(4*f) - A6 * np.sin(6*f))
        xgk = sigma + ((dl**2)/2) * N * np.sin(f) * np.cos(f) * (1 + ((dl**2)/12)*(np.cos(f)**2)*(5 - t2 + 9 * n2 + 4 * n4) + (dl4/360) * (np.cos(f)**4)*(61 - (58 * t2) + t4 + (270 * n2) - (330 * n2 * t2)))
        ygk = dl * N * np.cos(f) * (1 + (dl2/6) * (np.cos(f)**2) * (1 - t2 + n2) + (dl4/120) * (np.cos(f)**4) * (5 - (18 * t2) + t4 + (14 * n2) - 58 * n2 * t2))
        x92 = xgk * 0.9993 - 5300000
        y92 = ygk * 0.9993 + 500000
        return(x92,y92)
    
    
    def flh2PL00(self, f, l, h):
        
        if l >= 13.5 and l < 16.5:
            l0 = np.radians(15)
        elif l >= 16.5 and l < 19.5:
            l0 = np.radians(18)
        elif l >= 19.5 and l < 22.5:
            l0 = np.radians(21)
        elif l >= 22.5 and l <= 25.5:
            l0 = np.radians(24)
        else:
            raise NotImplementedError(f"{l} ten południk nie jest obsługiwany przez układ współrzędnych płaskich PL2000")
        
        if f > 55 and f < 48.9:
            raise NotImplementedError(f"{f} ten równoleżnik nie jest obsługiwany przez układ współrzędnych płaskich PL2000")
            
        f = radians(f)
        l = radians(l)
        a2 = self.a**2
        b2 = a2 * (1 - self.e2)
        e_2 = (a2 - b2)/b2
        dl = l - l0
        dl2 = dl**2
        dl4 = dl**4
        t = tan(f)
        t2 = t**2
        t4 = t**4
        n2 = e_2 * (cos(f)**2)
        n4 = n2 ** 2
        N = Transformacje.get_np(self, f)
        e4 = self.e2**2
        e6 = self.e2**3
        A0 = 1 - (self.e2/4) - ((3*e4)/64) - ((5*e6)/256)
        A2 = (3/8) * (self.e2 + e4/4 + (15*e6)/128)
        A4 = (15/256) * (e4 + (3*e6)/4)
        A6 = (35*e6)/3072
        sigma = self.a * ((A0 * f) - A2 * sin(2*f) + A4 * sin(4*f) - A6 * sin(6*f))
        xgk = sigma + ((dl**2)/2) * N * sin(f) * cos(f) * (1 + ((dl**2)/12)*(cos(f)**2)*(5 - t2 + 9 * n2 + 4 * n4) + (dl4/360) * (cos(f)**4)*(61 - (58 * t2) + t4 + (270 * n2) - (330 * n2 * t2)))
        ygk = dl * N * cos(f) * (1 + (dl2/6) * (cos(f)**2) * (1 - t2 + n2) + (dl4/120) * (cos(f)**4) * (5 - (18 * t2) + t4 + (14 * n2) - 58 * n2 * t2))
        strefa = round(l0 * 180/np.pi / 3)
        x00 = xgk * 0.999923
        y00 = ygk * 0.999923 + strefa * 1000000 + 500000
        return(x00,y00)
    
    
    def GK2PL92(xgk,ygk):
        x_92 = xgk * 0.9993 - 5300000
        y_92 = ygk * 0.9993 + 500000
        return(x_92, y_92)
    
    
    def GK2PL00(xgk,ygk,l0):
        strefa = int(l0 * 180/pi)/3
        x_00 = xgk * 0.999923
        y_00 = ygk * 0.999923 + strefa * 1000000 + 500000
        return(x_00, y_00)
    
    

    """
    def PoleProstokata(BokProstokata, PodstawaProstokata):
        Pole = BokProstokata * PodstawaProstokata
        return(Pole)
    
    def main():
        parser = argparse.ArgumentParser(description="Policz pole prostokąta")
        parser.add_argument("-h" "--BokProstokata", type=int, help="Podaj bok Prostokata")
        parser.add_argument("-r" "--PodstawaProstokata", type=int, help="Podaj podstawe Prostokata")
        args = parser.parse_args()
    """

    def wczytaniePliku(a):
        with open(a, "r") as plik:
            for i in plik:
                for e in i:
                    if "X" in e:
                        pass
    
    def zapisaniePliku(X, Y, Z, f, l, h, x92, y92, x00, y00, neu): 
        with open("Wyniki transformacji", "w") as plik:
            plik.write(f"Wyniki_obliczen_Geodezyjnych\n")
            plik.write("-"*50)
            plik.write(f"\n")
            plik.write(f"|   X    |    Y    |     Z     |     f     |     l     |     h     |   x1992   |   y1992   |   x2000   |   y2000   |    neu    |")
            plik.write(f"\n")
            plik.write("-"*50)
            plik.write(f"\n")
            plik.write(f"|   {X}    |    {Y}    |     {Z}     |     {f}     |     {l}     |     {h}     |   {x92}   |   {y92}   |   {x00}   |   {y00}   |    {neu}    |")


if __name__ == "__main__":
   
    model = Transformacje("GRS80")
    
    
    x,y,z = Transformacje.hirvonen(model,300,200,100)
    print(x)
    
    
    f,l,h = Transformacje.flh2XYZ(model,1,1,1)
    print("Dane w flh2XYZ:",f,l,h)
    
    
    fsto = 53+11/60+59.79018/3600; lsto = 16+41/60+50.52003/3600
    x92, y92 = Transformacje.flh2PL92(model,fsto,lsto,1)
    print("Dane w PL92:",strefa ,x92, y92)
    
    
    fsto = 53+11/60+59.79018/3600; lsto = 16+41/60+50.52003/3600
    x00, y00 = Transformacje.flh2PL00(model,fsto,lsto,1)
    print("Dane w PL20:",strefa ,x00, y00)
    
    
    fa = radians(10); la = radians(12); Xa = 100; Ya = 200; Za = 500; Xb = 300; Yb = 400; Zb = 500
    neu = Transformacje.xyz2neu(fa,la, Xa, Ya, Za, Xb, Yb, Zb)
    print(neu)

    print(Transformacje.zapisaniePliku(x,y,z,f,l,h,x92,y92,x00,y00,neu))

"""
    def PoleProstokata(BokProstokata, PodstawaProstokata):
        Pole = BokProstokata * PodstawaProstokata
        return(Pole)
    
    #def main():
    parser = argparse.ArgumentParser(description="Policz pole prostokąta")
    parser.add_argument("-w", type=int, help="Podaj bok Prostokata")
    parser.add_argument("-r", type=int, help="Podaj podstawe Prostokata")
    args = parser.parse_args()
    
    #P = PoleProstokata(4, 5)
    #print(P)
    # print(main(), P)
    print(PoleProstokata(args.BokProstokata, args.PodstawaProstokata))


    print(PoleProstokata(args.BokProstokata, args.PodstawaProstokata))

    
    a_GRS80 = 6378137.000
    e2_GRS80 = 0.00669438002290


    a_kras = 6378245.000
    e2_kras = 0.00669342162296


    a_WGS84 = 6378137.000
    e2_WGS84 = 0.00669437999013
"""