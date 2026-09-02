# vendoo_web

Sitio público de **Vendoo**, la aplicación Android de fuerza de ventas de campo
de **GUUAO LLC**. Cuatro páginas: inicio, contacto, términos de servicio y
política de privacidad, más la de «no encontrado».

**HTML, CSS y un poco de JavaScript. No hay framework, no hay build y no hay
dependencias**: ni npm, ni un generador de sitios, ni un CDN. Lo que está en el
repositorio es exactamente lo que se sirve. Eso no es minimalismo por deporte —
es lo que permite que la política de seguridad de contenido sea tan cerrada como
es (todo desde el propio origen) y que cualquiera pueda corregir una coma de la
política de privacidad sin instalar nada.

**Qué vende esta página** (2-sep-2026): Vendoo es un **producto B2B** para
fuerzas de venta de distribución. Está publicada en Google Play y cualquiera la
descarga, pero sin una cuenta que entregue la empresa que la contrata no hace
nada — la aplicación no permite registrarse. Ese matiz es el que hay que
mantener en cualquier texto nuevo: **descargable, pero no es una app de
consumo**.

> ⚠️ **Vendoo no es la app de una sola empresa y el sitio no nombra a ninguna.**
> Hasta el 2-sep-2026 el sitio decía que era «la aplicación interna de Grupo
> Leiros» y que no se podía obtener. Ya no: es un producto de GUUAO LLC y el
> texto habla en genérico —«distribuidoras», «tu equipo comercial», «tu ERP»—.
> Si vas a agregar un dato de campo, decilo sin nombre propio.

---

## Estructura

```
.
├── index.html            Inicio: la portada de producto entera
├── contacto.html         Demo, soporte, privacidad y datos  (#demo es el ancla del CTA)
├── terminos.html         Términos de servicio
├── privacidad.html       Política de privacidad
├── 404.html              Página no encontrada, con enlaces a todo
├── favicon.svg           El isotipo, copiado de la app
├── robots.txt
├── sitemap.xml
├── site.webmanifest
├── _headers              Referencia de cabeceras (Pages no las sirve; la CSP va en <meta>)
├── CNAME                 El dominio que sirve GitHub Pages
├── assets/
│   ├── css/estilo.css    TODO el estilo del sitio, en un solo archivo
│   ├── js/sitio.js       Lo único que hace JavaScript: el cambio de tema
│   ├── fonts/            Poppins 400/500/600/700, subconjunto latino (~9 KB c/u)
│   └── img/
│       ├── og.png        Imagen social 1200×630 — se genera con tool/og.html
│       ├── isotipo.svg, favicon-32.png, icono-180.png, icono-512.png
│       └── capturas/     Las seis capturas de la app (ver su README)
├── tool/verificar.py     El chequeo que corre en CI y también en tu máquina
├── tool/og.html          El molde de la imagen social. NO se publica.
└── .github/workflows/publicar.yml
```

### La cabecera y el pie están copiados en cada página

A propósito, y conviene saberlo antes de tocarlos: son unas cuarenta líneas
idénticas al principio y al final de los cinco HTML. **Si cambiás una, cambiala
en las cinco.** La alternativa era inyectarlas con JavaScript, y eso significa
que el menú y el pie no existen para quien tenga el script bloqueado ni para un
buscador que no ejecute JS. Para cinco páginas, la copia sale más barata que ese
costo.

Lo único que cambia entre página y página dentro de la cabecera es el
`aria-current="page"` del enlace activo.

### El menú son anclas del inicio, y por qué

El menú es **Inicio · Producto · Cómo funciona · Integraciones · Seguridad ·
Contacto**, más el botón **Descargar** a la derecha. Los cuatro del medio son
**anclas de la portada** (`/#producto`, `/#como`, `/#integraciones`,
`/#seguridad`) y no páginas propias.

