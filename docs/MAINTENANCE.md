# Mantenimiento del perfil

El README combina texto en Markdown con SVG generados. Los textos de las
imágenes no se editan a mano en `assets/`: salen de `content/profile.toml`.

## Estructura

```
README.md                 composición del perfil
content/profile.toml      fuente única de los textos visuales
scripts/build_assets.py   genera los SVG en variantes dark y light
scripts/check_readme.py   comprueba que el README apunte a recursos existentes
assets/                   SVG generados (no editar a mano)
.github/workflows/ci.yml  valida que todo lo anterior esté sincronizado
```

## Cambios habituales

| Quiero…                         | Edito                                   |
|---------------------------------|-----------------------------------------|
| Cambiar rol, titular o chips    | `[hero]` en `content/profile.toml`      |
| Añadir una tecnología           | el grupo correspondiente en `[[stack]]` |
| Añadir un proyecto              | un bloque `[[projects]]` y su `<picture>` en el README |
| Cambiar un enlace de contacto   | `[[contact]]` y el `href` del README    |
| Ajustar colores                 | `THEMES` en `scripts/build_assets.py`   |

Después de cualquier cambio:

```bash
python3 scripts/build_assets.py
python3 scripts/check_readme.py
```

Requiere Python 3.11 o superior y no tiene dependencias externas.

## Flujo de trabajo

1. Crear una rama desde `main` (`feat/…`, `fix/…`, `docs/…`).
2. Commits con [Conventional Commits](https://www.conventionalcommits.org/es/).
3. Abrir un pull request; la CI debe quedar en verde antes de fusionar.

## Diseño

- Paleta: grafito con acento cian (`#22D3EE` / `#0E7490`) y degradado a índigo.
- Tipografía: la del sistema (sans para texto, monoespaciada para etiquetas),
  porque GitHub sirve los SVG como imágenes y no carga fuentes externas.
- Animaciones solo en CSS dentro del SVG, se desactivan con
  `prefers-reduced-motion`.
- Cada recurso tiene variante dark y light, elegida con `<picture>`.
