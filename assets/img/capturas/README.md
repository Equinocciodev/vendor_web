# Capturas de la aplicación

Las seis imágenes que la portada muestra en la sección **«Pantalla por
pantalla»** (`index.html`, `#pantallas`).

| Archivo | Qué tiene que mostrar |
|---|---|
| `inicio.png` | El Inicio: objetivo del mes con su semáforo, indicadores del día y avisos. |
| `ruta.png` | La ruta del día: las paradas en el orden del vendedor, con el progreso. |
| `visita.png` | La visita: los ocho pasos, con los primeros ya cerrados. |
| `pedido.png` | El pedido: líneas con su precio, base imponible, impuestos y total cotizado. |
| `cobranza.png` | La cobranza: facturas abiertas del cliente, lo aplicado y el comprobante. |
| `conversacion.png` | La conversación del documento con la oficina. |

## Reglas

- **1080 × 2400 píxeles, en retrato.** Es la caja del teléfono con el que se
  prueba la aplicación, y el sitio ya está maquetado para esa proporción
  (`aspect-ratio: 1080 / 2400`). Una captura de otra medida se recorta.
- **PNG.** Los nombres son fijos: cambiarlos obliga a tocar `index.html`.
- **Van anonimizadas.** Nombres de comercios, RIF, montos, teléfonos,
  direcciones y el nombre del vendedor: nada real. Es una página pública y
  esos datos son de clientes de otra empresa.
- **Sin barra de notificaciones comprometida**: la hora está bien, pero no
  dejes a la vista avisos de otras aplicaciones.
- Modo claro u oscuro, pero **el mismo en las seis**: puestas en fila se ven
  juntas.

## Cómo se sirven

De cada maestra PNG salen tres WebP (`<nombre>-360.webp`, `-720.webp`,
`-1080.webp`) que la portada nombra con `<picture>` y `srcset`; la maestra
queda como respaldo para un navegador sin WebP. Los genera
`python3 tool/imagenes.py`, que además anota la huella SHA-256 de cada
maestra en `derivadas.json`.

**Reemplazar una captura es dejar el PNG nuevo con el mismo nombre y correr
ese script.** Si no se corre, `tool/verificar.py` falla —«cambió y sus
derivadas WebP son de la versión anterior»— y el sitio no se publica: es lo
que evita servir la pantalla vieja en WebP y la nueva sólo en el respaldo.
Si la que cambió es `inicio.png`, regenerá también la imagen social
(`assets/img/og.png`, ver el README de la raíz): es la pantalla del teléfono
que se ve al pegar el enlace en un chat.

## Lo que hay hoy

Las seis son **reales** desde el 2-sep-2026: las mismas de la ficha de Play,
con el vendedor ficticio «Victor S», una distribuidora inventada y datos
sembrados a propósito. Ninguna es de un cliente.
