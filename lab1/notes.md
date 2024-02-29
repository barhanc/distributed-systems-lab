# Warstwa transportowa

Styk warstwy transportowej i warstwy sesji jest ustandaryzowany i obowiązuje tzw. *interfejs
socketowy*. Warstwa transportowa zapewnia niezawodne przesyłanie danych. Zasadniczo wyróżniamy dwa
protokoły:
- TCP - ma charakter **połączeniowy** tzn. składa się z etapów nawiązania połączenia, uzgadniania
  parametrów połączenia, przesyłania danych i zakończenia połączenia

- UDP - ma charakter **bezpołączeniowy** tzn. składa się tylko z etapu transmisji danych


### Porty

Na poziomie warstwy transportowej adresacja *procesu* działającego w ramach systemu operacyjnego
opiera się o *porty*. Proces uzyskuje dostęp do określonego portu - abstrakcyjnego punktu docelowego
identyfikowanego za pomocą dodatniej liczby całkowitej (2B); działa to poniekąd jak deskryptor
pliku.

Port identyfikuje "skrzynkę odbiorczo/nadawczą", do której proces może pisać i z której może czytać
dane. Odpowiednikiem adresacji w warstwie transportowej są właśnie porty.

### Porty - programowanie

* *asocjacja* = (protokół [TCP/UDP], adr. lok. [adr. IP komp.], proc. lok. [port lok.], adr. obcy
[adr. IP zdalny], proc. obcy [port zdalny])

* *gniazdo* (*socket*, *półasocjacja*) = (protokół, adr. [lok. lub obcy], proc. [lok. lub obcy])

Zestaw dobrze znanych portów określa porty, z którymi mogą łączyć się klienci np. 21 FTP, 23 Telnet,
25 Mail, 80 HTTP.

*Porty efemeryczne* - krótkotrwałe, przypisywane procesom tylko na czas połączenia (numery > 1023)

### TCP (Transmission Control Protocol)

* możliwość przesyłania strumieni danych bez konieczności wpisywania w każdy program obsługi błędów
* połączeniowy - każde połączenie ma dokładnie dwa końce, za pomocą połączenia możliwa jest
  transmisja w obie strony (full-duplex)
* niezawodny - potwierdzenia odbioru, retransmisje, kontrola przepływu danych, FCS dla nagłówka i
  danych, porządkowanie kolejności segmentów, usuwanie zdublowanych segmentów, kontrola przeciążeń
* point-point


TCP specyfikuje format danych oraz procedury inicjalizacji i zamykania połączenia. Nie specyfikuje
natomiast API.

#### Nagłówek TCP
Rozmiar = 20B + opcje
```

nr portu src (16b)   |   nr portu dst (16b)
-------------------------------------------
            nr sekwencyjny (32b)
-------------------------------------------
len (4b) | r (6b) | flags (6b) | rozm. okna
-------------------------------------------
suma kontr. (16b)    |  wsk. ważności (16b)
-------------------------------------------
                   opcje

-------------------------------------------
                    dane

-------------------------------------------
```

rozmiar okna - ilość miejsca wolnego w buforze odbiorczym na kolejne dane od nadawcy (tak
realizowana jest kontrola przepływu)

TCP stosujemy przy przesyłaniu danych wrażliwych na gubienie pakietów. Jest to protokół dość
skomplikowany, nie pozwala na transmisję grupową.

### UDP (User Datagram Protocol)

UDP to prosty, bezpołączeniowy protokół warstwy transportowej. Jest szybki, ale zawodny: nie ma
potwierdzeń, kontroli przepływu.


```
netstat [-p | -a | -b] - wyświetla używane gniazda [protokół | all (domyślnie tylko połączone) | nazwy procesów]
```

* Kolejność bajtów w pamięci (byte order / endianness):
    * Big endian np. dla liczby 59DC ACF0 | 59 | DC | AC | F0 |
    
    * Little endian np. dla liczby 59DC ACF0 | F0 | AC | DC | 59 | (najmłodszy” bit/bajt na
      początku, tzn. pod najniższym adresem, „najstarszy” bit/bajt na końcu.)

* W praktyce współczesne kompilatory (takie jak GCC) na maszynach 32-bitowych zazwyczaj stosują typy
  o następujących rozmiarach:

    * short int ma 16 bitów
    
    * int jest równy long int i ma 32 bity
    
    * long long int ma 64 bity
