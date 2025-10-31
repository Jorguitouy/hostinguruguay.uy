from __future__ import annotations
import sys
from pathlib import Path
from typing import Dict

try:
    from ftfy import fix_text
except Exception as e:
    print("[ERROR] ftfy no está instalado o no se pudo importar:", e)
    sys.exit(1)

# Archivos objetivo (páginas de producción)
TARGET_FILES = [
    "index.html",
    "alojamiento-web.html",
    "buscador-de-dominios.html",
    "registro-de-dominios.html",
    "transferencia-de-dominios.html",
]

# Reemplazos adicionales específicos (post-ftfy) para casos rebeldes
EXTRA_MAP: Dict[str, str] = {
    # Espacios duros y restos de byte-order
    "\u00C2\u00A0": " ",  # NBSP con C2 A0 a espacio normal
    "\u00EF\u00BB\u00BF": "",  # BOM a vacío si apareciera dentro del contenido
    # Signos de interrogación/exclamación invertidos con residuo
    "\u00C2\u00BF": "¿",
    "\u00C2\u00A1": "¡",
    # Variante común "Ã¢â‚¬Å“" y similares
    "Ã¢â‚¬Å“": "“",
    "Ã¢â‚¬Â": "”",
    "Ã¢â‚¬â€œ": "–",
    "Ã¢â‚¬â€": "—",
    "Ã¢â‚¬â„¢": "’",
    "Ã¢â‚¬Ëœ": "‘",
    "Ã¢â‚¬Â¢": "•",
}


def fix_file(path: Path) -> bool:
    try:
        original = path.read_text(encoding="utf-8", errors="strict")
    except UnicodeDecodeError:
        # Si hay error, intentar leer en latin-1 y luego pasar por ftfy
        original = path.read_text(encoding="latin-1", errors="strict")
    fixed = fix_text(original)
    # Aplicar mapa extra
    for bad, good in EXTRA_MAP.items():
        if bad in fixed:
            fixed = fixed.replace(bad, good)
    if fixed != original:
        path.write_text(fixed, encoding="utf-8", newline="\n")
        return True
    return False


def main(root: Path) -> int:
    changed = 0
    for rel in TARGET_FILES:
        p = root / rel
        if not p.exists():
            print(f"[WARN] No existe: {p}")
            continue
        if fix_file(p):
            changed += 1
            print(f"[OK] Arreglado mojibake: {p}")
        else:
            print(f"[SKIP] Sin cambios: {p}")
    print(f"\nResumen: {changed} archivo(s) corregido(s).")
    return 0


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    sys.exit(main(project_root))
