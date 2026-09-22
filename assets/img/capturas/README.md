# Capturas de la aplicación

Acá viven **dos familias** y tienen contratos distintos. La primera son las
seis de la portada; la segunda, las del manual del vendedor (`manual-*`), que
entraron el 19-sep-2026 y están al final de este archivo.

## Las seis de la portada

Las imágenes que la portada muestra en la sección **«Pantalla por pantalla»**
(`index.html`, `#pantallas`).

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


---

## Las del manual del vendedor (`manual-*`, 19-sep-2026)

Las nueve capturas de `/docs/`. Son de la **5.2.5** y ésa es la primera regla:
**el manual dice de qué versión habla, así que sus capturas tienen que ser de
esa versión.** Por eso no se reusó ninguna de las seis de arriba — son del
2-sep-2026 y ya no coinciden con el texto (el octavo botón del Inicio cambió
de nombre y la línea de tasas perdió un renglón). Una captura que contradice
al párrafo de al lado enseña a desconfiar de los dos.

| Archivo | Qué muestra | Sección |
|---|---|---|
| `manual-inicio.jpg` | Tasas, bloque «Hoy» y los accesos rápidos | Tu Inicio |
| `manual-panel.jpg` | El panel de sincronización | Entrar · Sin internet |
| `manual-ruta.jpg` | Las tres paradas con su deuda | La ruta del día |
| `manual-checkin.jpg` | Paso 1 de 8 | La visita |
| `manual-pedido.jpg` | Paso 3 de 8, con el selector UND/CAJ | La visita |
| `manual-cobranza.jpg` | Comprobantes y facturas pendientes | Cobrar |
| `manual-facturas.jpg` | La cartera y «CÓBRALE HOY» | Las facturas |
| `manual-actividad.jpg` | Pedidos › «Abiertos» | Actividad |
| `manual-catalogo.jpg` | Buscador, chips y fichas de producto | El catálogo |
| `manual-devolucion.jpg` | Paso 5 de 8: el motivo dentro de la tarjeta y el pie «De la devolución» | La visita |
| `manual-devoluciones.jpg` | Los contadores de Actividad › Devoluciones | Actividad |
| `manual-multipedido.jpg` | Paso 3 de 8 con tres pedidos abiertos y sus chips | La visita |
| `manual-conversacion.jpg` | Una nota interna, un mensaje y el compositor | Hablar con la oficina |

### Reglas propias

- **Son JPG, y es a propósito.** Llegan así del teléfono. Re-codificarlas a
  PNG no les devuelve la calidad que ya perdieron y duplica lo que pesan.
  `tool/imagenes.py` acepta las dos extensiones.
- **No tienen medida fija.** Las de la portada son 1080 × 2400 porque el marco
  del teléfono de `#pantallas` está maquetado con esa proporción; el manual
  las pinta dentro de una columna de texto y la proporción la da cada `<img>`
  con su `width`/`height`. De una maestra de 620 px salen `-360` y `-620`:
  **nunca se agranda una maestra.**
- 🔴 **Cinco son RECORTES y por eso no llevan el marco del teléfono**
  (`manual-inicio`, `manual-panel`, `manual-devolucion`, `manual-devoluciones`,
  `manual-multipedido`).
  Se recortaron para sacar de la imagen el nombre de una compañía o de un
  comercio reales. Recortar no falsea nada; poner un marco de teléfono
  alrededor de medio Inicio sí, porque diría que eso es una pantalla completa.

  Las dos de la devolución (22-sep-2026) se recortaron así:

  - **`manual-devolucion`** — se le quitó **la barra de arriba**, que lleva el
    nombre del comercio que se está visitando, y **el pie**, que en esa pantalla
    es un tercio de negro porque el paso está filtrado por código. Lo que queda
    es el flujo entero del paso: cantidad, motivos sugeridos, motivo escrito, y
    el bloque «De la devolución» con observaciones y foto.
  - **`manual-multipedido`** — mismo recorte superior que la anterior, por la
    misma razón: la barra lleva el nombre del comercio.
  - **`manual-conversacion`** — **entera y sin recortar**, porque no hacía
    falta: esa pantalla no nombra a ningún comercio ni a ninguna compañía. Es
    la única del lote del 22-sep que se pudo publicar completa, y por eso sí
    lleva el marco del teléfono.
  - **`manual-devoluciones`** — de la lista de Actividad sólo entró **la banda
    de contadores**. 🔴 Las tarjetas de abajo llevan **cinco nombres de
    comercios reales**, y ahí recortar no alcanzaba: los nombres *son* el
    contenido de esa lista. Publicarla entera necesita datos sembrados o el
    permiso del dueño.

### 🔴 Lo que NO se publicó, y por qué

Del lote original quedaron afuera capturas que estaban bien hechas:

- Una muestra **un número de cuenta bancaria completo** de la empresa.
- **Cinco muestran el nombre de una compañía real** del grupo que usa la
  aplicación, con su logo en dos de ellas.

La regla de arriba —«van anonimizadas, es una página pública»— vale igual para
el manual, y además **el sitio entero habla en genérico y no nombra a ningún
cliente**. Publicar una captura con el nombre de una empresa de verdad es una
decisión del dueño, no de quien arma la página. Si se autoriza, o si se vuelve
a capturar con una empresa sembrada, entran las que faltan: el Inicio entero,
el Perfil y el formulario de cobranza por arriba.

**Reemplazar una de éstas es dejar el JPG nuevo con el mismo nombre y correr
`python3 tool/imagenes.py`**, igual que con las de la portada.
