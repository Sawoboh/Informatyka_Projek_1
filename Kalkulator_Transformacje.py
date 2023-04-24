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
parser.add_argument('-x', '--x', type=float)
parser.add_argument('-y', '--y', type=float)
parser.add_argument('-z', '--z', type=float)
args = parser.parse_args()


geo = Transformacje(model = args.m)


f, l, h = geo.hirvonen(args.x, args.y, args.z)
fi, lam, ha = geo.hirvonen(args.x, args.y, args.z, output="dms")
x92, y92 = geo.flh2PL92(f, l)
x00, y00 = geo.flh2PL00(f, l)

print("")
print(f"Wyniki_z_algorytmu_hirvonen'a; fi = {fi}, lam = {lam}, ha = {ha:^.3f}[m]")
print("")
print(f"Wyniki_z_przeliczenia_na_układ_PL1992; x1992 = {x92:^.3f}, y1992 = {y92:^.3f}")
print("")
print(f"Wyniki_z_przeliczenia_na_układ_PL2000; x2000 = {x00:^.3f}, y2000 = {y00:^.3f}")




print(Transformacje_Projekt.__name__)

