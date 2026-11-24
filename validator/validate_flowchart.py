#!/usr/bin/env python3
"""Validator für Mermaid-Flussdiagramme nach DIN ISO 5807 (Projekt Flowchart-DE-Norm).

Prüft eine .mmd-Datei gegen die Fehlerregeln E01–E07 und die Warnregeln W01–W05.
Verwendet ausschließlich die Python-Standardbibliothek.

Aufruf:
    python3 validate_flowchart.py <datei.mmd> [--strict] [--quiet]

Exit-Codes:
    0 = gültig (Warnungen zulässig, außer mit --strict)
    1 = mindestens ein Fehler (bzw. eine Warnung mit --strict)
    2 = Aufruffehler (Datei nicht gefunden, falsche Argumente)
"""

import argparse
import re
import sys
from dataclasses import dataclass, field

VERSION = "1.0.0"

MELDUNGEN = {
    "E01": "Erste Anweisung muss 'flowchart TD' sein (kein 'graph', keine andere Richtung)",
    "E02": "Start-Terminator fehlerhaft (genau ein Stadion-Knoten id([\"...\"]) mit Start/Anfang/Beginn erforderlich)",
    "E03": "Kein Ende-Terminator gefunden (Stadion-Knoten mit Ende/Stop/Abbruch/Abschluss/Fertig)",
    "E04": "Entscheidung ohne vollständige Ja/Nein-Beschriftung (mindestens 2 ausgehende, beschriftete Kanten)",
    "E05": "Dicker Pfeil '==>' bzw. '===' ist verboten",
    "E06": "Runde-Klammer-Syntax 'id(...)' ist verboten (erlaubt sind id([\"...\"]) und id((\"...\")))",
    "E07": "Knoten mit leerem Beschriftungstext",
    "W01": "Unsprechende Knoten-ID (sprechende, kleingeschriebene IDs verwenden)",
    "W02": "Fallback-Symbol verwendet (Mermaid kennt keine Normform dafür)",
    "W03": "Kantenbeschriftung länger als 20 Zeichen",
    "W04": "Zeile länger als 120 Zeichen",
    "W05": "Mehr als 25 eindeutige Knoten (Diagramm aufteilen)",
}

START_WORTE = ("start", "anfang", "beginn")
ENDE_WORTE = ("ende", "stop", "abbruch", "abschluss", "fertig")
JA_NEIN = re.compile(r"\b(ja|nein|yes|no|wahr|falsch)\b")
UNSPRECHEND = re.compile(r"^[A-Za-z]{1,2}\d*$")

ID = r"(?<![\w])([A-Za-z_][\w]*)"
TXT = r'\s*"([^"]*)"\s*'
# Reihenfolge wichtig: mehrzeichenige Formen zuerst.
FORMEN = [
    ("terminator", r"\(\[" + TXT + r"\]\)"),
    ("datenspeicher", r"\[\(" + TXT + r"\)\]"),
    ("unterprozess", r"\[\[" + TXT + r"\]\]"),
    ("daten", r"\[/" + TXT + r"/\]"),
    ("vorbereitung", r"\{\{" + TXT + r"\}\}"),
    ("verbinder", r"\(\(" + TXT + r"\)\)"),
    ("prozess", r"\[" + TXT + r"\]"),
    ("entscheidung", r"\{" + TXT + r"\}"),
    ("rund", r"\(" + TXT + r"\)"),
]
KNOTEN_RE = re.compile(
    ID + "(?:" + "|".join("(?P<%s>%s)" % (name, muster) for name, muster in FORMEN) + ")"
)
RUNDE_KLAMMER_RE = re.compile(ID + r"\((?![\[(])")
OPERATOR_RE = re.compile(r"-\.->|==>|===|-->|---")
ID_TOKEN_RE = re.compile(r"[A-Za-z_][\w]*")
ANFUEHRUNG_RE = re.compile(r'"[^"]*"')
PIPE_RE = re.compile(r"\|[^|]*\|")


