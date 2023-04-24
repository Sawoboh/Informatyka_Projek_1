# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 11:56:02 2023

@author: Sawob
"""

import numpy as np
import argparse


class Transformacje:
    
    
    def __init__(self, model: str="WGS84"):
        """
        Parametry elipsoid:
            a - duża półoś elipsoidy - promień równikowy
            e2 - mimośród^2 - ((promień równikowy^2+promień południkowy ^2)/promień równikowy^2)
        + WGS84: https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84
        + Inne powierzchnie odniesienia: https://en.wikibooks.org/wiki/PROJ.4#Spheroid
        + Parametry planet: https://nssdc.gsfc.nasa.gov/planetary/factsheet/index.html
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

    def dms(x):
        '''
        Funkcja dms służy do zamienienia wizualnego FLOAT (radiany) na stopnie minuty i sekundy.   

        Parameters
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
        x1=(f'{d}°{m}′{round(s,5)}″')  
        return(x1)
        
        
    def get_np(self, f):
        N = self.a / np.sqrt(1 - self.e2 * np.sin(f)**2)
        return(N)
    
    
    def hirvonen(self, X, Y, Z, output="dms"):
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
         fi
             [stopnie dziesiętne] - szerokość geodezyjna.
         lam
             [stopnie dziesiętne] - długośc geodezyjna.
         h : TYPE
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
            return (fi, lam, h )
        elif output == "dms":
            fi = Transformacje.dms(f)
            lam = Transformacje.dms(l)
            return fi,lam,h 
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

        Parameters
        ----------
        f : FLOAT
            [RADIANY] - szerokość geodezyjna..
        l : FLOAT
            [RADIANY] - długośc geodezyjna.
        h : FLOAT
            [metry] - wysokość elipsoidalna

        Returns
        -------
         X, Y, Z : FLOAT
              współrzędne w układzie orto-kartezjańskim

        '''
        N = Transformacje.get_np(self, f)
        X = (N + h) * np.cos(f) * np.cos(l)
        Y = (N + h) * np.cos(f) * np.sin(l)
        Z = (N * (1 - self.e2) + h) * np.sin(f)
        return(X,Y,Z)
    
    
    def flh2PL92(self, f, l, h):
        '''
        Układ współrzędnych 1992 (Państwowy Układ Współrzędnych Geodezyjnych 1992) – układ współrzędnych 
        płaskich prostokątnych oparty na odwzorowaniu Gaussa-Krügera dla elipsoidy GRS80 w jednej dziesięciostopniowej strefie.

        Parameters
        ----------
        f : FLOAT
            [stopnie dziesiętne] - szerokość geodezyjna..
        l : FLOAT
            [stopnie dziesiętne] - długośc geodezyjna.
        h : FLOAT
            [metry] - wysokość elipsoidalna

        Returns
        -------
         X1992, Y1992 : FLOAT
              współrzędne w układzie 1992

        '''
        
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
        '''
        Układ współrzędnych 2000 – układ współrzędnych płaskich prostokątnych zwany układem „2000”, 
        powstały w wyniku zastosowania odwzorowania Gaussa-Krügera dla elipsoidy GRS 80 w czterech 
        trzystopniowych strefach o południkach osiowych 15°E, 18°E, 21°E i 24°E, oznaczone odpowiednio numerami – 5, 6, 7 i 8.

        Parameters
        ----------
        f : FLOAT
            [stopnie dziesiętne] - szerokość geodezyjna..
        l : FLOAT
            [stopnie dziesiętne] - długośc geodezyjna.
        h : FLOAT
            [metry] - wysokość elipsoidalna

        Returns
        -------
         X2000, Y2000 : FLOAT
              współrzędne w układzie 2000

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
            raise NotImplementedError(f"{l} ten południk nie jest obsługiwany przez układ współrzędnych płaskich PL2000")
        
        if f > 55 and f < 48.9:
            raise NotImplementedError(f"{f} ten równoleżnik nie jest obsługiwany przez układ współrzędnych płaskich PL2000")
            
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
        funkcja liczy macierz rówżnicy współrzednych punktów A i B

        Parameters
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
        

        Parameters
        ----------
        f : FLOAT
            [radiany] - szerokość geodezyjna..
        l : FLOAT
            [radiany] - długośc geodezyjna.

        Returns
        -------
        R ARRAY
            macierz obrotu
             
        '''
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

        Parameters
        ----------
        f : FLOAT
            [radiany] - szerokość geodezyjna..
        l : FLOAT
            [radiany] - długośc geodezyjna.
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
        

        Parameters
        ----------
        X, Y, Z : FLOAT
             współrzędne w układzie orto-kartezjańskim, 
         f : FLOAT
             [dms] - szerokość geodezyjna..
         l : FLOAT
             [dms] - długośc geodezyjna.
         h : FLOAT
             [metry] - wysokość elipsoidalna
            X1992, Y1992 : FLOAT
                 współrzędne w układzie 1992
         X2000, Y2000 : FLOAT
              współrzędne w układzie 2000
        neu : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
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

       
    geo = Transformacje(model = "GRS80")
    
    
    f,l,h = geo.hirvonen(3853080,1425040,4863020,output="dms")
    print("Dane w hirvonenie:", f, l, h)
    

    x,y,z = geo.flh2XYZ(1,1,1)
    print("Dane w flh2XYZ:", x,y,z)
    
    
    fsto = 53+11/60+59.79018/3600; lsto = 16+41/60+50.52003/3600
    x92, y92 = geo.flh2PL92(fsto,lsto,1)
    print("Dane w PL92:", x92, y92)
    
    
    fsto = 53+11/60+59.79018/3600; lsto = 16+41/60+50.52003/3600
    x00, y00 = geo.flh2PL00(fsto,lsto,1)
    print("Dane w PL00:", x00, y00)
    
    
    fa = np.radians(10); la = np.radians(12); Xa = 100; Ya = 200; Za = 500; Xb = 300; Yb = 400; Zb = 500
    neu = Transformacje.xyz2neu(fa,la, Xa, Ya, Za, Xb, Yb, Zb)
    print("Dane w neu:", neu)
    #𝐴=[595218.264; 346242.070] wynik w 1992
    #𝐴=[5897209.810; 6412958.174] wynik w 2000'''