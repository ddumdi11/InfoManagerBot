## Prompt 1

Du arbeitest im Repo "InfoManagerBot".

Ziel:
Lege eine saubere MVP-Grundstruktur für das Projekt an, ohne schon Implementierungslogik zu erfinden. Nutze bestehende Dateien weiter, überschreibe nichts unnötig, und arbeite konservativ, nachvollziehbar und minimal.

Wichtige Leitplanken:

- Dies ist ein source-first Projekt.
- Browser-Capture ist noch NICHT Teil des MVP.
- Jetzt geht es nur um Repo-Grundstruktur, Dokumentationsstruktur und Basiskonfiguration.
- Bestehende Dateien wie README.md, LICENSE, .gitignore und docs/planning/umsetzungsplan_mvp.md sollen respektiert und nur sinnvoll ergänzt werden.
- Die bestehende .gitignore basiert bereits auf dem GitHub-Python-Template. Ergänze sie nur dort, wo es für dieses Projekt zusätzlich sinnvoll ist.
- docs/ darf NICHT ignoriert werden.
- Noch keine Business-Logik, keine Adapter-Implementierung, keine SQLite-Implementierung, keine Docker-Implementierung.
- Falls du Annahmen treffen musst, halte sie minimal und dokumentiere sie.

Aufgaben:

1. Prüfe die bestehende Repo-Struktur.

2. Ergänze eine erste sinnvolle Ordnerstruktur für den MVP:
   - docs/architecture/
   - docs/requirements/
   - docs/planning/   (falls noch nicht vorhanden, sonst unverändert lassen)
   - config/
   - src/infomanagerbot/
   - src/infomanagerbot/config/
   - src/infomanagerbot/domain/
   - src/infomanagerbot/adapters/
   - src/infomanagerbot/persistence/
   - src/infomanagerbot/archive/
   - src/infomanagerbot/utils/
   - tests/
   - migrations/
3. Lege in Python-Paketen sinnvolle leere __init__.py-Dateien an, aber keine unnötigen Dummy-Klassen.

