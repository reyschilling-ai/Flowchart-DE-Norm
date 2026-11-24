# DIN ISO 5807 im Überblick

Die DIN ISO 5807 ist die deutsche Fassung der ISO 5807:1985 („Informationsverarbeitung; Sinnbilder und ihre Anwendung für Datenflusspläne, Programmablaufpläne, Programmnetzpläne und Datennetzpläne“). Sie legt fest, welche Symbolform welchen Schritttyp darstellt und wie Abläufe zu zeichnen sind. Ein Leser, der die Norm kennt, erkennt am Umriss eines Kastens, ob es sich um einen Verarbeitungsschritt, eine Entscheidung oder einen Datenbestand handelt.

Dieses Projekt setzt die Norm in Mermaid-Syntax um. Die draw.io-Stilangaben dienen als Zweitbeschreibung für alle, die Diagramme grafisch nachbearbeiten.

## Schreibkonventionen

- Kopfzeile ist immer exakt `flowchart TD`, weil die Norm Abläufe von oben nach unten liest.
- Knoten-IDs sind sprechend und kleingeschrieben (`pruefung`, nicht `B2`).
- Jeder Knoten- und Kantentext steht in doppelten Anführungszeichen.
- Ein Blatt enthält genau einen Ablauf: ein Start, mindestens ein Ende.

## Symbole

| Nr. | Symbol | Normform | Mermaid | draw.io |
|---|---|---|---|---|
| 1 | Terminator (Anfang/Ende) | Stadion / abgerundetes Rechteck | `id(["Text"])` | `rounded=1;whiteSpace=wrap;html=1;arcSize=50;` |
| 2 | Prozess | Rechteck | `id["Text"]` | `rounded=0;whiteSpace=wrap;html=1;` |
| 3 | Entscheidung | Raute | `id{"Text"}` | `rhombus;whiteSpace=wrap;html=1;` |
| 4 | Daten (Ein-/Ausgabe) | Parallelogramm | `id[/"Text"/]` | `shape=parallelogram;whiteSpace=wrap;html=1;` |
| 5 | Vordefinierter Prozess | Rechteck mit Doppelstrichen | `id[["Text"]]` | `shape=process;whiteSpace=wrap;html=1;` |
| 6 | Vorbereitung | Sechseck | `id{{"Text"}}` | `shape=hexagon;whiteSpace=wrap;html=1;fixedSize=1;size=20;` |
| 7 | Datenspeicher | Zylinder | `id[("Text")]` | `shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;` |
| 8 | Verbinder | Kreis | `id(("Text"))` | `ellipse;whiteSpace=wrap;html=1;fixedSize=1;size=40;` |
| 9 | Dokument (Fallback) | Rechteck mit gewellter Unterkante | `id["📄 Text"]` | `shape=document;whiteSpace=wrap;html=1;size=0.35;` |
| 10 | Manuelle Eingabe (Fallback) | Trapez | `id["Manuell: Text"]` | `shape=trapezoid;whiteSpace=wrap;html=1;fixedSize=1;size=20;` |
| 11 | Anzeige (Fallback) | Anzeigeform (gebogenes Display) | `id["Anzeige: Text"]` | `shape=display;whiteSpace=wrap;html=1;` |

## Flusslinien

| Linie | Bedeutung | Mermaid | draw.io |
|---|---|---|---|
| Ablauflinie | Kontrollfluss, durchgezogen, Pfeilspitze in Flussrichtung | `a --> b`, `a -->\|"Ja"\| b` | `edgeStyle=orthogonalEdgeStyle;html=1;endArrow=block;` |
| Informationslinie | Informations- und Datenfluss, gestrichelt | `a -.-> b`, `a -.->\|"Referenz"\| b` | `edgeStyle=orthogonalEdgeStyle;html=1;endArrow=block;dashed=1;` |

Dicke Pfeile (`==>`, `===`) und die Runde-Klammer-Knotensyntax (`A(Text)`, `A("Text")`) sind in dieser Umsetzung verboten.

## Grenzen der Mermaid-Notation

Für drei Normsymbole kennt Mermaid keine passende Form. Das Projekt nutzt deshalb ein Rechteck mit eindeutigem Präfix:

- **Dokument:** `id["📄 Text"]`
- **Manuelle Eingabe:** `id["Manuell: Text"]`
- **Anzeige:** `id["Anzeige: Text"]`

Diese Fallbacks sind erlaubt, lösen im Validator aber die Warnung **W02** aus. Mit `--strict` gilt ein solches Diagramm als ungültig. Wer die exakte Normform braucht, überträgt das Diagramm mit den draw.io-Stilangaben aus der Tabelle.

## Literatur

- ISO 5807:1985 – Information processing – Documentation symbols and conventions for data, program and system flowcharts, program network charts and system resources charts.
- DIN ISO 5807 – Informationsverarbeitung; Sinnbilder und ihre Anwendung für Datenflusspläne, Programmablaufpläne, Programmnetzpläne und Datennetzpläne (deutsche Fassung der ISO 5807:1985).

## Weiterführend im Projekt

- Maschinenlesbare Symboldefinitionen: [`../symbols/iso-5807-symbols.json`](../symbols/iso-5807-symbols.json)
- System-Prompt für Sprachmodelle: [`../prompts/system-prompt.md`](../prompts/system-prompt.md)
- Validator: [`../validator/validate_flowchart.py`](../validator/validate_flowchart.py)
