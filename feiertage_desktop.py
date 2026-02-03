#!/usr/bin/env python3
"""Fetch public holidays and write a desktop text file with the current year's summary."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Iterable

API_URL = "https://date.nager.at/api/v3/PublicHolidays/{year}/{country}"


def fetch_public_holidays(year: int, country_code: str) -> list[dict]:
    url = API_URL.format(year=year, country=country_code.upper())
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Konnte API nicht erreichen: {exc}") from exc

    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Antwort der API ist kein gültiges JSON.") from exc

    if not isinstance(data, list):
        raise RuntimeError("Unerwartetes API-Format: Liste erwartet.")
    return data


def desktop_path() -> Path:
    home = Path.home()
    desktop = home / "Desktop"
    if desktop.exists():
        return desktop
    return home


def format_holiday_list(holidays: Iterable[dict]) -> list[str]:
    lines = []
    for holiday in sorted(holidays, key=lambda item: item.get("date", "")):
        date = holiday.get("date", "?")
        local_name = holiday.get("localName", "Unbekannt")
        name = holiday.get("name", "")
        if name and name != local_name:
            label = f"{local_name} ({name})"
        else:
            label = local_name
        lines.append(f"- {date}: {label}")
    return lines


def build_report(year: int, country_code: str, holidays: list[dict]) -> str:
    count = len(holidays)
    lines = [
        f"Feiertage in {country_code.upper()} für {year}",
        "=" * 38,
        f"Anzahl der Feiertage: {count}",
        "",
        "Liste:",
        *format_holiday_list(holidays),
        "",
        "Quelle: https://date.nager.at",
    ]
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Ermittelt Feiertage über die Nager.Date-API und schreibt eine Textdatei "
            "auf den Desktop."
        )
    )
    parser.add_argument(
        "--country",
        default="DE",
        help="Ländercode nach ISO 3166-1 alpha-2 (Standard: DE).",
    )
    parser.add_argument(
        "--year",
        type=int,
        default=dt.date.today().year,
        help="Jahr der Feiertage (Standard: aktuelles Jahr).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Optionaler Ausgabepfad. Standard: Desktop/Feiertage_<Jahr>.txt",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        holidays = fetch_public_holidays(args.year, args.country)
    except RuntimeError as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return 1

    report = build_report(args.year, args.country, holidays)

    if args.out is None:
        output_path = desktop_path() / f"Feiertage_{args.year}.txt"
    else:
        output_path = args.out

    try:
        output_path.write_text(report, encoding="utf-8")
    except OSError as exc:
        print(f"Fehler beim Schreiben der Datei: {exc}", file=sys.stderr)
        return 1

    print(f"Feiertage gespeichert in: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