4. Ergänze die bestehende .gitignore nur um projektspezifisch sinnvolle Einträge, falls sie noch fehlen:
   - data/
   - output/
   - logs/
   - optional .env
   - optional config/*.local.yaml
   Achte darauf, docs/ NICHT zu ignorieren.

5. Lege Beispiel-/Platzhalterdateien nur dort an, wo sie für die Struktur sinnvoll sind, z. B.:
   - config/sources.example.yaml
   - config/policies.example.yaml
   - config/settings.example.yaml
6. Erstelle KEINE produktive Konfiguration mit echten Quellen.

7. Ergänze README.md knapp und sachlich um einen sehr kleinen Abschnitt "Projektstruktur" oder "Aktueller Stand", aber blähe die Datei nicht auf.

8. Lege eine kurze Architektur-Notiz als neue Datei an:
   - docs/architecture/mvp_scope.md
   Inhalt:
   - MVP umfasst RSS/Atom und YouTube-Kanäle
   - Browser-Capture ist bewusst nicht Teil von Phase 1
   - source-first statt browser-first
   - SQLite, YAML, Markdown/JSON-Archiv und Docker Compose sind vorgesehen, aber noch nicht implementiert
   Halte diese Datei kurz.
9. Lege eine kurze Requirements-Notiz an:
   - docs/requirements/mvp_requirements_short.md
   Inhalt:
   - nur stichpunktartige Kurzfassung der MVP-Ziele
   - keine große Wiederholung des kompletten Umsetzungsplans
10. Füge keine unnötigen Tools, Dependencies oder Framework-Dateien hinzu.

Wichtig:

- Arbeite minimalistisch und strukturiert.
- Keine Overengineering-Spuren.
- Keine Platzhaltertexte wie "TODO everything".
- Keine erfundenen Implementierungsdetails.
- Wenn du Dateien anlegst, dann mit knappem, brauchbarem Inhalt.

Am Ende:

- Zeige eine kurze Zusammenfassung der angelegten/geänderten Dateien.

- Begründe kurz, warum du die .gitignore ergänzt hast.
- Weise auf Stellen hin, die bewusst noch leer geblieben sind.

## Prompt 2

Du arbeitest im Repo "InfoManagerBot".

Ziel:
Baue das Python-Grundgerüst für den MVP weiter aus, ohne schon echte Adapter-, Datenbank- oder Archivlogik vollständig zu implementieren. Das Ergebnis soll ein sauberes, kleines, startbares Basispaket sein.

Wichtige Leitplanken:

- Keine Browser-Capture-Implementierung.
- Keine Business-Logik für RSS/YouTube im Detail.
- Keine SQLite-Schema-Implementierung in dieser Runde.
- Keine Docker-Implementierung in dieser Runde.
- Konservativ und minimal arbeiten.
- Bestehende Struktur respektieren.

Aufgaben:

1. Lege eine minimale Python-Projektkonfiguration an:
   - `pyproject.toml`
   - sinnvolle Basis für ein modernes Python-Projekt
   - Projektname: `infomanagerbot`
   - Python-Version pragmatisch und aktuell-stabil wählen
   - noch nur wenige, wirklich notwendige Dependencies aufnehmen

2. Lege einen kleinen startbaren CLI-/App-Einstieg an:
   - `src/infomanagerbot/main.py`
   - `src/infomanagerbot/__main__.py`
   Anforderungen:
   - App soll startbar sein
   - beim Start Logging initialisieren
   - Konfiguration laden/validieren vorbereiten
   - noch keine echten Adapterläufe ausführen
   - eine knappe, ehrliche Konsolenausgabe erzeugen wie: Projektgrundgerüst geladen / Konfiguration erfolgreich geprüft / weitere Implementierung folgt

3. Lege eine minimale Logging-Konfiguration an:
   - `src/infomanagerbot/logging_config.py`
   - zunächst einfache, saubere Standardkonfiguration
   - kein Overengineering
   - strukturierbar angelegt, aber noch nicht mit komplexen JSON-Logger-Setups überfrachten

4. Lege Konfigurationsmodelle an:
   - `src/infomanagerbot/config/models.py`
   - `src/infomanagerbot/config/loader.py`
   Anforderungen:
   - Modelle für Settings, Policies und Sources vorbereiten
   - Pydantic oder eine ähnlich saubere Validierungslösung verwenden
   - nur MVP-relevante Felder modellieren
   - Quellentypen zunächst auf `rss_atom` und `youtube_channel` begrenzen
   - `browser_capture` noch nicht als aktiver Typ
   - Beispiel-YAML-Dateien sollen zu den Modellen passen
   - Loader soll Beispiel-/Produktivpfade laden können, aber noch keine komplizierte Fallback-Magie einbauen

5. Ergänze die Beispielkonfigurationen bei Bedarf so, dass sie zu den Modellen passen.
   - keine echten Quellen eintragen
   - nur neutrale Platzhalter

6. Lege erste Domänenmodelle an:
   - `src/infomanagerbot/domain/models.py`
   Anforderungen:
   - nur einfache Dataclasses oder Pydantic-Modelle für:
     - Source
     - Policy
     - DiscoveredItem
     - RunInfo
   - noch keine Persistenzlogik
   - noch keine Businessmethoden

7. Lege eine sehr kleine Orchestrator-Vorbereitung an:
   - `src/infomanagerbot/orchestrator.py`
   Anforderungen:
   - nur ein dünnes Grundgerüst
   - darf z. B. Konfiguration entgegennehmen und einen Stub-Lauf vorbereiten
   - keine Polling-Schleife, keine echte Verarbeitung

8. README.md nur dann minimal ergänzen, wenn ein Startkommando sinnvoll dokumentiert werden kann.
   - Bitte README nicht unnötig aufblasen.

Wichtig:

- Keine erfundenen Features als schon implementiert darstellen.
- Keine Dummy-Methodenflut.
- Lieber wenige saubere Dateien als viel Gerüstlärm.
- Code klar, knapp und nachvollziehbar.
- Falls du Entscheidungen treffen musst, dokumentiere sie knapp im Code oder in der Zusammenfassung.

Am Ende:

- Zeige die angelegten/geänderten Dateien.
- Erkläre kurz die gewählten Dependencies.
- Nenne bewusst noch nicht implementierte Teile.

## Prompt 3

Du arbeitest im Repo "InfoManagerBot".

Ziel:
Baue als nächsten Schritt die SQLite- und Persistenzbasis für den MVP auf. Es geht um ein sauberes, kleines Fundament: Datenbankschema, Migrationsbasis, DB-Verbindung und erste Repository-Struktur. Noch keine vollständige Business-Logik, keine Adapterimplementierung, keine Archivlogik, keine Docker-Umsetzung.

Wichtige Leitplanken:

- Konservativ und minimal arbeiten.
- Bestehende Struktur respektieren.
- Keine erfundenen Features als fertig darstellen.
- Noch keine echte Polling- oder Processing-Logik implementieren.
- Noch keine Browser-Capture-Logik.
- Noch keine vollständige Archivierung.
- Noch keine komplexen ORMs einführen.
- SQLite direkt und schlank verwenden.

Wichtiger Zusatzauftrag zur Doku:

- Pflege `docs/planning/dev_log.md` mit.
- Falls die Datei bereits existiert, ergänze sie.
- Falls für den letzten Arbeitsschritt (Prompt 2: Python-Grundgerüst, Config-Modelle, CLI-Einstieg) noch kein sinnvoller Eintrag enthalten ist, ergänze auch diesen knapp nachträglich.
- Ergänze außerdem einen neuen kurzen Eintrag für diesen aktuellen Schritt.
- Halte die Dev-Log-Einträge knapp, sachlich und entscheidungsorientiert. Kein Roman, keine Datei-für-Datei-Chronik.

Aufgaben:

1. Lege eine schlanke Persistenzbasis an unter:

   - `src/infomanagerbot/persistence/connection.py`
   - `src/infomanagerbot/persistence/schema.py`
   - `src/infomanagerbot/persistence/repositories.py`
   - optional weitere sehr kleine Hilfsdateien, falls wirklich sinnvoll

2. Lege ein Initialschema als SQL-Datei an:
   - `migrations/001_initial_schema.sql`
   Anforderungen:
   - Tabellen mindestens für:
     - `sources`
     - `items`
     - `artifacts`
     - `runs`
     - `policies`
     - `schema_migrations`
   - Foreign Keys sinnvoll setzen
   - Eindeutigkeitsregeln sinnvoll und konservativ definieren
   - Fokus auf MVP, nicht auf spätere Maximalfälle
   - Keine unnötig exotischen SQLite-Konstrukte

3. Ergänze eine schlanke Schema-/Migrationsunterstützung:
   Anforderungen:
   - prüfen können, ob das Initialschema bereits angewendet wurde
   - `schema_migrations` sauber nutzen
   - keine komplexe Migrationsengine bauen
   - einfache, nachvollziehbare Lösung

4. Implementiere eine minimale SQLite-Verbindungslogik:
   Anforderungen:
   - Datenbankpfad aus Settings oder sinnvoller Konfiguration ableitbar
   - Foreign Keys aktivieren
   - WAL-Modus aktivieren
   - Code klar und klein halten

5. Lege erste Repository-Grundgerüste an:
   Anforderungen:
   - nur kleine, sinnvolle Klassen/Funktionen
   - mindestens vorbereiten für:
     - Policies lesen
     - Sources lesen/synchronisieren
     - Runs anlegen/abschließen
   - noch keine komplette CRUD-Flut
   - keine Business-Entscheidungen in die Repositories verlagern

6. Falls nötig, ergänze die Config-Modelle minimal, damit der Datenbankpfad sauber abbildbar ist. Aber:

   - keine große Modell-Umbauaktion
   - nur das ergänzen, was für die Persistenzbasis wirklich gebraucht wird

7. Ergänze `src/infomanagerbot/main.py` nur minimal:
   Anforderungen:
   - Datenbankinitialisierung vorbereiten
   - Schemaanwendung beim Start ermöglichen
   - weiterhin ehrlich bleiben: noch keine eigentliche Verarbeitung starten
   - Konsole/Logging soll klar erkennen lassen, dass Konfiguration und Persistenzbasis vorbereitet wurden

8. README.md nur minimal ergänzen, falls jetzt ein sinnvoller Start-/Init-Hinweis hinzugefügt werden kann.
   Sonst lieber nicht anfassen.

9. Achte darauf, dass bestehende Beispiel-YAMLs und Modelle nicht unnötig zerbrechen.
   Wenn du Felder ergänzen musst, dann konsistent und knapp.

Wichtig:

- Kein ORM.
- Kein SQLAlchemy.
- Keine übergroßen Repository-Klassen.
- Kein Overengineering.
- Keine vorweggenommene Adapterlogik.
- Keine künstliche Vollständigkeit.

Am Ende:

- Zeige die angelegten/geänderten Dateien.
- Erkläre kurz die wichtigsten Schema-Entscheidungen.
- Nenne bewusst noch nicht implementierte Teile.
- Erwähne kurz, wie `dev_log.md` ergänzt wurde.

## PROMPT 4

Du arbeitest im Repo "InfoManagerBot".

Ziel:
Implementiere als nächsten Schritt ein kleines, sauberes Adapter-Framework für den MVP und den ersten produktiv nutzbaren Quellentyp: RSS/Atom. Es geht noch nicht um vollständige Verarbeitung, Archivierung oder YouTube. Der Schwerpunkt liegt auf einer klaren Adapter-Schnittstelle, normierten entdeckten Items und einem ersten RSS-Adapter.

Wichtige Leitplanken:

- Konservativ und minimal arbeiten.
- Bestehende Struktur respektieren.
- Kein Overengineering.
- Noch keine Browser-Capture-Logik.
- Noch keine YouTube-Implementierung.
- Noch keine vollständige Processing-Pipeline.
- Noch keine Archivlogik.
- Noch keine Polling-Endlosschleife.
- Noch keine Item-Persistenzlogik im großen Stil.
- Adapter sollen Daten liefern, nicht das ganze System steuern.

Wichtiger Zusatzauftrag zur Doku:

- Pflege `docs/planning/dev_log.md` mit einem knappen neuen Eintrag für diesen Arbeitsschritt.
- Halte den Eintrag kurz, sachlich und entscheidungsorientiert.

Aufgaben:

1. Lege eine kleine Adapter-Basis an unter:

   - `src/infomanagerbot/adapters/base.py`
   - `src/infomanagerbot/adapters/registry.py`
   - optional weitere sehr kleine Hilfsdateien, falls wirklich nötig

2. Definiere eine klare Basisschnittstelle für Adapter.
   Anforderungen:
   - Pflichtmethode: `discover(...)`
   - optional vorbereitbar: `enrich(...)`, aber noch nicht überkomplex ausbauen
   - Adapter sollen keine DB-Commits ausführen
   - Adapter sollen keine Archivdateien schreiben
   - Adapter sollen keine Orchestrierungsentscheidungen treffen

3. Nutze oder erweitere die vorhandenen Domänenmodelle so, dass ein normiertes `DiscoveredItem` sauber verwendet werden kann.
   Anforderungen:
   - keine unnötige Modellinflation
   - Felder nur soweit ergänzen, wie RSS sie sinnvoll braucht
   - `external_id`, `title`, `source_key`, `url`, `published_at`, `content_text` oder ähnlich sinnvoll strukturieren
   - lieber klar als maximal generisch

4. Implementiere einen RSS-/Atom-Adapter unter:
   - `src/infomanagerbot/adapters/rss.py`
   Anforderungen:
   - geeignete kleine Library verwenden, falls noch nicht vorhanden und wirklich nötig
   - Feed aus der Source-Konfiguration laden
   - Einträge in normierte `DiscoveredItem`s überführen
   - externe ID möglichst stabil ableiten
   - falls keine gute ID vorhanden ist, eine konservative Fallback-ID bilden
   - Fehlerbehandlung knapp und sauber halten
   - noch kein Volltext-Nachladen von Artikeln
   - nur Feed-Inhalt bzw. Eintragsinhalt nutzen

5. Ergänze `pyproject.toml` nur um die wirklich nötige Dependency für RSS/Atom, falls erforderlich.
   - keine Tool-Lawine
   - begründe die Wahl kurz in der Zusammenfassung

6. Ergänze die Config-Modelle nur minimal, falls für RSS noch sinnvolle source-spezifische Felder fehlen.
   Aber:
   - keine große Modellumbauaktion
   - keine Vorwegnahme von YouTube- oder Browser-Sonderlogik

7. Ergänze `config/sources.example.yaml` sinnvoll, damit mindestens eine neutrale RSS-Beispielquelle zur Modellstruktur passt.
   - keine echten produktiven Feeds
   - neutrale Platzhalterwerte

8. Ergänze den Orchestrator nur minimal, falls nötig.
   Anforderungen:
   - maximal so weit, dass ein vorbereiteter Discovery-Schritt denkbar ist
   - noch keine echte Gesamtpipeline bauen

9. Lege nach Möglichkeit einen sehr kleinen Test an:
   - z. B. für Fallback-ID-Bildung oder Mapping eines Feed-Eintrags in `DiscoveredItem`
   - nur wenn sinnvoll und ohne Test-Overkill

10. README nur dann minimal ergänzen, wenn jetzt ein sinnvoller Hinweis zum aktuellen Entwicklungsstand dazukommt.
    Sonst lieber nicht anfassen.

Wichtig:

- Kein komplettes Polling-System bauen.
- Kein Speichern der gefundenen Items in SQLite in dieser Runde.
- Keine künstliche Abstraktionsschicht für fünf zukünftige Adaptertypen.
- Keine Vollständigkeits-Illusion.
- Der RSS-Adapter soll klein, brauchbar und gut lesbar sein.

Am Ende:

- Zeige die angelegten/geänderten Dateien.
- Erkläre kurz die Adapter-Schnittstelle.
- Erkläre kurz, wie die externe ID für RSS-Einträge bestimmt wird.
- Nenne bewusst noch nicht implementierte Teile.
- Erwähne kurz den neuen `dev_log.md`-Eintrag.

## PROMPT 5

Du arbeitest im Repo "InfoManagerBot" auf dem aktuell ausgecheckten Feature-Branch.

Wichtige Prozessanweisung:

- Bleibe auf dem aktuellen Branch.
- Führe keinen Push aus.
- Erstelle keinen Pull Request.
- Nimm keine Git-Operationen vor, die Branches wechseln, mergen oder remote verändern.
- Nach Abschluss deiner Änderungen sollst du stoppen und auf unser Go warten.

Ziel:
Erweitere das MVP-Grundgerüst um den zweiten geplanten Quellentyp: YouTube-Kanal-Discovery. Baue dazu einen kleinen, sauberen YouTube-Adapter, der neue Videoeinträge aus einem Kanalfeed in normierte `DiscoveredItem`s überführt. Es geht noch nicht um Transkript-Erfassung, Archivierung, Item-Persistenz oder eine vollständige Pipeline.

Wichtige Leitplanken:

- Konservativ und minimal arbeiten.
- Bestehende Struktur respektieren.
- Kein Overengineering.
- Keine Browser-Capture-Logik.
- Keine Transkript-Logik in dieser Runde.
- Keine Item-Speicherung in SQLite.
- Keine vollständige Orchestrierungs- oder Polling-Logik.
- Kein Vollausbau der Registry über das Nötige hinaus.
- Adapter liefern normierte Daten, nicht mehr.

Wichtiger Zusatzauftrag zur Doku:

- Pflege `docs/planning/dev_log.md` mit einem knappen neuen Eintrag für diesen Arbeitsschritt.
- Halte den Eintrag kurz, sachlich und entscheidungsorientiert.

Aufgaben:

1. Implementiere einen YouTube-Discovery-Adapter unter:
   - `src/infomanagerbot/adapters/youtube.py`

2. Nutze für YouTube einen pragmatischen Feed-basierten Ansatz.
   Anforderungen:
   - Kein API-Key-Zwang
   - Kein YouTube-Data-API-Setup
   - Kein Download von Videos
   - Kein Transkriptabruf
   - Fokus nur auf Discovery von Kanalinhalten
   - Verwende einen stabilen, einfachen Weg über den Kanalfeed

3. Ergänze die Adapter-Registry so, dass neben RSS jetzt auch `youtube_channel` unterstützt wird.
   - Klein halten
   - Keine unnötige Abstraktionsinflation

4. Ergänze Config-Modelle nur minimal, falls für YouTube ein sinnvolles Feld fehlt.
   Anforderungen:
   - keine große Umbauaktion
   - keine Vorwegnahme von Browser- oder Transkript-Sonderlogik
   - falls möglich mit bestehenden Source-Feldern arbeiten
   - wenn du ein spezifisches Feld ergänzt (z. B. channel_id), dann knapp und konsistent

5. Ergänze `config/sources.example.yaml` um eine neutrale YouTube-Beispielquelle, die zur Modellstruktur passt.
   - keine echten produktiven Kanäle
   - neutrale Platzhalterwerte

6. Ergänze vorhandene Domänenmodelle nur minimal, falls YouTube-spezifische Discovery-Felder wirklich nötig sind.
   Aber:
   - `DiscoveredItem` nicht unnötig aufblasen
   - nur ergänzen, wenn RSS und YouTube gemeinsam davon profitieren

7. Ergänze den Orchestrator nur minimal, falls nötig.
   Anforderungen:
   - maximal so weit, dass ein Discovery-Schritt für verschiedene Adapter vorbereitet werden kann
   - keine Endlosschleife
   - keine vollständige Gesamtpipeline

8. Lege nach Möglichkeit einen kleinen Test an:
   - z. B. Mapping eines YouTube-Feed-Eintrags in `DiscoveredItem`
   - nur wenn sinnvoll und ohne Test-Overkill

9. Ergänze `pyproject.toml` nur dann, wenn für den Feed-basierten YouTube-Ansatz wirklich eine zusätzliche Dependency nötig ist.
   Falls bestehende RSS/Atom-Mechanik bzw. `feedparser` schon reicht, verwende bevorzugt das.

10. README nur dann minimal ergänzen, wenn jetzt ein kurzer, ehrlicher Hinweis zum Entwicklungsstand sinnvoll ist.
    Sonst lieber nicht anfassen.

Wichtig:

- Kein YouTube-Transcript in dieser Runde.
- Kein Download von Medien.
- Keine Speicherung der entdeckten Items in SQLite.
- Kein Vorgriff auf spätere Volltext-/Archivlogik.
- Kein API-Key-Management.
- Keine künstliche Universalabstraktion.

Am Ende:

- Zeige die angelegten/geänderten Dateien.
- Erkläre kurz, wie der YouTube-Adapter Discovery betreibt.
- Erkläre kurz, wie die externe ID für YouTube-Einträge bestimmt wird.
- Nenne bewusst noch nicht implementierte Teile.
- Erwähne kurz den neuen `dev_log.md`-Eintrag.
- Bestätige ausdrücklich, dass du NICHT gepusht und KEINEN PR erstellt hast.

## PROMPT 6

Du arbeitest im Repo "InfoManagerBot" auf dem aktuell ausgecheckten Feature-Branch.

Wichtige Prozessanweisung:

- Bleibe auf dem aktuellen Branch.
- Führe keinen Push aus.
- Erstelle keinen Pull Request.
- Nimm keine Git-Operationen vor, die Branches wechseln, mergen oder remote verändern.
- Nach Abschluss deiner Änderungen sollst du stoppen und auf unser Go warten.

Ziel:

Führe eine kleine, gezielte Konsolidierungs- und Qualitätsrunde durch. Übernimm nur die sinnvollen, aktuell passenden Verbesserungen aus dem Code-Review. Kein großer neuer Feature-Block in dieser Runde.

Wichtige Leitplanken:

- Konservativ und minimal arbeiten.
- Bestehende Struktur respektieren.
- Kein Overengineering.
- Keine neuen größeren Features.
- Keine YouTube-Transkripte.
- Keine Browser-Capture-Logik.
- Keine Item-Persistenz in dieser Runde.
- Keine Gesamtpipeline in dieser Runde.
- Keine Rename-Orgie ohne klaren Nutzen.

Wichtiger Zusatzauftrag zur Doku:

- Pflege `docs/planning/dev_log.md` mit einem knappen neuen Eintrag für diese Konsolidierungsrunde.
- Halte den Eintrag kurz, sachlich und entscheidungsorientiert.

Bitte setze in dieser Runde gezielt nur die folgenden Punkte um:

1. Markdown-Fix
- Prüfe `docs/planning/umsetzungsplan_mvp.md` auf eine fehlerhafte schließende Code-Fence mit vier Backticks.
- Falls vorhanden, korrigiere sie auf die normale Drei-Backtick-Variante.
- Nimm keine sonstigen inhaltlichen Änderungen am Umsetzungsplan vor.

2. RSS-Adapter: bozo-Handling robuster machen
- In `src/infomanagerbot/adapters/rss.py` soll `bozo=True` nicht mehr pauschal als harter Fehler behandelt werden.
- Logge stattdessen eine Warnung mit Ausnahme-Details.
- Wirf nur dann `AdapterError`, wenn der Feed keine brauchbaren `entries` enthält oder wenn der Fehler klar auf einen unbrauchbaren Feed hinausläuft.
- Halte die Lösung klein und pragmatisch.

3. Orchestrator: source_count fachlich korrekt machen
- In `src/infomanagerbot/orchestrator.py` soll `prepare_run()` nur die Quellen zählen, die auch tatsächlich für Discovery vorgesehen sind.
- Verwende dafür dieselbe Filterlogik wie für die Discovery-Quellen.
- Keine zusätzliche Orchestrierungslogik einbauen.

4. RunRepository.finish_run absichern
- In `src/infomanagerbot/persistence/repositories.py` soll `finish_run()` prüfen, ob das UPDATE tatsächlich eine Zeile getroffen hat.
- Wenn `rowcount == 0`, wirf eine klare `RuntimeError`.
- Commit nur bei erfolgreichem Update.

5. Repository-Sync atomarer machen
- In `PolicyRepository.sync()` und `SourceRepository.sync()` die Schleifen in `with self.connection:` ausführen, damit Commit/Rollback atomarer und sauberer sind.
- Keine komplette Repository-Umstrukturierung.

6. Adapter-Registry nicht bei jedem Aufruf neu bauen
- In `src/infomanagerbot/adapters/registry.py` eine kleine gecachte Registry einführen.
- Keine unnötige Komplexität, einfach und lesbar halten.

7. Config-Loader: bessere Validierungsfehler
- In `src/infomanagerbot/config/loader.py` Validation-Fehler mit kontextreichen Meldungen versehen, z. B. für Settings / Policies / Sources.
- Ursprüngliche Exceptions sauber chainen.

8. Logging-Konfiguration: ungültiges Log-Level kenntlich machen
- In `src/infomanagerbot/logging_config.py` bei ungültigem Log-Level eine Warnung ausgeben und auf INFO zurückfallen.
- Kein Umbau der Logging-Architektur.

9. Kleine Typ-/Dokuverbesserungen nur wenn sehr günstig
- Falls ohne Umbau sinnvoll, darfst du `DiscoveryAdapter.source_type` typmäßig etwas schärfen.
- Falls sehr leichtgewichtig, darfst du in Feed-Zeitstempel-Parsing einen kurzen Kommentar zur UTC-Annahme ergänzen.
- Diese beiden Punkte sind optional und nur umzusetzen, wenn sie ohne Folgeschäden klein bleiben.

Bitte in dieser Runde ausdrücklich NICHT umsetzen:
- keine Umbenennung von `DiscoveredItem.source_key`
- keine größere Schema-Erweiterung der `items`-Tabelle
- keine Änderungen an Test-Importstrategie Richtung `pip install -e .`
- keine package-relative CLI-Pfad-Architektur in `main.py`
- keine neue Migrationsrunde
- keine neuen Features jenseits der obigen Qualitätsfixes

Am Ende:
- Zeige die angelegten/geänderten Dateien.
- Liste kurz auf, welche Review-Hinweise du übernommen hast.
- Nenne bewusst nicht umgesetzte Hinweise, die du absichtlich zurückgestellt hast.
- Erwähne kurz den neuen `dev_log.md`-Eintrag.
- Bestätige ausdrücklich, dass du NICHT gepusht und KEINEN PR erstellt hast.

## PROMPT 7

Du arbeitest im Repo "InfoManagerBot" auf dem aktuell ausgecheckten Feature-Branch.

Wichtige Prozessanweisung:

- Bleibe auf dem aktuellen Branch.
- Führe keinen Push aus.
- Erstelle keinen Pull Request.
- Nimm keine Git-Operationen vor, die Branches wechseln, mergen oder remote verändern.
- Nach Abschluss deiner Änderungen sollst du stoppen und auf unser Go warten.

Ziel:
Implementiere den ersten echten MVP-Discovery-Durchlauf: aktive Quellen sollen über die vorhandenen Adapter entdeckt werden können, neue `DiscoveredItem`s sollen dedupliziert geprüft und als erste persistierte `items` in SQLite gespeichert werden. Es geht noch NICHT um Archivierung, Markdown/JSON-Ausgabe, Transkripte, Browser-Capture oder eine vollständige End-to-End-Pipeline.

Wichtige Leitplanken:

- Konservativ und minimal arbeiten.
- Bestehende Struktur respektieren.
- Kein Overengineering.
- Keine Archivdateien schreiben.
- Keine Browser-Capture-Logik.
- Keine YouTube-Transkript-Logik.
- Keine komplexe Scheduler-/Polling-Endlosschleife.
- Keine vollständige Retry-Engine.
- Keine ORM-Einführung.
- Keine große Schema-Neuerfindung.

Wichtiger Zusatzauftrag zur Doku:

- Pflege `docs/planning/dev_log.md` mit einem knappen neuen Eintrag für diesen Arbeitsschritt.
- Halte den Eintrag kurz, sachlich und entscheidungsorientiert.

Aufgaben:

1. Implementiere eine kleine Discovery-Ausführung im Orchestrator.
   Anforderungen:
   - aktive Discovery-Quellen aus der Konfiguration verwenden
   - passenden Adapter aus der Registry holen
   - `discover(...)` aufrufen
   - Ergebnisse pro Quelle sammeln
   - Fehler pro Quelle sauber behandeln, ohne den gesamten Lauf unnötig sofort zu zerstören
   - keine Endlosschleife bauen

2. Erweitere die Persistenzbasis um eine kleine `ItemRepository`-Struktur.
   Anforderungen:
   - neue Datei oder Ergänzung in `src/infomanagerbot/persistence/repositories.py`
   - mindestens vorbereiten für:
     - prüfen, ob ein Item für `(source_id, external_id)` bereits existiert
     - neues Item anlegen
     - optional kleine List-/Lookup-Helfer, wenn wirklich nötig
   - klein und lesbar halten
   - keine CRUD-Lawine

3. Passe das Schema nur an, wenn es für die erste Item-Persistenz wirklich nötig ist.
   Anforderungen:
   - Wenn zusätzliche Item-Felder in SQLite zwingend gebraucht werden, erstelle dafür eine neue Migration statt die bestehende Initialmigration still umzuschreiben.
   - Wenn die aktuelle `items`-Tabelle für den MVP-Discovery-Schritt ausreicht, belasse das Schema.
   - Keine große Schema-Erweiterung nur „für später vielleicht“.

4. Implementiere eine kleine Persistenzabbildung von `DiscoveredItem` -> `items`.
   Anforderungen:
   - mindestens speichern:
     - zugehörige Quelle
     - `external_id`
     - Titel
     - URL
     - Status
     - Zeitstempel für Entdeckung
   - wenn sinnvoll und ohne Schemaumbau machbar, dürfen auch `published_at` oder ähnliches berücksichtigt werden
   - keine inhaltliche Archivierung

5. Deduplizierung:
   Anforderungen:
   - primär auf Basis von `(source_id, external_id)`
   - bereits vorhandene Items nicht doppelt anlegen
   - Ergebnis des Laufs soll unterscheiden können zwischen:
     - neu gespeichert
     - bereits bekannt
     - Fehler bei Discovery/Persistenz

6. Run-Integration:
   Anforderungen:
   - vorhandene `runs`-Logik sinnvoll nutzen
   - `prepare_run()` nicht nur vorbereiten, sondern die Discovery-Ausführung damit verbinden
   - am Ende einen ehrlichen Run-Status setzen
   - keine überkomplexen Laufmetriken, aber ein paar sinnvolle Zahlen oder Notizen sind willkommen, wenn sie klein bleiben

7. CLI-/main-Integration:
   Anforderungen:
   - `main.py` so erweitern, dass der Discovery-Lauf jetzt tatsächlich ausgeführt werden kann
   - Konsolenausgabe und Logging ehrlich halten
   - klar machen, dass jetzt Discovery + Item-Persistenz laufen, aber Archivierung noch nicht

8. Tests:
   Lege nach Möglichkeit ein oder zwei kleine sinnvolle Tests an, zum Beispiel für:
   - Deduplizierung / `exists`-Logik
   - Persistenz neuer Items
   - Orchestrator-Verhalten bei bereits bekannten Items
   Aber:
   - kein Test-Overkill
   - keine riesige Testinfrastruktur

9. README nur dann minimal ergänzen, wenn jetzt ein kurzer Hinweis zum aktuellen Funktionsstand sinnvoll ist.
   Sonst lieber nicht anfassen.

Wichtig:

- Noch keine Markdown-/JSON-Archivartefakte.
- Noch keine `artifacts`-Erzeugung.
- Noch keine vollständige Pipeline über Discovery hinaus.
- Noch keine Browser-/Transkript-Themen.
- Keine automatische Git-Aktion.

Am Ende:

- Zeige die angelegten/geänderten Dateien.
- Erkläre kurz, wie Discovery-Ausführung und Deduplizierung jetzt funktionieren.
- Erkläre kurz, welche Item-Daten tatsächlich persistiert werden.
- Nenne bewusst noch nicht implementierte Teile.
- Erwähne kurz den neuen `dev_log.md`-Eintrag.
- Bestätige ausdrücklich, dass du NICHT gepusht und KEINEN PR erstellt hast.

## Prompt 8

Du arbeitest im Repo "InfoManagerBot" auf dem aktuell ausgecheckten Feature-Branch.

Wichtige Prozessanweisung:
- Bleibe auf dem aktuellen Branch.
- Führe keinen Push aus.
- Erstelle keinen Pull Request.
- Nimm keine Git-Operationen vor, die Branches wechseln, mergen oder remote verändern.
- Nach Abschluss deiner Änderungen sollst du stoppen und auf unser Go warten.

Ziel:
Implementiere die erste Archivierungsschicht für den MVP. Bereits entdeckte und in SQLite persistierte Items sollen als einfache Archivartefakte ins Dateisystem geschrieben werden. Pro neu verarbeitetem Item sollen mindestens `metadata.json` und `content.md` entstehen. Zusätzlich sollen erzeugte Artefakte in der Tabelle `artifacts` registriert werden. Es geht noch nicht um Browser-Capture, YouTube-Transkripte, Retry-Logik oder eine vollständige Produktionspipeline.

Wichtige Leitplanken:
- Konservativ und minimal arbeiten.
- Bestehende Struktur respektieren.
- Kein Overengineering.
- Keine Browser-Capture-Logik.
- Keine YouTube-Transkript-Logik.
- Keine Volltext-Nachlade-Logik.
- Keine Scheduler-/Daemon-Logik.
- Keine künstliche Universal-Archiv-Engine.
- Lesbare, kleine Dateien und Funktionen bevorzugen.

Wichtiger Zusatzauftrag zur Doku:

- Pflege `docs/planning/dev_log.md` mit einem knappen neuen Eintrag für diesen Arbeitsschritt.
- Halte den Eintrag kurz, sachlich und entscheidungsorientiert.

Aufgaben:
1. Lege eine kleine Archivierungsbasis an unter:

   - `src/infomanagerbot/archive/writer.py`
   - optional kleine Hilfsdateien unter `src/infomanagerbot/archive/`, falls wirklich sinnvoll
   Ziel:
   - zentrale, kleine Funktionen/Klassen zum Schreiben der Archivartefakte

2. Implementiere ein einfaches Archivierungsformat.
   Anforderungen:
   - pro Item mindestens:
     - `metadata.json`
     - `content.md`
   - `metadata.json` soll die wichtigsten Metadaten strukturiert enthalten
   - `content.md` soll lesbar und schlicht sein, keine große Template-Maschinerie
   - keine HTML-/Rich-Export-Komplexität

3. Definiere eine stabile Pfadstruktur für Archivobjekte.
   Anforderungen:
   - unterhalb von `output/`
   - sinnvoll gegliedert nach Quellentyp und Quelle
   - lesbarer, stabiler Zielpfad pro Item
   - nicht nur titelbasiert; eine stabile ID/Short-ID soll einfließen
   - Kollisionen vermeiden
   - Beispielrichtung:
     `output/<source_type>/<source_key>/<YYYY-MM-DD>_<shortid>_<slug>/`
   - wenn nötig, kleine Hilfsfunktionen für Slug/Short-ID/Pfade ergänzen

4. Erweitere die Persistenzbasis um eine kleine Artifact-Registrierung.
   Anforderungen:
   - Ergänzung in `src/infomanagerbot/persistence/repositories.py`
   - mindestens:
     - Artifact-Eintrag anlegen
     - ggf. prüfen, ob ein bestimmter Artifact-Typ für ein Item schon registriert ist
   - klein und lesbar halten
   - keine CRUD-Lawine

5. Implementiere eine kleine Verarbeitungslogik für bereits persistierte Items.
   Anforderungen:
   - finde Items, die archiviert werden sollen
   - erzeuge pro Item `metadata.json` und `content.md`
   - registriere die Artefakte in `artifacts`
   - markiere das Item sinnvoll als archiviert/verarbeitet, falls dafür eine kleine Schema-Erweiterung wirklich nötig ist
   - wenn dafür eine Schemaänderung nötig ist, lege eine neue Migration an, statt alte Migrationen umzuschreiben
   - keine große Workflow-Engine

6. Schema nur minimal erweitern, falls wirklich nötig.
   Anforderungen:
   - wenn für Item-Status oder Artifact-Tracking zusätzliche DB-Felder nötig sind, nutze eine neue Migration
   - keine unnötige Schema-Ausdehnung „für später vielleicht“

7. Integriere die Archivierung klein in Orchestrator und/oder `main.py`.
   Anforderungen:
   - nach erfolgreicher Discovery/Persistenz kann ein einfacher Archivierungsdurchlauf folgen
   - Logging ehrlich und knapp halten
   - klar machen, dass jetzt Discovery + Persistenz + erste Archivierung laufen
   - noch keine komplexe Mehrphasen-Orchestrierung

8. Metadateninhalt pragmatisch wählen.
   `metadata.json` sollte mindestens etwas wie Folgendes enthalten:
   - interne Item-ID
   - source_key
   - source_type
   - external_id
   - title
   - url
   - discovered_at
   - published_at (falls vorhanden)
   - run_id (falls vorhanden)
   - status
   Aber:
   - keine unnötige Metadateninflation

9. Markdown-Inhalt pragmatisch wählen.
   `content.md` sollte mindestens enthalten:
   - Titel als Überschrift
   - Quelle
   - URL
   - Zeitstempel, soweit vorhanden
   - eigentlichen Content-Text, soweit verfügbar
   Falls für manche Items noch kein sinnvoller Text vorliegt, dann:
   - ehrlicher, kleiner Hinweis statt künstlicher Fülltexte

10. Tests:

   Lege nach Möglichkeit ein oder zwei kleine sinnvolle Tests an, zum Beispiel für:

- Pfadbildung / Slug / Short-ID
- Schreiben von `metadata.json`
- Registrierung von `artifacts`

   Aber:

   - kein Test-Overkill
   - keine riesige Testinfrastruktur

11. README nur dann minimal ergänzen, wenn jetzt ein kurzer, ehrlicher Hinweis zum neuen Archivierungsstand sinnvoll ist. Sonst lieber nicht anfassen.

Wichtig:

- Noch keine Browser-Quellen.
- Noch keine Transkript-Dateien.
- Noch keine Bild-/Screenshot-Artefakte.
- Noch keine Volltext-Nachbeschaffung.
- Keine automatische Git-Aktion.
- Keine unnötige Template-Engine.

Am Ende:

- Zeige die angelegten/geänderten Dateien.
- Erkläre kurz, wie Archivpfad und Artefakt-Erzeugung funktionieren.
- Erkläre kurz, welche Metadaten in `metadata.json` landen.
- Nenne bewusst noch nicht implementierte Teile.
- Erwähne kurz den neuen `dev_log.md`-Eintrag.
- Bestätige ausdrücklich, dass du NICHT gepusht und KEINEN PR erstellt hast.
