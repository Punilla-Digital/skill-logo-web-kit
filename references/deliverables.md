# Especificación de entrega

## Estructura recomendada

```text
logo-web-kit/
├─ svg/
│  ├─ logo.svg
│  ├─ logo-negative.svg
│  ├─ isotype.svg
│  └─ wordmark.svg
├─ png/
│  ├─ logo.png
│  ├─ logo-negative.png
│  ├─ isotype.png
│  └─ wordmark.png
├─ webp/
│  ├─ logo.webp
│  ├─ logo-negative.webp
│  ├─ isotype.webp
│  └─ wordmark.webp
├─ favicon/
│  ├─ favicon.ico
│  ├─ favicon-16x16.png
│  ├─ favicon-32x32.png
│  ├─ apple-touch-icon.png
│  ├─ android-chrome-192x192.png
│  ├─ android-chrome-512x512.png
│  └─ site.webmanifest
├─ manifest.json
└─ README.md
```

Omitir componentes que realmente no existan. No duplicar la marca completa como “isotipo” o “logotipo” solo para llenar la estructura.

## Valores por defecto

- `logo.png`: fondo transparente, lado mayor de hasta 2048 px, sin ampliación innecesaria.
- PNG de componentes: fondo transparente y espacio de seguridad conservador.
- WebP: sin pérdida cuando la identidad dependa de bordes nítidos o colores planos.
- Versión negativa: blanco puro con el alfa original, salvo reglas de marca diferentes.
- Favicon: lienzo cuadrado, isotipo centrado, aproximadamente 12 % de margen por lado.
- ICO: incluir 16, 32, 48, 64, 128 y 256 px cuando el codificador lo permita.
- Apple touch icon: 180 × 180 px.
- Android/manifest: 192 × 192 y 512 × 512 px.

## SVG

Un SVG vectorial real debe contener trazados, formas o texto convertido según corresponda. Optimizar sin borrar metadatos legales ni modificar la apariencia. Añadir `viewBox` y evitar dimensiones físicas innecesarias.

Si la entrada solo permite un contenedor raster, nombrarlo `logo-raster-wrapper.svg` y registrar en el manifiesto:

```json
{
  "file": "svg/logo-raster-wrapper.svg",
  "kind": "embedded-raster",
  "vector": false
}
```

## Control visual

Comprobar al menos:

- fondo blanco, negro y transparente a cuadros;
- 16, 32, 180 y 512 px;
- que el favicon sea reconocible;
- coincidencia de texto y proporciones con la fuente;
- que no haya píxeles de fondo en bordes o huecos interiores;
- que las versiones negativa y positiva ocupen el mismo encuadre.

## Manifiesto

Registrar nombre, ruta, función, dimensiones, transparencia y naturaleza `vector`, `raster` o `embedded-raster`. Añadir advertencias cuando la fuente sea pequeña, esté comprimida o no permita separar componentes con fidelidad.

## README

Generar siempre un `README.md` en la raíz del paquete. Debe incluir:

- resumen de la marca y fecha o contexto de exportación cuando se conozcan;
- inventario de los archivos realmente incluidos, sin enumerar variantes ausentes;
- explicación de marca completa, isotipo, logotipo y versión negativa;
- indicación de qué archivo usar como favicon y por qué;
- ejemplos mínimos de integración de `favicon.ico`, Apple touch icon y `site.webmanifest`;
- recomendación de usar SVG cuando sea vectorial y PNG/WebP cuando corresponda;
- advertencias sobre resolución, vectorización, fondos, colores o componentes que no pudieron separarse;
- referencia a `manifest.json` como inventario técnico.

Si se genera `AGENTS.md` por pedido del usuario, orientar su contenido a herramientas automáticas: rutas canónicas, archivos preferidos, restricciones de modificación y criterios para elegir variantes. No usarlo como sustituto de la documentación humana.
