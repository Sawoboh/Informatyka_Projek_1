# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 20:16:17 2023

@author: Sawob
"""
import Transformacje_Projekt   
from Transformacje_Projekt import Transformacje
import tkinter as tk


def get_values():
    val1 = float(oknoinput2.get())
    val2 = float(oknoinput3.get())
    val3 = float(oknoinput4.get())
    val4 = str(oknoinput1.get())
    geo = Transformacje(val4)
    f,l,h = geo.hirvonen(val1, val2, val3, "dms")
    h = "%.3f"%h
    g = f" fi = {f}, l = {l}, h = {h}"
    Tabelka5 = tk.Label(root2, text=g)
    Tabelka5.grid(row=0,column=0, sticky="w")
    
    f1,l1,h1 = geo.hirvonen(val1, val2, val3)
    h1 = "%.3f"%h1
    f1 = "%.10f"%f1
    l1 = "%.10f"%l1
    g1 = f" fi = {f1}, l = {l1}, h = {h1}"
    Tabelka6 = tk.Label(root2, text=g1)
    Tabelka6.grid(row=1,column=0, sticky="w")
    
    f1,l1,h1 = geo.hirvonen(val1, val2, val3, "radiany")
    h1 = "%.3f"%h1
    f1 = "%.12f"%f1
    l1 = "%.12f"%l1
    g1 = f" fi = {f1}, l = {l1}, h = {h1}"
    Tabelka7 = tk.Label(root2, text=g1)
    Tabelka7.grid(row=2,column=0, sticky="w")
    

root = tk.Tk()
root.geometry('262x272+300+300')
root.title("Kalkulator graficzny")
root.lift()
root.attributes("-topmost", True)



Tabelka = tk.Label(root, text="Podaj jedną z elipsoid; GRS80, WGS84, Krasowski:").grid(row=0,column=0)
oknoinput1 = tk.Entry(root, width=42)
oknoinput1.grid(row=1,column=0)
oknoinput1.insert(0, "GRS80")


Spacja = tk.Label(root, text="").grid(row=2,column=0)


Tabelka2 = tk.Label(root, text="Podaj współrzędną ortokartezjańską 'X':").grid(row=3,column=0)
oknoinput2 = tk.Entry(root, width=42)
oknoinput2.grid(row=4,column=0)
oknoinput2.insert(0, "3664940.500")


Spacja = tk.Label(root, text="").grid(row=5,column=0)


Tabelka3 = tk.Label(root, text="Podaj współrzędną ortokartezjańską 'Y':").grid(row=6,column=0)
oknoinput3 = tk.Entry(root, width=42)
oknoinput3.grid(row=7,column=0)
oknoinput3.insert(0, "1409153.590")


Spacja = tk.Label(root, text="").grid(row=8,column=0)


Tabelka4 = tk.Label(root, text="Podaj współrzędną ortokartezjańską 'Z'").grid(row=9,column=0)
oknoinput4 = tk.Entry(root, width=42)
oknoinput4.grid(row=10,column=0)
oknoinput4.insert(0, "5009571.170")


Spacja = tk.Label(root, text="").grid(row=11,column=0)


przycisk = tk.Button(root, text="Dokonaj Obliczeń", command=get_values).grid(row=12,column=0)




root2 = tk.Tk()
root2.geometry('262x272+580+300')
root2.title("Wyniki Obliczeń")
root2.lift()
root2.attributes("-topmost", True)

root.mainloop()
