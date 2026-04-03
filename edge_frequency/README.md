##### wykrywacz częstotliwości modulacji ON/OFF dla Raspberry Pi.

Metoda mierzenia okresow





* mierzymy okres między zboczami narastającymi sygnału.
* Wykorzystuje przerwania sprzętowe (callbacki) biblioteki lgpio.
* Automatyczne odrzucanie szumów i uśrednianie ostatnich 5-10 próbek.



test.py

Symulacja czujnika bez dodatkowego sprzętu:



zakładamy ze laczymy przewodem Pin 18 (Nadajnik) z Pinem 17 (Odbiornik).

Skrypt w osobnym wątku generuje sygnał na pinie 18.

Detektor na pinie 17 odbiera dane i weryfikuje ich poprawność.





Pliki

* detector.py – Klasa PomiarOkresu (serce systemu).
* main.py – Przykład użycia detektora.
* test.py – Pełny test symulujący działanie czujnika.





pobranie na linux

sudo apt update \&\& sudo apt install python3-lgpio

