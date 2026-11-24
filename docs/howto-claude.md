# How-to: Flussdiagramme nach DIN ISO 5807 mit Claude

Diese Anleitung zeigt zwei Wege: Claude im Browser oder in der App (claude.ai) für den Alltag und Claude Code für die Arbeit direkt im Repository. Beide nutzen denselben System-Prompt und denselben Validator.

## Weg 1: claude.ai mit einem Projekt

Ein Projekt merkt sich die Regeln. Du richtest es einmal ein und musst den Prompt danach nie wieder einfügen.

### Einrichten (einmalig, ca. 3 Minuten)

1. Auf claude.ai links **Projekte** öffnen und ein neues Projekt anlegen, z. B. „Flussdiagramme DIN ISO 5807“.
2. In den **Projektanweisungen** den kompletten Inhalt von [`prompts/system-prompt.md`](../prompts/system-prompt.md) einfügen.
3. Unter **Dateien** bzw. Projektwissen die Datei [`symbols/iso-5807-symbols.json`](../symbols/iso-5807-symbols.json) hochladen. Das ist optional, hilft aber bei Rückfragen zu Symbolen und draw.io-Stilen.

### Benutzen

Im Projekt einen neuen Chat öffnen und den Ablauf in eigenen Worten beschreiben. Je konkreter die Entscheidungen benannt sind, desto besser wird das Diagramm.

Beispiel:

> Erstelle den Ablauf für eingehende Nebenwirkungsmeldungen: Meldung empfangen, prüfen, ob die Mindestkriterien erfüllt sind. Wenn nein, Follow-up anfordern und erneut prüfen. Wenn ja, Fall erfassen, in der Safety-Datenbank speichern, Kausalität bewerten, Ende.

Claude antwortet mit einem Satz zur Einordnung und dem Diagramm im Codeblock. Wenn du das Diagramm sehen willst, schreib dazu: „Zeig mir das Diagramm auch gerendert.“

### Prüfen

Den Codeblock als Datei speichern, z. B. `meldung.mmd`, und den Validator laufen lassen:

```bash
python3 validator/validate_flowchart.py meldung.mmd --strict
```

Meldet der Validator Fehler, kopierst du die Ausgabe zurück in den Chat mit „Bitte korrigieren“. Claude kennt die Codes E01–E08 und W01–W05 aus dem System-Prompt.

## Weg 2: Claude Code im Repository

Claude Code arbeitet direkt in deinem lokalen Klon und kann den Validator selbst ausführen. Damit entfällt das Hin- und Herkopieren.

1. Repository klonen und Claude Code im Ordner starten:
   ```bash
   git clone https://github.com/reyschilling-ai/Flowchart-DE-Norm.git
   cd Flowchart-DE-Norm
   claude
   ```
2. Claude Code liest beim Start automatisch die Datei [`CLAUDE.md`](../CLAUDE.md) im Repository. Darin steht, dass es den System-Prompt befolgen und jedes Diagramm validieren muss.
3. Den Ablauf beschreiben und den Dateinamen nennen:
   > Erstelle `examples/05-meldung.mmd` für folgenden Ablauf: …
4. Claude Code schreibt die Datei, ruft den Validator mit `--strict` auf und korrigiert, bis das Ergebnis „GÜLTIG (0 Fehler, 0 Warnungen)“ lautet.

Neue Beispiele in `examples/` prüft die CI bei jedem Push automatisch mit. Gibt die CI Rot, liegt das fast immer an einer Warnung, die im strengen Modus als Fehler zählt.

## Typische Stolpersteine

| Problem | Ursache | Abhilfe |
|---|---|---|
| E01 trotz `flowchart TD` | Leerzeichen oder Text hinter `TD` | Kopfzeile exakt `flowchart TD` |
| E04 an einer Raute | Eine Kante ohne `\|"Ja"\|` bzw. `\|"Nein"\|` | Jede ausgehende Kante beschriften |
| W01 | IDs wie `A`, `B2` | Sprechende IDs wie `pruefung` |
| W02 | Fallback-Symbol (📄, „Manuell:“, „Anzeige:“) | Nur nutzen, wenn wirklich nötig; mit `--strict` zählt es als Fehler |
| W05 | Mehr als 25 Knoten | In Teilabläufe aufteilen und über `id[["Teilablauf"]]` verbinden |
