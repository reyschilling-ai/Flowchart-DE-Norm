# Beispiele

Alle Beispiele bestehen den Validator im strengen Modus (`--strict`): 0 Fehler, 0 Warnungen.

| Datei | Inhalt | Verwendete Symbole |
|---|---|---|
| [`01-reihenfolge.mmd`](01-reihenfolge.mmd) | Lineare Bestellabwicklung | Terminator, Daten, Prozess |
| [`02-entscheidung.mmd`](02-entscheidung.mmd) | Auftragsfreigabe mit Verzweigung | Terminator, Prozess, Entscheidung |
| [`03-schleife.mmd`](03-schleife.mmd) | Zeichenweise Verarbeitung mit Zähler | Terminator, Vorbereitung, Entscheidung, Prozess |
| [`04-unterprozess.mmd`](04-unterprozess.mmd) | Tarifberechnung und Versicherungsschein | Terminator, Daten, Vordefinierter Prozess, Datenspeicher, Prozess |

## Prüfen

```bash
for datei in examples/*.mmd; do python3 validator/validate_flowchart.py "$datei" --strict; done
```

## Rendern

Mit der Mermaid-CLI lässt sich jedes Beispiel als SVG oder PNG ausgeben:

```bash
npx @mermaid-js/mermaid-cli -i examples/02-entscheidung.mmd -o 02-entscheidung.svg
```
