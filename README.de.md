# GitAccess

![GitAccess Logo](https://i.imgur.com/1PxbyHA.png)

**GitAccess** ist ein Tool, das es ermöglicht, LLM-Modelle mit einem GitHub-Repository zu verbinden, um dessen Inhalte abzurufen. So kannst du das Modell über den aktuellen Stand des Projekts befragen und stets auf dem neuesten Stand bleiben.

## 📦 Beschreibung

- **Autor**: ErrorRExorY/CptExorY
- **Website**: [pascal-frerks.de](https://pascal-frerks.de)
- **GitHub Repo**: [GitAccess auf GitHub](https://github.com/WhyWaitServices/open-webui-gitaccess.git)
- **Erforderliche OpenWebUI-Version**: 0.6.0
- **Version**: 0.1.0
- **Lizenz**: MIT

## 🚀 Installation

Um GitAccess in deiner selbst gehosteten OpenWebUI-Instanz zu installieren, kannst du den folgenden Schritten folgen:

### Über den Marktplatz
1. Öffne deine OpenWebUI Instanz.
2. Gehe zum [Marktplatz](https://openwebui.com/t/cptexory/gitaccess "Marktplatz").
3. Füge den Link zu GitAccess hinzu: (https://github.com/WhyWaitServices/open-webui-gitaccess.git).

### Manuelle Installation
1. Kopiere den Code aus der `GitCccess.py` Datei heraus.
2. Füge den kopierten Code zu deiner OpenWebUI-Instanz hinzu, indem du unter Arbeitsbereich>Werkzeuge ein neues Tool erstellst.
3. Füge den kopierten Code aus der `GitAccess.py` Datei im großen Eingabefeld ein und veregib einen Namen und eine Beschreibung.
4. Speichere das Tool.

## ⚙️ Konfiguration 

### Environment Variables (Valves)

- **Zugang zu den Valves**: Die Umgebungsvariablen für das Tool werden in der OpenWebUI gesetzt. Klicke auf den Zahnrad-Button, wenn du das Tool öffnest, um die Valves zu konfigurieren.
  - **GITHUB_ACCESS_TOKEN**: Ein persönlicher Zugriffstoken von GitHub, das die erforderlichen Zugriffsrechte auf das Repository hat.
  - **GITHUB_REPO_URL**: Die URL des GitHub-Repositories, das im Format `username/repo` angegeben werden muss.

### UserValves

- **Setzen der UserValves**: Wenn du das Tool in einem Chat oder Modell aktiviert hast, kannst du die UserValves über den „Controls“-Button (oben rechts, direkt links neben dem Profilbild) setzen. Ein Sheet wird geöffnet, wo du die UserValves des Tools konfigurieren kannst.

## 🛠️ Nutzung

Nach der Installation kannst du GitAccess wie folgt nutzen:

1. Stelle sicher, dass du richtig konfiguriert bist (Zugangstoken und Repo-URL).
2. Starte das Tool in deiner OpenWebUI-Instanz.
3. Verwende einfache Prompts wie:
   - „Was ist der Inhalt meines GitHub-Repos?“
   - „Gib mir den Inhalt zweier Dateien in Codeblöcken aus.“

Die Antwort könnte wie folgt aussehen:
![Example Screenshot](https://i.imgur.com/tPMQwyf.png)

Der Status der Aktionen wird in der Benutzeroberfläche durch Statusmeldungen angezeigt.

## 🤖 Funktionen

- **Repository Inhalten abrufen**: Lese die Struktur und die Dateien eines angegebenen GitHub-Repositories.
- **Dynamische Filter**: Unterscheidung zwischen Verzeichnissen und Dateien, um die gewünschten Daten effizient abzurufen.
- **Ereignis-Emitter**: Echtzeit-Feedback über die Progression der Abfragen und andere Aktionen.

## 📋 Lizenz

Dieses Projekt steht unter der MIT Lizenz. Weitere Informationen findest du in der [LICENSE](LICENSE) Datei.

## 🤝 Mitwirken

Beiträge sind willkommen! Bitte öffne ein Issue oder eine Pull-Request, um Anregungen zu teilen oder Verbesserungen vorzuschlagen.

## 📞 Kontakt

Bei Fragen oder Feedback kannst du mich unter [contact@example.com](mailto:contact@example.com) kontaktieren.

Vielen Dank, dass du GitAccess nutzt!