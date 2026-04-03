from detector import pomiar_okresu

TARGET = 10
detektor = pomiar_okresu()

try:
    wykryto, zmierzono = detektor.wykryj(TARGET)
    print(f"{'WYKRYTO' if wykryto else 'NIE WYKRYTO'}")
    print(f"  cel: {TARGET} Hz | zmierzono: {zmierzono:.2f} Hz")
finally:
    detektor.zamknij()

