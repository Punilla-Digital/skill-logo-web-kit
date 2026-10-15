---
name: logo-web-kit
description: "Convierte un logo suministrado por el usuario en un sistema de archivos listo para web: SVG, PNG, WebP, favicon, versiones positiva y negativa, isotipo y logotipo. Úsala al adaptar, normalizar, separar o exportar activos de marca; no la uses para inventar una marca nueva salvo que el usuario lo pida expresamente."
---

# Logo Web Kit

Crear un paquete web fiel al logo original. Aceptar imágenes raster, SVG, PDF y archivos editables que las herramientas disponibles puedan leer. No rediseñar, corregir tipografía ni cambiar proporciones, colores o espaciado sin autorización.

## Flujo

1. Inspeccionar el archivo y registrar formato, dimensiones, transparencia, colores visibles, legibilidad y si contiene símbolo, nombre o ambos.
2. Determinar los componentes disponibles:
   - **Marca completa:** símbolo y nombre combinados.
   - **Isotipo:** símbolo sin el nombre.
   - **Logotipo:** nombre tipográfico sin el símbolo.
   - **Favicon:** normalmente derivado del isotipo, nunca de un nombre largo salvo que no exista otra opción.
3. Si los componentes están en capas o vectores, separarlos sin reconstruirlos. Si solo existe una imagen plana, recortar cuando la separación sea inequívoca. Si elementos se superponen o faltan, pedir una decisión antes de inventarlos.
4. Limpiar el fondo y producir una fuente maestra con transparencia. Para una imagen raster, usar edición de imagen cuando haga falta aislar el logo; preservar bordes, texto y geometría exactamente. No usar generación creativa para “mejorar” la marca.
5. Conservar un SVG vectorial real cuando la entrada lo permita. Para entradas raster:
   - vectorizar solo formas simples y validar visualmente el resultado;
   - si no es fiable, crear un SVG contenedor con la imagen incrustada y declararlo como **SVG raster incrustado**, no como vector;
   - nunca afirmar que una imagen quedó vectorizada solo por guardarla con extensión `.svg`.
6. Crear la versión negativa en blanco manteniendo la transparencia y, si aporta valor, una variante monocroma oscura. No invertir automáticamente fotografías, degradados o marcas multicolor protegidas; conservarlas o pedir criterio.
7. Exportar el paquete conforme a [references/deliverables.md](references/deliverables.md). Para maestros PNG transparentes ya preparados, se puede ejecutar `scripts/package_logo.py` para generar las variantes raster y los iconos de forma consistente.
8. Revisar visualmente fondos claro y oscuro, tamaños pequeños y bordes transparentes antes de entregar.

## Decisiones que requieren confirmación

Detenerse y preguntar solo si la respuesta cambia materialmente la identidad: cuál elemento debe ser el isotipo, si se permite reconstruir una parte oculta, si puede eliminarse un eslogan, o si una variante negativa debe conservar colores corporativos. Para cuestiones de exportación ordinarias, usar los valores por defecto de esta skill.

## Reglas de fidelidad

- El texto de marca debe coincidir carácter por carácter.
- Mantener relación de aspecto; nunca estirar.
- Evitar halos, bordes dentados, fondos residuales y recortes apretados.
- No ampliar una fuente raster pequeña como si ganara detalle. Indicar la limitación.
- Mantener perfiles de color web estándar, preferentemente sRGB.
- No sobrescribir el archivo fuente.
- Si el usuario aporta normas de marca, estas prevalecen sobre los valores por defecto.

## Entrega

Entregar una carpeta comprimible con nombres estables, un `manifest.json` legible por máquinas y un `README.md` orientado a personas. El README debe explicar qué se exportó, para qué sirve cada variante, cómo integrar los favicons, cuándo usar la versión negativa y cualquier limitación de la fuente. Si el usuario pide documentación específica para agentes, se puede añadir además `AGENTS.md`, pero no reemplazar el README humano salvo que lo solicite expresamente.
