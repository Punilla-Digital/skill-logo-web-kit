#!/usr/bin/env python3
"""Package prepared transparent PNG logo masters for web delivery."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    raise SystemExit("Falta Pillow. Instálalo en el entorno activo con: python -m pip install Pillow")


MAX_MASTER = 2048
ICON_SIZES = (16, 32, 48, 64, 128, 256)


def load_master(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGBA")
    alpha = image.getchannel("A")
    if alpha.getextrema() == (255, 255):
        raise ValueError(f"{path.name} no tiene transparencia. Prepara primero un maestro PNG transparente.")
    bbox = alpha.getbbox()
    if not bbox:
        raise ValueError(f"{path.name} está completamente transparente.")
    return image.crop(bbox)


def contain(image: Image.Image, maximum: int) -> Image.Image:
    if max(image.size) <= maximum:
        return image.copy()
    scale = maximum / max(image.size)
    size = tuple(max(1, round(value * scale)) for value in image.size)
    return image.resize(size, Image.Resampling.LANCZOS)


def negative(image: Image.Image) -> Image.Image:
    white = Image.new("RGBA", image.size, (255, 255, 255, 0))
    white.putalpha(image.getchannel("A"))
    return white


def square_icon(image: Image.Image, size: int, padding_ratio: float = 0.12) -> Image.Image:
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    usable = max(1, round(size * (1 - 2 * padding_ratio)))
    scale = min(usable / image.width, usable / image.height)
    target = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    resized = image.resize(target, Image.Resampling.LANCZOS)
    position = ((size - target[0]) // 2, (size - target[1]) // 2)
    canvas.alpha_composite(resized, position)
    return canvas


def save_variant(name: str, image: Image.Image, root: Path, manifest: list[dict]) -> None:
    prepared = contain(image, MAX_MASTER)
    png_path = root / "png" / f"{name}.png"
    webp_path = root / "webp" / f"{name}.webp"
    prepared.save(png_path, optimize=True)
    prepared.save(webp_path, lossless=True, method=6)
    for path in (png_path, webp_path):
        manifest.append({
            "file": path.relative_to(root).as_posix(),
            "kind": "raster",
            "dimensions": list(prepared.size),
            "transparent": True,
        })


def write_readme(root: Path, brand_name: str, masters: dict[str, Image.Image], manifest: list[dict]) -> None:
    labels = {
        "logo": "Marca completa",
        "isotype": "Isotipo",
        "wordmark": "Logotipo",
    }
    components = [labels[name] for name in ("logo", "isotype", "wordmark") if name in masters]
    favicon_source = "del isotipo" if "isotype" in masters else "de la marca completa (no se proporcionó un isotipo separado)"
    rows = []
    for asset in manifest:
        if "dimensions" in asset:
            detail = " × ".join(str(value) for value in asset["dimensions"]) + " px"
        elif "sizes" in asset:
            detail = ", ".join(f"{value} px" for value in asset["sizes"])
        else:
            detail = "—"
        rows.append(f'| `{asset["file"]}` | {asset["kind"]} | {detail} |')

    readme = f"""# Kit web de {brand_name}

Este paquete contiene las variantes de identidad visual preparadas para uso web. Fue generado automáticamente; revisa las observaciones antes de publicarlo.

## Componentes incluidos

{chr(10).join(f'- **{component}**' for component in components)}

- **Versión negativa:** variante blanca con transparencia, pensada para fondos oscuros.
- **Favicon:** derivado {favicon_source} y centrado con margen de seguridad.

## Inventario

| Archivo | Tipo | Tamaño o resoluciones |
|---|---|---|
{chr(10).join(rows)}

El inventario técnico completo también está disponible en `manifest.json`.

## Uso recomendado

- Usa SVG cuando exista una versión vectorial real y necesites escalabilidad.
- Usa PNG para transparencia y compatibilidad amplia.
- Usa WebP para reducir peso conservando bordes y transparencia.
- Usa las variantes `-negative` únicamente sobre fondos oscuros o de alto contraste.
- No estires ni alteres la relación de aspecto.

## Favicons

Incluye estas etiquetas dentro de `<head>`:

```html
<link rel="icon" href="/favicon/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon/favicon-32x32.png">
<link rel="apple-touch-icon" href="/favicon/apple-touch-icon.png">
<link rel="manifest" href="/favicon/site.webmanifest">
```

Completa los campos `name`, `short_name`, `theme_color` y `background_color` de `favicon/site.webmanifest` antes de publicar.

## Observaciones

- Los archivos raster no se convierten en vectores reales por cambiar su extensión.
- Revisa el favicon a 16 y 32 px antes de producción.
- Si faltan SVG en este paquete, deben exportarse desde una fuente vectorial o reconstruirse y validarse por separado.
"""
    (root / "README.md").write_text(readme, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--logo", required=True, type=Path, help="Maestro PNG transparente de la marca completa")
    parser.add_argument("--isotype", type=Path, help="Maestro PNG transparente del isotipo")
    parser.add_argument("--wordmark", type=Path, help="Maestro PNG transparente del logotipo")
    parser.add_argument("--brand-name", default="la marca", help="Nombre que aparecerá en el README")
    parser.add_argument("--out", required=True, type=Path, help="Carpeta de salida")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.out.resolve()
    for folder in ("png", "webp", "favicon"):
        (root / folder).mkdir(parents=True, exist_ok=True)

    manifest: list[dict] = []
    masters: dict[str, Image.Image] = {"logo": load_master(args.logo)}
    if args.isotype:
        masters["isotype"] = load_master(args.isotype)
    if args.wordmark:
        masters["wordmark"] = load_master(args.wordmark)

    for name, image in masters.items():
        save_variant(name, image, root, manifest)
        save_variant(f"{name}-negative", negative(image), root, manifest)

    icon_source = masters.get("isotype", masters["logo"])
    favicon_dir = root / "favicon"
    for size in (16, 32):
        path = favicon_dir / f"favicon-{size}x{size}.png"
        square_icon(icon_source, size).save(path, optimize=True)
        manifest.append({"file": path.relative_to(root).as_posix(), "kind": "raster", "dimensions": [size, size], "transparent": True})

    ico_path = favicon_dir / "favicon.ico"
    square_icon(icon_source, 256).save(ico_path, format="ICO", sizes=[(size, size) for size in ICON_SIZES])
    manifest.append({"file": ico_path.relative_to(root).as_posix(), "kind": "icon", "sizes": list(ICON_SIZES), "transparent": True})

    for filename, size in (("apple-touch-icon.png", 180), ("android-chrome-192x192.png", 192), ("android-chrome-512x512.png", 512)):
        path = favicon_dir / filename
        square_icon(icon_source, size).save(path, optimize=True)
        manifest.append({"file": path.relative_to(root).as_posix(), "kind": "raster", "dimensions": [size, size], "transparent": True})

    webmanifest = {
        "name": "",
        "short_name": "",
        "icons": [
            {"src": "android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"},
        ],
        "theme_color": "#ffffff",
        "background_color": "#ffffff",
        "display": "standalone",
    }
    (favicon_dir / "site.webmanifest").write_text(json.dumps(webmanifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (root / "manifest.json").write_text(json.dumps({"assets": manifest}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_readme(root, args.brand_name, masters, manifest)
    print(f"Paquete creado en {root}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Error: {exc}")
