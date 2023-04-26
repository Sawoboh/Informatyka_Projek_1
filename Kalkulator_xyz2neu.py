# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 00:37:42 2023

@author: Sawob
"""

from argparse import ArgumentParser
import Transformacje_Projekt   
from Transformacje_Projekt import Transformacje

parser = ArgumentParser()
parser.add_argument('-m', '--m', type=str, help="Podaj jedną z wskazanych elipsoid: GRS80, WGS84, Krasowski")
parser.add_argument('-xa', '--xa', type=float)
parser.add_argument('-ya', '--ya', type=float)
parser.add_argument('-za', '--za', type=float)
parser.add_argument('-xb', '--xb', type=float)
parser.add_argument('-yb', '--yb', type=float)
parser.add_argument('-zb', '--zb', type=float)
args = parser.parse_args()


geo = Transformacje(model = args.m)
f, l, h = geo.hirvonen(args.xa, args.ya, args.za)
n, e, u = geo.xyz2neu(f, l, args.xa, args.ya, args.za, args.xb, args.yb, args.zb)


n = float(n)
e = float(e)
u = float(u)


print("")
print("")
print("")
print("")
print("Elipsida:", args.m)
print(f"Wyniki_z_xyz2neu; n = {n}, e = {e}, u = {u}")
print("Nazwa pliku głównego:", Transformacje_Projekt.__name__)
print("")
print("")
print("")
print("")
