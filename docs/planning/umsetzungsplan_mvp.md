# Umsetzungsplan MVP – InfoManagerBot

## Ziel

Der MVP von InfoManagerBot soll ein lokal betreibbares, portables Quellen- und Archivsystem bereitstellen, das RSS-/Atom-Quellen und YouTube-Kanäle regelmäßig abfragt, neue Inhalte dedupliziert, als Markdown/JSON archiviert und den Zustand in SQLite verwaltet. Browser-Capture ist in diesem MVP noch nicht enthalten.

---

## Leitprinzipien

- Source-first statt browser-first
- MVP bewusst klein, stabil und testbar halten
- Klare Trennung von Konfiguration, Persistenz, Adapterlogik, Processing und Archivierung
- Portabilität und Wiederherstellbarkeit von Anfang an mitdenken
- Sync und Backup fachlich sauber trennen

---

## Projektphasen

## Phase 0 – Projektgrundlage und Repo-Struktur

### Ziel

Eine saubere, minimale Arbeitsbasis im Repo schaffen.

### Aufgaben

- Basis-Ordnerstruktur anlegen
- Python-Projektstruktur definieren
- `README.md` knapp auf Projektziel ausrichten
- `.gitignore` für Python-, VS-Code- und Laufzeitartefakte ergänzen
- `docs/`-Struktur für Architektur, Anforderungen und Planung anlegen

### Ergebnis

Ein sauberes Repo, das für Implementierung und Dokumentation vorbereitet ist.

---

## Phase 1 – Konfiguration und Domänenmodell

### Ziel

Die fachlichen Grundobjekte und die Konfiguration verbindlich festlegen.

### Aufgaben

- Konfigurationsdateien definieren:
  - `config/sources.yaml`
  - `config/policies.yaml`
  - `config/settings.yaml`
- Konfigurationsschema in Python definieren
- Validierung beim Start implementieren
- Domänenmodelle für folgende Kernobjekte definieren:
  - Source
  - Item
  - Artifact
  - Run
  - Policy
- Quellentypen für den MVP festlegen:
  - `rss_atom`
  - `youtube_channel`

### Ergebnis

Ein stabiles fachliches Grundgerüst für alle weiteren Schritte.

---

## Phase 2 – SQLite-Schema und Persistenz

### Ziel

Den lokalen Zustand robust und nachvollziehbar speichern.

### Aufgaben

- SQLite-Schema erstellen für:
  - `sources`
  - `items`
  - `artifacts`
  - `runs`
  - `policies`
  - `schema_migrations`
- Initialschema als SQL-Datei anlegen
- Migrationsmechanismus mit nummerierten SQL-Dateien vorbereiten
- SQLite-Verbindung mit sinnvollen Standardeinstellungen aufsetzen:
  - WAL-Modus
  - Foreign Keys aktiv
- Repository-/Persistence-Schicht für Lesen/Schreiben anlegen

### Ergebnis

Eine belastbare Persistenzbasis, auf der Adapter und Pipeline arbeiten können.

---

## Phase 3 – Logging, Laufverwaltung und Orchestrierung

### Ziel

Das System kontrollierbar und nachvollziehbar machen.

### Aufgaben

- Strukturiertes Logging einführen
- Run-Tracking implementieren
- Scheduler und Orchestrator getrennt anlegen
- Startpunkt (`main.py`) schlank halten
- Polling-Loop mit Intervallsteuerung vorbereiten
- Fehlerzustände und Run-Status definieren

### Ergebnis

Ein lauffähiger Rahmen, in den Adapter eingehängt werden können.

---

## Phase 4 – Adapter-Framework

### Ziel

Eine saubere Grundlage für unterschiedliche Quellentypen schaffen.

### Aufgaben

- Basisschnittstelle für Adapter definieren
- Trennung festlegen zwischen:
  - `discover()`
  - optionalem `enrich()`
- Adapter-Registry oder Factory implementieren
- Gemeinsame Datentransferobjekte für entdeckte Items definieren
- Regeln festlegen:
  - Adapter schreiben keine Archivdateien
  - Adapter entscheiden nicht über DB-Deduplizierung
  - Adapter liefern normierte Daten an die Pipeline

### Ergebnis

Ein stabiles Adapter-Pattern für RSS und YouTube.

---

## Phase 5 – RSS-/Atom-Adapter

### Ziel

Den ersten produktiv nutzbaren Quellentyp implementieren.

### Aufgaben

- RSS-/Atom-Adapter implementieren
- Feed-Einträge in normierte DiscoveredItems überführen
- Primäre Identität festlegen:
  - bevorzugt externe Feed-ID
  - sonst deterministische Fallback-ID
- Konfigurierbar machen:
  - nur Feed-Inhalt nutzen
  - optional Volltext später nachladbar vorbereiten
- Erste echte Testquellen anbinden

### Ergebnis

InfoManagerBot kann RSS-/Atom-Quellen pollend verarbeiten.

---

## Phase 6 – YouTube-Adapter

### Ziel
YouTube-Kanalfeeds und Transkripte als zweiten Quellentyp integrieren.

### Aufgaben

