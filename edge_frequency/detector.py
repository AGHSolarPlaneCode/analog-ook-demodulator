import lgpio, time
from collections import deque


GPIO_CHIP = 4
GPIO_PIN = 17
TOLERANCJA  = 0.05
MIN_CYKLI = 5


class pomiar_okresu:
    def __init__(self, pin=GPIO_PIN):
        self.pin = pin
        self.last_rise = None
        self.periods = deque(maxlen=10)
        self.h = lgpio.gpiochip_open(GPIO_CHIP) #otwieramy polaczenie
        lgpio.gpio_claim_input(self.h, pin)     # ustawienie pinu na input
        self._cb = lgpio.callback(
            self.h, pin, lgpio.RISING_EDGE, self._na_zbocze   #jesli na pinie zmieni sie 0 na 1 to wykonujemy _na_zbocze
        )
    def _na_zbocze(self, chip, pin, gpio, level, tick):
        teraz = time.perf_counter()                  #time.perf_counter() jest dokladniejsze niz monotonic
        if self.last_rise is not None:
            okres = teraz - self.last_rise
            if 0.004 < okres < 0.7:             # lapiemy od 1,43hz do 143hz
                self.periods.append(okres)
        self.last_rise = teraz

    def wykryj(self, cel_hz, timeout=None):
        if timeout is None:
            timeout = (MIN_CYKLI + 2) / cel_hz   #czas  badania modulacji, +2 bo +1 bo lapiemy 5 przerw miedzy puknktami, czyli 6 punktow(zbocz) i +1 jesli zaczelisbysmy pomiear zaras po zboczu
        
        oczekiwany_okres = 1.0 / cel_hz
        koniec_pomiaru = timeout + time.monotonic()
        
        while time.monotonic() < koniec_pomiaru:
            if len(self.periods) >= MIN_CYKLI:
                sredni = sum(self.periods) / len(self.periods)
                odchylenie = abs(sredni - oczekiwany_okres) / oczekiwany_okres
                if odchylenie <= TOLERANCJA:
                    return True, 1.0 / sredni
            time.sleep(0.005)                      # nie chce sprawdzac caly czas bo usmazymy cpu, tylko sprawdzamy czy mamy wystarczajaco cykli wiec mozemy ustawic sztywna wartosc
        return False, 0.0                          # brak sygnalu
    
    def zamknij(self):
        self._cb.cancel()
        lgpio.gpiochip_close(self.h)