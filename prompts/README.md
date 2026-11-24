# Prompts

Hier liegt der System-Prompt, mit dem ein Sprachmodell Flussdiagramme nach DIN ISO 5807 in Mermaid erzeugt.

## Nutzung

1. Den Inhalt von [`system-prompt.md`](system-prompt.md) als System-Nachricht setzen (bzw. als Projekt- oder Custom-Instruktion).
2. Optional [`../symbols/iso-5807-symbols.json`](../symbols/iso-5807-symbols.json) als zusätzlichen Kontext mitgeben.
3. Den gewünschten Ablauf in eigenen Worten beschreiben lassen, z. B. „Erstelle den Ablauf der Auftragsfreigabe mit Prüfung und Ablehnung“.
4. Die Ausgabe als `.mmd`-Datei speichern und prüfen:
   ```bash
   python3 validator/validate_flowchart.py mein-ablauf.mmd --strict
   ```

## Die 8 Regeln in Kürze

1. **R1** Nur `flowchart TD`.
2. **R2** Ein Start-Terminator, mindestens ein Ende-Terminator.
3. **R3** Jede Raute hat beschriftete Ja/Nein-Kanten.
4. **R4** Keine dicken Pfeile (`==>`, `===`).
5. **R5** Keine Runde-Klammer-Syntax (`A(Text)`).
6. **R6** Alle Texte in doppelten Anführungszeichen.
7. **R7** Keine Styling-Anweisungen.
8. **R8** Vor Auslieferung validieren, auch warnungsfrei.
