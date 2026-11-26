"""Validate the generated Al-Muhit Indonesia override files."""

from __future__ import annotations

import re
from pathlib import Path

EXPECTED = {
    "631-Western Java.txt": {
        "id": 631,
        "manpower": 71459074,
        "resources": {
            "oil": 38,
            "steel": 61,
            "aluminium": 30,
            "coal": 10,
            "chromium": 20,
            "tungsten": 20,
            "rubber": 44,
        },
    },
    "1114-Central Java.txt": {
        "id": 1114,
        "manpower": 62457880,
        "resources": {
            "steel": 50,
            "aluminium": 20,
            "coal": 10,
            "chromium": 20,
            "tungsten": 10,
        },
    },
    "634-Eastern Java.txt": {
        "id": 634,
        "manpower": 69567280,
        "resources": {
            "oil": 13,
            "steel": 40,
            "aluminium": 10,
            "chromium": 10,
            "tungsten": 10,
            "rubber": 46,
        },
    },
    "640-Kalimantan.txt": {
        "id": 640,
        "manpower": 13561961,
        "resources": {
            "oil": 122,
            "steel": 82,
            "aluminium": 210,
            "coal": 80,
            "chromium": 60,
            "tungsten": 153,
            "rubber": 92,
        },
    },
    "639-Sulawesi.txt": {
        "id": 639,
        "manpower": 16396503,
        "resources": {
            "steel": 78,
            "aluminium": 80,
            "coal": 20,
            "chromium": 90,
            "tungsten": 50,
            "rubber": 46,
        },
    },
}


def as_int(value: str) -> int | float:
    number = float(value)
    return int(number) if number.is_integer() else number


def validate() -> None:
    state_dir = Path(__file__).resolve().parents[1] / "history" / "states"
    totals = {
        "oil": 0,
        "steel": 0,
        "aluminium": 0,
        "coal": 0,
        "chromium": 0,
        "tungsten": 0,
        "rubber": 0,
    }

    for filename, expected in EXPECTED.items():
        path = state_dir / filename
        if not path.is_file():
            raise AssertionError(f"missing {path}")
        text = path.read_text(encoding="utf-8")

        state_id = re.search(r"(?m)^\s*id\s*=\s*(\d+)", text)
        manpower = re.search(r"(?m)^\s*manpower\s*=\s*(\d+)", text)
        if not state_id or not manpower:
            raise AssertionError(f"{filename}: id/manpower not found")
        assert int(state_id.group(1)) == expected["id"], f"{filename}: id mismatch"
        assert int(manpower.group(1)) == expected["manpower"], f"{filename}: manpower mismatch"

        block = re.search(r"(?ms)^([ \t]*)resources\s*=\s*\{\s*\n(.*?)^\1\}", text)
        actual = {}
        if block:
            for line in block.group(2).splitlines():
                item = re.match(r"\s*([a-z_]+)\s*=\s*([0-9.]+)", line)
                if item:
                    actual[item.group(1)] = as_int(item.group(2))

        assert actual == expected["resources"], (
            f"{filename}: resources mismatch\n"
            f"expected {expected['resources']}\n"
            f"actual   {actual}"
        )
        for key, value in actual.items():
            totals[key] += value

    expected_totals = {
        "oil": 173,
        "steel": 311,
        "aluminium": 350,
        "coal": 120,
        "chromium": 200,
        "tungsten": 243,
        "rubber": 228,
    }
    assert totals == expected_totals, f"totals mismatch: {totals}"

    print(
        "VALIDASI OK: 5 state MD, manpower Jawa x2, "
        "tambahan SDA sesuai komposisi, rubber +100."
    )
    print(f"total resource: {totals}")


if __name__ == "__main__":
    validate()
