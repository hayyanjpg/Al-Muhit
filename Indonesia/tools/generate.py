"""Generate the Al-Muhit Indonesia override from the installed Millennium Dawn files.

Source of truth: the SPECS table below. The original MD state files are only
read; nothing inside the Millennium-Dawn folder is modified.
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

RESOURCE_ORDER = ["oil", "steel", "aluminium", "coal", "chromium", "tungsten", "rubber"]

SPECS = {
    "631-Western Java.txt": {
        "id": 631,
        "manpower_multiplier": 2,
        "add": {
            "oil": 20,
            "steel": 60,
            "aluminium": 30,
            "coal": 10,
            "chromium": 20,
            "tungsten": 20,
            "rubber": 20,
        },
    },
    "1114-Central Java.txt": {
        "id": 1114,
        "manpower_multiplier": 2,
        "add": {
            "steel": 50,
            "aluminium": 20,
            "coal": 10,
            "chromium": 20,
            "tungsten": 10,
        },
    },
    "634-Eastern Java.txt": {
        "id": 634,
        "manpower_multiplier": 2,
        "add": {
            "oil": 10,
            "steel": 40,
            "aluminium": 10,
            "chromium": 10,
            "tungsten": 10,
            "rubber": 20,
        },
    },
    "640-Kalimantan.txt": {
        "id": 640,
        "manpower_multiplier": 1,
        "add": {
            "oil": 120,
            "steel": 80,
            "aluminium": 200,
            "coal": 80,
            "chromium": 60,
            "tungsten": 80,
            "rubber": 40,
        },
    },
    "639-Sulawesi.txt": {
        "id": 639,
        "manpower_multiplier": 1,
        "add": {
            "steel": 70,
            "aluminium": 80,
            "coal": 20,
            "chromium": 90,
            "tungsten": 50,
            "rubber": 20,
        },
    },
}


def fmt(value: float) -> str:
    if float(value).is_integer():
        return str(int(value))
    return str(value)


def find_resources(text: str):
    match = re.search(r"(?ms)^([ \t]*)resources\s*=\s*\{\s*\n(.*?)^\1\}", text)
    if not match:
        return None
    values = {}
    for line in match.group(2).splitlines():
        item = re.match(r"\s*([a-z_]+)\s*=\s*([0-9.]+)", line)
        if item:
            values[item.group(1)] = float(item.group(2))
    return match, values


def build_state(text: str, spec: dict) -> str:
    found = find_resources(text)
    if found is None:
        values = {}
        indent = "\t"
    else:
        match, values = found
        indent = match.group(1)

    for key, amount in spec["add"].items():
        values[key] = values.get(key, 0.0) + amount
    values = {key: value for key, value in values.items() if value > 0}

    lines = "\n".join(
        f"{indent}\t{key} = {fmt(values[key])}"
        for key in RESOURCE_ORDER
        if key in values
    )
    block = f"{indent}resources = {{\n{lines}\n{indent}}}"

    if found is not None:
        start, end = found[0].span()
        text = text[:start] + block + text[end:]
    else:
        name_line = re.search(r'(?m)^[ \t]*name\s*=\s*"[^"]+"\s*\n', text)
        if not name_line:
            raise ValueError("state has no name line to anchor resources block")
        text = text[: name_line.end()] + block + "\n" + text[name_line.end() :]

    multiplier = spec["manpower_multiplier"]
    if multiplier != 1:
        def replace_manpower(m: re.Match[str]) -> str:
            raw = m.group(0)
            indent_mp = raw[: len(raw) - len(raw.lstrip())]
            return f"{indent_mp}manpower = {int(m.group(2)) * multiplier}"

        text, count = re.subn(
            r"(?m)^([ \t]*)manpower\s*=\s*(\d+)",
            replace_manpower,
            text,
            count=1,
        )
        if count != 1:
            raise ValueError("manpower field not found")

    return text


def default_md_path() -> Path:
    return (
        Path(os.environ["USERPROFILE"])
        / "Documents"
        / "Paradox Interactive"
        / "Hearts of Iron IV"
        / "mod"
        / "Millennium-Dawn"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--md", type=Path, default=default_md_path())
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    target_dir = args.out / "history" / "states"
    target_dir.mkdir(parents=True, exist_ok=True)

    for filename, spec in SPECS.items():
        source = args.md / "history" / "states" / filename
        if not source.is_file():
            raise FileNotFoundError(source)
        result = build_state(source.read_text(encoding="utf-8"), spec)
        (target_dir / filename).write_text(result, encoding="utf-8")
        print(f"generated {filename}")

    print("GENERATE OK")


if __name__ == "__main__":
    main()