Se evaluó partirlas en `producto.html` e `integraciones.html`. No se hizo:
serían dos páginas delgadas compitiendo por las mismas palabras que la portada,
que es donde está contada la historia completa y donde llega el que hace clic
en el anuncio o en el enlace de Play. **Cuatro páginas con contenido de verdad
rinden más que seis con relleno.** Si algún día «Integraciones» crece hasta
merecer su propia página —un caso por ERP, por ejemplo—, se parte entonces: el
ancla `/#integraciones` se convierte en `/integraciones.html` y hay que tocar el
menú y el pie de las cinco páginas, el `sitemap.xml` y el `BreadcrumbList`.

**Términos y privacidad NO están en el menú** (decisión del dueño): viven en el
pie y en la página de contacto.

### Cómo está compuesta la portada

Encargo del dueño (2-sep-2026): **«menos texto, más infografías y
animaciones; ponle corazón a la página»**, con Odoo y Salesforce como
referencias de *composición* (no de contenido: no se copió ni un texto, ni un
logo, ni una ilustración de ellos).

De ahí salen cinco reglas que conviene no deshacer:

1. **Una idea por sección.** Rótulo, titular corto, **una** frase de apoyo y un
   dibujo que cuente el resto. Si algo se puede mostrar, no se escribe: la
   portada tiene hoy la mitad del texto que tenía y dice más.
2. **Claro por defecto**, con mucho blanco y secciones alternadas
   (`.seccion--velo`). El oscuro sigue existiendo y sigue habiendo tres
   estados: claro, oscuro y seguir al sistema.
3. **Mosaico de aplicaciones** para las capacidades: doce fichas con su ícono
   propio y dos palabras (`.mosaico`). Es lo que reemplazó a doce tarjetas con
   un párrafo cada una.
4. **Producto a la vista**: la ilustración del vendedor con el teléfono, las
   capturas en marcos, las cifras que cuentan al entrar. Pantallas, no
   párrafos.
5. **Corazón**: la tira de los tres latidos —el sol, la señal que se va, el
   cliente que espera— y un acento **cálido** (`--calido`) para los momentos
   buenos. No es `--alerta`: eso avisa, esto celebra.

#### Las infografías, y qué cuenta cada una

Todas están **dibujadas a mano en SVG en línea**, con los tokens del tema y
sin una sola librería. Las informativas llevan `role="img"` con `<title>` y
`<desc>`; las decorativas, `aria-hidden="true"`.

| Sección | Infografía | Qué muestra |
|---|---|---|
| Portada | La escena de la calle | El vendedor con su teléfono frente a una bodega, y la app al lado con la visita en curso. Los pasos se completan en bucle lento. |
| La ruta | Mapa esquemático | El recorrido se dibuja y las paradas se marcan con su hora; la última queda pendiente. |
| La visita | Línea de tiempo | Los ocho pasos con un riel que se llena y los números que se encienden en orden. |
| Sin señal | La cola | Tres envíos guardados en el teléfono viajan al ERP cuando vuelve la red, y el ERP confirma. |
| La regla de fondo | Dos papeles | El total del teléfono y el del ERP, uno al lado del otro: lo que se firma contra lo que se recalcula. |
| Integraciones | Teléfono ↔ Vendoo ↔ ERP | El dato va y vuelve; el ERP con Odoo nativo y SAP u otros a medida. |
| Seguridad | Tres capas | PIN por fuera, base cifrada en el medio, sesión del ERP adentro. |

⚠️ **Las infografías llevan tope de ancho** (`.info`, 620 px; `.info--ancha`,
780 px). Un `<svg>` con `width: 100%` y un `viewBox` de 460 se estira a los
1.120 px de la envoltura **y escala su texto con él**: el «3 en cola» de 11 px
terminaba dibujado a 28 px, como un cartel de la calle.

### De dónde sale la identidad visual

Nada de esto se inventó acá: todo viene de `../vendoo_app`.

| Qué | De dónde |
|---|---|
| Colores | `lib/theme/app_themes.dart`, preset `vendoo` (`kVendooThemeConfig`) |
| Tipografía | `assets/google_fonts/Poppins-*.ttf`, reducidos a un subconjunto latino |
| Logotipo (la palabra) | `assets/logotipo_vendoo.svg`, en línea y con `currentColor` |
| Isotipo (el círculo) | `assets/logo_vendoo.svg` |
| Radios, grosor de borde | el mismo preset: tarjeta 16 px, botón 14 px, borde 1,3 px |

