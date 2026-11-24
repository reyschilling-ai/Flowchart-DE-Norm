# Mitarbeit an Flowchart-DE-Norm

Beiträge sind willkommen. So läuft ein Beitrag ab:

1. Repository forken.
2. Einen Branch anlegen: `feature/<kurzname>` für Neues, `fix/<kurzname>` für Korrekturen.
3. Lokal prüfen:
   ```bash
   for datei in examples/*.mmd; do python3 validator/validate_flowchart.py "$datei" --strict; done
   python3 -m unittest discover -s validator/tests -p 'test_*.py' -v
   ```
4. Pull Request gegen `main` stellen. Die CI führt dieselben Prüfungen aus.

## Vorgaben

- Der Validator nutzt ausschließlich die Python-Standardbibliothek. Keine pip-Abhängigkeiten.
- Eine neue Regel kommt nur zusammen mit Code (E../W..), Meldungstext und mindestens einem Unit-Test.
- Alle Beispiele in `examples/` bleiben warnungsfrei, also gültig mit `--strict`.
- `symbols/iso-5807-symbols.json` bleibt gültiges JSON und beschreibt weiterhin alle 11 Symbole und 2 Flusslinien vollständig.
- Commit-Meldungen, Kommentare und Dokumentation sind auf Deutsch.