@dataclass
class Bericht:
    fehler: list = field(default_factory=list)      # [(code, zeile, detail)]
    warnungen: list = field(default_factory=list)   # [(code, zeile, detail)]

    def codes(self):
        return {c for c, _, _ in self.fehler} | {c for c, _, _ in self.warnungen}

    def gueltig(self, strict=False):
        return not self.fehler and not (strict and self.warnungen)


def _maskieren(zeile, spannen):
    zeichen = list(zeile)
    for anfang, ende in spannen:
        for i in range(anfang, ende):
            zeichen[i] = " "
    return "".join(zeichen)


def _knoten_text(treffer):
    for name, _ in FORMEN:
        if treffer.group(name) is not None:
            # Text ist die letzte nicht-None-Gruppe innerhalb dieser Form
            spanne = treffer.span(name)
            text = re.search(r'"([^"]*)"', treffer.string[spanne[0]:spanne[1]]).group(1)
            return name, text
    return None, None


def validiere_text(text):
    bericht = Bericht()
    knoten = {}          # id -> {"form", "text", "zeile"}
    erste_nennung = {}   # id -> zeile
    kanten = []          # (quelle, ziel, label, zeile)
    kopf_geprueft = False

    for nr, original in enumerate(text.splitlines(), start=1):
        if len(original.rstrip("\r\n")) > 120:
            bericht.warnungen.append(("W04", nr, "%d Zeichen" % len(original.rstrip())))
        zeile = original.split("%%", 1)[0].rstrip()
        if not zeile.strip():
            continue
        if not kopf_geprueft:
            kopf_geprueft = True
            if zeile.strip() != "flowchart TD":
                bericht.fehler.append(("E01", nr, "gefunden: '%s'" % zeile.strip()))
            continue

        # Knotendefinitionen
        spannen = []
        for t in KNOTEN_RE.finditer(zeile):
            kid = t.group(1)
            form, ktext = _knoten_text(t)
            spannen.append((t.end(1), t.end()))
            erste_nennung.setdefault(kid, nr)
            if form == "rund":
                bericht.fehler.append(("E06", nr, "Knoten '%s'" % kid))
                continue
            if not ktext.strip():
                bericht.fehler.append(("E07", nr, "Knoten '%s'" % kid))
            if "📄" in ktext or ktext.startswith("Manuell:") or ktext.startswith("Anzeige:"):
                bericht.warnungen.append(("W02", nr, "Knoten '%s': '%s'" % (kid, ktext)))
            knoten.setdefault(kid, {"form": form, "text": ktext, "zeile": nr})

        maskiert = _maskieren(zeile, spannen)
        maskiert = _maskieren(maskiert, [m.span() for m in ANFUEHRUNG_RE.finditer(maskiert)])
        pipes = [m.span() for m in PIPE_RE.finditer(maskiert)]
        maskiert = _maskieren(maskiert, pipes)

        # E06: id( ohne folgendes [ oder (
        for t in RUNDE_KLAMMER_RE.finditer(maskiert):
            bericht.fehler.append(("E06", nr, "Knoten '%s'" % t.group(1)))

        # Kanten
        ops = list(OPERATOR_RE.finditer(maskiert))
        for i, op in enumerate(ops):
            if op.group() in ("==>", "==="):
                bericht.fehler.append(("E05", nr, "Operator '%s'" % op.group()))
            vorher_start = ops[i - 1].end() if i > 0 else 0
            nachher_ende = ops[i + 1].start() if i + 1 < len(ops) else len(maskiert)
            vorher = ID_TOKEN_RE.findall(maskiert[vorher_start:op.start()])
            nachher = ID_TOKEN_RE.findall(maskiert[op.end():nachher_ende])
            if not vorher or not nachher:
                continue
            quelle, ziel = vorher[-1], nachher[0]
            label = None
            rest = zeile[op.end():]
            m = re.match(r"\s*\|([^|]*)\|", rest)
            if m:
                label = m.group(1).strip().strip('"')
            for kid in (quelle, ziel):
                erste_nennung.setdefault(kid, nr)
            kanten.append((quelle, ziel, label, nr))
            if label is not None and len(label) > 20:
                bericht.warnungen.append(("W03", nr, "'%s' (%d Zeichen)" % (label, len(label))))

    if not kopf_geprueft:
        bericht.fehler.append(("E01", None, "Datei enthält keine Anweisung"))

    # E02 / E03
    terminatoren = [k for k in knoten.values() if k["form"] == "terminator"]
    starts = [k for k in terminatoren if any(w in k["text"].lower() for w in START_WORTE)]
    enden = [k for k in terminatoren if any(w in k["text"].lower() for w in ENDE_WORTE)]
    if not starts:
        bericht.fehler.append(("E02", None, "keine Stadionform mit Starttext"))
    elif len(starts) > 1:
        bericht.fehler.append(("E02", starts[1]["zeile"], "%d Start-Terminatoren gefunden" % len(starts)))
    if not enden:
        bericht.fehler.append(("E03", None, "keine Stadionform mit Endetext"))

    # E04
    for kid, k in knoten.items():
        if k["form"] != "entscheidung":
            continue
        aus = [kante for kante in kanten if kante[0] == kid]
        if len(aus) < 2:
            bericht.fehler.append(("E04", k["zeile"],
                                   "Entscheidung '%s' hat weniger als 2 ausgehende Kanten" % kid))
            continue
        ohne = [kante for kante in aus if not kante[2] or not JA_NEIN.search(kante[2].lower())]
        if ohne:
            bericht.fehler.append(("E04", k["zeile"],
                                   "Entscheidung '%s': %d Kante(n) ohne Ja/Nein-Beschriftung" % (kid, len(ohne))))

    # W01 / W05
    for kid, nr in sorted(erste_nennung.items(), key=lambda x: x[1]):
        if UNSPRECHEND.match(kid):
            bericht.warnungen.append(("W01", nr, "ID '%s'" % kid))
    if len(erste_nennung) > 25:
        bericht.warnungen.append(("W05", None, "%d Knoten" % len(erste_nennung)))

    schluessel = lambda e: (e[1] or 0, e[0])
    bericht.fehler.sort(key=schluessel)
    bericht.warnungen.sort(key=schluessel)
    return bericht


