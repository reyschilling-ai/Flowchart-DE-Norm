# Hinweise für Claude Code

Dieses Repository enthält ein Toolkit für Flussdiagramme nach DIN ISO 5807 in Mermaid.

- Für jedes neue oder geänderte Diagramm gelten die Regeln aus `prompts/system-prompt.md`. Lies die Datei, bevor du ein Diagramm schreibst.
- Diagramme liegen als `.mmd`-Dateien in `examples/`, Dateiname mit fortlaufender Nummer (z. B. `05-meldung.mmd`).
- Jedes Diagramm muss vor Abschluss bestehen: `python3 validator/validate_flowchart.py <datei> --strict`. Korrigiere, bis „GÜLTIG (0 Fehler, 0 Warnungen)“ erscheint.
- Bei Änderungen am Validator: `python3 -m unittest discover -s validator/tests -p 'test_*.py' -v` muss grün sein. Neue Regeln nur mit Code, Meldung und Unit-Test.
- Der Validator nutzt nur die Python-Standardbibliothek. Keine pip-Abhängigkeiten.
- Texte, Kommentare und Commit-Meldungen auf Deutsch.