Tres reglas heredadas de la app que **no** hay que "arreglar":

- **La marca es el LOGOTIPO: la palabra «vendoo».** Regla del dueño
  (2-sep-2026). El **isotipo** —el círculo con el disco— es sólo para íconos:
  favicon, `apple-touch-icon`, manifiesto y el ícono de la aplicación. En la
  cabecera, la portada, el pie y la imagen social va la palabra.
- **El violeta de marca `#9B5DE5` no se usa como color de interfaz.** Da 4,13:1
  sobre blanco y no pasa AA. El único sitio del sitio donde aparece es **el
  disco de la última «o»** del logotipo, y **cambia con el tema**
  (`--marca-disco`): `#8644D5` en claro (5,52:1) y `#9B5DE5` en oscuro (4,84:1).
  No existe un violeta que pase AA sobre blanco *y* sobre negro, así que la app
  tiene dos variantes del logotipo y acá se resuelve con un token.
  Para interfaz: `#6D28D9` en claro y `#B57BFF` en oscuro.
- **La tarjeta la define el borde, no el relleno.** Por eso la superficie está
  pegada al fondo y hay un borde de 1,3 px en todas.

---

## El botón de Google Play

La aplicación está publicada como `com.leiros.vendoo`. El botón sale en la
portada, en el pie de las cinco páginas, en la cabecera (versión compacta,
«Descargar»), en contacto y en la imagen social.

**Está dibujado en SVG en línea**, con el triángulo de Play en sus cuatro
colores. No se descarga el badge oficial de Google, y ésa es la razón: el sitio
no le pide **un solo byte** a un tercero, ni siquiera una imagen — es lo que
sostiene la política de seguridad de contenido y lo que evita que Google sepa
quién visita la página antes de hacer clic.

> **Si Legal prefiere el badge oficial de Google**, se puede cambiar: hay que
> descargar el PNG/SVG oficial desde el *Google Play Badge Generator*, dejarlo
> en `assets/img/`, respetar sus normas de marca (proporciones, área de
> resguardo, no re-teñirlo) y reemplazar el `<a class="boton boton--play">` de
> las cinco páginas. **Seguiría siendo un recurso propio**, servido desde
> nuestro origen, así que `tool/verificar.py` no se queja.

Los cuatro colores del triángulo (`#00A0FF`, `#00E676`, `#FFCE00`, `#FF3A44`)
son **lo único del sitio que no sale del preset «vendoo»**: re-teñirlos con los
tokens del tema lo dejaría de hacer reconocible.

---

## Las capturas de la aplicación

La sección «Pantalla por pantalla» (`index.html`, `#pantallas`) muestra seis
imágenes de `assets/img/capturas/`, a 1080 × 2400 y con `loading="lazy"`.

⚠️ **Hoy las seis son marcadores de posición** generados con Python, con el
cartel «Captura pendiente» adentro. Están versionadas a propósito: el
verificador comprueba que todo recurso exista, y un `<img>` roto en producción
es peor que un marcador honesto. **Para reemplazarlas alcanza con dejar los
archivos reales con el mismo nombre y la misma medida.** Las reglas —qué tiene
que mostrar cada una, y que van anonimizadas— están en
`assets/img/capturas/README.md`.

Cuando lleguen las de verdad, conviene además **agregarlas al `screenshot` del
JSON-LD `SoftwareApplication`** de `index.html`: hoy no están puestas justamente
porque son marcadores.

---

## Las animaciones, y por qué la página se ve igual sin ellas

Tres cosas se mueven al hacer scroll: las secciones **aparecen una vez** al
entrar en pantalla, las **cifras cuentan** desde cero y cada infografía
**arranca cuando se la ve** (y no antes, corriendo en vano arriba del todo).
Lo maneja un `IntersectionObserver` en `assets/js/sitio.js`, con
`unobserve` en cuanto dispara: no vuelve a animar al subir.

