# Flowchart-DE-Norm

Flussdiagramme nach DIN ISO 5807 mit Mermaid: Symboldefinitionen, System-Prompt, Validator und CI.

Das Projekt übersetzt die Sinnbilder der DIN ISO 5807 in Mermaid-Syntax (mit draw.io-Stilangaben als Zweitbeschreibung), gibt einem Sprachmodell einen passenden System-Prompt mit und prüft jedes Diagramm automatisch gegen feste Regeln.

## Bausteine

| Baustein | Datei | Inhalt |
|---|---|---|
| Symbol-JSON | [`symbols/iso-5807-symbols.json`](symbols/iso-5807-symbols.json) | 11 Symbole und 2 Flusslinien mit Mermaid- und draw.io-Syntax |
| System-Prompt | [`prompts/system-prompt.md`](prompts/system-prompt.md) | Sofort nutzbarer Prompt für einen Fachassistenten nach DIN ISO 5807 |
| Validator | [`validator/validate_flowchart.py`](validator/validate_flowchart.py) | Prüft `.mmd`-Dateien auf Fehler E01–E07 und Warnungen W01–W05, nur Standardbibliothek |
| Beispiele | [`examples/`](examples/) | 4 Diagramme: Reihenfolge, Entscheidung, Schleife, Unterprozess |
| CI-Workflow | [`.github/workflows/validate.yml`](.github/workflows/validate.yml) | Validiert alle Beispiele streng und führt die Unit-Tests aus |
| Normüberblick | [`docs/iso-5807-ueberblick.md`](docs/iso-5807-ueberblick.md) | Symboltabelle, Grenzen der Mermaid-Notation, Literatur |

## Schnellstart

```bash
python3 validator/validate_flowchart.py examples/02-entscheidung.mmd --strict
```

Optionen: `--strict` wertet Warnungen als Fehler, `--quiet` unterdrückt die Ausgabe, `--version` zeigt die Version.

### Exit-Codes

| Code | Bedeutung |
|---|---|
| 0 | gültig (Warnungen zulässig, außer mit `--strict`) |
| 1 | mindestens ein Fehler E01–E07 (bzw. eine Warnung mit `--strict`) |
| 2 | Aufruffehler (Datei nicht gefunden, falsche Argumente) |

## Prüfregeln

### Fehler

| Code | Regel |
|---|---|
| E01 | Erste Anweisung (ohne Leer- und `%%`-Kommentarzeilen) muss exakt `flowchart TD` sein. |
| E02 | Genau ein Start-Terminator: Stadionform `id(["..."])`, Text enthält Start, Anfang oder Beginn. |
| E03 | Mindestens ein Ende-Terminator: Text enthält Ende, Stop, Abbruch, Abschluss oder Fertig. |
| E04 | Jede Entscheidung (Raute) hat mindestens 2 ausgehende Kanten, jede mit Ja/Nein (auch Wahr/Falsch, Yes/No) beschriftet. |
| E05 | Dicke Pfeile `==>` und `===` sind verboten. |
| E06 | Runde-Klammer-Syntax `id(...)` ist verboten; erlaubt bleiben `id(["..."])` und `id(("..."))`. |
| E07 | Kein Knoten mit leerem Text (z. B. `id[""]`). |

### Warnungen

| Code | Regel |
|---|---|
| W01 | Unsprechende Knoten-ID nach Muster `^[A-Za-z]{1,2}\d*$` (z. B. `A`, `B2`). |
| W02 | Fallback-Symbol: Text enthält 📄 oder beginnt mit „Manuell:“ bzw. „Anzeige:“. |
| W03 | Kantenbeschriftung länger als 20 Zeichen. |
| W04 | Zeile länger als 120 Zeichen. |
| W05 | Mehr als 25 eindeutige Knoten: Diagramm aufteilen. |

## Tests

```bash
python3 -m unittest discover -s validator/tests -p 'test_*.py' -v
```

Erwartet werden 22 Tests mit dem Ergebnis `OK`.

Alle Beispiele auf einmal prüfen:

```bash
for datei in examples/*.mmd; do python3 validator/validate_flowchart.py "$datei" --strict; done
```

## Die 8 Regeln in Kürze

1. **R1** Nur `flowchart TD`.
2. **R2** Ein Start-Terminator, mindestens ein Ende-Terminator.
3. **R3** Jede Raute hat beschriftete Ja/Nein-Kanten.
4. **R4** Keine dicken Pfeile (`==>`, `===`).
5. **R5** Keine Runde-Klammer-Syntax (`A(Text)`).
6. **R6** Alle Texte in doppelten Anführungszeichen.
7. **R7** Keine Styling-Anweisungen (`style`, `classDef`, `class`, `linkStyle`, `subgraph`).
8. **R8** Vor Auslieferung validieren, auch warnungsfrei.

## Lizenz und Mitarbeit

MIT-Lizenz, siehe [LICENSE](LICENSE). Hinweise zur Mitarbeit stehen in [CONTRIBUTING.md](CONTRIBUTING.md).
