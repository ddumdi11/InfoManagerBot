# InfoManagerBot

## Aktueller Stand

Das Repository enthält derzeit die minimale MVP-Grundstruktur für ein source-first Projekt.
Der Fokus liegt auf Dokumentation, Konfiguration und Paketstruktur; Implementierungen für Business-Logik, Adapter, Persistenz und Archivierung sind bewusst noch offen.

Nach einer lokalen Installation, z. B. mit `python -m pip install -e .`, ist das Basispaket über `infomanagerbot --settings config/settings.example.yaml --policies config/policies.example.yaml --sources config/sources.example.yaml` startbar; dabei wird bei Bedarf auch das Initialschema der SQLite-Datenbank angelegt.