⚠️ **Nada queda en `opacity: 0` si el JavaScript no corre**, y el mecanismo es
el punto delicado:

- El script **en línea del `<head>`** pone `data-anim` en el `<html>` antes del
  primer pintado. Todas las reglas que esconden algo cuelgan de ese atributo.
  Si estuviera en `sitio.js` —que va con `defer`— lo que va a aparecer se
  vería un instante antes de esconderse.
- Ese mismo script arma una **red de seguridad**: a los dos segundos quita
  `data-anim` **si `sitio.js` no llegó a marcar `data-listo`**. O sea que un
  script bloqueado, un error de red o un navegador viejo dejan la página
  entera visible, quieta y completa.
- Con `prefers-reduced-motion: reduce` **no se anima nada**: `sitio.js` quita
  `data-anim` y se va. No es una animación más rápida, es ninguna. Las cifras
  se quedan en el valor que ya está escrito en el HTML — que es además lo que
  lee un buscador.

**El escalonado va por clase** (`.revelar--b`, `--c`, `--d`) y no por
`style="--i:2"`: un atributo `style` obligaría a abrir `style-src` a
`'unsafe-inline'` y tirar abajo la política de seguridad de contenido. El
verificador rechaza cualquier `style=`.

⚠️ **Para revisar una animación con capturas, `--virtual-time-budget` no
alcanza**: el reloj virtual no lleva las animaciones CSS hasta el final y la
captura sale a mitad de camino (se ve un trazo dibujado por la mitad y las
paradas todavía invisibles). Para ver el **estado final** —que es el que
importa— hay que renderizar la página **sin los `<script>`**: es el mismo
estado de reposo que ve quien tenga el JavaScript apagado.

## Probarlo en tu máquina

```bash
cd vendoo_web
python3 -m http.server 8000
```

Y abrir <http://localhost:8000>. Hace falta un servidor —no vale abrir el
archivo con doble clic— porque los enlaces son absolutos (`/contacto.html`) y
las fuentes se piden con `crossorigin`.

Antes de subir nada:

```bash
python3 tool/verificar.py
```

Comprueba que estén las páginas, que el HTML cierre sus etiquetas, que cada
página tenga `title`, `description`, `lang`, `canonical`, `viewport`, Open Graph,
Twitter Card y un solo `h1`; que ningún enlace interno ni ancla apunte a algo
que no existe; que **ningún recurso** sea externo; que no haya `style=`; que
cada `<script>` en línea tenga su hash en la CSP de su página, y que cada
bloque JSON-LD sea JSON válido. Es el mismo script que corre en CI.

### Recurso externo y enlace externo no son lo mismo

Desde el 2-sep-2026 el verificador los trata distinto, y la distinción importa:

- Un **recurso** externo (hoja de estilo, script, fuente, imagen de otro
  dominio) sigue siendo **un error**. Lo carga el navegador solo, lo bloquearía
  la CSP y le cuenta a un tercero quién entró al sitio.
- Un **enlace** externo es una navegación que decide el visitante. No lo toca la
  CSP y no delata a nadie hasta que se hace clic. Hace falta uno: el de Google
  Play.

Sigue siendo **lista blanca** (`ENLACES_EXTERNOS_PERMITIDOS`, hoy sólo
`play.google.com`), tiene que ser `https` y tiene que llevar `rel="noopener"`.
Cualquier otro dominio es un error, para que nadie meta un pixel de seguimiento
disfrazado de enlace.

### Ninguna fila con una sola tarjeta

Regla de composición, reportada desde la página publicada el 2-sep-2026:
«Para quién es» tenía cuatro tarjetas y a 1280 px quedaban **3 + 1**, con la
última huérfana abajo.

La causa es `grid-template-columns: repeat(auto-fit, minmax(...))`: elige
**cuantas columnas entren**, sin saber cuántos elementos hay. Sirve cuando el
número de tarjetas divide bien por 1, 2 y 3 —las rejas de **6** y de **12** no
necesitan nada—, y falla justo cuando no.

