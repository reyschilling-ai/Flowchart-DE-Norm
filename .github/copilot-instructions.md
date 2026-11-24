# Anweisungen für GitHub Copilot

Dieses Repository enthält ein Toolkit für Flussdiagramme nach DIN ISO 5807 in Mermaid. Antworte auf Deutsch.

## Diagramme erstellen

Für jedes Diagramm gelten die Regeln aus `prompts/system-prompt.md`. Die wichtigsten:

1. Kopfzeile exakt `flowchart TD`.
2. Genau ein Start-Terminator `start(["Start"])`, mindestens ein Ende-Terminator `ende(["Ende"])`.
3. Jede Raute `id{"Frage?"}` hat mindestens zwei ausgehende Kanten, jede mit `|"Ja"|` oder `|"Nein"|` beschriftet.
4. Keine dicken Pfeile `==>` oder `===`.
5. Keine Runde-Klammer-Knoten `id(Text)` oder `id("Text")`.
6. Alle Texte in doppelten Anführungszeichen.
7. Keine Styling-Anweisungen: kein `style`, `classDef`, `class`, `linkStyle`, `subgraph`, `:::`.
8. Sprechende, kleingeschriebene Knoten-IDs (`pruefung`, nicht `B2`), Kantentexte höchstens 20 Zeichen, höchstens 25 Knoten.

Symbole: Prozess `id["Text"]`, Entscheidung `id{"Text?"}`, Daten `id[/"Text"/]`, Unterprozess `id[["Text"]]`, Vorbereitung `id{{"Text"}}`, Datenspeicher `id[("Text")]`, Verbinder `id(("Text"))`. Details in `symbols/iso-5807-symbols.json`.

## Prüfen

Neue Diagramme als `.mmd` in `examples/` ablegen und prüfen:

```bash
python3 validator/validate_flowchart.py <datei> --strict
```

Erst fertig, wenn „GÜLTIG (0 Fehler, 0 Warnungen)“ erscheint. Bei Änderungen am Validator zusätzlich:

```bash
python3 -m unittest discover -s validator/tests -p 'test_*.py' -v
```

Der Validator nutzt nur die Python-Standardbibliothek.
