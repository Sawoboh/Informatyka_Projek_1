# Informatyka_Projekt_1

Program służy do przeliczenia poprzez odpowiednie trasformacjie współrzędnych ortokartezjańskich geocentrycznych [X, Y, Z] lub współrzędnych geodezyjnych elipsoidealnych [f, l, h] do współrzędnych; topocentrycznych [n, e, u], współrzędnych płaskich PL1992 [x1992, y1992] oraz współrzędnych płaskich PL2000 [x2000, y2000]
Przeliczenia są możliwe tylko dla elipsoid; [GRS80, WGS84, Krasowski].

Program wymaga posiadania następujących bibliotek: tkinter, pytest, numpy, os, argarse.

Program napisany jest dzięki językowi programowania PYTHON.
Program napisany jest dla systemu Windows.
Program został testowany na Windows11, Windows10, Python 3.9.10 oraz Python 3.10.

Program posiada 4 kalkulatory cmd'kowe, 1 kalkulator graficzny, 1 plik, który sprawdza poprawność funkcji, 1 plik przeliczający dane z notatnika do innego notatnika.

Błędy: Program nie działa dla obliczenia kordynatów [X,Y,Z] = [0,0,0], kalkulator graficzny może źle działać jak użytkownik usunie dane z tablicy danych jeżeli takowej nie ma w folderze programu.


- Pierwszy kalkulator cmd'kowy Kalkulator_flh2neu wywołanie: python Kalkulator_flh2neu.py -m GRS80 -neu Wyniki_przeliczenia1.txt -fa 1.12345 -la 1.12345 -ha 1.123 -fb 1.12345 -lb 1.12345 -hb 1.123.

- Drugi kalkulator cmd'kowy Kalkulator_flh2xyz_PL1992_PL2000 wywołanie: python Kalkulator_flh2xyz_PL1992_PL2000.py -m GRS80 -xyz Wyniki_przeliczenia2.txt -f 1.12345 -l 1.12345 -ha 1.123 -output dec_degree.

- Trzeci kalkulator cmd'kowy Kalkulator_xyz2flh_PL1992_PL2000 wywołanie: python Kalkulator_xyz2flh_PL1992_PL2000.py -m GRS80 -xyz Wyniki_przeliczenia3.txt -x 1.12345 -y 1.12345 -z 1.12345 -output dec_degree.

- Czwarty kalkulator cmd'kowy Kalkulator_xyz2neu wywołanie: python Kalkulator_xyz2neu.py -m GRS80 -neu Wyniki_przeliczenia4.txt -xa 1.12345 -ya 1.12345 -za 1.12345 -xb 1.12345 -yb 1.12345 -zb 1.12345.

- Pierwszy kalkulator graficzny Kalkulator_graficzny_xyz2flh_PL1992_PL2000 wywołanie: naciśnięcie LPM na plik w folderze.

- Pierwszy plik sprawdzający działanie funkcji wywołanie: python -m pytest Testy_dla_funkcji.py -vvv

- Pierwszy plik przyjmujący dane z notatnika, który przeliczy dane do drugiego notatnika i wyświetli tam wyniki wywołanie: -m GRS80 -t Dane.txt -d dec_degree -xyz Wyniki_przeliczeń_flh_PL1992_PL2000.txt -neu Wyniki_przeliczeń_neu.txt
