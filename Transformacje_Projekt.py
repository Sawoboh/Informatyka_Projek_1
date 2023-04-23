# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 11:56:02 2023

@author: Sawob
"""

import numpy as np
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

    """
    def Np(self, f):
        N = self.a / np.sqrt(1 - self.e2 * np.sin(f)**2)
        return(N)
    """
    
    
    def hirvonen(self, X, Y, Z):
        p = np.sqrt(X**2 + Y**2)
        f = np.arctan(Z/(p * (1 - self.e2)))
        while True:
            #N = Np(self, f)
            N = self.a / np.sqrt(1 - self.e2 * np.sin(f)**2)
            h = (p / np.cos(f)) - N
            fp = f
            f = np.arctan(Z / (p * (1 - self.e2 * (N / (N+h)))))
            if np.abs(fp - f) < (0.000001/206265):
                break
        l = np.arctan2(Y, X)
        return(f,l,h)
    

if __name__ == "__main__":
    pass