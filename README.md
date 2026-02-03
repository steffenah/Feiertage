# Feiertage Desktop Textbox

Dieses kleine Skript ermittelt Feiertage über die öffentliche Nager.Date-API und schreibt eine Textdatei auf den Desktop (oder ins Home-Verzeichnis, falls kein Desktop-Ordner existiert).

## Nutzung

```bash
python3 feiertage_desktop.py
```

Optionen:

```bash
python3 feiertage_desktop.py --country DE --year 2024
python3 feiertage_desktop.py --out /pfad/zu/Feiertage_2024.txt
```

## Hinweise

- Standard-Ländercode ist `DE` (Deutschland).
- Quelle der Daten: <https://date.nager.at>
