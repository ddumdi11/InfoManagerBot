# Dev Log

## 2026-03-21

- Repo-Grundstruktur für den MVP angelegt.
- `.gitignore` um Laufzeitordner und lokale Config-Overrides ergänzt.
- Markdownlint für MD024 mit `siblings_only` konfiguriert.
- Python-Grundgerüst mit `pyproject.toml`, Config-Modellen und kleinem CLI-Einstieg vorbereitet.
- SQLite-Persistenzbasis mit Initialschema, schlanker Migrationsprüfung und kleinen Repositories ergänzt.
- Kleines Adapter-Framework und erster RSS/Atom-Adapter mit normiertem `DiscoveredItem` ergänzt.
- YouTube-Kanal-Discovery ueber den oeffentlichen Channel-Feed als zweiten Adaptertyp vorbereitet.
- Kleine Konsolidierungsrunde: robusteres RSS-Bozo-Handling, atomarere Repository-Syncs und klarere Validierungs-/Logging-Fehler ergänzt.
- Ersten echten Discovery-Lauf mit Deduplizierung und minimaler Item-Persistenz in SQLite ergänzt.
- Erste Archivierungsschicht mit `metadata.json`, `content.md` und Artifact-Registrierung im Dateisystem ergänzt.
- Browser-Capture weiterhin bewusst nicht Teil von Phase 1.
