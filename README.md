# Informatyka_Projekt_1

Program służy do przeliczenia poprzez odpowiednie trasformacje współrzędnych ortokartezjańskich geocentrycznych [X, Y, Z] [metry] lub współrzędnych geodezyjnych elipsoidealnych [f, l, h] [ do współrzędnych; topocentrycznych [n, e, u] [metry], współrzędnych płaskich PL1992 [x1992, y1992] [metry] oraz współrzędnych płaskich PL2000 [x2000, y2000] [metry].
Przeliczenia są możliwe tylko dla elipsoid; [GRS80, WGS84, _Krasowski - błędne przeliczenia._].

Program wymaga posiadania następujących bibliotek: tkinter, pytest, numpy, os, argarse.

Program napisany jest dzięki językowi programowania PYTHON.
Program napisany jest dla systemu Windows.
Program został testowany na Windows11, Windows10, Python 3.9.10 oraz Python 3.10.

Program posiada 4 kalkulatory cmd'kowe, 1 kalkulator graficzny, 1 plik, który sprawdza poprawność funkcji, 1 plik przeliczający dane z notatnika do innego notatnika.

Błędy: Program nie działa dla obliczenia kordynatów [X,Y,Z] = [0,0,0], kalkulator graficzny może źle działać jak użytkownik usunie dane z tablicy danych jeżeli takowej nie ma w folderze programu. Program przy pobieraniu danych i zapisywaniu danych do nowego notatnika tworzy zamiast dwóch cztery pliki tekstowe.
**Transformacje dla elipsoidy Krasowskiego dają błędne wyniki dla układu PL2000 i układu PL1992, dlatego nie można ich używać. Powód: Funckje zostały źle zaimplementowane.**

- Pierwszy kalkulator cmd'kowy Kalkulator_flh2neu wywołanie: python Kalkulator_flh2neu.py -m GRS80 -neu Wyniki_przeliczenia1.txt -fa 1.12345 -la 1.12345 -ha 1.123 -fb 1.12345 -lb 1.12345 -hb 1.123.
Punktem będącym początkiem układu NEU jest punkt punkt a.
[-m] - [GRS80, WGS84, Krasowski] - wybranie modelu elipsoidy.
[-neu] - [Nazwapliku.rozszerzenie] - wybranie nazwy i rozrzezenia pliku - tak zostanie zapisany plik wynikowy.
[-fa, -la, -ha, -fb, -lb, -hb] - [stopnie dziesietne] - współrzędne geodezyjne elipsoidealne punktów [a, b], wysokość [metry].
Wyniki: Współrzędne topocentryczne [n, e, u] [metry].

- Drugi kalkulator cmd'kowy Kalkulator_flh2xyz_PL1992_PL2000 wywołanie: python Kalkulator_flh2xyz_PL1992_PL2000.py -m GRS80 -xyz Wyniki_przeliczenia2.txt -f 1.12345 -l 1.12345 -ha 1.123 -output dec_degree.
[-m] - [GRS80, WGS84, Krasowski] - wybranie modelu elipsoidy.
[-xyz] - [Nazwapliku.rozszerzenie] - wybranie nazwy i rozrzezenia pliku - tak zostanie zapisany plik wynikowy.
[-f, -l, -ha] - [stopnie dziesietne] - współrzędne geodezyjne elipsoidealne punktu, wysokość [metry].
[-output] - [dms/dec_degree/radiany] - wybieramy w jakich jednostkach chcemy mieć wyniki.
Wyniki: Współrzędne ortokartezjańskie geocentryczne [Jednostki wybrane przez użytkownika], współrzędne płaskie PL1992 [metry], współrzędne płaskie PL2000 [metry]. [x, y, z, h, x1992, y1992, x2000, y2000].

- Trzeci kalkulator cmd'kowy Kalkulator_xyz2flh_PL1992_PL2000 wywołanie: python Kalkulator_xyz2flh_PL1992_PL2000.py -m GRS80 -xyz Wyniki_przeliczenia3.txt -x 1.12345 -y 1.12345 -z 1.12345 -output dec_degree.
[-m] - [GRS80, WGS84, Krasowski] - wybranie modelu elipsoidy.
[-xyz] - [Nazwapliku.rozszerzenie] - wybranie nazwy i rozrzezenia pliku - tak zostanie zapisany plik wynikowy.
[-x, -y, -z] - [metry] - współrzędne ortokartezjańskie geocentryczne punktu.
[-output] - [dms/dec_degree/radiany] - wybieramy w jakich jednostkach chcemy mieć wyniki.
Wyniki: Współrzędne geodezyjne elipsoidealne [Jednostki wybrane przez użytkownika], współrzędne płaskie PL1992 [metry], współrzędne płaskie PL2000 [metry]. [f, l, h, x1992, y1992, x2000, y2000].

- Czwarty kalkulator cmd'kowy Kalkulator_xyz2neu wywołanie: python Kalkulator_xyz2neu.py -m GRS80 -neu Wyniki_przeliczenia4.txt -xa 1.12345 -ya 1.12345 -za 1.12345 -xb 1.12345 -yb 1.12345 -zb 1.12345.
Punktem będącym początkiem układu NEU jest punkt punkt a.
[-m] - [GRS80, WGS84, Krasowski] - wybranie modelu elipsoidy.
[-neu] - [Nazwapliku.rozszerzenie] - wybranie nazwy i rozrzezenia pliku - tak zostanie zapisany plik wynikowy.
[-xa, -ya, -za, -xb, -yb, -zb] - [metry] - współrzędne geodezyjne elipsoidealne punktów [a, b].
Wyniki: Współrzędne topocentryczne [n, e, u] [metry].

- Pierwszy kalkulator graficzny Kalkulator_graficzny_xyz2flh_PL1992_PL2000 wywołanie: naciśnięcie LPM na plik w folderze.
[pierwszy wiersz danych] - [GRS80, WGS84, Krasowski] - wybranie modelu elipsoidy.
[drugi wiersz danych] - [metry] - Trzeba podać współrzędną ortokartezjańską geocentryczną 'X'.
[trzeci wiersz danych] - [metry] - Trzeba podać współrzędną ortokartezjańską geocentryczną 'Y'.
[czwarty wiersz danych] - [metry] - Trzeba podać współrzędną ortokartezjańską geocentryczną 'Z'.
[piąty wiersz danych] - [TAK/NIE] - Użytkownik podaje, czy chce zapisać przeliczenie do notatnika.
[szósty wiersz danych] - [dms/stopnie_dziesiętne/radiany] - Użytkownik wybiera w jakich jednostkach mają zostać zapisane dane do notatnika.
[siódmy wiersz danych] - [TAK/NIE] - Użytkownik wybiera, czy tablica wyników ma zostać wyczyszczona.
Wyniki: Współrzędne geodezyjne elipsoidealne [Jednostki wybrane przez użytkownika], współrzędne płaskie PL1992 [metry], współrzędne płaskie PL2000 [metry]. [f, l, h, x1992, y1992, x2000, y2000].

- Pierwszy plik Testy_dla_funkcji sprawdzający działanie funkcji wywołanie: python -m pytest Testy_dla_funkcji.py -vvv
[wersja poprawna] - [wszystkie testy PASSED] - program działa dobrze.
[werscja niepoprawna] - [conajmniej jeden test FAILURE] - program niedziała dobrze. Sprawdź, czy używasz wersji oprogramowania Windows10/Windows11, bądź Python(3.9.10)/Python(3.10).
Wyniki: Testy przeszły negatywnie, bądź pozytywnie. [PASSED/FAILURE]

- Pierwszy plik Transformacje_Projekt przyjmujący dane z notatnika (przykładowy notatnik z danymi "wsp_inp.txt" znaduję się w folderze do pobrania na githubie). Pierwsze cztery wiersze pliku txt są wierszami opisowymi - nie powinny zawierać danych. W kolejnych wierszach należy wpisać współrzędne kartezjańskie w odpowiedniej kolejności - [X,Y,Z]. Dane oddzielić przecinkiem przykład: (100.100,200.200,300.300). Program przeliczy dane do drugiego notatnika i wyświetli tam wyniki wywołanie: python Transformacje_Projekt.py -m GRS80 -t Dane.txt -d dec_degree -xyz Wyniki_przeliczeń_flh_PL1992_PL2000.txt -neu Wyniki_przeliczeń_neu.txt
[-m] - [GRS80, WGS84, Krasowski] - wybranie modelu elipsoidy.
[-t] - [Nazwapliku.rozszerzenie] - zaimplementowanie danych do programu.
[-d] - [dms/dec_degree/radiany] - wybranie jednostek w jakich ma się zapisać [f,l] do notatnika [h] [metry] będzie zapisane w metrach.
[-xyz] - [Nazwapliku.rozszerzenie] - wybranie nazwy i rozrzezenia pliku - tak zostanie zapisany plik wynikowy dla wyników bez neu.
[-neu] - [Nazwapliku.rozszerzenie] - wybranie nazwy i rozrzezenia pliku - tak zostanie zapisany plik wynikowy tylko wyniki neu.
Wyniki: Współrzędne geodezyjne elipsoidealne [Jednostki wybrane przez użytkownika], współrzędne płaskie PL1992 [metry], współrzędne płaskie PL2000 [metry]. [f, l, h, x1992, y1992, x2000, y2000].
