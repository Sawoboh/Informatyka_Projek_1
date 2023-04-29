# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 20:06:03 2023

@author: Sawob
"""

from argparse import ArgumentParser
import Transformacje_Projekt   
from Transformacje_Projekt import Transformacje

parser = ArgumentParser()
parser.add_argument('-m', '--m', type=str, help="Podaj jedną z wskazanych elipsoid: GRS80, WGS84, Krasowski")
parser.add_argument('-xyz', '--xyz', type=str, help="Podaj nazwe pliku wynikiowego dla xyz_flh_PL1992_PL2000 z rozszerzeniem txt")
parser.add_argument('-x', '--x', type=float)
parser.add_argument('-y', '--y', type=float)
parser.add_argument('-z', '--z', type=float)
parser.add_argument('-output', '--output', type=str)
args = parser.parse_args()


geo = Transformacje(model = args.m)


f, l, h = geo.hirvonen(args.x, args.y, args.z)
fi, lam, ha = geo.hirvonen(args.x, args.y, args.z, output="dms")

print("")
print("")
print("Elipsida:", args.m)
print(f"Wyniki_z_algorytmu_hirvonen'a; fi = {fi}, lam = {lam}, ha = {ha:^.3f}[m]")

fi, lam, ha = geo.hirvonen(args.x, args.y, args.z)
if lam >= 13.5 and lam <= 25.5 and fi <= 55.0 and fi >= 48.9:
    x92, y92 = geo.flh2PL92(fi,lam)
    x00, y00 = geo.flh2PL00(fi,lam)
    print(f"Wyniki_z_transformacji_flh2PL92_I_flh2PL00; X1992 = {x92:^.3f}[m], Y1992 = {y92:^.3f}[m], X2000 = {x00:^.3f}[m], Y2000 = {y00:^.3f}[m]")
else:
    x92 = " '-' " 
    y92 = " '-' " 
    x00 = " '-' " 
    y00 = " '-' " 
    print(f"Wyniki_z_transformacji_flh2PL92_i_flh2PL00; X1992 = {x92}[m], Y1992 = {y92}[m], X2000 = {x00}[m], Y2000 = {y00}[m]")
    print("To położenie nie jest obsługiwane przez układy współrzędnych płaskich PL1992 i PL2000")

print("Nazwa pliku głównego:", Transformacje_Projekt.__name__)
print("")
print("")

geo.zapis_w_kalkulatorach_xyz_flh_PL1992_PL2000(args.xyz, args.x, args.y, args.z, output = args.output )

