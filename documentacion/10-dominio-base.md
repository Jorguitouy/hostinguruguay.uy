# Dominio base del sitio

Fecha: 2025-10-30

Dominio productivo: https://www.hostinguruguay.uy

## Lineamientos de uso

- Usar SIEMPRE URLs absolutas con HTTPS en:
  - `<link rel="canonical">`
  - Meta `og:url` y `og:image`
  - Datos estructurados JSON-LD (Breadcrumbs, FAQ, Organization, etc.)
- Mantener coherencia de paths (ej: `/buscador-de-dominios.html`, `/assets/img/...`).
- Evitar apuntar a entornos locales (127.0.0.1) o staging en producción.

## Aplicaciones realizadas

- `buscador-de-dominios.html`:
  - Canonical: `https://www.hostinguruguay.uy/buscador-de-dominios.html`
  - OG URL: `https://www.hostinguruguay.uy/buscador-de-dominios.html`
  - OG Image: `https://www.hostinguruguay.uy/assets/img/domain-checker.svg`
  - JSON-LD Breadcrumb:
    - `https://www.hostinguruguay.uy/index.html`
    - `https://www.hostinguruguay.uy/buscador-de-dominios.html`

## Pendientes recomendados

- Repetir este ajuste en el resto de páginas (canonical, OG y JSON-LD si aplica):
  - `domain-transfer.html`, `buscador-de-dominios.html`, `index.html`, y demás landings.
- Actualizar `sitemap.xml` y `robots.txt` para reflejar el dominio productivo.
- Si hay emails de marca, validar dominio (ej: soporte@hostinguruguay.uy) antes de cambiarlos.
