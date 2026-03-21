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
