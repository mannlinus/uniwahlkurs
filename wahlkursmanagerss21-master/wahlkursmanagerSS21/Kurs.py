class Kurs(object):

    def __init__(self, id="", nr=-1, min=0, max=100, gesetzt=False, real=0, findetStatt=False):
        """Konstruktor fuer Kurs-Objekte

        Args:
            id: Name des Kurses
            nr: Kursnummer
            min: Mindest-Teilnehmerzahl
            max: Hoechst-Teilnehmerzahl
            gesetzt: Gibt an, ob der Kurs gesetzt ist
            real: Anzahl der Kurs-Teilnehmer
            findetStatt: Gibt an, ob der Kurs stattfindet
        """

        self.id = id
        self.nr = nr
        self.min = min
        self.max = max
        self.gesetzt = gesetzt
        self.real = real
        self.findetStatt = findetStatt
        self.ergebnis = list()
        self.anzahlErstwahlen = 0
        self.anzahlZweitwahlen = 0
        self.anzahlDrittwahlen = 0
        self.score = 0

    def __str__(self):
        return "id: {0}, nr: {1}, min: {2}, max: {3}, gesetzt: {4}, real: {5}, findetStatt: {6}".format(self.id,
                                                                                                        self.nr,
                                                                                                        self.min,
                                                                                                        self.max,
                                                                                                        self.gesetzt,
                                                                                                        self.real,
                                                                                                        self.findetStatt)