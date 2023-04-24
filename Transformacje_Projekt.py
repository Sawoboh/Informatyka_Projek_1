# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 11:56:02 2023

@author: Sawob
"""

import numpy as np
import argparse
from math import radians


class Transformacje:
    
    
    def __init__(self, model: str="WGS84"):
        """
        Parametry elipsoid:
            a - duża półoś elipsoidy - promień równikowy
            e2 - mimośród^2 - ((promień równikowy^2+promień południkowy ^2)/promień równikowy^2)
        + WGS84: https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84
        + Inne powierzchnie odniesienia: https://en.wikibooks.org/wiki/PROJ.4#Spheroid
        """
        
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

    def dms(self, x):
        '''
        Funkcja dms służy do zamienienia wizualnego FLOAT (radiany) na stopnie minuty i sekundy.   

        Parametry
        ----------
        x : FLOAT
            [radiany].

        Returns
        x : str
            [dms] - stopnie, minuty, sekundy
        '''
        sig = ' '
        if x < 0:
            sig = '-'
            x = abs(x)
        x = x * 180/np.pi
        d = int(x)
        m = int(60 * (x - d))
        s = (x - d - m/60)*3600
        if m<10:
            m=str(m)
            m="0"+m
        if s<10:
            s=("%.5f"%s)
            s=str(s)
            s="0"+s
        else:
            s = ("%.5f"%s)
        x1=(f'{d}°{m}′{s}″')  
        return(x1)
        
        
    def get_np(self, f):
        '''
        funkcja liczy promień przekroju w pierwszym wertykale, który potrzebny jest nam do algorymu hirvonena,
        funkcji: flh2XYZ, flh2PL92, flh2PL00
        
        
        Parameters
        ----------
        f : FLOAT
            [radiany] - szerokość geodezyjna

        Returns
        -------
        N : float
            [metry] - promień przekroju w pierwszym wertykale

        '''
        N = self.a / np.sqrt(1 - self.e2 * np.sin(f)**2)
        return(N)
    
    
    def hirvonen(self, X, Y, Z, output="dec_degree"):
        '''
        Algorytm Hirvonena – algorytm służący do transformacji współrzędnych ortokartezjańskich 
        (prostokątnych) x, y, z na współrzędne geodezyjne fi, Lambda, h. Jest to proces iteracyjny. 
        W wyniku kilkukrotnego powtarzania procedury można przeliczyć współrzędne na poziomie dokładności 1 mm.

         Parametry
         ----------
         X, Y, Z : FLOAT
              współrzędne w układzie orto-kartezjańskim, 

         Returns
         -------
         fi : FLOAT
             [stopnie dziesiętne] - szerokość geodezyjna.
         lam : FLOAT
             [stopnie dziesiętne] - długośc geodezyjna.
         h : FLOAT
             [metry] - wysokość elipsoidalna
         output [STR] - opcjonalne, domylne 
             dec_degree - stopnie dziesiętne
             dms - stopnie, minuty, sekundy
             radiany - radiany 
         """
        '''

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
        if output == "dec_degree":
            fi=(f*180/np.pi)
            lam=(l*180/np.pi)
            return (fi, lam, h)
        elif output == "dms":
            fi = Transformacje.dms(self, f)
            lam = Transformacje.dms(self, l)
            return (fi,lam,h) 
        elif output == 'radiany':
            fi=f
            lam=l
            return(f,l,h)
        else:
            raise NotImplementedError(f"{output} - output format not defined")

    
    
    def flh2XYZ(self, f, l, h):
        '''
        Algorytm odwrotny do algorytmu Hirvonena - służy do transformacji współrzędnych geodezyjnych B, L, H 
        na współRzędne ortokartezjańskie x, y, z.

        Parametry
        ----------
        f : FLOAT
            [stopnie dziesiętne] - szerokość geodezyjna.
        l : FLOAT
            [stopnie dziesiętne] - długośc geodezyjna.
        h : FLOAT
            [metry] - wysokość elipsoidalna
        Returns
        -------
         X, Y, Z : FLOAT
              [metry] - współrzędne w układzie orto-kartezjańskim

        '''
        f=radians(f)
        l=radians(l)
        N = Transformacje.get_np(self, f)
        X = (N + h) * np.cos(f) * np.cos(l)
        Y = (N + h) * np.cos(f) * np.sin(l)
        Z = (N * (1 - self.e2) + h) * np.sin(f)
        return(X,Y,Z)
    
    
    def flh2PL92(self, f, l):
        '''
        Układ współrzędnych 1992 (Państwowy Układ Współrzędnych Geodezyjnych 1992) – układ współrzędnych 
        płaskich prostokątnych oparty na odwzorowaniu Gaussa-Krügera dla elipsoidy GRS80 w jednej dziesięciostopniowej strefie.

        Parametry
        ----------
        f : FLOAT
            [stopnie dziesiętne] - szerokość geodezyjna..
        l : FLOAT
            [stopnie dziesiętne] - długośc geodezyjna.

        Returns
        -------
         X1992, Y1992 : FLOAT
              [metry] - współrzędne w układzie 1992

        '''
        
        if l > 25.5 or l < 13.5:
            raise NotImplementedError(f"{Transformacje.dms(self, radians(l))} ten południk nie jest obsługiwany przez układ współrzędnych płaskich PL1992")
            
        if f > 55 or f < 48.9:
            raise NotImplementedError(f"{Transformacje.dms(self, radians(f))} ten równoleżnik nie jest obsługiwany przez układ współrzędnych płaskich PL1992")
            
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
    
    
    def flh2PL00(self, f, l):
        '''
        Układ współrzędnych 2000 – układ współrzędnych płaskich prostokątnych zwany układem „2000”, 
        powstały w wyniku zastosowania odwzorowania Gaussa-Krügera dla elipsoidy GRS 80 w czterech 
        trzystopniowych strefach o południkach osiowych 15°E, 18°E, 21°E i 24°E, oznaczone odpowiednio numerami – 5, 6, 7 i 8.

        Parametry
        ----------
        f : FLOAT
            [stopnie dziesiętne] - szerokość geodezyjna..
        l : FLOAT
            [stopnie dziesiętne] - długośc geodezyjna.

        Returns
        -------
         X2000, Y2000 : FLOAT
              [metry] - współrzędne w układzie 2000

        '''
          
        if l >= 13.5 and l < 16.5:
            l0 = np.radians(15)
        elif l >= 16.5 and l < 19.5:
            l0 = np.radians(18)
        elif l >= 19.5 and l < 22.5:
            l0 = np.radians(21)
        elif l >= 22.5 and l <= 25.5:
            l0 = np.radians(24)
        else:
            raise NotImplementedError(f"{Transformacje.dms(self, radians(l))} ten południk nie jest obsługiwany przez układ współrzędnych płaskich PL2000")
        
        if f > 55 or f < 48.9:
            raise NotImplementedError(f"{Transformacje.dms(self, radians(f))} ten równoleżnik nie jest obsługiwany przez układ współrzędnych płaskich PL2000")
            
        f = np.radians(f)
        l = np.radians(l)
        a2 = self.a**2
        b2 = a2 * (1 - self.e2)
        e_2 = (a2 - b2)/b2
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
        strefa = round(l0 * 180/np.pi)/3
        x00 = xgk * 0.999923
        y00 = ygk * 0.999923 + strefa * 1000000 + 500000
        return(x00,y00)
    
    
    def get_dXYZ(xa, ya, za, xb, yb, zb):
        '''
        funkcja liczy macierz rówżnicy współrzednych punktów A i B, która jest potrzebna do obliczenia macierzy neu

        Parametry
        ----------
        XA, YA, ZA, XB, YB, ZB: FLOAT
             współrzędne w układzie orto-kartezjańskim, 

        Returns
        -------
        dXYZ : ARRAY
            macierz różnicy współrzędnych

        '''
        dXYZ = np.array([xb-xa, yb-ya, zb-za])
        return(dXYZ)
    
    
    def rneu(f, l):
        '''
        Funkcja tworzy macierz obrotu R, która jest potrzebna do obliczenia macierzy neu

        Parametry
        ----------
        f : FLOAT
            [stopnie dziesiętne] - szerokość geodezyjna..
        l : FLOAT
            [stopnie dziesiętne] - długośc geodezyjna.

        Returns
        -------
        R ARRAY
            macierz obrotu R
             
        '''
        f=radians(f)
        l=radians(l)
        R = np.array([[-np.sin(f)*np.cos(l), -np.sin(l), np.cos(f)*np.cos(l)],
                      [-np.sin(f)*np.sin(l),  np.cos(l), np.cos(f)*np.sin(l)],
                      [np.cos(f),             0,         np.sin(f)          ]])
        return(R)
    
    
    def xyz2neu(f, l, xa, ya, za, xb, yb, zb):
        '''
        Układ współrzędnych horyzontalnych – układ współrzędnych astronomicznych, w którym oś główną stanowi 
        lokalny kierunek pionu, a płaszczyzną podstawową jest płaszczyzna horyzontu astronomicznego. 
        Biegunami układu są zenit i nadir. Ich położenie na sferze niebieskiej zależy od współrzędnych geograficznych 
        obserwatora oraz momentu obserwacji, tak więc współrzędne horyzontalne opisują jedynie chwilowe położenie ciała niebieskiego.

        Parametry
        ----------
        f : FLOAT
            [stopnie dziesiętne] - szerokość geodezyjna..
        l : FLOAT
            [stopnie dziesiętne] - długośc geodezyjna.
        XA, YA, ZA, XB, YB, ZB: FLOAT
             współrzędne w układzie orto-kartezjańskim, 

        Returns
        -------
        neu ARRAY
            współrzędne horyzontalne
            

        '''
        dX = Transformacje.get_dXYZ(xa, ya, za, xb, yb, zb)
        R = Transformacje.rneu(f,l)
        neu = R.T @ dX
        return(neu)
    
    
    def zapisaniePliku(X, Y, Z, f, l, h, x92, y92, x00, y00, neu): 
        '''
        funkcja zapisuje wyniki obliczeń (x, y, z, f, l, h, x92, y92, x1992, y1992, x2000, y2000 ,neu).
        Tworzy z nich tabele.

        Parametry
        ----------
        X, Y, Z : LIST
             [metry] - współrzędne w układzie orto-kartezjańskim, 
         f : LIST
             [dms] - szerokość geodezyjna..
         l : LIST
             [dms] - długośc geodezyjna.
         h : LIST
             [metry] - wysokość elipsoidalna
        X1992, Y1992 : LIST
             [metry] - współrzędne w układzie 1992
         X2000, Y2000 : LIST
             [metry] - współrzędne w układzie 2000
        neu : ARRAY
            współrzędne horyzontalne

        Returns
        -------
        PLIK TXT

        '''
        with open("Wyniki transformacji.txt", "w",  encoding="utf-8") as plik:
            plik.write(f"Wyniki_obliczen_Geodezyjnych:\n")
            plik.write("-"*180)
            plik.write(f"\n")
            plik.write(f"|       X        |        Y        |         Z         |           f           |           l           |       h       |     x1992    |     y1992    |     x2000     |     y2000     |    neu    |")
            plik.write(f"\n")
            plik.write("-"*180)
            plik.write(f"\n")
            for x, y, z, f, l, h,x92, y92, x00, y00, neu in zip(X, Y, Z, f, l, h, x92, y92, x00, y00, neu):
                plik.write(f"|  {x:^.3f}   |   {y:^.3f}   |    {z:^.3f}    |    {f}    |    {l}    |    {h:^.3f}    |  {x92:^.3f}  |  {y92:^.3f}  |  {x00:^.3f}  |  {y00:^.3f}  |   {neu}   | \n")
            plik.write("-"*180)
    
    
    def wczytanie_pliku(Dane):
        '''
        funkcja wczytuje plik z Danymi X, Y, Z i tworzy z nich liste posegregowanych X,Y i Z.

        
        Parametry
        ----------
        Dane [STR]
            [STR] - nazwa pliku wczytywanego wraz z rozszerzeniem txt
        Returns
        -------
        X, Y, Z [LIST]
            [LIST] - listy danych X Y i Z
        '''
        
        with open(Dane, "r") as plik:
            tab=np.genfromtxt(plik, delimiter=",", dtype = '<U10', skip_header = 4)
            X=[]
            Y=[]
            Z=[]
            for i in tab:
                x=i[0]
                X.append(float(x))
                y=i[1]
                Y.append(float(y))
                z=i[2]
                Z.append(float(z))
        return(X, Y, Z)
 
    
if __name__ == "__main__":
 
    
    geo = Transformacje(model = "GRS80")
    X, Y, Z = Transformacje.wczytanie_pliku("wsp_inp.txt")
    F=[]
    L=[]
    H=[]
    X92=[]
    Y92=[]
    X00=[]
    Y00=[]
    NEU=[]
    #Chwilowe
    for i in X:
        a=3
        NEU.append(a)
    for x, y, z in zip(X, Y, Z):
        f,l,h = geo.hirvonen(x, y, z, output="dms")
        F.append(f)
        L.append(l)
        H.append(h)
        f,l,h = geo.hirvonen(x, y, z)
        x92, y92 = geo.flh2PL92(f,l)
        X92.append(x92)
        Y92.append(y92)
        x00, y00 = geo.flh2PL00(f,l)
        X00.append(x00)
        Y00.append(y00)
    Transformacje.zapisaniePliku(X, Y, Z, F, L, H, X92, Y92, X00, Y00, NEU)
    #zrobić neu
    '''
        if 
        neu=geo.xyz2neu(f,l, Xa, Ya, Za, Xb, Yb, Zb)
        '''
    Transformacje.zapisaniePliku(X, Y, Z, F, L, H, X92, Y92, X00, Y00, NEU)
    
    f,l,h = geo.hirvonen(2, 2, 2, output="dms")
    print(f)