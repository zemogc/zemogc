# Mantenimiento del perfil

El perfil es una «pared de pantallas»: cada sección es un canal que emite.
Los SVG de `assets/` se generan; no se editan a mano.

## Canales

| Canal | Archivo | Qué muestra |
|-------|---------|-------------|
| CH 01 | `assets/hero-*.svg` | Presentación con escenas rotativas, ficha lateral y rótulo de noticias |
| CH 02 | `assets/system-*.svg` | Ficha estilo neofetch con rol y stack |
| CH 03 | `assets/activity-*.svg` | Ciudad isométrica con las contribuciones reales del último año |
| CH 04 | `assets/products-*.svg` | Un monitor por producto con su mini interfaz animada |
| CH 05 | `assets/outro-*.svg` y `assets/contact/` | Contacto y cierre |

## Estructura

```
content/profile.toml        textos de todos los canales
data/github.json            actividad real (la escribe el workflow refresh)
scripts/build_assets.py     punto de entrada del generador
scripts/render/             un módulo por canal + kit.py (paleta, marcos, logo)
scripts/fetch_github.py     lee la gráfica pública de contribuciones
tests/                      pruebas del lector de la gráfica
scripts/check_readme.py     comprueba que el README apunte a recursos existentes
.github/workflows/ci.yml    valida cada pull request
.github/workflows/refresh.yml  actualiza la actividad a diario (06:17 UTC)
```

## Cambios habituales

| Quiero…                        | Edito                                        |
|--------------------------------|----------------------------------------------|
| Cambiar nombre, rol o titular  | `[identity]` en `content/profile.toml`       |
| Añadir una tecnología          | la fila correspondiente en `[[system]]`      |
| Añadir o cambiar un producto   | `[[products]]` (escena: playlist, route, agents, ticket, devices, pulse) |
| Pasar un producto a producción | `status = "live"` en su bloque               |
| Cambiar el rótulo inferior     | `[ticker]`                                   |
| Ajustar colores                | `SCREEN` y `THEMES` en `scripts/render/kit.py` |

Después de cualquier cambio:

```bash
python3 scripts/build_assets.py
python3 scripts/check_readme.py
```

`scripts/fetch_github.py` lee la gráfica pública del perfil
(`https://github.com/users/<login>/contributions`), la misma que ve cualquier
visitante: incluye las contribuciones privadas mientras el perfil tenga activada
la opción *Private contributions*. No necesita token. Si GitHub cambia el
formato de esa página, el script falla en lugar de escribir cifras incorrectas
y la CI lo detecta en el siguiente pull request.

Requiere Python 3.11 o superior y no tiene dependencias externas.

## Flujo de trabajo

1. Crear una rama desde `main` (`feat/…`, `fix/…`, `docs/…`).
2. Commits con [Conventional Commits](https://www.conventionalcommits.org/es/).
3. Abrir un pull request; la CI debe quedar en verde antes de fusionar.

## Diseño

- Las pantallas son oscuras en ambos temas, como un display real; lo que cambia
  con el tema de GitHub es el chasis.
- Acento cian `#22D3EE` con degradado a índigo `#818CF8`; rojo `EN VIVO`,
  verde producción y ámbar desarrollo, siempre acompañados de texto.
- Tipografía del sistema: GitHub sirve los SVG como imágenes y no carga fuentes externas.
- Animaciones solo en CSS dentro del SVG; se desactivan con `prefers-reduced-motion`
  y el estado estático muestra siempre la escena principal.
