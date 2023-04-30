# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 20:16:17 2023

@author: Sawob
"""
import Transformacje_Projekt   
from Transformacje_Projekt import Transformacje
import tkinter as tk
from tkinter import ttk


def get_values():
    val1 = float(oknoinput2.get())
    val2 = float(oknoinput3.get())
    val3 = float(oknoinput4.get())
    val4 = str(oknoinput1.get())
    geo = Transformacje(val4)
    
    Tabelka8 = tk.Label(root2, text="Wyniki fi, lambda, h: 'dms':").grid(row=0, column=0)
    f,l,h = geo.hirvonen(val1, val2, val3, "dms")
    h = "%.3f"%h
    g = f" fi = {f}, l = {l}, h = {h}"
    Tabelka5 = tk.Label(root2, text=g)
    Tabelka5.grid(row=1,column=0, sticky="w")
    
    Spacja = tk.Label(root2, text="").grid(row=2,column=0)
    
    Tabelka9 = tk.Label(root2, text="Wyniki fi, lambda, h: 'stopnie_dziesiętne':").grid(row=3, column=0)
    f1,l1,h1 = geo.hirvonen(val1, val2, val3)
    h2 = "%.3f"%h1
    f2 = "%.10f"%f1
    l2 = "%.10f"%l1
    g1 = f" fi = {f2}, l = {l2}, h = {h2}"
    Tabelka6 = tk.Label(root2, text=g1)
    Tabelka6.grid(row=4,column=0, sticky="w")
    
    Spacja = tk.Label(root2, text="").grid(row=5,column=0)
    
    Tabelka10 = tk.Label(root2, text="Wyniki fi, lambda, h: 'radiany':").grid(row=6, column=0)
    f3,l3,h3 = geo.hirvonen(val1, val2, val3, "radiany")
    h4 = "%.3f"%h3
    f4 = "%.12f"%f3
    l4 = "%.12f"%l3
    g2 = f" fi = {f4}, l = {l4}, h = {h4}"
    Tabelka7 = tk.Label(root2, text=g2)
    Tabelka7.grid(row=7,column=0, sticky="w")
    
    Spacja = tk.Label(root2, text="").grid(row=8,column=0)
    
    Tabelka15 = tk.Label(root2, text="Wyniki x1992, y1992:").grid(row=9, column=0)
    if l1 >= 13.5 and l1 <= 25.5 and f1 <= 55.0 and f1 >= 48.9:
        x92, y92 = geo.flh2PL92(f1, l1)
        x92_3 = "%.3f"%x92
        y92_3 = "%.3f"%y92
        g3 = f" x1992 = {x92_3}, y1992 = {y92_3}"
    else:
        g3= f"Dla podanych współrzędnych nie liczy się x1992 i y1992"
    Tabelka16 = tk.Label(root2, text=g3)
    Tabelka16.grid(row=10,column=0, sticky="w")
    
    Spacja = tk.Label(root2, text="").grid(row=11,column=0)
    
    Tabelka15 = tk.Label(root2, text="Wyniki x2000, y2000:").grid(row=12, column=0)
    if l1 >= 13.5 and l1 <= 25.5 and f1 <= 55.0 and f1 >= 48.9:
        x00, y00 = geo.flh2PL00(f1, l1)
        x00_3 = "%.3f"%x00
        y00_3 = "%.3f"%y00
        g4 = f" x2000 = {x00_3}, y2000 = {y00_3}"
    else:
        g3= f"Dla podanych współrzędnych nie liczy się x2000 i y2000"
    Tabelka16 = tk.Label(root2, text=g4)
    Tabelka16.grid(row=13,column=0, sticky="w")
    
    Spacja = tk.Label(root2, text="").grid(row=14,column=0)
    
    val6 = str(oknoinput6.get())
    if val6 == "stopnie_dziesiętne":
        val6 = "dec_degree"
        
    val7 = str(oknoinput7.get())
    if val7 == "TAK":
        with open("Wyniki_z_kalkulatora_graficznego.txt", "r") as plik:
            wiersze = plik.readlines()
        with open("Wyniki_z_kalkulatora_graficznego.txt", "w") as plik:
            plik.writelines(wiersze[0:6])    
        root3 = tk.Tk()
        root3.geometry('572x477+300+300')
        root3.title("Czyszczenie tablicy z danymi")
        root3.lift()
        root3.attributes("-topmost", True)
        Spacja = tk.Label(root3, text="").pack()
        Spacja = tk.Label(root3, text="").pack()
        Spacja = tk.Label(root3, text="").pack()
        Spacja = tk.Label(root3, text="").pack()
        Spacja = tk.Label(root3, text="").pack()
        Spacja = tk.Label(root3, text="").pack()
        Spacja = tk.Label(root3, text="").pack()
        Spacja = tk.Label(root3, text="").pack()
        Spacja = tk.Label(root3, text="").pack()
        Tabelka16 = tk.Label(root3, text="Trwa czyszczenie tablicy - proszę czekać.")
        Tabelka16.pack()
        ladowanie = ttk.Progressbar(root3, orient=tk.HORIZONTAL, length=250, mode='determinate')
        ladowanie.pack()
        for i in range(1, 101):
            ladowanie['value'] = i
            ladowanie.update()
            root.after(20)
            if i == 100:
                root3.destroy()
        root.mainloop()

    
    val5 = str(oknoinput5.get())
    if val5 == "TAK":
        Tabelka17 = tk.Label(root2, text="====================================").grid(row=15, column=0)
        Tabelka18 = tk.Label(root2, text="    Wyniki zostały zapisane do notatnika.    ").grid(row=16, column=0)
        Tabelka19 = tk.Label(root2, text="====================================").grid(row=17, column=0)
        geo.zapis_w_kalkulatorach_xyz_flh_PL1992_PL2000("Wyniki_z_kalkulatora_graficznego.txt", val1, val2, val3, output = val6)
    else:
        Tabelka20 = tk.Label(root2, text="====================================").grid(row=15, column=0)
        Tabelka31 = tk.Label(root2, text="Wyniki NIE zostały zapisane do notatnika.").grid(row=16, column=0)
        Tabelka32 = tk.Label(root2, text="====================================").grid(row=17, column=0)
    
    

root = tk.Tk()
root.geometry('262x477+300+300')
root.title("Kalkulator graficzny")
root.lift()
root.attributes("-topmost", True)



Tabelka = tk.Label(root, text="Podaj elipsoidę: [GRS80/WGS84/Krasowski]").grid(row=0,column=0)
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


Tabelka4 = tk.Label(root, text="Podaj współrzędną ortokartezjańską 'Z':").grid(row=9,column=0)
oknoinput4 = tk.Entry(root, width=42)
oknoinput4.grid(row=10,column=0)
oknoinput4.insert(0, "5009571.170")


Spacja = tk.Label(root, text="").grid(row=11,column=0)


Tabelka13 = tk.Label(root, text="Zapisać przeliczenie do notatnika? [TAK/NIE]").grid(row=12,column=0)
oknoinput5 = tk.Entry(root, width=42)
oknoinput5.grid(row=13,column=0)
oknoinput5.insert(0, "NIE")


Spacja = tk.Label(root, text="").grid(row=14,column=0)


Tabelka13 = tk.Label(root, text="W jakich jednostkach zapisać f, l, h do notatnika?").grid(row=15,column=0)
Tabelka15 = tk.Label(root, text="[dms/stopnie_dziesiętne/radiany]").grid(row=16,column=0,padx=0.001, pady=0.001)
oknoinput6 = tk.Entry(root, width=42)
oknoinput6.grid(row=17,column=0)
oknoinput6.insert(0, "stopnie_dziesiętne")


Spacja = tk.Label(root, text="").grid(row=18,column=0)


Tabelka22 = tk.Label(root, text="Czy wyczyścić tablice z danymi? [TAK/NIE]").grid(row=19,column=0)
oknoinput7 = tk.Entry(root, width=42)
oknoinput7.grid(row=20,column=0)
oknoinput7.insert(0, "NIE")


Spacja = tk.Label(root, text="").grid(row=21,column=0)


przycisk = tk.Button(root, text="Dokonaj Obliczeń", command=get_values).grid(row=22,column=0)



root2 = tk.Tk()
root2.geometry('292x375+580+300')
root2.title("Wyniki Obliczeń")
root2.lift()
root2.attributes("-topmost", True)

root.mainloop()
