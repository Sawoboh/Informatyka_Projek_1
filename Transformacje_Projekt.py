# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 11:56:02 2023

@author: Sawob
"""

import numpy as np
from argparse import ArgumentParser
import os as os


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
        x : STR
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
        
        d = str(d)
        if len(d) == 1:
            d = "  " + d
        elif len(d) == 2:
            d = " " + d
        elif len(d) == 3:
            d = d
            
        if m < 10:
            m = str(m)
            m = "0" + m
            
        if s < 10:
            s = "%.5f"%s
            s = str(s)
            s= "0" + s
        else:
            s = ("%.5f"%s)
            
        x1=(f'{d}°{m}′{s}″')  
        return(x1)
        
        
    def get_np(self, f):
        '''
        funkcja liczy promień przekroju w pierwszym wertykale, który potrzebny jest nam między innymi do algorymu hirvonena,
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
        f=np.radians(f)
        l=np.radians(l)
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
            raise NotImplementedError(f"{Transformacje.dms(self, np.radians(l))} ten południk nie jest obsługiwany przez układ współrzędnych płaskich PL1992")
            
        if f > 55 or f < 48.9:
            raise NotImplementedError(f"{Transformacje.dms(self, np.radians(f))} ten równoleżnik nie jest obsługiwany przez układ współrzędnych płaskich PL1992")
            
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
            raise NotImplementedError(f"{Transformacje.dms(self, np.radians(l))} ten południk nie jest obsługiwany przez układ współrzędnych płaskich PL2000")
        
        if f > 55 or f < 48.9:
            raise NotImplementedError(f"{Transformacje.dms(self, np.radians(f))} ten równoleżnik nie jest obsługiwany przez układ współrzędnych płaskich PL2000")
            
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
    
    
    def get_dXYZ(self, xa, ya, za, xb, yb, zb):
        '''
        funkcja liczy macierz różnicy współrzednych punktów A i B, która jest potrzebna do obliczenia macierzy neu

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
    
    
    def rneu(self, f, l):
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
        f=np.radians(f)
        l=np.radians(l)
        R = np.array([[-np.sin(f)*np.cos(l), -np.sin(l), np.cos(f)*np.cos(l)],
                      [-np.sin(f)*np.sin(l),  np.cos(l), np.cos(f)*np.sin(l)],
                      [np.cos(f),             0,         np.sin(f)          ]])
        return(R)
    
    
    def xyz2neu(self, f, l, xa, ya, za, xb, yb, zb):
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
        n , e, u : STR
            współrzędne horyzontalne
            

        '''
        dX = Transformacje.get_dXYZ(self, xa, ya, za, xb, yb, zb)
        R = Transformacje.rneu(self, f,l)
        neu = R.T @ dX
        n = neu[0];   e = neu[1];   u = neu[2]
        n = "%.16f"%n; e = "%.16f"%e; u="%.16f"%u
        dlugosc = []
        xx = len(n); dlugosc.append(xx)
        yy = len(e); dlugosc.append(yy)
        zz = len(u); dlugosc.append(zz)
        P = 50
        
        while xx < P:
            n = str(" ") + n
            xx += 1
        
        while yy < P:
            e = str(" ") + e
            yy += 1
            
        while zz < P:
            u = str(" ") + u
            zz +=1
            
        return(n, e, u)
    

    def zapisaniePliku(self, X, Y, Z, f, l, h, x92, y92, x00, y00, N, E, U, xyz_txt, neu_txt ): 
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
        n, e, u : str
            współrzędne horyzontalne

        Returns
        -------
        PLIK TXT

        '''
        for i in range(len(X)):
            X[i] = Transformacje.zamiana_float2string(self, X[i])
            Y[i] = Transformacje.zamiana_float2string(self, Y[i])
            Z[i] = Transformacje.zamiana_float2string(self, Z[i])
        
        with open(xyz_txt , "w",  encoding="utf-8") as plik:
            plik.write(f"Wyniki_obliczen_Geodezyjnych; X, Y, Z, fi, lambda, h, x1992, y1992, x2000, y2000.\n")
            plik.write(f"Znak '-' w koordynatach; x1992, y1992, x2000, y2000 oznacza, że dla podanych współrzędnych ortokartezjańskich (X, Y, Z) po obliczeniu współrzędnych geodezyjnych fi i lambda. fi i lambda nie należą do dozwolonych współrzędnych \ngeodezyjnych układów PL1992, PL2000.\n")
            plik.write("-"*221)
            plik.write(f"\n")
            plik.write(f"|          X          |          Y          |          Z          |          fi         |        lambda       |          h          |        x1992        |        y1992        |        x2000        |        y2000        |")
            plik.write(f"\n")
            plik.write("-"*221)
            plik.write(f"\n")
            for x, y, z, f, l, h, x92, y92, x00, y00 in zip(X, Y, Z, f, l, h, x92, y92, x00, y00):
                plik.write(f"|{x}|{y}|{z}|     {f}|     {l}|{h}|{x92}|{y92}|{x00}|{y00}|")
                plik.write(f"\n")
            plik.write("-"*221)
        
        with open(neu_txt , "w", encoding="utf-8") as plik1:
            plik1.write(f"Wyniki_obliczen_Geodezyjnych; n, e, u.\n")
            plik1.write("-"*154)
            plik1.write(f"\n")
            plik1.write(f"|                        n                         |                        e                         |                        u                         |")
            plik1.write(f"\n")
            plik1.write("-"*154)
            plik1.write(f"\n")
            for n, e, u in zip(N, E, U):
                plik1.write(f"|{n}|{e}|{u}|")
                plik1.write(f"\n")
            plik1.write("-"*154)
    
    
    def wczytanie_pliku(self, Dane):
        '''
        funkcja wczytuje plik z Danymi X, Y, Z i tworzy z nich liste posegregowanych X, Y i Z.

        
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
            tab=np.genfromtxt(plik, delimiter=",", dtype = '<U20', skip_header = 4)
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
            ilosc_wierszy = len(X)
        return(X, Y, Z, ilosc_wierszy)
    
    
    def wczytanie_zapisanie_pliku(self, Dane, output ='dms' , xyz_txt = 'Wyniki_transformacji_X_Y_Z_fi_lambda_h_x1992_y1992_x2000_y2000.txt', neu_txt = "Wyniki_transformacji_n_e_u.txt" ):
        '''
        wczytanie i zapisanie pliku za pomocą jednej funkcji

        Parameters
        ----------
        Dane : txt
            Plik z danymi xyz.
        output : str
            sposób w jakiej ma zapisywać współrzędne f, l [dms, radiany, dec_degree] .
        XYZ_txt: STR
            nazwa pliku wynikowego na xyz, flh, PL1992, PL2000
        NEU_txt: STR

        Returns
        -------
        Plik txt

        '''
        X, Y, Z, C = Transformacje.wczytanie_pliku(self, Dane)
        F=[]
        L=[]
        H=[]
        X92=[]
        Y92=[]
        X00=[]
        Y00=[]
        N=[]
        E=[]
        U=[]
        
        for x, y, z in zip(X, Y, Z):
            f,l,h = Transformacje.hirvonen(self, x, y, z, output = output)
            if output == "dms":
                F.append(f)
                L.append(l)
            elif output == "radiany":
                f=Transformacje.zamiana_float2string_rad(self,f)
                l=Transformacje.zamiana_float2string_rad(self,l)
                F.append(f)
                L.append(l)
            else:
                f=Transformacje.zamiana_float2string_fl(self,f)
                l=Transformacje.zamiana_float2string_fl(self,l)
                F.append(f)
                L.append(l)
            H.append(Transformacje.zamiana_float2string(self, h))
            f,l,h = Transformacje.hirvonen(self, x, y, z)
            
            if l >= 13.5 and l <= 25.5 and f <= 55.0 and f >= 48.9:
                x92, y92 = Transformacje.flh2PL92(self, f,l)
                X92.append(Transformacje.zamiana_float2string(self, x92))
                Y92.append(Transformacje.zamiana_float2string(self, y92))
                x00, y00 = Transformacje.flh2PL00(self, f,l)
                X00.append(Transformacje.zamiana_float2string(self, x00))
                Y00.append(Transformacje.zamiana_float2string(self, y00))
            else:
                x92 = "         '-'         " ; X92.append(x92)
                y92 = "         '-'         " ; Y92.append(y92)
                x00 = "         '-'         " ; X00.append(x00)
                y00 = "         '-'         " ; Y00.append(y00)
        
        f1, l1, h1 = Transformacje.hirvonen(self, X[0], Y[0], Z[0])
        n1, e1, u1 = Transformacje.xyz2neu(self, f1, l1, X[0], Y[0], Z[0], X[-1], Y[-1], Z[-1])
        N.append(n1)
        E.append(e1)
        U.append(u1)
        
        i=0
        while i<(C-1):
            f, l, h = Transformacje.hirvonen(self, X[i], Y[i], Z[i])
            n, e, u = Transformacje.xyz2neu(self, f, l, X[i], Y[i], Z[i], X[i+1], Y[i+1], Z[i+1])
            N.append(n)
            E.append(e)
            U.append(u)
            i+=1
        
        Transformacje.zapisaniePliku(self, X, Y, Z, F, L, H, X92, Y92, X00, Y00, N, E, U, xyz_txt, neu_txt )     
        
        
    def zamiana_float2string_rad(self, liczba):
        '''
        zamienia z float na str z dokładnocia taką jaką musi mieć jednostka radiany. 
        Zrobione jest to po to żeby wynik się ładnie zapisywał w pliku wynikowym 

        Parameters
        ----------
        liczba : FLOAT
            Liczba w radianach.

        Returns
        -------
        liczba : STR
            string z okreloną stała iloscia znaków

        '''
        zm_liczba = "%.12f"%liczba
        P = 16
        xx = len(zm_liczba)
        while xx < P:
            zm_liczba = str(" ") + zm_liczba
            xx += 1
        return(zm_liczba)  

    
    def zamiana_float2string_fl(self, liczba):
        '''
        zamienia z float na str z dokładnocia taką jaką musi mieć jednostka stopnie dziesiętne. 
        Zrobione jest to po to żeby wynik się ładnie zapisywał w pliku wynikowym 

        Parameters
        ----------
        liczba : FLOAT
            Liczba w stopniach dziesiętnych.

        Returns
        -------
        liczba : STR
            string z okreloną stała iloscia znaków

        '''
        zm_liczba = "%.10f"%liczba
        P = 16
        xx = len(zm_liczba)
        while xx < P:
            zm_liczba = str(" ") + zm_liczba
            xx += 1
        return(zm_liczba)        
    
    
    def zamiana_float2string(self, liczba):
        '''
        zamienia z float na str z dokładnocia taką jaką musi mieć jednostka dms. 
        Zrobione jest to po to żeby wynik się ładnie zapisywał w pliku wynikowym 

        Parameters
        ----------
        liczba : FLOAT
            Liczba w dms.

        Returns
        -------
        liczbe : STR
            string z okreloną stała iloscia znaków


        '''
        zm_liczba = "%.3f"%liczba
        P = 21
        xx = len(zm_liczba)
        while xx < P:
            zm_liczba = str(" ") + zm_liczba
            xx += 1
        return(zm_liczba)
    
    
    def zapis_w_kalkulatorach_xyz_flh_PL1992_PL2000(self, xyz_txt, x, y, z, f, l, h, x92, y92, x00, y00, output = "dms"):
        '''
        Zapisanie pliku txt z danych wprowadzanych do pliku Kalkulatora który przelicza na PL2000, PL1992 ,xyz i flh

        Parameters
        ----------
        xyz_txt : STR
            PLIK TXT
        X, Y, Z : FLOAT
             [metry] - współrzędne w układzie orto-kartezjańskim,
        f : FLOAT
             [stopnie dziesiętne] - szerokość geodezyjna.
        l : FLOAT
             [stopnie dziesiętne] - długośc geodezyjna.
        h : FLOAT
             [metry] - wysokość elipsoidalna
        X1992, Y1992 : FLOAT
             [metry] - współrzędne w układzie 1992
        X2000, Y2000 : FLOAT
             [metry] - współrzędne w układzie 2000
        output : TYPE, optional
            DESCRIPTION. The default is "dms".

        Returns
        -------
        Plik txt

        '''
        f,l,h = Transformacje.hirvonen(self, x, y, z, output = output)
            
        if output == "dms":
            f=f
            l=l
        elif output == "radiany":
            f=Transformacje.zamiana_float2string_rad(self,f)
            l=Transformacje.zamiana_float2string_rad(self,l)
        else:
            f=Transformacje.zamiana_float2string_fl(self,f)
            l=Transformacje.zamiana_float2string_fl(self,l)
        h = Transformacje.zamiana_float2string(self, h)
        F,L,H = Transformacje.hirvonen(self, x, y, z)
        
        if L >= 13.5 and L <= 25.5 and F <= 55.0 and F >= 48.9:
            x92, y92 = Transformacje.flh2PL92(self, F,L)
            x92 = Transformacje.zamiana_float2string(self, x92)
            y92 = Transformacje.zamiana_float2string(self, y92)
            x00, y00 = Transformacje.flh2PL00(self, F,L)
            x00 = Transformacje.zamiana_float2string(self, x00)
            y00 = Transformacje.zamiana_float2string(self, y00)
        else:
            x92 = "         '-'         " 
            y92 = "         '-'         " 
            x00 = "         '-'         "
            y00 = "         '-'         "
        x = Transformacje.zamiana_float2string(self, x)
        y = Transformacje.zamiana_float2string(self, y)
        z = Transformacje.zamiana_float2string(self, z)
        
        if not os.path.exists(xyz_txt):
            with open(xyz_txt, "w", encoding="utf-8") as plik:
                plik.write(f"Wyniki_obliczen_Geodezyjnych; X, Y, Z, fi, lambda, h, x1992, y1992, x2000, y2000.\n")
                plik.write(f"Znak '-' w koordynatach; x1992, y1992, x2000, y2000 oznacza, że dla podanych współrzędnych ortokartezjańskich (X, Y, Z) po obliczeniu współrzędnych geodezyjnych fi i lambda. fi i lambda nie należą do dozwolonych współrzędnych \ngeodezyjnych układów PL1992, PL2000.\n")
                plik.write("-"*221)
                plik.write(f"\n")
                plik.write(f"|          X          |          Y          |          Z          |          fi         |        lambda       |          h          |        x1992        |        y1992        |        x2000        |        y2000        |")
                plik.write(f"\n")
                plik.write("-"*221)
                plik.write(f"\n")
                plik.write(f"|{x}|{y}|{z}|     {f}|     {l}|{h}|{x92}|{y92}|{x00}|{y00}|")
                plik.write(f"\n")
                plik.write("-"*221)
                plik.write(f"\n")
        else:
            with open(xyz_txt, "a", encoding="utf-8") as plik:
                plik.write(f"|{x}|{y}|{z}|     {f}|     {l}|{h}|{x92}|{y92}|{x00}|{y00}|")
                plik.write(f"\n")
                plik.write("-"*221)
                plik.write(f"\n")
            
        
    def zapis_w_kalkulatorze_neu(self, neu_txt, n, e, u):
        '''
        funkcja zapisuje do pliku dane w układzie neu

        Parameters
        ----------
        neu_txt : TYPE
            DESCRIPTION.
        n, e, u : str
            współrzędne horyzontalne

        Returns
        -------
        Plik txt

        '''
        if not os.path.exists(neu_txt):
            with open(neu_txt , "w", encoding="utf-8") as plik1:
                plik1.write(f"Wyniki_obliczen_Geodezyjnych; n, e, u.\n")
                plik1.write("-"*154)
                plik1.write(f"\n")
                plik1.write(f"|                        n                         |                        e                         |                        u                         |")
                plik1.write(f"\n")
                plik1.write("-"*154)
                plik1.write(f"\n")
                plik1.write(f"|{n}|{e}|{u}|")
                plik1.write(f"\n")
                plik1.write("-"*154)  
                plik1.write(f"\n")
        else:
            with open(neu_txt , "a", encoding="utf-8") as plik1:
                plik1.write(f"|{n}|{e}|{u}|")
                plik1.write(f"\n")
                plik1.write("-"*154)
                plik1.write(f"\n")
        
if __name__ == "__main__":
    geo = Transformacje("GRS80")
    geo.wczytanie_zapisanie_pliku("wsp_inp.txt")
    
    
    parser = ArgumentParser()
    parser.add_argument('-m', '--m', type=str, help="Podaj jedną z wskazanych elipsoid: GRS80, WGS84, Krasowski")
    parser.add_argument('-t', '--t', type=str, help="Podaj nazwe pliku tekstowegoz danymi z rozszerzeniem txt")
    parser.add_argument('-d', '--d', type=str, help="Podaj forme w jakiej ma sie zapisać fi i lambda: dms , radiany, dec_degree ")
    parser.add_argument('-xyz', '--xyz', type=str, help="Podaj nazwe pliku wynikiowego dla xyz_flh_PL1992_PL2000 z rozszerzeniem txt")
    parser.add_argument('-neu', '--neu', type=str, help="Podaj nazwe pliku wynikiowego dla neu z rozszerzeniem txt")
    
    args = parser.parse_args()
    geo = Transformacje(args.m)
    geo.wczytanie_zapisanie_pliku(args.t, args.d, args.xyz, args.neu)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
