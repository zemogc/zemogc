"""Verifica que cada recurso local referenciado en README.md exista."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    refs = sorted(set(re.findall(r'(?:src|srcset)="(assets/[^"]+)"', readme)))
    missing = [ref for ref in refs if not (ROOT / ref).is_file()]
    for ref in missing:
        print(f"falta: {ref}")
    print(f"{len(refs) - len(missing)}/{len(refs)} recursos encontrados")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
