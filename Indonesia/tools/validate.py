"""Validate the generated Al-Muhit Indonesia override files."""

from __future__ import annotations

import re
from pathlib import Path

EXPECTED = {
    "631-Western Java.txt": {
        "id": 631,
        "manpower": 35729537,
        "resources": {
            "oil": 78,
            "steel": 181,
            "aluminium": 90,
            "coal": 30,
            "chromium": 60,
            "tungsten": 60,
            "rubber": 84,
        },
    },
    "1114-Central Java.txt": {
        "id": 1114,
        "manpower": 31228940,
        "resources": {
            "steel": 150,
            "aluminium": 60,
            "coal": 30,
            "chromium": 60,
            "tungsten": 30,
        },
    },
    "634-Eastern Java.txt": {
        "id": 634,
        "manpower": 34783640,
        "resources": {
            "oil": 33,
            "steel": 120,
            "aluminium": 30,
            "chromium": 30,
            "tungsten": 30,
            "rubber": 86,
        },
    },
    "640-Kalimantan.txt": {
        "id": 640,
        "manpower": 13561961,
        "resources": {
            "oil": 362,
            "steel": 242,
            "aluminium": 610,
            "coal": 240,
            "chromium": 180,
            "tungsten": 313,
            "rubber": 172,
        },
    },
    "639-Sulawesi.txt": {
        "id": 639,
        "manpower": 16396503,
        "resources": {
            "steel": 218,
            "aluminium": 240,
            "coal": 60,
            "chromium": 270,
            "tungsten": 150,
            "rubber": 86,
        },
    },
}

# Extra shared slots = MD category's local_building_slots, so total slots x2.
EXPECTED_SLOTS = {
    "623-Northern Sumatra.txt": 43,
    "627-Riau Islands.txt": 10,
    "629-Southern Sumatra.txt": 43,
    "631-Western Java.txt": 55,
    "634-Eastern Java.txt": 55,
    "635-Lesser Sunda Islands.txt": 33,
    "636-Moluccas.txt": 10,
    "637-North Moluccas.txt": 8,
    "638-West Papua.txt": 18,
    "639-Sulawesi.txt": 40,
    "640-Kalimantan.txt": 36,
    "734-Loro Munu.txt": 4,
    "936-Natuna Islands.txt": 1,
    "1113-Banten.txt": 29,
    "1114-Central Java.txt": 51,
    "1185-West Timor.txt": 8,
    "1226-Timor Leste.txt": 8,
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

    for filename, slots in EXPECTED_SLOTS.items():
        path = state_dir / filename
        if not path.is_file():
            raise AssertionError(f"missing {path}")
        text = path.read_text(encoding="utf-8")
        actual_slots = re.findall(
            r"(?m)^[ \t]*add_extra_state_shared_building_slots[ \t]*=[ \t]*(\d+)",
            text,
        )
        assert len(actual_slots) == 1, (
            f"{filename}: expected exactly one add_extra_state_shared_building_slots, "
            f"got {actual_slots}"
        )
        assert int(actual_slots[0]) == slots, (
            f"{filename}: slot mismatch, expected {slots}, got {actual_slots[0]}"
        )

    indonesian_files = {
        path.name
        for path in state_dir.glob("*.txt")
        if re.search(r"(?m)^[ \t]*owner[ \t]*=[ \t]*IND\b", path.read_text(encoding="utf-8"))
    }
    assert indonesian_files == set(EXPECTED_SLOTS), (
        f"Indonesian state coverage mismatch: "
        f"missing={set(EXPECTED_SLOTS) - indonesian_files}, "
        f"unexpected={indonesian_files - set(EXPECTED_SLOTS)}"
    )

    expected_totals = {
        "oil": 473,
        "steel": 911,
        "aluminium": 1030,
        "coal": 360,
        "chromium": 600,
        "tungsten": 583,
        "rubber": 428,
    }
    assert totals == expected_totals, f"totals mismatch: {totals}"

    print(
        "VALIDASI OK: manpower Jawa md asli, bonus SDA x3 sesuai komposisi, "
        f"slot bangunan x2 di {len(EXPECTED_SLOTS)} state IND."
    )
    print(f"total resource: {totals}")


if __name__ == "__main__":
    validate()