Por eso, en las rejas cuyo número de elementos no se lleva bien con tres
columnas, las columnas van **explícitas**:

| Reja | Elementos | Saltos |
|---|---|---|
| `.datos` (franja de cifras) | 4 | 4 → 2 → 1, nunca 3 |
| `.reja--4` («Para quién es») | 4 | 4 → 2 → 1, nunca 3 |
| `.flujo` (cómo funciona) | 4 | 4 → 2 → 1, nunca 3 |
| `.cadena` (la cola sin señal) | 4 | 4 → 2 → 1, nunca 3 |
| `.integra` (integraciones) | 3 | 3 → 2 con la última a lo ancho → 1 |

**Tres elementos no se reparten en dos columnas sin dejar uno solo**, así que
ahí la última tarjeta ocupa la fila entera (`grid-column: 1 / -1`): queda
deliberada en vez de huérfana. Si agregás una cuarta tarjeta a
«Integraciones», ese `:last-child` hay que sacarlo y pasar la reja a los
saltos de cuatro.

Se comprueba con el navegador, contando las columnas que de verdad calculó
—no las que uno cree—: metiendo la página en un `<iframe>` del ancho a medir
y leyendo `getComputedStyle(reja).gridTemplateColumns` desde el padre, junto
con `children.length`. Si `elementos % columnas === 1`, hay una huérfana.
Medido así de 320 a 1440 px en las tres páginas con rejas: ninguna.

### El desborde que no se ve venir: `1fr` no baja del min-content

Una pista `1fr` de CSS Grid **no se encoge por debajo del `min-content` de lo
que lleva adentro**. En el mosaico de capacidades, «Multiempresa» —una sola
palabra de doce letras— medía 113 px, y con dos columnas y el relleno de la
ficha la reja se estiraba a 304 px dentro de una ventana de 320: la página
entera se iba al desplazamiento horizontal por una palabra.

Se arregla por los tres lados a la vez, y los tres importan: la ficha puede
encogerse (`min-width: 0`), la palabra puede partirse si no queda otra
(`overflow-wrap: break-word`) y en pantalla angosta la ficha aprieta un poco
su tipografía y su relleno. **Si agregás una palabra larga a un mosaico,
medí a 320 px.**

### Medir que no haya desplazamiento horizontal

Medido el 2-sep-2026 de **320 a 1440 px** en las cinco páginas: `scrollWidth`
nunca supera al `innerWidth`. Chrome sin interfaz **no baja de 500 px de ancho
de ventana**, así que por debajo de eso hay que medir metiendo la página en un
`<iframe>` del ancho que se quiera y leyendo `contentDocument.documentElement.
scrollWidth` desde el padre. Si medís con `--window-size=320,900` y te da 500,
no estás midiendo 320.

---

## SEO

Lo que hay puesto, para no repetirlo ni olvidarlo:

- `lang="es-VE"`, `hreflang="es"` y `x-default` en las cinco páginas.
- `title` y `description` **únicos por página**, `canonical` propio, `robots`
  (`404.html` va con `noindex, follow`).
- Open Graph y Twitter Card completos, con `og:image` de **1200 × 630 en PNG**
  (OpenGraph no acepta SVG) más `og:image:alt`.
- JSON-LD: `WebSite`, `Organization` y `SoftwareApplication` en la portada;
  `ContactPage` y `BreadcrumbList` en contacto; `WebPage` y `BreadcrumbList` en
  las dos legales. **No hay `aggregateRating`**: inventar una calificación es
  mentir, y sin reseñas reales no hay ninguna. El `offers` con `price: 0` es
  cierto —la descarga es gratuita—; si algún día el listado pasa a ser de pago,
  hay que cambiarlo.
- `robots.txt` con `Sitemap:`, y `sitemap.xml` con `lastmod` real.
- Un solo `h1` por página, jerarquía en orden, `alt` en todas las imágenes,
  `theme-color` por tema y `apple-touch-icon` + manifiesto coherentes.
