# Informatyka_Projekt_1

Program służy do przeliczenia poprzez odpowiednie trasformacjie współrzędnych ortokartezjańskich geocentrycznych [X, Y, Z] lub współrzędnych geodezyjnych elipsoidealnych [f, l, h] do współrzędnych; topocentrycznych [n, e, u], współrzędnych płaskich PL1992 [x1992, y1992] oraz współrzędnych płaskich PL2000 [x2000, y2000]
Przeliczenia są możliwe tylko dla elipsoid; [GRS80, WGS84, Krasowski].

Program wymaga posiadania następujących bibliotek: tkinter, pytest, numpy, os, argarse.

Program napisany jest dzięki językowi programowania PYTHON.
Program napisany jest dla systemu Windows.
Program został testowany na Windows11, Windows10, Python 3.9.10 oraz Python 3.10.

Program posiada 4 kalkulatory cmd'kowe, 1 kalkulator graficzny, 1 plik, który sprawdza poprawność funkcji, 1 plik przeliczający dane z notatnika do innego notatnika.

Błędy: Program nie działa dla obliczenia kordynatów [X,Y,Z] = [0,0,0], kalkulator graficzny może źle działać jak użytkownik usunie dane z tablicy danych jeżeli takowej nie ma w folderze programu.


- Pierwszy kalkulator cmd'kowy Kalkulator_flh2neu wywołanie: python Kalkulator_flh2neu.py -m GRS80 -neu Wyniki_przeliczenia.txt -fa 1.12345 -la 1.12345 -ha 1.123 -fb 1.12345 -lb 1.12345 -hb 1.123

- Drugi kalkulator cmd'kowy Kalkulator_flh2xyz_PL1992_PL2000 wywołanie: python Kalkulator_flh2xyz_PL1992_PL2000.py -m GRS80 -xyz Wyniki_przeliczenia.txt -f 1.12345 -l 1.12345 -ha 1.123 -output dec_degree

- Trzeci kalkulator cmd'kowy Kalkulator_xyz2flh_PL1992_PL2000.py wywołanie: python Kalkulator_xyz2flh_PL1992_PL2000.py -m GRS80 -xyz Wyniki_przeliczenia.txt -x 1.12345 -y 1.12345 -z 1.12345 -output dec_degree
