import lgpio
import time
import threading
from detector import AutomatStanow

CHIP           = 4
PIN_ODBIORNIKA = 17  # Nasz detektor
PIN_NADAJNIKA  = 18  # Nasz sztuczny generator sygnału

def generuj_sygnal(docelowa_hz, czas_trwania_s):

    h = lgpio.gpiochip_open(CHIP)
    lgpio.gpio_claim_output(h, PIN_NADAJNIKA)
    
    okres = 1.0 / docelowa_hz
    polowa_okresu = okres / 2.0
    deadline = time.monotonic() + czas_trwania_s
    
    try:
        while time.monotonic() < deadline:
            lgpio.gpio_write(h, PIN_NADAJNIKA, 1)  # Włącz 
            time.sleep(polowa_okresu)
            lgpio.gpio_write(h, PIN_NADAJNIKA, 0)  # Wyłącz
            time.sleep(polowa_okresu)
    finally:
        lgpio.gpiochip_close(h)



if __name__ == "__main__":
    SZUKANE_HZ = 10
    CZAS_TESTU = 5
    
    print(f"--- START TESTU ---")
    print(f"Uruchamiam sztuczny nadajnik: {SZUKANE_HZ} Hz na pinie {PIN_NADAJNIKA}...")
    
    #Uruchamiamy nadajnik w tle
    nadajnik = threading.Thread(
        target=generuj_sygnal, 
        args=(SZUKANE_HZ, CZAS_TESTU)
    )
    nadajnik.start()
    
    time.sleep(0.2)
    
    # 2. Tworzymy Twój obiekt do pomiaru
    detektor = AutomatStanow(pin=PIN_ODBIORNIKA)
    
    try:
        print(f"Detektor nasłuchuje na pinie {PIN_ODBIORNIKA}...")
        wykryto, zmierzono = detektor.wykryj(SZUKANE_HZ)
        
        if wykryto:
            print(f">>> SUKCES! Detektor prawidłowo wykrył sygnał: {zmierzono:.2f} Hz")
        else:
            print(">>> PORAŻKA. Detektor nic nie wykrył (Timeout).")
            
    finally:
        detektor.zamknij()