def _ausgabe(bericht, strict):
    def zeile(eintrag):
        code, nr, detail = eintrag
        ort = "Zeile %d" % nr if nr else "Datei"
        return "  [%s] %s: %s (%s)" % (code, ort, MELDUNGEN[code], detail)

    if bericht.fehler:
        print("Fehler:")
        for e in bericht.fehler:
            print(zeile(e))
    if bericht.warnungen:
        print("Warnungen:")
        for w in bericht.warnungen:
            print(zeile(w))
    status = "GÜLTIG" if bericht.gueltig(strict) else "UNGÜLTIG"
    print("Ergebnis: %s (%d Fehler, %d Warnungen)" % (status, len(bericht.fehler), len(bericht.warnungen)))


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="validate_flowchart.py",
        description="Prüft Mermaid-Flussdiagramme gegen DIN ISO 5807 (Regeln E01–E07, W01–W05).",
    )
    parser.add_argument("datei", help="Pfad zur .mmd-Datei")
    parser.add_argument("--strict", action="store_true", help="Warnungen als Fehler werten")
    parser.add_argument("--quiet", action="store_true", help="keine Ausgabe, nur Exit-Code")
    parser.add_argument("--version", action="version", version="%(prog)s " + VERSION)
    try:
        args = parser.parse_args(argv)
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 2

    try:
        with open(args.datei, encoding="utf-8") as f:
            text = f.read()
    except (OSError, UnicodeDecodeError) as e:
        if not args.quiet:
            print("Aufruffehler: Datei '%s' kann nicht gelesen werden (%s)" % (args.datei, e), file=sys.stderr)
        return 2

    bericht = validiere_text(text)
    if not args.quiet:
        _ausgabe(bericht, args.strict)
    return 0 if bericht.gueltig(args.strict) else 1


if __name__ == "__main__":
    sys.exit(main())
