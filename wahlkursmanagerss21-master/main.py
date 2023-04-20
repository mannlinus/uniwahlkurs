import pandas as pd
import numpy as np

from wahlkursmanagerSS21.Kurs import Kurs
from wahlkursmanagerSS21.Schueler import Schueler
from wahlkursmanagerSS21.Verwaltung import Verwaltung

pfadZuKursDaten = r'./wahlkursmanager/projekte1.csv'
pfadZuSchuelerDaten = r'./wahlkursmanager/schülerwahl1.csv'


def ladeDaten(pfad):
    """Laedt eine .csv-Tabelle gemaess Pfad und gibt die eingelesenen Daten als pandas-Dataframe entsprechend der
    eingelesenen Tabelle zurueck. Ueber das Dataframe-Objekt kann Zeilen- und Spaltenweise iteriert werden,
    es kann aber auch ueber dataframe.loc[zeile, spalte] auf einzelne Zellen direkt zugegriffen werden."""

    return pd.read_csv(pfad, sep=";", encoding='ISO-8859-1')


kursDaten = ladeDaten(pfadZuKursDaten)
schuelerDaten = ladeDaten(pfadZuSchuelerDaten)


def findeKurs(id, alleKurse):
    """ Hilfsfunktion: Gibt aus einer Liste aller Kursobjekte das Kursobjekt,
    das zu dem String "id" gehoert zurueck, ansonsten Fehlermeldung."""

    for i in range(len(alleKurse)):
        if (alleKurse[i].nr == id):
            return alleKurse[i]
    if (str(id) == "nan"):
        print("In Schuelertabelle fehlt eine Erst-, Zweit- oder Drittwahl")
    else:
        print("Kurs aus Schuelertabelle " + str(id) + " existiert nicht!")
    # error()


def transformiereBool(string):
    """ Hilfsfunktion: Wandelt ein "x" in den Boolschen Wert "True" um und liefert ansonsten "False"."""

    if (string == "x"):
        return True
    else:
        return False


def ladeDatenKlassen():
    """ Benoetigt Pfad-Angaben fuer .csv Input-Dateien fuer Projekte (Kurse) und Schuelerwahlen.
    Greift auf Variablen kursDaten und schuelerDaten zu und  wandelt sie in Objekte mit Attributen fuer
    jeden Kurs und jeden Schueler um. Liefert eine Objektliste der Schueler und Kurse zurueck."""

    alleKurse = list()
    alleSchueler = list()

    for _, row in kursDaten.iterrows():
        gesetzt = transformiereBool(row["gesetzt"])
        kurs = Kurs(id=row["Projekt"], nr=row["Nr"], min=row["min_Teilnehmer"], max=row["max_Teilnehmer"],
                    gesetzt=gesetzt)
        alleKurse.append(kurs)

    for _, row in schuelerDaten.iterrows():
        erstwahl = findeKurs(row["erstwahl"], alleKurse)
        zweitwahl = findeKurs(row["zweitwahl"], alleKurse)
        drittwahl = findeKurs(row["drittwahl"], alleKurse)
        schueler = Schueler(id=row["Name"], erstwahl=erstwahl, zweitwahl=zweitwahl, drittwahl=drittwahl)
        alleSchueler.append(schueler)
    return alleKurse, alleSchueler


def fuelleKursDatenSpalten(kursDaten, verwaltung):
    """Befuellt einzelne Spalten der Kurs-Daten mit Werten der Felder der Kurs-Objekte aus dem Verwaltungs-Objekt."""

    for kurs in verwaltung.alleKurse:
        index = kursDaten[kursDaten['Nr'] == kurs.nr].index
        kursDaten.loc[index, 'Anzahl_Erstwahlen'] = kurs.anzahlErstwahlen
        kursDaten.loc[index, 'Anzahl_Zweitwahlen'] = kurs.anzahlZweitwahlen
        kursDaten.loc[index, 'Anzahl_Drittwahlen'] = kurs.anzahlDrittwahlen
        kursDaten.loc[index, 'Anzahl_Teilnehmer'] = kurs.real
        kursDaten.loc[index, 'Findet_Statt'] = 'x' if kurs.findetStatt else ''


