# Logo Web Kit

Adaptación de logos existentes: variantes positiva y negativa, isotipo y logotipo cuando se puedan separar, PNG, WebP, favicon y SVG según la naturaleza de la fuente.

- Instrucciones: [SKILL.md](SKILL.md).
- Recursos e iconos: incluidos en `assets/` y `agents/`.
- Referencias: `references/`.

## Requisitos

Python y Pillow para scripts/package_logo.py. Para limpiar o vectorizar, herramientas de edición adicionales según el archivo original. El script empaqueta maestros PNG transparentes y no realiza vectorización automática.

## Uso e instalación

1. Descargar el repositorio.
2. Usar la carpeta del repositorio como carpeta de la skill.
3. En un agente compatible, copiar la carpeta completa con el nombre `logo-web-kit` a su directorio de skills. Conservar scripts, referencias y recursos junto al SKILL.md. Si el entorno ofrece importación, seguir su procedimiento; publicar en GitHub no instala automáticamente la skill en ChatGPT.
4. Resolver las rutas de recursos desde la carpeta de la skill. En otros asistentes, adjuntar solo SKILL.md no carga automáticamente scripts ni imágenes.

Las menciones a habilidades de PDF o generación de imágenes requieren herramientas equivalentes en el entorno; no se incluyen habilidades de terceros. Los iconos de agents/openai.yaml dependen del soporte del agente.

## Ejemplo

> Prepará un kit web de este logo, con variantes para fondos claros y oscuros y favicons.

## Identidad y recursos

Conservar los logos y las reglas incluidas. Aplicar los cambios de marca, colores o formato que admita la habilidad y solicite el usuario. No inventar un logo ni presentar archivos como generados antes de crearlos y verificarlos.

## Origen y alcance

Copia de la habilidad personal de Punilla Digital aprobada para este repositorio el 15/10/2026. Se preservan sus instrucciones y recursos funcionales; esta publicación no modifica la habilidad instalada en Complementos.

[Punilla Digital](https://punilladigital.com.ar/) · Consultar [LICENSE](LICENSE).
