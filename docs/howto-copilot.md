# How-to: Flussdiagramme nach DIN ISO 5807 mit Copilot

„Copilot“ meint zwei verschiedene Produkte. Microsoft 365 Copilot ist der Assistent in Teams, Word und Outlook, also das, was in den meisten Firmen verfügbar ist. GitHub Copilot ist der Assistent für Entwickler in VS Code und auf GitHub. Für beide gibt es hier einen eigenen Abschnitt.

## Teil A: Microsoft 365 Copilot mit einem eigenen Agenten

Im normalen Copilot-Chat müsstest du den System-Prompt jedes Mal neu einfügen. Ein Agent speichert ihn dauerhaft.

### Agent einrichten (einmalig, ca. 5 Minuten)

1. Die Microsoft 365 Copilot App öffnen und links **Agent erstellen** wählen. Je nach Lizenz und Freigabe durch die IT kann der Punkt fehlen; dann bei der IT nach Agent Builder fragen.
2. Den Schritt „Beschreiben“ überspringen und direkt **Konfigurieren** öffnen.
3. Felder ausfüllen:
   - **Name:** `Flussdiagramm DIN ISO 5807` (höchstens 30 Zeichen)
   - **Beschreibung:** `Erstellt Programmablaufpläne nach DIN ISO 5807 als Mermaid-Code.`
   - **Anweisungen:** den kompletten Inhalt von [`prompts/system-prompt.md`](../prompts/system-prompt.md). Der Text hat rund 4.300 Zeichen und passt in das Feld (Grenze 8.000 Zeichen).
4. Unter **Wissen** die Datei [`symbols/iso-5807-symbols.json`](../symbols/iso-5807-symbols.json) hochladen. Lehnt Copilot das JSON-Format ab, die Datei vorher in `iso-5807-symbols.txt` umbenennen.
5. Optional unter **Startprompts** einen Beispielprompt hinterlegen, etwa „Erstelle einen Programmablaufplan für …“.
6. **Erstellen** klicken. Der Agent erscheint danach links in der Agentenliste.

### Benutzen

Den Agenten öffnen und den Ablauf beschreiben, genau wie in einem normalen Chat. Der Agent antwortet mit Mermaid-Code.

### Ansehen und weiterverarbeiten

Copilot zeigt Mermaid je nach Oberfläche nur als Code an. Zum Ansehen gibt es zwei Wege:

- **draw.io / diagrams.net:** Menü **Anordnen → Einfügen → Erweitert → Mermaid**, Code einfügen, **Einfügen** klicken. Das Diagramm lässt sich danach als PNG, SVG oder PDF exportieren und in Word oder PowerPoint einbauen. Die Desktop-Version von draw.io arbeitet lokal, das ist für interne Prozesse die unkritischere Wahl.
- **mermaid.live:** Code einfügen, Vorschau erscheint sofort. Das ist eine externe Website; für vertrauliche Abläufe lieber draw.io Desktop nehmen.

### Prüfen

Der Validator braucht Python. Wenn Python auf dem Firmenrechner verfügbar ist:

```bash
python3 validator/validate_flowchart.py ablauf.mmd --strict
```

Ohne Python kannst du den Code in einen Claude-Chat oder eine andere Umgebung mit Python geben und dort prüfen lassen. Fehlermeldungen kopierst du zurück in den Agenten-Chat mit „Bitte korrigieren“.

## Teil B: GitHub Copilot in VS Code

GitHub Copilot liest Anweisungen direkt aus dem Repository. Das Repository bringt sie schon mit: [`.github/copilot-instructions.md`](../.github/copilot-instructions.md).

### Einrichten

1. Repository klonen und in VS Code öffnen:
   ```bash
   git clone https://github.com/reyschilling-ai/Flowchart-DE-Norm.git
   code Flowchart-DE-Norm
   ```
2. Sicherstellen, dass die Erweiterung GitHub Copilot (mit Copilot Chat) installiert und angemeldet ist.
3. Nichts weiter: Copilot Chat hängt `.github/copilot-instructions.md` automatisch an jede Anfrage in diesem Repository an. Ob die Datei genutzt wurde, siehst du in der Antwort unter **Referenzen**.

### Benutzen

Copilot Chat öffnen, in den **Agent**-Modus wechseln und den Ablauf mit Zieldatei beschreiben:

> Erstelle `examples/05-meldung.mmd` für folgenden Ablauf: … Validiere danach mit dem Validator im strengen Modus.

Im Agent-Modus kann Copilot den Validator im Terminal ausführen. VS Code fragt vor dem ersten Befehl nach deiner Freigabe.

### Auf github.com

Copilot Chat auf github.com liest dieselbe Datei `.github/copilot-instructions.md`, kann den Validator dort aber nicht ausführen. Neue `.mmd`-Dateien in `examples/` prüft stattdessen die CI nach dem Push.
