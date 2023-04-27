# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 12:34:21 2023

@author: amaks
"""
from argparse import ArgumentParser
import Transformacje_Projekt   
from Transformacje_Projekt import Transformacje

parser = ArgumentParser()
parser.add_argument('-m', '--m', type=str, help="Podaj jedną z wskazanych elipsoid: GRS80, WGS84, Krasowski")
parser.add_argument('-neu', '--neu', type=str, help="Podaj nazwe pliku wynikiowego dla neu z rozszerzeniem txt")
parser.add_argument('-fa', '--fa', type=float)
parser.add_argument('-la', '--la', type=float)
parser.add_argument('-ha', '--ha', type=float)
parser.add_argument('-fb', '--fb', type=float)
parser.add_argument('-lb', '--lb', type=float)
parser.add_argument('-hb', '--hb', type=float)
args = parser.parse_args()

geo = Transformacje(model = args.m)


xa, ya, za = geo.flh2XYZ(args.fa, args.la, args.ha)
xb, yb, zb = geo.flh2XYZ(args.fb, args.lb, args.hb)

print("")
print("")
n, e, u=geo.xyz2neu(args.fa, args.la, xa, ya, za, xb, yb, zb)
   
geo.zapis_w_kalkulatorze_neu(args.neu, n, e, u)

n = float(n)
e = float(e)
u = float(u)


print("Elipsida:", args.m)
print(f"Wyniki_z_flh2neu; n = {n}, e = {e}, u = {u}")
print("Nazwa pliku głównego:", Transformacje_Projekt.__name__)
print("")
print("")