- YouTube-Kanalfeed anbinden
- neue Videos erkennen
- normierte Items erzeugen
- Transcript-Erfassung integrieren
- Transcript in Archiv-Output überführen
- Fehlerbehandlung für fehlende oder deaktivierte Transkripte ergänzen

### Ergebnis

InfoManagerBot kann neue YouTube-Inhalte erkennen und textbasiert archivieren.

---

## Phase 7 – Processing-Pipeline und Deduplizierung

### Ziel

Neue Items zuverlässig verarbeiten und Duplikate vermeiden.

### Aufgaben

- Pipeline-Schritte implementieren:
  1. Identität bestimmen
  2. Duplikat prüfen
  3. Metadaten normalisieren
  4. Content bereitstellen
  5. Artefakte schreiben
  6. Status aktualisieren
- Deduplizierung primär über `(source_id, external_id)`
- optional `content_hash` vorbereiten
- Retry pro Item statt pro Gesamtlauf umsetzen

### Ergebnis

Eine quellentyp-unabhängige Verarbeitungslogik.

---

## Phase 8 – Archivschreiber

### Ziel

Verarbeitete Inhalte stabil und lesbar im Dateisystem ablegen.

### Aufgaben

- Ordnerkonvention definieren:
  - `output/<source_type>/<source_slug>/<YYYY-MM-DD>_<shortid>_<slug>/`
- `metadata.json` schreiben
- `content.md` schreiben
- Artefakte in der DB registrieren
- Pfadstabilität sicherstellen

### Ergebnis

Ein nutzbares lokales Archiv als Kernwert des Systems.

---

## Phase 9 – Docker-Compose und lokale Betriebsfähigkeit

### Ziel

Das System reproduzierbar startbar machen.

### Aufgaben

- Dockerfile anlegen
- Docker-Compose-Datei anlegen
- Mounts definieren für:
  - `config/`
  - `data/`
  - `output/`
- Umgebungsvariablen bzw. Settings sauber anbinden
- lokales Starten und Stoppen testen

### Ergebnis

Der MVP läuft reproduzierbar in einem Container-Setup.

---

## Phase 10 – Backup- und Betriebsgrundlagen

### Ziel

Wiederherstellbarkeit und sauberen Betrieb absichern.

### Aufgaben

- SQLite-Backup per `.backup` oder `VACUUM INTO` vorbereiten
- Backup-Skript oder Backup-Command definieren
- Syncthing nur für `output/` vorsehen
- Trennung von Sync und Backup dokumentieren
- erste Retention-Regeln festhalten

### Ergebnis

Ein MVP, der nicht nur läuft, sondern auch betrieblich sauber gedacht ist.

---

## Phase 11 – Tests und MVP-Abnahme

### Ziel

Sicherstellen, dass der MVP nicht nur „irgendwie läuft“, sondern belastbar ist.

### Aufgaben

- Unit-Tests für:
  - Konfigurationsvalidierung
  - ID-/Deduplogik
  - Archivpfaderzeugung
- Integrationstests für:
  - RSS-Verarbeitung
  - YouTube-Verarbeitung
- manueller Docker-Testlauf
- MVP-Abnahmekriterien prüfen

### Ergebnis

Ein validierter MVP mit klarer Erfolgskontrolle.

---

## Empfohlene erste Ordnerstruktur

```text
InfoManagerBot/
├─ docs/
│  └─ planning/
│     └─ umsetzungsplan_mvp.md
├─ config/
│  ├─ sources.yaml
│  ├─ policies.yaml
│  └─ settings.yaml
├─ src/
│  └─ infomanagerbot/
│     ├─ main.py
│     ├─ scheduler.py
│     ├─ orchestrator.py
│     ├─ pipeline.py
│     ├─ logging_config.py
│     ├─ config/
│     ├─ domain/
│     ├─ adapters/
│     ├─ persistence/
│     ├─ archive/
│     └─ utils/
├─ tests/
├─ migrations/
├─ data/
├─ output/
├─ .gitignore
├─ README.md
└─ docker-compose.yml
````

**Hinweis:**

- `data/` und `output/` sind Laufzeitordner
- `docs/`, `config/`, `src/`, `tests/`, `migrations/` gehören ins Repo
- `data/` und `output/` sollten in Git in der Regel ignoriert werden

---

## Reihenfolge für die praktische Umsetzung

1. Repo-Struktur anlegen
2. Konfigurationsdateien und Schemas definieren
3. SQLite-Schema und Migrationsbasis erstellen
4. Logging + Run-Tracking + Orchestrator-Grundgerüst anlegen
5. Adapter-Framework bauen
6. RSS-Adapter implementieren
7. YouTube-Adapter implementieren
8. Processing-Pipeline + Archivschreiber vervollständigen
9. Docker-Compose ergänzen
10. Backup und Tests abrunden

---

## Definition of Done für den MVP

- Docker-Compose-Start funktioniert
- mindestens zwei RSS-Quellen laufen
- mindestens ein YouTube-Kanal läuft
- neue Inhalte werden dedupliziert erkannt
- `metadata.json` und `content.md` werden geschrieben
- Runs und Fehler sind nachvollziehbar geloggt
- SQLite-Backup ist konsistent möglich
- `output/` ist für Syncthing geeignet
