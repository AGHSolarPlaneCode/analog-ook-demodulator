import time
# Importujemy Twoją maszynę z pliku detektor.py
from detector import AutomatStanow, MIN_POTWIERDZEN

def wykrywanie():
    szukana_czestotliwosc = 10  
    
    print(f" szykamy czestotliwosci {szukana_czestotliwosc} Hz.")
    
    detektor = AutomatStanow(pin=17)
    
    try:
        print("jesmy nad ladowiskiem, wlaczamy czujnik")
        
        # 3. Odpalamy naszą maszynę stanów. 
        # Program główny zawiesza się tutaj na np. 2-3 sekundy i czeka na werdykt.
        sukces, wykryto_hz = detektor.wykryj(docelowa_hz=szukana_czestotliwosc)
        
        # 4. Podejmujemy decyzję na podstawie tego, co zwróciła maszyna
        if sukces:
            print(f"[SUKCES] Złapano {MIN_POTWIERDZEN} idealne cykle! Potwierdzono lądowisko {wykryto_hz} Hz.")
            
        else:
            print("[BŁĄD] Nie wykryto czystego sygnału. To fałszywe lądowisko lub szum.")
                   
    finally:
        print("koniec wykrywania")
        detektor.zamknij()

if __name__ == "__main__":
    wykrywanie()