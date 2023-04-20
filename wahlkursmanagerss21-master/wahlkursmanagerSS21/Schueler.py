class Schueler(object):
    '''
    Objekte dieser Klasse stehen fuer einen einzelnen Schueler
    '''

    def __init__(self, id="", erstwahl=None, zweitwahl=None, drittwahl=None, ergebnis=None):
        """Konstruktor fuer Schueler-Objekte

        Args:
            id: Name des Schuelers
            erstwahl: Erstwahl des Schuelers
            zweitwahl: Zweitwahl des Schuelers
            drittwahl: Drittwahl des Schuelers
            ergebnis: Dem Schueler zugewiesener Kurs
        """
        self.id = id
        self.erstwahl = erstwahl
        self.zweitwahl = zweitwahl
        self.drittwahl = drittwahl
        self.ergebnis = ergebnis
        self.strafpunkte = 0

    def __str__(self):
        return "id: {0}, erstwahl: {1}, zweitwahl: {2}, drittwahl: {3}, ergebnis: {4}, strafpunkte: {5}".format(self.id,
                                                                                                                self.erstwahl,
                                                                                                                self.zweitwahl,
                                                                                                                self.drittwahl,
                                                                                                                self.ergebnis,
                                                                                                                self.strafpunkte)