- **Nada externo**: ni Google Fonts, ni analítica, ni píxeles. La página no
  llama a nadie.

### Regenerar la imagen social

`assets/img/og.png` se rasteriza desde `tool/og.html` (que **no** se publica).
Desde la raíz del repositorio:

```bash
python3 -m http.server 8000
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --hide-scrollbars \
  --window-size=1200,630 --screenshot=assets/img/og.png \
  http://localhost:8000/tool/og.html
```

El molde usa el logotipo dibujado (no un texto tecleado con Poppins) y la misma
fuente autohospedada del sitio. Si cambia el claim de la portada, cambialo
también ahí: son las dos frases que la gente ve antes de entrar.

---

## Publicación: GitHub Pages

Cada push a `main` corre `.github/workflows/publicar.yml`: verifica el sitio y,
si pasa, lo publica en GitHub Pages con `actions/deploy-pages`. No hay
secretos que cargar: el workflow se autoriza con su propio token.

### 1. Encender Pages en el repositorio (una vez)

**Settings → Pages → Build and deployment → Source: «GitHub Actions».** Sin
esto el trabajo «Publicar» falla con *«Get Pages site failed»*.

### 2. Apuntar el dominio

En **Settings → Pages → Custom domain** escribí `vendooapp.com` y guardá; el
archivo `CNAME` del repo ya lo lleva, así cada publicación lo conserva. Marcá
**Enforce HTTPS** cuando GitHub termine de emitir el certificado (minutos).

En Cloudflare (DNS de `vendooapp.com`), **solo la raíz y `www`** — los
`<slug>.vendooapp.com` de las bases de clientes no se tocan:

| Tipo | Nombre | Valor | Proxy |
|---|---|---|---|
| A | `@` | `185.199.108.153` | DNS only (nube gris) |
| A | `@` | `185.199.109.153` | DNS only |
| A | `@` | `185.199.110.153` | DNS only |
| A | `@` | `185.199.111.153` | DNS only |
| CNAME | `www` | `equinocciodev.github.io` | DNS only |

«DNS only» mientras GitHub verifica el dominio y emite el certificado; después
se puede pasar a proxy si se quiere, con SSL en modo **Full**.

### 3. Comprobar

`https://vendooapp.com/` y `https://www.vendooapp.com/` tienen que responder
la página de inicio; `https://vendooapp.com/robots.txt` tiene que existir. El
estado de cada publicación está en la pestaña **Actions** y en **Settings →
Pages**.

### Cabeceras de seguridad

GitHub Pages no permite cabeceras propias, así que la política de seguridad
de contenido va como `<meta http-equiv="Content-Security-Policy">` en cada
página (sin `frame-ancestors`, que no se admite en `<meta>`). El archivo
`_headers` se conserva solo como referencia de lo que se serviría con un
CDN que sí las admita.

**Los bloques JSON-LD no necesitan hash.** Están comprobados contra Chrome:
`<script type="application/ld+json">` no se ejecuta, así que `script-src` no lo
alcanza y no genera violación. El único script que sí necesita su hash es el del
tema, que va en línea en el `<head>`.

---

## Lo que falta, y quién lo decide

| Qué | Dónde | Quién |
|---|---|---|
| **Las seis capturas reales** de la aplicación | `assets/img/capturas/` | Dueño |
| Teléfono y horario de atención públicos, si se quieren | `contacto.html` | Dueño |
| Un canal de WhatsApp de soporte, si se quiere publicar | `contacto.html` | Dueño |
| Revisión de abogado venezolano de las cláusulas 15 y 17 de los términos | `terminos.html` | Legal |

Nada de eso se inventa: un correo que rebota o un número que no existe es peor
que no poner ninguno. Hoy el único dato de contacto publicado es
**hola@vendooapp.com**, y tiene que decir lo mismo en tres sitios: acá, en la
política de privacidad y en el `VENDOO_CORREO_PRIVACIDAD` con el que se compila
la app. Si difieren, el vendedor lee uno y escribe al otro.

