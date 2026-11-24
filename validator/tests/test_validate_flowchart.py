"""Unit-Tests für validate_flowchart.py (Abnahmekontrakt: 22 Tests)."""

import contextlib
import io
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from validate_flowchart import main, validiere_text  # noqa: E402

REFERENZ = """flowchart TD
    start(["Start"]) --> eingabe[/"Bestellmenge erfassen"/]
    eingabe --> pruefung["Verfügbarkeit prüfen"]
    pruefung --> versand["Versand auslösen"]
    versand --> ende(["Ende"])
"""

ENTSCHEIDUNG = """flowchart TD
    start(["Start"]) --> freigabe{"Freigabe erteilt?"}
    freigabe -->|"Ja"| ausfuehren["Auftrag ausführen"]
    freigabe -->|"Nein"| ablehnen["Auftrag ablehnen"]
    ausfuehren --> ende(["Ende"])
    ablehnen --> ende
"""


def rumpf(*zeilen):
    """Baut ein gültiges Gerüst (Start/Ende) um die angegebenen Zeilen."""
    mitte = "\n".join("    " + z for z in zeilen)
    return 'flowchart TD\n    start(["Start"]) --> schritt["Schritt"]\n%s\n    schritt --> ende(["Ende"])\n' % mitte


class GueltigeDiagramme(unittest.TestCase):
    def test_referenzdiagramm(self):
        b = validiere_text(REFERENZ)
        self.assertEqual(b.fehler, [])
        self.assertEqual(b.warnungen, [])

    def test_entscheidung_ja_nein(self):
        b = validiere_text(ENTSCHEIDUNG)
        self.assertEqual(b.fehler, [])
        self.assertEqual(b.warnungen, [])


class Fehlerregeln(unittest.TestCase):
    def assertCode(self, text, code):
        self.assertIn(code, validiere_text(text).codes())

    def test_e01a_graph_td(self):
        self.assertCode(REFERENZ.replace("flowchart TD", "graph TD"), "E01")

    def test_e01b_flowchart_lr(self):
        self.assertCode(REFERENZ.replace("flowchart TD", "flowchart LR"), "E01")

    def test_e02_ohne_start(self):
        self.assertCode(REFERENZ.replace('start(["Start"])', 'start["Bestellung"]'), "E02")

    def test_e03_ohne_ende(self):
        self.assertCode(REFERENZ.replace('ende(["Ende"])', 'ende["Archivieren"]'), "E03")

    def test_e04a_unbeschriftete_kanten(self):
        text = ENTSCHEIDUNG.replace('-->|"Ja"|', "-->").replace('-->|"Nein"|', "-->")
        self.assertCode(text, "E04")

    def test_e04b_nur_eine_kante(self):
        text = """flowchart TD
    start(["Start"]) --> freigabe{"Freigabe erteilt?"}
    freigabe -->|"Ja"| ende(["Ende"])
"""
        self.assertCode(text, "E04")

    def test_e05_dicker_pfeil(self):
        self.assertCode(rumpf('schritt ==> weiter["Weiter"]'), "E05")

    def test_e06_runde_klammer(self):
        self.assertCode(rumpf('schritt --> alt("Variante")'), "E06")

    def test_e06_negativ_kreis_und_stadion(self):
        b = validiere_text(rumpf('schritt --> kreis(("K1"))', 'kreis --> marke(["Zwischenstand"])'))
        self.assertNotIn("E06", b.codes())

    def test_e07_leerer_text(self):
        self.assertCode(rumpf('schritt --> leer[""]'), "E07")


class Warnregeln(unittest.TestCase):
    def assertCode(self, text, code):
        self.assertIn(code, validiere_text(text).codes())

    def test_w01_unsprechende_id(self):
        self.assertCode(rumpf('schritt --> b["Weiter"]'), "W01")

    def test_w02_fallback(self):
        self.assertCode(rumpf('schritt --> dokument["📄 Rechnung"]'), "W02")

    def test_w03_langes_label(self):
        self.assertCode(rumpf('schritt -->|"Diese Beschriftung ist deutlich zu lang"| weiter["Weiter"]'), "W03")

    def test_w04_lange_zeile(self):
        self.assertCode(rumpf('schritt --> weiter["%s"]' % ("x" * 130)), "W04")

    def test_w05_zu_viele_knoten(self):
        zeilen = ['flowchart TD', '    start(["Start"]) --> schritt1["Schritt 1"]']
        for i in range(1, 30):
            zeilen.append('    schritt%d --> schritt%d["Schritt %d"]' % (i, i + 1, i + 1))
        zeilen.append('    schritt30 --> ende(["Ende"])')
        self.assertCode("\n".join(zeilen) + "\n", "W05")


class CliExitCodes(unittest.TestCase):
    def setUp(self):
        self.verzeichnis = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.verzeichnis.cleanup()

    def datei(self, inhalt):
        pfad = os.path.join(self.verzeichnis.name, "test.mmd")
        with open(pfad, "w", encoding="utf-8") as f:
            f.write(inhalt)
        return pfad

    def aufruf(self, *args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return main(list(args))

    def test_gueltig_exit_0(self):
        self.assertEqual(self.aufruf(self.datei(REFERENZ)), 0)

    def test_fehler_exit_1(self):
        self.assertEqual(self.aufruf(self.datei(REFERENZ.replace("flowchart TD", "graph TD"))), 1)

    def test_fehlende_datei_exit_2(self):
        self.assertEqual(self.aufruf(os.path.join(self.verzeichnis.name, "gibtsnicht.mmd")), 2)

    def test_warnung_strict_und_normal(self):
        pfad = self.datei(rumpf('schritt --> b["Weiter"]'))
        self.assertEqual(self.aufruf(pfad, "--strict"), 1)
        self.assertEqual(self.aufruf(pfad), 0)

    def test_gueltig_strict_quiet(self):
        self.assertEqual(self.aufruf(self.datei(REFERENZ), "--strict", "--quiet"), 0)


if __name__ == "__main__":
    unittest.main()
