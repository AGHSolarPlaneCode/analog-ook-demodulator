import lgpio, time
from enum import Enum

GPIO_CHIP        = 4
GPIO_PIN         = 17
TOLERANCJA       = 0.10
MIN_POTWIERDZEN  = 4

class Stan(Enum):
    OCZEKIWANIE  = 0
    HIGH_AKTYWNY = 1
    LOW_AKTYWNY  = 2

class AutomatStanow:
    def __init__(self, pin=GPIO_PIN):
        self.pin        = pin
        self.stan       = Stan.OCZEKIWANIE
        self.t_zbocze   = None
        self.ok_cykle   = 0
        self._pol_okres = None
        self.h          = lgpio.gpiochip_open(GPIO_CHIP)
        lgpio.gpio_claim_input(self.h, pin)
        self._cb = lgpio.callback(
            self.h, pin, lgpio.BOTH_EDGES, self._na_zbocze
        )

    def _na_zbocze(self, chip, gpio, level, tick):
        now = tick / 1_000_000_000.0    #uzycie tick jest dokaldniejsze
        pp = self._pol_okres
        if pp is None: return

        if level == 1:                             #narastające
            if self.stan == Stan.LOW_AKTYWNY and self.t_zbocze:
                czas_low = now - self.t_zbocze
                if abs(czas_low - pp) / pp <= TOLERANCJA:
                    self.ok_cykle += 1
                else:
                    self.ok_cykle = 0
            self.stan = Stan.HIGH_AKTYWNY
            self.t_zbocze = now

        elif level == 0:                           #opadające
            if self.stan == Stan.HIGH_AKTYWNY and self.t_zbocze:
                czas_high = now - self.t_zbocze
                if abs(czas_high - pp) / pp > TOLERANCJA:
                    self.ok_cykle = 0           # błędna faza HIGH
            self.stan     = Stan.LOW_AKTYWNY
            self.t_zbocze = now

    def wykryj(self, docelowa_hz, timeout_s=None):
        self.ok_cykle   = 0
        self.stan       = Stan.OCZEKIWANIE
        self._pol_okres = 1.0 / (2 * docelowa_hz)

        if timeout_s is None:
            timeout_s = (MIN_POTWIERDZEN + 3) / docelowa_hz

        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline:
            if self.ok_cykle >= MIN_POTWIERDZEN:
                return True, docelowa_hz
            time.sleep(0.002)

        return False, 0.0

    def zamknij(self):
        self._pol_okres = None
        self._cb.cancel()
        lgpio.gpiochip_close(self.h)