def fuelleSchuelerDatenSpalten(schuelerDaten, verwaltung):
    """Befuellt einzelne Spalten der Schueler-Daten mit Werten der Felder der Schueler-Objekte aus dem Verwaltungs-Objekt."""

    for schueler in verwaltung.alleSchueler:
        index = schuelerDaten[schuelerDaten['Name'] == schueler.id].index
        schuelerDaten.loc[index, 'Zugewiesen'] = schueler.ergebnis.nr
        schuelerDaten.loc[index, 'Strafpunkte'] = schueler.strafpunkte
    schuelerDaten.loc[0, 'Gesamt_Strafpunkte'] = verwaltung.berechneBewertung()


def ausgabe(kursDaten, pfadZuKursDaten, schuelerDaten, pfadZuSchuelerDaten, verwaltung, suffix):
    """Befuellt einzelne Spalten der Ausgabedatei mit Werten der Attribute der Kurs- und Schueler-Objekte.
    Es werden nur die Eintraege der Schueler mit gueltigen Wahlen befuellt

        Args:
            kursDaten: Die Kurs-Daten
            pfadZuKursDaten: Der Pfad zu den Projekt-Daten
            schuelerDaten: Die Schueler-Daten
            pfadZuSchuelerDaten: Der Pfad zu den Schueler-Daten
            verwaltung: Das Verwaltungs-Objekt, um dessen Inhalt die Kurs-
                und Schueler-Daten erweitert werden sollen
            suffix: Das Dateinamen-Suffix, das die Ausgabe-Datei haben soll
    """

    # Fuer den Fall, dass das Pogramm mit der Ausgabe einer alten Zuweisung als Eingabe aufgerufen wurde, werden die durch die alte Zuweisung hinzughefuegten Spalten vorher entfernt.
    columns = ['Anzahl_Erstwahlen', 'Anzahl_Zweitwahlen', 'Anzahl_Drittwahlen', 'Anzahl_Teilnehmer', 'Findet_Statt']
    kursDaten = kursDaten.drop(columns, axis=1, errors='ignore')
    for i in columns:
        kursDaten[i] = np.nan
    fuelleKursDatenSpalten(kursDaten, verwaltung)

    columns = ['Zugewiesen', 'Strafpunkte', 'Gesamt_Strafpunkte']
    schuelerDaten = schuelerDaten.drop(columns, axis=1, errors='ignore')
    for i in columns:
        schuelerDaten[i] = np.nan

    fuelleSchuelerDatenSpalten(schuelerDaten, verwaltung)

    kursDaten.to_csv(pfadZuKursDaten.replace('.csv', "") + suffix + '.csv', sep=';', index=False, encoding='ISO-8859-1')
    schuelerDaten.to_csv(pfadZuSchuelerDaten.replace('.csv', "") + suffix + '.csv', sep=';', index=False,
                         encoding='ISO-8859-1')


def zuweisen(alleKurse, alleSchueler):
    """Fuehrt eine vollstaendige Zuweisung durch Aufruf der Verwaltungs-Klasse aus und berechnet dessen Bewertung.
    Rueckgabe: Verwaltungsobjekt, das die Zuweisung enthaelt, sowie Bewertung (als Zahl)."""

    verwaltung = Verwaltung(alleSchueler, alleKurse)
    verwaltung.auswaehlenKurse(1.6)
    verwaltung.zuordneSchueler()
    verwaltung.verteileRestlicheSchueler()
    bewertung = verwaltung.berechneBewertung()
    print("Ergebnis: " + str(bewertung))
    return verwaltung, bewertung


def zuweisenWiederholt(anzahl):
    """ wiederholt zuweisen "Anzahl" oft und gibt das beste ERgebnis aus. Liest jedesmal die Daten neu ein."""
    bewertungBest = np.Infinity
    verwaltungBest = None
    for _ in range(0, anzahl):
        alleKurse1, alleSchueler1 = ladeDatenKlassen()
        verwaltung, bewertung = zuweisen(alleKurse1, alleSchueler1)
        if (bewertung < bewertungBest):
            bewertungBest = bewertung
            verwaltungBest = verwaltung
    print("Bestes Ergebnis: " + str(bewertungBest))
    return verwaltungBest, bewertungBest


if __name__ == '__main__':
    alleKurse1, alleSchueler1 = ladeDatenKlassen()
    # verwaltung, bewertung = zuweisen(alleKurse1, alleSchueler1) # fuehrt eine einzelne Zuordnung zu
    verwaltung, bewertung = zuweisenWiederholt(anzahl=100)
    ausgabe(kursDaten, pfadZuKursDaten, schuelerDaten, pfadZuSchuelerDaten, verwaltung, "_best")



