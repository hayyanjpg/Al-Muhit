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

# Global multiplier applied only to the bonus below; MD baseline stays intact.
BONUS_MULTIPLIER = 3

# Indonesia gets a second batch of slots on top of its MD state category,
# effectively doubling the category's local_building_slots.
EXTRA_SLOT_MULTIPLIER = 2

SPECS = {
    "631-Western Java.txt": {
        "id": 631,
        "manpower_multiplier": 1,
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
        "manpower_multiplier": 1,
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
        "manpower_multiplier": 1,
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


def load_category_slots(md_dir: Path) -> dict[str, int]:
    """Read local_building_slots from MD's state_category definitions."""
    result: dict[str, int] = {}
    category_dir = md_dir / "common" / "state_category"
    for path in sorted(category_dir.glob("*.txt")):
        current: str | None = None
        depth = 0
        for line in path.read_text(encoding="utf-8").splitlines():
            header = re.match(r"^[ \t]*(state_[A-Za-z0-9_]+)[ \t]*=[ \t]*\{", line)
            if current is None and header and header.group(1) != "state_categories":
                current = header.group(1)
                depth = 1
                continue
            if current is not None:
                slot = re.search(r"local_building_slots[ \t]*=[ \t]*(\d+)", line)
                if slot is not None:
                    result[current] = int(slot.group(1))
                depth += line.count("{") - line.count("}")
                if depth <= 0:
                    current = None
    return result


def is_indonesian_state(text: str) -> bool:
    return re.search(r"(?m)^[ \t]*owner[ \t]*=[ \t]*IND\b", text) is not None


def get_state_category(text: str) -> str:
    match = re.search(r"(?m)^[ \t]*state_category[ \t]*=[ \t]*(\S+)", text)
    if match is None:
        raise ValueError("state has no state_category")
    return match.group(1)


def add_extra_slots(text: str, slots: int) -> str:
    """Add a history effect granting extra shared building slots."""
    line = f"add_extra_state_shared_building_slots = {slots}"

    def insert(m: re.Match[str]) -> str:
        return f"{m.group(0)}\n{m.group(1)}\t{line}"

    text, count = re.subn(
        r"(?m)^([ \t]*)history[ \t]*=[ \t]*\{[ \t]*$",
        insert,
        text,
        count=1,
    )
    if count != 1:
        raise ValueError("history block not found")
    return text


def build_state(text: str, spec: dict) -> str:
    found = find_resources(text)
    if found is None:
        values = {}
        indent = "\t"
    else:
        match, values = found
        indent = match.group(1)

    for key, amount in spec["add"].items():
        values[key] = values.get(key, 0.0) + amount * BONUS_MULTIPLIER
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

    source_dir = args.md / "history" / "states"
    target_dir = args.out / "history" / "states"
    target_dir.mkdir(parents=True, exist_ok=True)

    # MD declares replace_path = "history/states", so the override must carry
    # the whole directory, not just the edited files.
    category_slots = load_category_slots(args.md)
    indonesia_count = 0

    for source in sorted(source_dir.glob("*.txt")):
        text = source.read_text(encoding="utf-8")

        if is_indonesian_state(text):
            category = get_state_category(text)
            if category not in category_slots:
                raise ValueError(f"unknown state category {category} in {source.name}")
            extra = category_slots[category] * (EXTRA_SLOT_MULTIPLIER - 1)
            text = add_extra_slots(text, extra)
            indonesia_count += 1

        if source.name in SPECS:
            text = build_state(text, SPECS[source.name])
            print(f"generated {source.name}")

        (target_dir / source.name).write_text(text, encoding="utf-8")

    print(f"extra building slots added to {indonesia_count} Indonesian states")
    print("GENERATE OK")


if __name__ == "__main__":
    main()
