Inna metoda rozpoznawania modulacji, na podstawie danych z czujnika, tym razem mierzymy czas trwania i stanu wysokiego i stanu niskiego,
sprawdzamy czy obie sa rowne okolo polowie okresu wynikajacego z szukanej modulacji.  
jesli w ogrnaiczonym czasie zbierzemy zadana liczbe pomiarow z rzedu ktore spelniaja waruki to zwracamy True --> wykryto, jesli nie to False
kazdy "zly" pomiar zeruje licznik pasujących pomiarów 
Konkretne wartosci sa jeszcze do ustalenia z testow
