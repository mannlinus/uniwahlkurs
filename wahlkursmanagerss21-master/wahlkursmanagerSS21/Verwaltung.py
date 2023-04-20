from wahlkursmanagerSS21.Kurs import Kurs
from random import shuffle


class Verwaltung:
    '''
    Klasse, die die Verwaltung der Schueler und Kurse uebernimmt. Sie enthaelt die Methoden und Funktionen,
    um eine Vorauswahl der Kurse zu treffen, Schueler den einzelnen Kursen zuzuordnen sowie Schueler aus Dummykursen
    regulaeren Kurse zuzuordnen.
    '''

    def __init__(self, alleSchueler=list(), alleKurse=list()):
        """Konstruktor fuer Verwaltungs-Objekte."""
        self.alleSchueler = alleSchueler
        self.alleKurse = alleKurse
        self.dummyKurs = Kurs(id="Dummy", nr=-1, min=0, max=len(alleSchueler))

    def auswaehlenKurse(self, x):
        """Vorauswahl der Kurse: x: Faktor, mit dem die Anzahl der minimal benoetigten Kursplaetze multipliziert wird."""

        # Zaehlung der Erst-, Zweit-, und Drittwahlen der Kurse
        for schueler in self.alleSchueler:
            schueler.erstwahl.anzahlErstwahlen += 1
            schueler.zweitwahl.anzahlZweitwahlen += 1
            schueler.drittwahl.anzahlDrittwahlen += 1

        ausgewaehlteKurse = list()
        restKurse = list()

        # Wenn Summe(Kurs.Erstwahlen) >= min, dann wird der Kurs ausgewaehlt
        for kurs in self.alleKurse:
            if (kurs.anzahlErstwahlen >= kurs.min or kurs.gesetzt):
                kurs.findetStatt = True
                ausgewaehlteKurse.append(kurs)
            else:
                kurs.score = kurs.anzahlErstwahlen + 0.5 * kurs.anzahlZweitwahlen + 0.25 * kurs.anzahlDrittwahlen
                restKurse.append(kurs)
        restKurse.sort(key=lambda x: x.score, reverse=True)

        # Wenn Summe(ausgewaehlteKurse.max) < Summe(alleSchueler) * x, nimm weitere Kurse in Reihenfolge ihrer Beliebheit hinzu
        maxSum = 0
        for aKurs in ausgewaehlteKurse:
            maxSum += aKurs.max
        while (maxSum < len(self.alleSchueler) * x):
            for rkurs in restKurse:
                rkurs.findetStatt = True
                ausgewaehlteKurse.append(rkurs)
                restKurse.remove(rkurs)
                maxSum += rkurs.max
                break

    def zuordneSchueler(self):
        """Zuordnung der Schueler zu den Kursen."""

        shuffle(self.alleSchueler)

        for s in self.alleSchueler:
            if (s.erstwahl.findetStatt and s.erstwahl.real < s.erstwahl.max):
                s.ergebnis = s.erstwahl
                s.erstwahl.real += 1
                s.erstwahl.ergebnis.append(s)
            elif (s.zweitwahl.findetStatt and s.zweitwahl.real < s.zweitwahl.max):
                s.ergebnis = s.zweitwahl
                s.zweitwahl.real += 1
                s.zweitwahl.ergebnis.append(s)
            elif (s.drittwahl.findetStatt and s.drittwahl.real < s.drittwahl.max):
                s.ergebnis = s.drittwahl
                s.drittwahl.real += 1
                s.drittwahl.ergebnis.append(s)
            else:
                s.ergebnis = self.dummyKurs
                self.dummyKurs.real += 1
                self.dummyKurs.ergebnis.append(s)

    def aktualisiereStrafpunkte(self):
        """Aktualisiert die Strafpunkte der Schueler."""
        for s in self.alleSchueler:
            if (s.ergebnis == s.erstwahl):
                s.strafpunkte = 0
            elif (s.ergebnis == s.zweitwahl):
                s.strafpunkte = 1
            elif (s.ergebnis == s.drittwahl):
                s.strafpunkte = 3
            elif (s.ergebnis == self.dummyKurs):
                s.strafpunkte = 1000
            else:
                s.strafpunkte = 1000

    def verteileRestlicheSchueler(self):
        """Weist den restlichen Schuelern aus dem Dummy-Kurs einen realen Kurs zu."""
        for s in self.dummyKurs.ergebnis:
            for kurs in self.alleKurse:
                if (kurs.real < kurs.max and kurs.findetStatt):
                    s.ergebnis = kurs
                    kurs.real += 1
                    kurs.ergebnis.append(s)
                    self.dummyKurs.real -= 1
                    break
        self.dummyKurs.ergebnis = ()
        assert (self.dummyKurs.real == 0)

    def berechneBewertung(self):
        """Berechnet die Bewertung der Zuordnung."""
        self.aktualisiereStrafpunkte()

        bewertung = 0
        for i in range(len(self.alleSchueler)):
            bewertung += self.alleSchueler[i].strafpunkte
        return bewertung