Si en el futuro hace falta dejar un dato a la vista sin inventarlo, la clase
`.pendiente` sigue en la hoja de estilo: pinta el marcador en punteado naranja.
**Hoy no la usa ninguna página.**

---

## Los dos documentos legales

Desde el 2-sep-2026 **son textos finales, no borradores**: el titular es
**GUUAO LLC**, el contacto es `hola@vendooapp.com` y no se publica ningún
domicilio.

- **`privacidad.html`** sale de `../vendoo_app/play/politica-privacidad.html` y
  de `../vendoo_app/docs/app_interna_distribucion_y_privacidad_2026-08-15.md`.
  **Los textos están tomados de ahí, no reescritos**: los redactó ese análisis
  con la norma en la mano. Lo que sí se actualizó, porque el hecho cambió, es la
  cláusula 2.a: hasta el 1-sep-2026 decía que la app no trazaba el recorrido
  entre visitas, y desde ese día el rastro continuo forma parte de la
  aplicación. La cláusula lo dice y lleva su nota de cambio.
  El plazo de conservación del recorrido **no se inventó**: la tarea de
  depuración existe con 90 días como valor de referencia, viene apagada de
  fábrica y hoy no está encendida, y el texto lo dice así.

- **`terminos.html`** se redactó para este sitio, sobre el comportamiento real
  de la app. Las cláusulas **15** (responsabilidad) y **17** (ley aplicable y
  controversias) están escritas de forma que **no pretenden que nadie renuncie a
  nada**: el art. 18 de la LOTTT hace nula toda estipulación que suponga
  renuncia o menoscabo de los derechos del trabajador, y la cláusula lo dice
  explícito. Aun así, **conviene que las lea un abogado venezolano.**

La política publicada tiene que quedar en una **URL pública, sin login, sin
geobloqueo y sin PDF**: es lo que exige la política de datos de usuario de
Google Play, y `https://vendooapp.com/privacidad.html` lo cumple.

---

## Accesibilidad y temas

- **Tres estados de tema, no dos:** claro, oscuro, y —el de fábrica— seguir al
  sistema. El botón alterna, y cuando la elección coincide con lo que dice el
  sistema el atributo se **quita** en vez de escribirse, para que el visitante
  que cambia su teléfono a oscuro por la noche vea el sitio cambiar con él.
- La lectura inicial del tema es un script **en línea en el `<head>`** de cada
  página: con `defer` el sitio parpadearía en claro antes de pintarse oscuro.
  Ese script está cubierto por un hash en la CSP — **si lo tocás, hay que
  recalcular el hash** (abajo), o el navegador lo bloqueará y el parpadeo
  volverá. El verificador te lo dice, con el hash que corresponde.
- Todos los colores vienen medidos de la auditoría de color de la app: los
  textos pasan AA o AAA y los bordes cumplen el 3:1 de WCAG 1.4.11.
- Foco visible en todo lo enfocable, enlace de «saltar al contenido»,
  `prefers-reduced-motion` respetado, y ninguna información transmitida sólo
  por color.
- **La portada se mueve poco y por una razón.** Tres cosas se animan en el
  teléfono ilustrado: el aviso de «sin señal» late, la barra del paso avanza una
  vez y la línea de la cola aparece después. Con `prefers-reduced-motion:
  reduce` la regla global las apaga y el dibujo queda en su estado final, que es
  el legible.

## Licencia

Material propiedad de GUUAO LLC. Todos los derechos reservados.

### Recalcular el hash de la CSP

Si se cambia el script en línea del `<head>`:

```bash
python3 - <<'EOF'
import re, hashlib, base64
t = open('index.html', encoding='utf-8').read()
c = re.search(r'<script>(.*?)</script>', t, re.S).group(1)
print('sha256-' + base64.b64encode(hashlib.sha256(c.encode()).digest()).decode())
EOF
```

y pegar el resultado en el `script-src` de las cinco páginas y de `_headers`. El
script tiene que ser **idéntico en las cinco**, o el hash sólo servirá para una.
`tool/verificar.py` comprueba justamente eso y te imprime el hash correcto.
