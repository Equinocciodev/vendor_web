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

## Lo que hay hoy

Los seis archivos son **marcadores de posición** generados con Python
(Pillow), con el cartel «Captura pendiente» adentro. Están versionados a
propósito: `tool/verificar.py` comprueba que todo recurso que el HTML nombra
exista, y un `<img>` roto en producción es peor que un marcador honesto.

**Reemplazalos por las capturas reales, con el mismo nombre y la misma
medida, y no hace falta tocar nada más.** El script que los generó quedó
fuera del repositorio: no se van a necesitar de nuevo.
