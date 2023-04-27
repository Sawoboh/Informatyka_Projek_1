# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 11:42:22 2023

@author: amaks
"""

from argparse import ArgumentParser
import Transformacje_Projekt   
from Transformacje_Projekt import Transformacje

parser = ArgumentParser()
parser.add_argument('-m', '--m', type=str, help="Podaj jedną z wskazanych elipsoid: GRS80, WGS84, Krasowski")
parser.add_argument('-xyz', '--xyz', type=str, help="Podaj nazwe pliku wynikiowego dla xyz_flh_PL1992_PL2000 z rozszerzeniem txt")
parser.add_argument('-f', '--f', type=float)
parser.add_argument('-l', '--l', type=float)
parser.add_argument('-ha', '--ha', type=float)
parser.add_argument('-output', '--output', type=str)

args = parser.parse_args()

geo = Transformacje(model = args.m)


print("")
print("")
print("Elipsida:", args.m)
x, y, z = geo.flh2XYZ(args.f, args.l, args.ha)
print(f"Wyniki_z_transformacji_flh2xyz; X = {x:^.3f}[m], Y = {y:^.3f}[m], Z = {z:^.3f}[m]")
if args.l >= 13.5 and args.l <= 25.5 and args.f <= 55.0 and args.f >= 48.9:
    x92, y92 = geo.flh2PL92(args.f,args.l)
    x00, y00 = geo.flh2PL00(args.f,args.l)
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

geo.zapis_w_kalkulatorach_xyz_flh_PL1992_PL2000(args.xyz, x, y, z, args.f, args.l, args.ha, x92, y92, x00, y00, output = args.output )