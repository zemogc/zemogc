# Política de seguridad

## Alcance

Este repositorio es un perfil de GitHub: un generador de SVG en Python sin
dependencias externas y dos workflows de GitHub Actions. No procesa datos de
usuarios ni expone servicios. Lo que sí interesa reportar:

- fallos en los workflows de `.github/` (permisos excesivos, inyección en comandos, secretos expuestos);
- vulnerabilidades en `scripts/`;
- secretos o datos personales publicados por error.

El código de los productos de ZemZysteM es privado y no forma parte de este repositorio.

## Versiones con soporte

Solo la rama `main`.

## Cómo reportar

Usa el reporte privado de GitHub:
[Reportar una vulnerabilidad](https://github.com/zemogc/zemogc/security/advisories/new).
Por favor, no abras un issue público con los detalles.

Incluye una descripción del problema, los pasos para reproducirlo y el impacto
que estimas. Se confirma la recepción en un plazo razonable y se informa del
avance hasta resolverlo.
