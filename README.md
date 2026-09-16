# vendoo_web

Sitio público de **Vendoo**, la aplicación de fuerza de ventas de campo de
**GUUAO LLC**, para **Android y iPhone**. Cuatro páginas: inicio, contacto, términos de servicio y
política de privacidad, más la de «no encontrado». Desde el 12-sep-2026 hay un
archivo HTML más, `soporte.html`, que **no es una página**: es un desvío de
veinte líneas a `contacto.html#soporte` y está explicado abajo, en «La página de
soporte».

**HTML, CSS y un poco de JavaScript. No hay framework, no hay build y no hay
dependencias**: ni npm, ni un generador de sitios, ni un CDN —con una sola
excepción, los dos módulos de Firebase de la analítica de visitas, que se
explica más abajo—. Lo que está en el repositorio es exactamente lo que se
sirve. Eso no es minimalismo por deporte —
es lo que permite que la política de seguridad de contenido sea tan cerrada como
es (todo desde el propio origen) y que cualquiera pueda corregir una coma de la
política de privacidad sin instalar nada.

**Qué vende esta página** (2-sep-2026): Vendoo es un **producto B2B** para
fuerzas de venta de distribución. Está publicada en Google Play y en App Store y
cualquiera la descarga, pero sin una cuenta que entregue la empresa que la
contrata no hace nada — la aplicación no permite registrarse. Ese matiz es el
que hay que mantener en cualquier texto nuevo: **descargable, pero no es una app
de consumo**.

> ⚠️ **Vendoo dejó de ser sólo de Android el 11-sep-2026.** Hasta ese día era una
> aplicación Android y el sitio estaba escrito así. Lo que lo salvó de una
> reescritura fue una regla del 2-sep-2026 —«es *la aplicación*, nunca *la app
> Android*», que `tool/verificar.py` hace cumplir— puesta justamente previendo
> este día: el texto de venta ya hablaba en genérico y **no hubo que tocar una
> sola frase del copy**. Lo que sí cambió: los botones de descarga son **dos**,
> el pie dice los dos requisitos, el `operatingSystem` del JSON-LD nombra los dos
> sistemas, la imagen social dice «Android y iOS» y **las dos páginas legales se
> revisaron enteras**, porque ahí Android no era una palabra de venta sino la
> descripción de un mecanismo (el Keystore, quién pide los permisos, por dónde
> viaja un aviso). Si agregás texto nuevo, la regla sigue siendo la misma:
> **nombrá un sistema operativo sólo cuando lo que decís dependa de cuál sea.**

> ⚠️ **El sitio está en dos idiomas desde el 15-sep-2026.** El español vive en
> la raíz —donde estaba y donde se queda: esas URL están registradas como
> Support URL en App Store Connect y como política de privacidad en Google
> Play, y **no se mueven**— y el inglés en **`/en/`**. Son ocho páginas, no
> cuatro, y están **emparejadas**: cada una declara su gemela con `hreflang` y
> el selector de la cabecera lleva a ella, no a la portada del otro idioma.
> Todo eso lo vigila `tool/verificar.py`. Está contado abajo, en «Los dos
> idiomas».

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
├── contacto.html         El formulario de demo, tres razones y los dos canales directos
├── terminos.html         Términos de servicio
├── privacidad.html       Política de privacidad
├── 404.html              Página no encontrada, BILINGÜE (Pages sirve una sola para todo el dominio)
├── en/                   El sitio en inglés. Las cuatro mismas páginas y el mismo desvío
│   ├── index.html        gemela de /index.html
│   ├── contact.html      gemela de /contacto.html
│   ├── terms.html        gemela de /terminos.html
│   ├── privacy.html      gemela de /privacidad.html
│   └── support.html      desvío a /en/contact.html#support (espejo de /soporte.html)
├── favicon.svg           El isotipo, copiado de la app
├── robots.txt
├── sitemap.xml
├── site.webmanifest
├── site.webmanifest      El manifiesto en español (lo enlazan las páginas de la raíz)
├── site-en.webmanifest   El mismo en inglés (lo enlazan las de /en/). Cambian cuatro campos: lang, name, description y start_url
├── _headers              Referencia de cabeceras: Pages NO las sirve (ver «Lo que Pages no puede hacer»)
├── CNAME                 El dominio que sirve GitHub Pages
├── assets/
│   ├── css/estilo.css    TODO el estilo del sitio, en un solo archivo
│   ├── js/sitio.js       Tema, animaciones, marcador del menú y el formulario de contacto
│   ├── js/analitica.js   GA4 por Firebase, cargado después de `load` y sin señales de anuncios
│   ├── fonts/            Poppins 400/500/600/700, subconjunto latino (~9 KB c/u)
│   └── img/
│       ├── og.png        Imagen social 1200×630 (español) — se genera con tool/og.html
│       ├── og-en.png     La misma en inglés — se genera con tool/og-en.html
│       ├── isotipo.svg, favicon-32.png, icono-180.png, icono-192.png,
│       │   icono-512.png, icono-512-maskable.png   (los PNG salen de tool/imagenes.py)
│       ├── tiendas/      Los badges OFICIALES de App Store y Google Play. NO se editan.
│       └── capturas/     Las seis capturas (PNG maestras + WebP derivadas + derivadas.json)
├── tool/verificar.py     El chequeo que corre en CI y también en tu máquina
├── tool/imagenes.py      Deriva los WebP de las capturas y los íconos. Se corre a mano.
├── tool/og.html          El molde de la imagen social en español. NO se publica.
├── tool/og-en.html       El mismo molde en inglés (og-en.png). NO se publica.
└── .github/workflows/publicar.yml
```

### La cabecera y el pie están copiados en cada página

A propósito, y conviene saberlo antes de tocarlos: son unas cuarenta líneas
idénticas al principio y al final de los cinco HTML **de cada idioma**. **Si
cambiás una, cambiala en las cinco** — y mirá si su gemela en el otro idioma
dice lo mismo.

⚠️ **Dos cosas cambian dentro de la cabecera, no una**: el `aria-current="page"`
del enlace activo y el **destino del selector de idioma**, que apunta a la
gemela de esa página y por lo tanto es distinto en cada una. Las dos las
comprueba `tool/verificar.py`. La alternativa era inyectarlas con JavaScript, y eso significa
que el menú y el pie no existen para quien tenga el script bloqueado ni para un
buscador que no ejecute JS. Para cinco páginas, la copia sale más barata que ese
costo.

Lo único que cambia entre página y página dentro de la cabecera es el
`aria-current="page"` del enlace activo.

### El menú son anclas del inicio, y por qué

El menú es **Inicio · Producto · Cómo funciona · Integraciones · Seguridad ·
Contacto**, y a la derecha los **dos badges de tienda** —o, en el teléfono, un
botón corto que lleva a los dos—. Los cuatro del medio son
**anclas de la portada** (`/#producto`, `/#como`, `/#integraciones`,
`/#seguridad`) y no páginas propias.

Se evaluó partirlas en `producto.html` e `integraciones.html`. No se hizo:
serían dos páginas delgadas compitiendo por las mismas palabras que la portada,
que es donde está contada la historia completa y donde llega el que hace clic
en el anuncio o en el enlace de Play. **Cuatro páginas con contenido de verdad
rinden más que seis con relleno.** Si algún día «Integraciones» crece hasta
merecer su propia página —un caso por ERP, por ejemplo—, se parte entonces: el
ancla `/#integraciones` se convierte en `/integraciones.html` y hay que tocar el
menú y el pie de las diez páginas, las dos versiones de la página nueva, el
`sitemap.xml`, el `BreadcrumbList` y la tabla `GEMELAS` de `tool/verificar.py`.

**Términos y privacidad NO están en el menú** (decisión del dueño): viven en el
pie y en la página de contacto.

#### El marcador del ítem activo, y por qué necesita JavaScript

Defecto reportado por el dueño el **2-sep-2026**: «el indicador de seleccionado
de los links del menú principal no funciona, siempre queda Inicio». Era literal
y era estructural: cuatro de los seis ítems son **anclas de la portada**, así
que el `aria-current="page"` escrito en el HTML se quedaba clavado en «Inicio»
durante todo el recorrido.

Lo resuelve un **scroll-spy** al final de `assets/js/sitio.js`. Cuatro reglas:

1. **El marcado estático del HTML es la verdad sin JavaScript**, y es correcto:
   «Inicio» en la portada, «Contacto» en `contacto.html`, y **ninguno** en
   términos y privacidad —no están en el menú, y encender «Inicio» ahí sería
   decir que estás en otra página—. `404.html` tampoco marca ninguno.
2. **Se observan TODAS las secciones de la portada, no sólo las cuatro del
   menú.** Cada una hereda el ítem de la última ancla que la precede, así que
   mientras se lee «Sin señal» o «Pantalla por pantalla» sigue encendido «Cómo
   funciona». Observar sólo las cuatro dejaba encendida la **siguiente**, que
   es peor que no marcar nada.
3. **La línea de detección va DEBAJO del `scroll-margin-top` de las secciones**
   (84 px, 104 en pantalla angosta; la línea es la altura de la cabecera + 28).
   Si quedara por encima, al saltar a `/#integraciones` la sección de arriba
   seguiría cruzándola y el menú encendería la **anterior** — medido: con +6
   fallaba por diez píxeles, que es un arreglo a medias y se ve igual que el
   defecto original.
4. **Al hacer clic se marca en el acto.** El sitio tiene `scroll-behavior:
   smooth` y durante ese viaje el observador iría encendiendo cada sección
   intermedia; por eso el clic fija el ítem y calla al observador hasta que el
   desplazamiento aterriza.

El `scroll-margin-top` de `.seccion[id]` entró con esto y arregla de paso otra
cosa: sin él, saltar a un ancla dejaba el titular **debajo** de la barra fija.

⚠️ **Esto no se puede probar con `--virtual-time-budget`.** Está medido: el
reloj virtual entrega la primera tanda del `IntersectionObserver` y después no
vuelve a entregar ninguna, así que el menú «no se mueve» y el revelado de las
secciones se queda en dos. Hace falta un Chrome con reloj de verdad, manejado
por CDP (`--remote-debugging-port` + `--remote-allow-origins=*`), scrolleando
con `window.scrollTo` y leyendo `.nav a[aria-current="page"]`. Así se verificó
el recorrido entero, la carga con `#hash` en las seis secciones, el clic en el
menú, 390 px y las otras cuatro páginas.

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
| Integraciones | Vendedor ↔ Vendoo ↔ ERP | El vendedor en la calle, Vendoo con su nube y su cola, y el ERP como servidor. Paquetes que viajan en los dos sentidos, rotulados con lo que llevan; en el medio, la cola que se llena sin señal y se vacía cuando la red vuelve. |
| Seguridad | Tres capas | PIN por fuera, base cifrada en el medio, sesión del ERP adentro. |

⚠️ **Las infografías llevan tope de ancho** (`.info`, 620 px; `.info--ancha`,
780 px). Un `<svg>` con `width: 100%` y un `viewBox` de 460 se estira a los
1.120 px de la envoltura **y escala su texto con él**: el «3 en cola» de 11 px
terminaba dibujado a 28 px, como un cartel de la calle.

⚠️ **Y el problema tiene un espejo hacia abajo, que se resolvió el 2-sep-2026
en el diagrama de integraciones** (`.info--flujo`, 880 px, `viewBox` de 700).
En un teléfono de 320 px ese dibujo se pinta a 0,4 de escala: un rótulo de
10,5 px termina en 4 px, que no es texto sino un rayón. Por eso ahí **los tres
tamaños de texto son clases y no atributos `font-size`** (`.d-eti`, `.d-nodo`,
`.d-mini`) y **suben en dos escalones** (≤ 620 px y ≤ 420 px), y por eso las
listas largas —«pedidos · cobranzas · visitas · clientes nuevos»— llevan clase
`.d-lista` y **se esconden** por debajo de 620 px, donde en su lugar sale un
rótulo corto (`.d-corto`: «Al ERP», «Del ERP»). Agrandar el texto sin acortarlo
lo hace chocar; acortarlo sin agrandarlo no lo hace legible. **Si agregás un
rótulo a ese diagrama, medilo a 320 px antes de darlo por bueno.**

⚠️ Los selectores de esas clases llevan `.info--flujo` **delante a propósito**:
`.info text` ya fija 13 px y le gana por especificidad a una clase sola.

### El muro de ERP, y por qué no hay ni un logotipo

En **Integraciones** hay doce fichas —Odoo, SAP S/4HANA, SAP Business One,
Oracle NetSuite, Dynamics 365 Business Central, QuickBooks, Sage, Zoho,
Salesforce, Siigo, Alegra y CONTPAQi—, la primera marcada **«Integración
nativa»** y las once restantes **«A medida»**.

⚠️ **Cada ficha es la marca ESCRITA, no su logotipo.** Son marcas registradas
de terceros: no se dibujan de memoria —saldría un logotipo falso, que es peor
que ninguno— y no se descargan de su servidor —sería un recurso externo, y
casi todas exigen aceptar antes su guía de marca—. Nombrar una marca por
escrito para decir con qué sistemas trabaja el producto es un uso nominativo;
poner su logotipo ya es usar su identidad visual.

Desde el **2-sep-2026** cada ficha lleva además **un ícono dibujado por
nosotros** (`.erp__icono`, monoline de 24×24, del mismo juego que el mosaico de
capacidades) que dice **de qué tipo de sistema se trata**: módulos para Odoo,
torres corporativas para S/4HANA, un local con toldo para Business One, una
nube con datos para NetSuite, un cubo para Business Central, una calculadora
para QuickBooks, un libro mayor para Sage, una cuadrícula de aplicaciones para
Zoho, dos personas para el CRM de Salesforce, una factura para Siigo, un
billete para Alegra y monedas para CONTPAQi.

⚠️ **El ícono NO es un logotipo, y por eso puede llevar el acento del sitio.**
Dice una categoría, no una marca. Lo que sigue apareciendo **sólo al pasar el
cursor** es el color de la marca —ahora sobre el ícono *y* sobre la palabra—,
que es la regla de abajo y no cambió. Si algún día llegan los SVG oficiales, el
ícono de categoría se queda: el que se reemplaza es el `<span
class="erp__marca">`.

El color de cada marca aparece **sólo al pasar el cursor** (`--erp-c` y su
variante para fondo oscuro). Las tres latinoamericanas no tienen color
asignado y usan el violeta del sitio: no lo confirmamos con su guía y no se
inventa, igual que con los datos de contacto.

El día que lleguen los SVG oficiales, la ficha se cambia **a mano**: se le
agrega `con-logo` y se reemplaza el `<span class="erp__marca">` por un
`<img class="erp__logo">`. El estilo ya está escrito y el paso a paso, con el
HTML listo para copiar, está en **`assets/img/erp/README.md`**. Se descartó un
`<img>` con `onerror` que cayera al texto: la CSP no admite manejadores en
línea, y un logotipo que sólo aparece si corre el JavaScript no es un
logotipo. **Que el HTML diga la verdad de lo que hay.**

⚠️ Y la regla que no se negocia: **una etiqueta «A medida» no se convierte en
«Integración nativa»** hasta que esa integración exista y esté corriendo. Hoy
la única es Odoo.

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

## Los dos botones de tienda

La aplicación está publicada como `com.leiros.vendoo` en las dos tiendas, y
desde el **11-sep-2026** la portada lleva **un botón por tienda**, del mismo
tamaño y con el mismo tratamiento: no hay una principal y una de relleno.

| Tienda | Sale en |
|---|---|
| Google Play (paquete `com.leiros.vendoo`) | portada, cabecera de las cinco **de cada idioma**, JSON-LD |
| App Store (Apple ID **6811065669**) | portada y cabecera de las cinco **de cada idioma** |

⚠️ **Hasta el 11-sep-2026 acá decía que la URL de Apple vivía en UN solo sitio
del marcado, a propósito. Dejó de ser cierto ese día**, cuando el dueño mandó
poner los dos badges también en la cabecera —y la cabecera es, por diseño,
cuarenta líneas copiadas en los cinco HTML—. La regla no se podía cumplir y no
se disimuló: se cambió por algo más fuerte.

Lo que esa regla protegía no era la copia, era **que una copia se quedara
vieja**. Eso ahora lo custodia `tool/verificar.py`: si el Apple ID o el paquete
de Google Play no son **el mismo en todo el sitio**, el chequeo se pone rojo y
dice en qué página está el distinto. Es el mismo movimiento que ya se había
hecho con el hash del script del tema, que también vive repetido en las cinco y
también lo vigila ese archivo. **Una convención que hay que recordar pasó a ser
un chequeo que no se puede olvidar.**

La fila «Descarga» de `privacidad.html` y de `terminos.html` **sigue sin repetir
ninguna URL**: nombra las dos tiendas y manda a `/#descargar`. Ahí no hace falta
un enlace de tienda, y menos texto legal es mejor texto legal.

⚠️ **Y hay algo medido que conviene no perder.** El 11-sep-2026, el día en que
se puso el enlace, la ficha de App Store **todavía contestaba 404**:

```bash
curl -o /dev/null -w '%{http_code}\n' https://apps.apple.com/app/id6811065669
curl -s 'https://itunes.apple.com/lookup?id=6811065669'   # -> resultCount: 0
```

O sea: el registro existe en App Store Connect —de ahí sale el Apple ID— pero
no había pasado revisión. **El enlace se puso igual, por decisión del dueño**
(«en un día lo montamos público»). Si el sitio se publica antes que la ficha,
ese botón lleva a un 404 durante esa ventana. Vale la pena volver a correr esos
dos comandos antes de dar por buena una publicación.

`tool/verificar.py` **no comprueba que un enlace conteste** y no va a hacerlo:
no sale a la red a propósito, para correr igual sin internet y en CI. Lo único
que sabe es que `apps.apple.com` está en su lista blanca de dominios
enlazables, que es otra cosa.

**Del pie salió el botón el 2-sep-2026**, y el paquete `com.leiros.vendoo` y los
requisitos de sistema **se nombran sólo donde identifican la app legalmente**:
la ficha de arriba de `privacidad.html` y de `terminos.html`, más «Android 7.0 y
iOS 15 o superior» una sola vez en el pie de la portada. En ningún otro texto de
venta (decisión del dueño, 2-sep-2026).

### Los badges son el arte OFICIAL, y se sirve desde acá (11-sep-2026)

⚠️ **Este apartado decía lo contrario hasta el 11-sep-2026**, y conviene leer el
cambio entero porque el razonamiento viejo no estaba mal: estaba incompleto.
Decía que los botones se dibujaban a mano —el triángulo de Play en sus cuatro
colores y un ícono nuestro en vez de la manzana— por tres razones: que el sitio
no le pide un byte a nadie, que los badges tienen guía de marca y que un
logotipo dibujado de memoria es un logotipo falso.

Ese día el dueño mandó seguir las guías, y enlazó las dos:

- <https://developer.apple.com/app-store/marketing/guidelines/>
- <https://partnermarketinghub.withgoogle.com/brands/google-play/google-play/lockups-icons-badges/#badges>

Las dos dicen, con todas las letras, que **el badge no se recrea**. Apple: *«Use
only the badge artwork provided in these guidelines»* y *«Don't modify, angle,
or animate the App Store badge»*. Google: *«Don't change the badge color»* y
*«Don't remove or rearrange badge elements, or otherwise adjust the badge in any
way»*. O sea que la razón 3 —«un logotipo dibujado de memoria es falso»— **era
un argumento a favor de usar el oficial**, no en contra; estaba aplicada al
revés.

🔴 **Y la tensión con «ningún byte de terceros» era aparente.** Un badge oficial
no obliga a pedírselo a su servidor: se baja **una vez**, se versiona en
`assets/img/tiendas/` y se sirve desde nuestro propio origen. Cero peticiones a
terceros, la CSP sigue con `img-src 'self'` sin un host nuevo, y el badge es el
de verdad. Las dos cosas a la vez.

De la lista vieja sobrevive intacta la razón 1 —**nada externo**— y la 2 cambia
de signo: la guía de marca ya no es un motivo para no ponerlos, es la
especificación de cómo ponerlos. Están aplicadas en `.tienda` / `.tiendas` de
`estilo.css` y explicadas con sus citas en **`assets/img/tiendas/README.md`**,
que es donde hay que mirar antes de tocar un tamaño. En corto:

| Regla | Quién la pide | Cómo se cumple acá |
|---|---|---|
| Alto mínimo en pantalla | Apple **40 px**, Google **28 px** | 48 px en la portada, **40 en la cabecera** (el mínimo exacto) |
| Zona de respeto = ¼ del alto | las dos | `gap` de 14 px sobre 48 y 12 sobre 40; medido también contra la marca y el interruptor de tema |
| Los dos del mismo tamaño | Google (*«the Google Play badge is the same size or larger than the other badges»*) | misma **altura**; el ancho sale del `viewBox`, y el de Play queda más ancho (3,37:1 contra 2,99:1) |
| El App Store va primero | Apple (*«Place the App Store badge first in the lineup of badges»*) | ése es el orden en la portada y en la cabecera |
| Negro, sin re-teñir, en los dos temas | Apple pide el negro **justamente** cuando hay otro badge al lado; Google tiene una sola versión | los dos traen su propio filete gris `#a6a6a6`, que es lo que los hace legibles sobre el fondo oscuro. **No hay variante clara y no hay que inventarla.** |
| Idioma de la campaña | las dos | español de América Latina: Apple **es-MX** («Descárgalo en el App Store») y Google **Spanish-LATAM** («DESCARGAR EN Google Play»). Apple avisa además que *«App Store»* nunca se traduce |

⚠️ **Van como `<img>`, no como `<svg>` en línea**, y es a propósito: un SVG
pegado en el HTML invita a que alguien le meta `currentColor` o un `fill` del
tema, que es exactamente lo que las dos guías prohíben. Como `<img>` el arte es
intocable desde la hoja de estilo. Por lo mismo **no hay efecto de `hover` ni de
`opacity`**: cualquiera de los dos modifica el badge. Queda el cursor y el
anillo de foco del sitio.

⚠️ **De la hoja de estilo se fue el último hex ajeno.** Los cuatro colores del
triángulo (`#00A0FF`, `#00E676`, `#FFCE00`, `#FF3A44`) eran «lo único del sitio
que no sale del preset vendoo» y se fueron con el botón dibujado, junto con
`.boton--play`, `.boton--mini`, `.play__texto` y los tokens `--play-*`.

⚠️ La clase `.boton--pronto` sigue sin usar, como `.pendiente`, pero **ya no
tiene con qué emparejarse**: su compañera `.boton--play` se fue. Si vuelve a
hacer falta anunciar una tienda que todavía no se puede enlazar, lo honesto es
una frase al lado de los badges — **no un tercer badge inventado**, que es justo
lo que las guías prohíben.

**Si hay que actualizar el arte**, se vuelve a bajar de esas dos fuentes y se
reemplaza entero. No se edita a mano, ni para sacarle el comentario del
generador de Illustrator.

### El renglón donde los dos badges NO entran: el teléfono

🔴 **Está medido, y es la única concesión del cambio.** A 40 px de alto los dos
badges miden **255 px juntos**, y en una ventana de 320 px el ancho útil es
**280**: con la marca y el interruptor de tema en la misma fila no hay forma.
No es cuestión de apretar el `gap` — a cualquier tamaño que entre, el badge deja
de ser legible, y achicarlo por debajo de los 40 px de Apple incumple la guía
que este cambio vino a cumplir.

Por eso **por debajo de 500 px los dos badges se reemplazan por un botón corto**
(`.descarga-corta`) que lleva a `/#descargar`, el bloque de la portada donde
están los dos de verdad. **No es un badge** —es texto y un ícono nuestro—, así
que no incumple ninguna guía, y resuelve igual el defecto que este encargo vino
a cerrar: hasta ese día la cabecera tenía **un** botón que decía «Descargar» y
llevaba **sólo a Google Play**, o sea que quien entraba desde un iPhone
aterrizaba en la tienda equivocada. Hoy aterriza donde están las dos. **Un toque
de más es mejor que la tienda equivocada.**

⚠️ **Y la cabecera pasó a partirse en dos renglones a 1160 px y no a 1000.**
También medido: con el menú sin partir, la fila pide **1.025 px**, y
`.envoltura` no da más de **1.040** (`--ancho` 1120 menos el relleno), así que
ni a 1.440 px de ventana entraba — el tope es la envoltura, no la pantalla. Se
veía como «Cómo funciona» partido en dos renglones y la cabecera 17 px más
alta. Van dos cosas juntas: el relleno horizontal de `.nav a` bajó de 11 a 7 px
(el alto de 40 px **no** se toca: es el blanco táctil) y el corte subió a 1160.
Es la tercera vez que ese número sube por la misma razón —660 → 1000 el
2-sep-2026, 1000 → 1160 hoy—: **cada vez que entra algo nuevo en esa fila, hay
que volver a medirla.** Si movés el corte, mové también el `scroll-margin-top`
de `.seccion[id]`: los dos describen el mismo alto de cabecera.

---

## Los dos idiomas (15-sep-2026)

Encargo del dueño: **«haz la página disponible en español/inglés»**. El sitio
existe ahora en dos lenguas, y las decisiones que lo sostienen son cinco.

### 1. El español se queda en la raíz; el inglés va a `/en/`

No hay `/es/`, y no es pereza: **mover el español habría roto tres cosas que no
están en este repositorio**. `https://vendooapp.com/contacto.html` es la
*Support URL* de la ficha de App Store, `https://vendooapp.com/privacidad.html`
es la URL de la política que exige la política de datos de usuario de Google
Play, y las dos están escritas en la app. Una traducción no vale una redirección
en un sitio que no sabe hacer redirecciones (Pages sólo sirve archivos).

| Español | Inglés |
|---|---|
| `/` | `/en/` |
| `/contacto.html` | `/en/contact.html` |
| `/terminos.html` | `/en/terms.html` |
| `/privacidad.html` | `/en/privacy.html` |
| `/soporte.html` (desvío) | `/en/support.html` (desvío) |
| `/404.html` | — *(no tiene: ver abajo)* |

Los nombres de archivo están **en su idioma** —`contact.html`, no
`contacto.html`— y las anclas también (`/en/#product`, `/en/#how`). Las únicas
que **no** se tradujeron son las de las dos legales: `#c1..#c11` y `#t1..#t18`
son las mismas en las dos versiones **a propósito**, para que
`/privacidad.html#c7` y `/en/privacy.html#c7` sean la misma cláusula y un
enlace a una cláusula sirva en las dos.

### 2. El selector es un enlace, y lleva a la gemela

En la cabecera, pegado al interruptor de tema, hay **un enlace** que dice el
idioma **al que lleva**: «EN» en las páginas en español y «ES» en las inglesas.

- **Es un enlace y no un menú** porque con dos idiomas un menú es un clic de más
  y una lista de uno. Y por ser un enlace de verdad, **funciona con el
  JavaScript apagado**, un buscador lo sigue y cada versión vive en su URL.
- **Lleva a la GEMELA, no a `/en/`.** Mandar todo a la portada es contestarle
  «esta página no existe en el otro idioma» a alguien que la está leyendo. Es
  la regla que más fácil se rompe al agregar una página, y por eso la comprueba
  el verificador.
- Lleva `lang` y `hreflang` del idioma de destino, para que un lector de
  pantalla pronuncie «EN» en inglés en vez de deletrear una sigla en castellano.
- La **404 es la excepción correcta**: apunta a `/en/` a secas porque no tiene
  gemela ni puede tenerla (abajo).

En el pie hay además un enlace **«English» / «Español»** en la columna «Sitio»,
para quien no mira la cabecera.

### 3. No hay detección automática, y es una decisión

Entrar en `/` con el navegador en inglés **no te manda a `/en/`**. Un redirigido
por JavaScript rompería «la página dice la verdad sin JS», obligaría a
recalcular el hash de la CSP y a Google no le gusta; y Pages no puede negociar
el idioma en el servidor porque no hay servidor. Lo que sí hay es lo que un
buscador necesita: **`hreflang` en las ocho páginas y en el `sitemap.xml`**, con
`x-default` apuntando siempre al **español**, que es el idioma original y el del
mercado del producto.

### 4. La 404 es bilingüe porque no puede ser dos páginas

⚠️ **GitHub Pages sirve UNA sola página de «no encontrado» para todo el
dominio**: la `404.html` de la raíz, también para lo que cuelgue de `/en/`. Un
`/en/404.html` existiría y no lo vería nadie. Por eso ahí conviven los dos
idiomas —el `<h1>` sigue siendo uno solo, el español, y el inglés entra como
`<p lang="en">`— y el botón lleva a `/en/`.

### 5. `sitio.js` lee el idioma del `<html lang>`

El sitio comparte **un solo** `assets/js/sitio.js`: es el mismo sitio, no dos.
Lo poco que ese archivo escribe por su cuenta está traducido adentro y sale del
atributo `lang` de la página, **no de la URL** (una página que se mudara de
carpeta seguiría diciendo en qué idioma está):

| Qué | Dónde |
|---|---|
| El rótulo del interruptor de tema | `ROTULO`, arriba del todo |
| El asunto y el cuerpo del correo del formulario, y sus avisos de estado | `T`, en el bloque del formulario |
| Cuál es «Inicio» para el marcador del menú | `VENDOO_BASE` (`/` o `/en/`) |

⚠️ **Los `name` de los campos del formulario NO se tradujeron** y no hay que
traducirlos: siguen siendo `nombre`, `empresa`, `email`, `telefono`, `equipo` y
`mensaje` en las dos versiones. Son la clave con la que un servicio de
formularios recibirá el mensaje el día que se contrate, y dos juegos de nombres
serían **dos integraciones**. Lo que cambia es el rótulo que se escribe en el
cuerpo del correo, que es lo que lee una persona.

⚠️ Y el marcador del menú pasó a buscar sus secciones con **`main > section`** y
no con `#principal > section`: el `id` de la envoltura es un gancho interno y en
las páginas en inglés se llama `main`. Hay un solo `<main>` por página, así que
el selector nombra lo mismo en las dos.

### Un manifiesto por idioma

`lang`, `name` y `description` del manifiesto son campos de **un** idioma, y no
hay forma de declararlos en dos. Con uno solo, quien instalara el sitio desde
`/en/` se encontraba el nombre y la descripción en castellano. Por eso hay
`site-en.webmanifest`, que es una copia con **cuatro** campos distintos —`lang`,
`name`, `description` y `start_url`— y todo lo demás igual: los íconos y los
colores son los mismos a propósito, porque es la misma marca y no dos.

⚠️ El `scope` se queda en **`/`** y NO pasa a `/en/`: el selector de idioma
lleva a la raíz, y con el alcance restringido ese enlace se saldría de la
aplicación instalada y abriría el navegador.

### El inglés es de Estados Unidos, y es una decisión

**Se escribe en inglés americano**: `catalog` y no `catalogue`, `authorized` y
no `authorised`, `organization`, `recognizing`, `traveling`, `canceled`,
`inquiry`. GUUAO LLC es una sociedad de **Florida**, las fichas de App Store y
de Google Play salen en `en-US` y el mercado es América. Mezclar las dos
ortografías es lo que delata una traducción hecha a pedazos, y en la primera
pasada estaban mezcladas: había `catalogue` y `authorized` en la misma página.

⚠️ **Y las comillas son `“ ”`, no `« »`.** Los guillemets son la comilla del
español y quedaron colados dentro del texto en inglés en la primera pasada
(«To send» en vez de “To send”). Cuidado al corregir esto con una sustitución
global: **los comentarios de `/en/` están en español** —como todos los de este
repositorio— y ahí `« »` es lo correcto. Lo que se cambia es el texto que se
ve, no los comentarios.

Tres frases más que se reescribieron porque eran calco y no inglés: «For whoever
sells out in the street» (que se lee como «se queda sin existencias» o
«traiciona»), «the rep **orders** the stops» (choca con *Order*, el pedido, dos
líneas más abajo) y «With no signal too».

### Lo que la traducción le costó a la cabecera

Lo de siempre, y ya es un patrón: **cada vez que entra algo nuevo en esa fila,
hay que volver a medirla.** El corte a dos renglones subió de **1160 a 1240 px**
—es la cuarta vez que sube: 660 → 1000 → 1160 → 1240—. Medido con el menú en
español, que es el largo (en inglés la fila pide ~80 px menos): la fila pedía
1.025 px y `.idioma` le agrega **64** —40 de ancho, 16 del `gap` y 8 de su
margen—, o sea 1.089, que necesitan una ventana de 1.169. 1240 deja 71 px de
holgura. Si movés ese número, mové también el `scroll-margin-top` de
`.seccion[id]`.

🔴 **Y hubo un defecto propio, que conviene no repetir.** Al principio `.idioma`
entró con `order: 3` y `.tema` se pasó a `order: 4`. El menú es `order: 4` con
`flex-basis: 100%`, así que **cualquier cosa en un order posterior al suyo se va
a un tercer renglón detrás de él**: la cabecera pasó de 69 a **149 px** y se
partió en cuatro filas. Los dos controles comparten `order: 3` y se ordenan por
su sitio en el HTML, que ya era el correcto. Medido de 320 a 1440 px en las
cinco páginas de los dos idiomas: **69 px en una fila por encima de 1240, 105 en
dos por debajo, y `scrollWidth` nunca supera al `innerWidth`.**

### Cómo se comprobó

Con Chrome de verdad manejado por CDP, **no con `--virtual-time-budget`** — el
README ya avisaba de que con el reloj virtual el `IntersectionObserver` entrega
una sola tanda, y en la primera pasada de este cambio volvió a pasar: el menú
parecía atrasado una sección y 25 bloques `.revelar` parecían quedarse
invisibles. Con reloj real, las dos cosas están bien:

- el **marcador del menú** en `/en/` recorre las siete secciones y hereda como
  debe (`#screens` → «Product», `#offline` → «How it works», `#who-for` →
  «Security»), y el español sigue igual;
- **cero** `.revelar` en `opacity: 0` al terminar el recorrido, ni a 1400 px ni
  a 390;
- **cero violaciones de CSP** en las cinco páginas nuevas (el `<script>` en
  línea es byte a byte el mismo, así que el hash de la CSP no cambió);
- el formulario arma el correo en el idioma de su página y con los mismos
  `name`.

---

## El formulario de contacto

Desde el **2-sep-2026** `contacto.html` es **una sola pieza**: rótulo,
titular, una frase, el formulario (nombre, empresa, correo, teléfono
opcional, vendedores en la calle opcional, mensaje) en su tarjeta como
centro, tres razones cortas al lado y los dos canales directos —correo y
WhatsApp— a la vista. Dos encargos del dueño el mismo día: primero *«Contacto
es un formulario que manda un correo a hola@vendooapp.com»*, y sobre la
primera versión publicada, *«mucho texto, el formulario roto; quita los cards
de Soporte, Privacidad, Descargar y Seguridad: no tienen lugar en la página de
contacto; haz algo muy bonito que inspire al cliente»*. Por eso **no hay
tarjetas de soporte, de descarga ni de política** en esa página: el correo del
pie sirve para todo, y la política y los términos tienen su enlace en el pie.
Sobre «roto»: la publicación lleva el HTML nuevo y `estilo.css` con
`max-age=600`, así que durante hasta diez minutos un navegador con la hoja
vieja en caché pinta los campos sin estilo. No es del código, pero conviene
saberlo cuando se publica un cambio de CSS y HTML a la vez.

**El sitio no tiene backend, así que hoy el envío es un `mailto:`.**
`sitio.js` valida con HTML5 (`checkValidity` + `reportValidity`, o sea los
mensajes nativos del navegador en el idioma del visitante), arma el asunto
—`Contacto desde vendooapp.com — <empresa>`— y el cuerpo con los campos, y
abre el cliente de correo con todo prellenado. Al lado del formulario siempre
está el enlace «o escribinos directo a hola@vendooapp.com», que es el camino
para quien no tiene cliente de correo configurado o tiene el JavaScript
apagado (la CSP lleva `form-action 'none'` y sin script el `<form>` no se va
a ningún lado; hay un `<noscript>` que lo dice).

### Pasar del `mailto:` a un servicio de formularios

Cuando el dueño cree la cuenta en **Formspree**, **Web3Forms** o parecido,
alcanza con **tres** cosas:

1. En `assets/js/sitio.js`, poner la URL en la constante
   `ENDPOINT_FORMULARIO` (hoy `''`). Con la constante vacía el formulario
   abre el correo; con una URL manda un `POST` JSON por `fetch` y muestra
   «Recibido» sin salir de la página. Los campos viajan con los `name` del
   HTML (`nombre`, `empresa`, `email`, `telefono`, `equipo`, `mensaje`) más
   `_subject` con el mismo asunto del `mailto:`. `email` se llama así, y no
   `correo`, porque es el nombre que esos servicios usan para el *reply-to*.
2. En la CSP de **`contacto.html` Y de `en/contact.html`**
   (`<meta http-equiv="Content-Security-Policy">`), agregar el host del
   servicio a `connect-src`: por ejemplo
   `connect-src 'self' https://formspree.io`. Sin eso el navegador bloquea el
   `fetch` en silencio. **Sólo en esas dos**: las otras ocho no envían nada.
   ⚠️ Son dos porque el formulario existe en los dos idiomas y comparte el
   mismo `ENDPOINT_FORMULARIO`; abrir el host en una sola deja el formulario
   del otro idioma fallando en silencio.
3. Si el servicio pide un dominio autorizado, registrar `vendooapp.com`.

`tool/verificar.py` no se queja de nada de esto: la constante vive en un
script propio (no hay hash que recalcular) y `connect-src` no es ni un recurso
ni un enlace. Si el servicio falla —red, 4xx, 5xx—, el estado del formulario
manda al correo, que sigue a la vista: **nunca se pierde un mensaje sin
decirlo.**

## La página de soporte

⚠️ **Hasta el 11-sep-2026 `contacto.html` era una página de venta y nada más**,
y su propio comentario lo decía: «nada de política, descarga ni soporte acá».
Eso dejó de valer el **12-sep-2026** por decisión del dueño:
`https://vendooapp.com/contacto.html` es la **Support URL** de la ficha de App
Store, y la guía de revisión de Apple pide que esa página traiga, textual,
*«legal address, email address, telephone number»*. Un correo y un WhatsApp
sueltos al costado de un formulario de demo no alcanzan.

La regla vieja **no se borró**, se reemplazó dejando el rastro —qué decía, quién
lo cambió, cuándo y qué implica—, que es como este repositorio documentó antes
la vuelta de los dos badges y el día que Vendoo dejó de ser sólo de Android.

**El soporte va DEBAJO del formulario, y el orden es la decisión.** Lo que el
dueño mandó sacar en septiembre eran cuatro tarjetas —Soporte, Privacidad,
Descargar, Seguridad— compitiendo con el formulario **antes** de que se viera;
el bloque `#soporte` va después, para el que lo viene a buscar, y no le roba el
primer pliegue a la demo. Descarga y política siguen sin tarjeta propia: viven
en la cabecera y en el pie, como desde el 2-sep.

Qué tiene, y de dónde salió cada dato:

| Dato | De dónde | Nota |
|---|---|---|
| Correo | `hola@vendooapp.com`, en el pie de las cinco páginas desde el 2-sep-2026 | El mismo de la política y del `VENDOO_CORREO_PRIVACIDAD` de la app |
| Teléfono | `+58 412-346 9712`, decisión del dueño del 2-sep-2026 | Va con `tel:` **y** con `wa.me`: es el mismo número dicho dos veces |
| Razón social | **GUUAO LLC**, titular de las dos legales | |
| **Dirección legal** | La entregó el dueño el 12-sep-2026 | «10302 NW South River Drive, Medley, FL 33178». Vive en DOS sitios que tienen que decir lo mismo: el `<dl>` de `#soporte` y el `address` del JSON-LD de esa cabeza — más sus dos gemelos en `en/contact.html`. Ver abajo |
| Aplicación, tienda, documentos | los mismos que la ficha de `privacidad.html` | Si cambian, cambian en los dos |

✅ **La dirección legal existe desde el 12-sep-2026**, y conviene conservar por
qué tardó. **No se inventó, y no se podía inventar**: se buscó en este
repositorio —páginas, README, historia de git— y en el de la aplicación, y no
estaba escrita en ninguna parte; en `vendoo_app/play/` figuraba desde agosto de
2026 como el marcador literal «domicilio fiscal completo», pendiente de
Legal/Administración. Durante esos días el `<dd>` salió con el marcador
`.pendiente` —punteado naranja, imposible de no ver— en vez de una dirección
plausible, porque **un domicilio falso de una empresa real es peor que no
publicar ninguno**: le da a un revisor de Apple algo concreto que verificar y
que no va a cuadrar. Y por lo mismo el JSON-LD se quedó **sin `address`** hasta
ese día: ahí el dato lo lee una máquina y un marcador no se puede escribir.

Ese día el dueño lo entregó, textual: «Warehouse / Principal Address: 10302 NW
South River Drive, Medley, FL 33178», y entró en los dos sitios a la vez. Desde
el 15-sep-2026 son **cuatro**, porque la página existe también en inglés: el
`<dl>` y el JSON-LD de `contacto.html`, y los de `en/contact.html`. **Si cambia,
cambia en los cuatro.**

**Los blancos táctiles.** El correo, el teléfono y el WhatsApp van además como
tres píldoras `.via` de **44 px de alto** arriba del `<dl>`, que es la pieza que
la página ya usaba para los canales directos. Medido a 390 px: las tres se
apilan, la más ancha mide 277 px y `scrollWidth` sigue siendo 390 — la página no
desborda por ningún lado.

### `/soporte.html` es un desvío, no una segunda página

`/soporte.html` **no existía y contestaba 404**. Es la dirección que cualquiera
adivina —un revisor, un vendedor al que le dictaron la URL por teléfono, un
borrador viejo de la ficha—, así que ahora existe. Lo que hay que saber:

- **No había un solo enlace roto que arreglar.** Se barrió el sitio entero y el
  repositorio de la aplicación: nadie apunta a `/soporte.html` (de este sitio,
  la app sólo enlaza `privacidad.html` y `terminos.html`). Esto es un seguro, no
  la reparación de un enlace.
- **Por eso es un desvío y no una página de soporte de verdad**: dos páginas de
  soporte se contradicen en el primer dato que alguien corrija en una sola.
- **Es un `meta refresh` a cero segundos** con la canónica apuntando al destino,
  porque GitHub Pages no sabe hacer una 301: lo único que puede servir es un
  archivo. El día que se apliquen las reglas de Cloudflare que están en «Lo que
  falta», la 301 de verdad va ahí y este archivo se puede borrar.
- **Fuera del `sitemap.xml` y con `noindex`**, más su `Disallow` en
  `robots.txt`, por lo mismo que `404.html`: no es contenido y no compite con la
  página de verdad. Lleva la analítica como las cinco páginas —el verificador la
  exige en todas—, y de paso cuenta si alguien llega por ahí: si en seis meses
  no entró nadie, se borra.
- **No se dejó caer en el 404** a propósito: el 404 le dice al visitante que se
  equivocó, y acá no se equivocó — la página que buscaba existe, con otro nombre.

Y en el pie de las cinco páginas hay ahora un enlace **«Soporte»** a
`/contacto.html#soporte`, entre «Contacto» y «Solicitar una demo» —y desde el
15-sep-2026, su gemelo **«Support»** a `/en/contact.html#support` en el pie de
las cinco inglesas—: es lo que
hace que el soporte se encuentre desde cualquier página sin agregar un séptimo
renglón al menú de la cabecera, que a 390 px ya se desplaza de lado.

## Las capturas de la aplicación

La sección «Pantalla por pantalla» (`index.html`, `#pantallas`) muestra seis
imágenes de `assets/img/capturas/`, con `loading="lazy"`, `width`/`height`
para que la página no salte, y **desde el 2-sep-2026 son las reales**: las
mismas de la ficha de Play, con el vendedor ficticio «Victor S» y datos
inventados. Las reglas —qué muestra cada una, y que van anonimizadas— están
en `assets/img/capturas/README.md`. Van también en el `screenshot` del
JSON-LD `SoftwareApplication` de la portada y una de ellas, el Inicio, es la
pantalla del teléfono de la imagen social.

**Cada captura se sirve en tres anchos y en WebP** (`<picture>` con un
`<source type="image/webp" srcset="…-360.webp 360w, …-720.webp 720w,
…-1080.webp 1080w">` y la maestra PNG de 1080 como respaldo). La caja mide de
280 a 360 px: mandar la maestra de 1080 a un teléfono de 2× era servir cuatro
veces los bytes que se ven. Medido: el WebP de 360 pesa entre 13 y 24 KB
contra 200–285 KB de la maestra.

⚠️ **Las seis capturas son de un teléfono Android, y desde el 11-sep-2026 eso
es una decisión y no un descuido.** La aplicación es la misma en los dos
sistemas —mismos íconos, misma tipografía, mismas pantallas: está decidido así
en `../vendoo_app/CLAUDE.md`, «los mismos iconos para ambas plataformas»—, así
que una segunda tanda desde un iPhone mostraría lo mismo con otra barra de
estado, a cambio de doblar el peso de la sección y de obligar a mantener doce
imágenes sincronizadas. **Lo que no se hace es inventarlas**: una captura de
iPhone tiene que salir de un iPhone. El día que haya una razón para mostrarlas
—una pantalla que de verdad se vea distinta—, van con las mismas reglas de
`assets/img/capturas/README.md`.

⚠️ **Las seis capturas son de un teléfono en español, y en `/en/` se sirven
igual.** El `alt` de cada una sí está en inglés —es texto nuestro—, pero lo que
se ve dentro de la pantalla («Hola, Victor», «Crear pedido») está en castellano,
y lo mismo vale para el teléfono de `og-en.png`. **No se retocan y no se
inventan**: una captura en inglés tiene que salir de una aplicación en inglés, y
hoy no existe. Es la misma regla que impide fabricar una captura de iPhone. El
día que la aplicación se traduzca, la segunda tanda entra con las reglas de
`assets/img/capturas/README.md` y hay que decidir si se sirven por idioma.

⚠️ **Cambiar una captura son dos pasos, no uno**: dejar el PNG nuevo con el
mismo nombre y la misma medida, y correr `python3 tool/imagenes.py`, que
vuelve a derivar los WebP y anota la huella de cada maestra en
`derivadas.json`. **Si te olvidás del segundo, `tool/verificar.py` se pone
rojo** («cambió y sus derivadas WebP son de la versión anterior»): sin esa
huella la portada serviría la pantalla vieja en WebP y la nueva sólo a los
navegadores sin WebP, que no existen. Y si la que cambió es la del Inicio,
regenerá también la imagen social (abajo).

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

⚠️ **El umbral del observer es doble, y no se vuelve a uno solo** (3-sep-2026).
El dueño reportó desde su iPhone que la reja de capturas de `#pantallas` era
«un espacio largo vacío». Con `threshold: 0.18` el observer avisa cuando el
18 % **del elemento** está en pantalla a la vez; esa `<ul>` mide ~5.000 px a
390 px de ancho (una columna de seis teléfonos), el 18 % son ~900 px y el
visor tiene 844: la condición era imposible, `.visible` no llegaba nunca y la
lista entera se quedaba en `opacity: 0`. En Chrome de escritorio la reja es
3 + 3 y cabe, por eso allá se veía — no era Safari, era cualquier teléfono.
Hoy se da por visto lo que muestra el 18 % de sí mismo **o** lo que ya ocupa
el 35 % del visor, y los umbrales van de 0,02 en 0,02 para que la segunda
condición tenga cuándo evaluarse. Si agregás un bloque `.revelar` alto,
probalo a 390 px recorriéndolo entero; el script que lo mide está descrito
en el comentario de `sitio.js`.

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

Y abrir <http://localhost:8000> —o <http://localhost:8000/en/> para la versión
en inglés—. Hace falta un servidor —no vale abrir el archivo con doble clic—
porque los enlaces son absolutos (`/contacto.html`) y las fuentes se piden con
`crossorigin`.

Antes de subir nada:

```bash
python3 tool/verificar.py
```

Comprueba que estén las páginas, que el HTML cierre sus etiquetas, que cada
página tenga `title`, `description`, `lang`, `canonical`, `viewport`, Open Graph,
Twitter Card y un solo `h1`; que ningún enlace interno ni ancla apunte a algo
que no existe; que **ningún recurso** sea externo; que no haya `style=`; que
cada `<script>` en línea tenga su hash en la CSP de su página; que la
analítica esté en las diez páginas con sus hosts en la CSP; que **todas las
URL de tienda del sitio nombren la misma aplicación** —un solo Apple ID y un
solo paquete de Play, que es lo que reemplazó a la regla de «la URL de Apple
en un solo sitio»—, y que cada bloque JSON-LD sea JSON válido. Es el mismo
script que corre en CI.

**Desde el 15-sep-2026 recorre también `en/`**, y ahí comprueba lo que hace que
una traducción no se descuelgue con el tiempo: que cada página tenga su gemela,
que las dos declaren `hreflang` es/en/x-default apuntando la una a la otra, que
la canónica de cada una sea la suya, que **el selector de idioma lleve a la
gemela y no a la portada**, que el `lang` del `<html>` diga la verdad de en qué
carpeta está —`sitio.js` lo lee para saber en qué idioma escribir—, que cada
página use la imagen social **de su idioma**, y que el `sitemap.xml` nombre las
ocho URL con sus alternativas. La tabla de equivalencias es la constante
`GEMELAS`, arriba del archivo: **si agregás una página, agregala ahí y el resto
se comprueba solo.**

⚠️ Y una trampa que costó encontrar: hasta ese día el verificador indexaba cada
página **por su nombre a secas**. Con dos idiomas hay dos `index.html`, y una
tapaba a la otra — las anclas de una se comprobaban contra los `id` de la otra.
Ahora la clave es la ruta relativa (`en/index.html`).

### La analítica del sitio (2-sep-2026)

Decisión del dueño: el sitio mide visitas con **Google Analytics 4 a través de
Firebase** (`assets/js/analitica.js`, un `<script type="module">` en **todas
las páginas —las cinco de cada idioma—**, con los módulos `firebase-app` y `firebase-analytics` **12.18.0**
importados desde gstatic, tal como los entrega la consola de Firebase para un
sitio sin empaquetador). **Es la única excepción a «nada externo»** y por eso
está en un archivo propio con su cabecera explicando qué host necesita y para
qué. Sólo analítica: nada de anuncios, y los hosts de publicidad que la guía
de CSP de Google sugiere «por si acaso» (`doubleclick.net`,
`googlesyndication.com`) **no están abiertos** a propósito.

Lo que eso abrió en la CSP de todas las páginas y de `_headers` —y nada más—:

| Directiva | Hosts | Por qué |
|---|---|---|
| `script-src` | `www.gstatic.com`, `www.googletagmanager.com` | los módulos de Firebase, y el `gtag.js` que `firebase-analytics` carga solo |
| `connect-src` | `*.google-analytics.com`, `analytics.google.com`, `*.analytics.google.com`, `www.googletagmanager.com`, `firebase.googleapis.com`, `firebaseinstallations.googleapis.com` | los hits, la configuración web de la app y el registro de la instalación |
| `img-src` | `*.google-analytics.com`, `www.googletagmanager.com` | el píxel de respaldo cuando no hay `sendBeacon` |

Está comprobado contra Chrome sin interfaz con la consola abierta: cero
violaciones de CSP. Si se sube la versión del SDK, hay que repetir esa prueba.

⚠️ **Esa frase fue falsa durante unas horas el 2-sep-2026**, y conviene saber
por qué. Lighthouse encontró **cinco errores de consola** por visita: gtag
mandaba el hit de la visita a `analytics.google.com` —**el apex, que el
comodín `*.analytics.google.com` no cubre**— y dos hits de publicidad a
`stats.g.doubleclick.net` y `www.google.com` que la CSP bloqueaba a propósito.
Lo primero significaba que **esa visita no se contaba**. Se abrió el apex en
`connect-src` (cinco páginas, `_headers` y `HOSTS_ANALITICA` del verificador) y
las señales de anuncios se **apagaron en el código** (`initializeAnalytics`
con `allow_google_signals: false` y `allow_ad_personalization_signals:
false`), que es decir en gtag lo que ya decía la CSP. Y el SDK **se carga
después del evento `load`** con `import()` dinámico: con los `import`
estáticos de la consola de Firebase, los ~100 KB del SDK competían con la
hoja de estilo y las fuentes que pintan el titular.
El script en línea del `<head>` **no cambió**, así que el hash de la CSP es el
mismo. `tool/verificar.py` exige que la analítica esté **en todas las páginas
o en ninguna** —las cinco de cada idioma, `/en/` incluido— y que cada página que la carga tenga los hosts en su CSP: una
página sin ella se cuenta como cero visitas, y una con el script y sin los
hosts falla en silencio. La política de privacidad lo dice en la cláusula 6
(«El sitio web»). Si algún día se apaga, hay que sacar las tres cosas: el
script, los hosts de la CSP y esa frase.

### Recurso externo y enlace externo no son lo mismo

Desde el 2-sep-2026 el verificador los trata distinto, y la distinción importa:

- Un **recurso** externo (hoja de estilo, script, fuente, imagen de otro
  dominio) sigue siendo **un error**. Lo carga el navegador solo, lo bloquearía
  la CSP y le cuenta a un tercero quién entró al sitio.
- Un **enlace** externo es una navegación que decide el visitante. No lo toca la
  CSP y no delata a nadie hasta que se hace clic. Hace falta uno: el de Google
  Play.

Sigue siendo **lista blanca** (`ENLACES_EXTERNOS_PERMITIDOS`: `play.google.com`
y, desde el 2-sep-2026, `wa.me` para el WhatsApp de Vendoo), tiene que ser
`https` y tiene que llevar `rel="noopener"`.
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
| `.trio` (sube / baja / la verdad) | 3 | 3 → 1, nunca 2 |
| `.latidos` (los tres del corazón) | 3 | 3 → 1, nunca 2 |
| `.mosaico` (capacidades) | 12 | 4 → 3 → 2 → 1: doce se divide por todas |
| `.erps` (muro de ERP) | 12 | 4 → 3 → 2 → 1, por lo mismo |

**Tres elementos no se reparten en dos columnas sin dejar uno solo**: por eso
las rejas de tres saltan de 3 a 1 y **nunca pasan por 2**. Y las de **doce**
—el mosaico de capacidades y el muro de ERP— no necesitan nada, porque doce se
divide exacto por 4, 3, 2 y 1: si alguna vez pasan a trece, hay que volver
acá.

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

- `lang="es-VE"` en las páginas en español y `lang="en"` en las de `/en/`,
  con `hreflang="es"`, `hreflang="en"` y `x-default` —al español— en las ocho
  que están emparejadas. Ver «Los dos idiomas».
- `title` y `description` **únicos por página**, `canonical` propio, `robots`
  (`404.html` va con `noindex, follow` y **sin `hreflang`**: no hay nada que
  indexar en otra lengua). Los títulos llevan la palabra clave por la que se
  busca —«app para vendedores de campo», «fuerza de ventas de campo»,
  «preventa», «Odoo»— y no sólo la marca: «Vendoo: app para vendedores de
  campo y preventa, integrada con Odoo», «Pedí una demo de Vendoo — app de
  fuerza de ventas de campo», y las dos legales con «Vendoo, app de fuerza de
  ventas de campo» detrás del nombre del documento.
- ⚠️ **«La aplicación», nunca «la app Android»** (regla del dueño,
  2-sep-2026: pronto habrá iOS). **Llegó el 11-sep-2026, y la regla se pagó
  sola**: el copy no dijo «Android» en ninguna parte, así que el día que la
  aplicación dejó de ser sólo Android no hubo que reescribir ni un título ni
  una descripción. Vale para títulos, descripciones, Open Graph, JSON-LD y el
  copy. Los sistemas operativos se nombran en tres sitios: `operatingSystem`
  del JSON-LD (dato técnico, hoy `Android 7.0+, iOS 15.0+`), los botones de
  descarga y el «Android 7.0 y iOS 15 o superior» del pie de la portada y de
  la ficha de las legales. `tool/verificar.py` se pone rojo si la cabeza de
  una página dice «app Android» o «aplicación Android»; el espejo «app iOS»
  no está en el chequeo porque nadie lo escribió nunca.
- `<meta name="referrer" content="strict-origin-when-cross-origin">`: es la
  única cabecera de seguridad que se puede poner **desde el HTML**, y por eso
  está. Las demás van en Cloudflare (abajo).
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
  `theme-color` por tema y `apple-touch-icon` + manifiesto coherentes, con un
  ícono de 192 y uno **maskable** de 512 (la teja a sangre y el anillo
  encogido a la zona segura, porque el lanzador de Android recorta con la
  forma que quiere). Los PNG de los íconos salen de `tool/imagenes.py`, que
  pinta las tres figuras del isotipo con sus proporciones.
  ✅ **Los títulos del pie son `<h3>` en todas las páginas** (Lighthouse
  marcaba «heading-order»: un `<h4>` después de un `<h2>`). Este renglón decía
  que `index.html` y `contacto.html` «siguen siendo `<h4>`, y cuando se toquen
  van a `<h3>` también»: **ya se tocaron y ya son `<h3>`**. La regla
  `.pie h3, .pie h4` se conserva porque los pinta igual y no estorba.
- **Rendimiento, medido con Lighthouse.** El 2-sep-2026, con Lighthouse 12 en
  móvil (servidor local, sin gzip; en Pages es mejor porque sí comprime), la
  portada pasó de rendimiento **83 → 98** (CLS **0,29 → 0**), accesibilidad
  95 → 98 y buenas prácticas **93 → 100** (los cinco errores de consola de la
  analítica, arriba); contacto, de 99 / 94 / 93 a 99 / 98 / 100.

  **Vuelto a medir el 15-sep-2026 con Lighthouse 13.4.1, las ocho páginas de
  los dos idiomas** (`--only-categories=performance,accessibility,best-practices,seo`):

  | | rend. | a11y | b. prácticas | SEO |
  |---|---|---|---|---|
  | `/` · `/contacto.html` · `/privacidad.html` · `/terminos.html` | 97–98 | **100** | **100** | **100** |
  | `/en/` · `/en/contact.html` · `/en/privacy.html` · `/en/terms.html` | 97–99 | **100** | **100** | **100** |

  Accesibilidad, buenas prácticas y SEO están en **100 en las ocho**, y
  Lighthouse no marca ni una auditoría fallida: los dos puntos de accesibilidad
  que faltaban eran el `<h4>` del pie, que ya no existe. Lo que movió el
  rendimiento en su día:
  - **Las cuatro Poppins van precargadas** (700 para el titular, 500 para el
    menú, 600 para los botones, 400 para el texto: ~9 KB cada una) y hay una
    `@font-face` de **respaldo con las métricas de Poppins** (`'Poppins
    Respaldo'`: Arial o Roboto con `size-adjust` y los tres `*-override`).
    El salto de 0,29 era el titular en 700 reflowando cuando la fuente
    llegaba tarde; con el respaldo a la misma medida, el cambio no mueve
    nada.
  - El «Descargar» del botón corto de la cabecera se esconde con `clip`
    y no con `display: none`, así que el enlace **conserva su nombre**
    accesible. (Desde el 11-sep-2026 ese botón es `.descarga-corta` y sólo
    sale por debajo de 500 px; los badges llevan su nombre en el `alt`.)
  - Las capturas en WebP y tres anchos (arriba), y la analítica después de
    `load`.
  - Lo que Lighthouse sigue marcando y **no se va a arreglar acá**: la hoja
    de estilo bloquea el pintado (es una sola, de 67 KB sin minificar: el
    repo se sirve tal cual, y minificarla en CI rompería «lo que está en el
    repositorio es lo que se sirve»); y la caché de 10 minutos de Pages, que
    se resuelve en Cloudflare (abajo).
- **Nada externo, con UNA excepción**: ni Google Fonts, ni píxeles, ni CDN.
  Lo único que la página le pide a un tercero es la analítica de visitas
  (abajo, «La analítica del sitio»), por decisión del dueño del 2-sep-2026.

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

El molde usa el logotipo dibujado (no un texto tecleado con Poppins), la
misma fuente autohospedada del sitio y, desde el 2-sep-2026, **un teléfono
con la captura real del Inicio** (`assets/img/capturas/inicio.png`) a la
derecha. **Ni un logotipo ajeno**, y desde el 11-sep-2026 ni uno dibujado: la
primera chapa decía «Google Play» con su triángulo y hoy dice **«Android y
iOS»**, porque nombrar una sola tienda pasó a ser media verdad.

⚠️ **Las chapas entran en UN renglón y nadie avisa si dejan de entrar.** `.pie`
lleva `flex-wrap`, así que una palabra de más no desborda: envuelve, el bloque
sube y el titular se descoloca. Medido el 11-sep-2026 en el molde: «Google Play
y App Store» y «Android y iPhone» **parten el renglón**; «Android y iOS» entra
justo y deja la composición idéntica a la anterior. Si tocás una chapa,
regenerá la imagen **y mirala**.

**Y son DOS desde el 15-sep-2026**, una por idioma, porque el claim que llevan
dibujado es texto. La inglesa sale igual, de `tool/og-en.html`:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --hide-scrollbars \
  --window-size=1200,630 --screenshot=assets/img/og-en.png \
  http://localhost:8000/tool/og-en.html
```

⚠️ **Y en inglés las chapas SÍ se salieron del renglón**, que es exactamente lo
que avisa el párrafo de arriba. La traducción literal —«No signal» y «Odoo and
your ERP»— medía **745 px de los 720** que da `.texto` y tiraba la cuarta chapa
a un segundo renglón, con el titular descolocado. Medido chapa por chapa, las
que entran son **«Android and iOS · Offline · Multi-company · Odoo & ERPs»**:
707 px, 13 de sobra. Las que se probaron y no entran: «Odoo and your ERP» (745),
«Odoo + your ERP» (744) y «Android & iOS» + «Odoo & your ERP» (721, **por un
píxel**).

Si cambia el claim de la portada o esa captura, regenerá **las dos** y miralas:
son lo primero que la gente ve antes de entrar. `tool/verificar.py` comprueba
que las dos existan, que midan 1200 × 630 y que **cada página apunte a la que le
toca** — un `og:image` con el claim en español en una página en inglés es el
error que nadie ve hasta que alguien pega el enlace en un chat.

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

El workflow arma `_sitio/` a mano (HTML, **la carpeta `en/`**, `assets/`,
`robots.txt`, `sitemap.xml`, `favicon.svg`, `site.webmanifest`, `CNAME` y un
`.nojekyll`), borra los `README.md` de `assets/` y **falla si `_headers`,
`tool/` o `.github/` terminaron adentro** — o si **`en/` no llegó**. Ese
segundo chequeo entró con la traducción: `cp -R en _sitio/` es una línea suelta
que alguien puede borrar al reordenar el bloque, y el sitio publicado no
protestaría: sólo se caería `/en/`, con las ocho `hreflang` apuntando a cuatro
404.

`_headers` **no hizo falta tocarlo**: su regla es `/*` y la CSP es la misma en
los dos idiomas —el `<script>` en línea es byte a byte el mismo, así que el hash
tampoco cambió—. La publicación en curso **no se cancela**
(`cancel-in-progress: false`): un `deploy-pages` cortado a la mitad deja el
sitio en un estado que GitHub no promete.

### Lo que Pages NO puede hacer, y lo que se resuelve en Cloudflare

Medido con `curl -sI https://vendooapp.com/` el 2-sep-2026: el sitio responde
**directo desde GitHub** (`server: GitHub.com`, sin `cf-ray`), o sea que hoy
Cloudflare es sólo el DNS. Lo que GitHub ya hace solo: `http://` → `https://`
(301), `www` → apex (301), HTTP/2, gzip/brotli y `cache-control: max-age=600`
en **todo**. Lo que **no** hace y **no se puede configurar** en Pages:

| No se puede en Pages | Por qué | Dónde se resuelve |
|---|---|---|
| Cabeceras HTTP propias (`_headers`, `.htaccess`, `netlify.toml`) | Pages sirve archivos y nada más | Cloudflare → Transform Rules |
| `Strict-Transport-Security` | Pages **no lo manda** en dominios propios (medido) | Cloudflare → SSL/TLS → HSTS |
| `Content-Security-Policy: frame-ancestors` | no se admite en `<meta>`; el resto de la CSP sí va en `<meta>` y ahí está | Cloudflare → Transform Rules |
| Caché por ruta (fuentes un año, imágenes una semana) | Pages pone 10 minutos a todo | Cloudflare → Cache Rules |
| Redirecciones del servidor (301 a medida, reescrituras) | sólo hay `404.html` | Cloudflare → Redirect Rules |
| Compresión o formato de imagen negociado en el borde | no hay servidor | ya está resuelto en el HTML (`<picture>` + WebP) |

⚠️ **El archivo `_headers` de la raíz lo ignora Pages** y ni siquiera se copia
a `_sitio/`: es la **referencia** de lo que hay que reproducir en Cloudflare,
y se mantiene al día con la CSP de las diez páginas (el verificador no lo
lee; es a mano). Nada de esto está aplicado —hace falta la cuenta de
Cloudflare—, y es el dueño quien lo hace. **Antes de todo, la nube naranja**:
las reglas de abajo sólo actúan con el proxy activo en `@` y `www`
(SSL/TLS en **Full (strict)**; el certificado de GitHub para el dominio ya
está emitido, que era la razón de tenerlo en «DNS only»).

**1. SSL/TLS → Edge Certificates → HSTS.** `max-age` 31536000
(un año), **sin** `includeSubDomains` —`<slug>.vendooapp.com` son los Odoo de
los clientes y ese bit los obligaría a todos—, sin `preload` hasta que Legal
lo pida.

**2. Rules → Transform Rules → Modify Response Header**, para
`(http.host eq "vendooapp.com")`, **Set static**:

| Cabecera | Valor |
|---|---|
| `X-Content-Type-Options` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | `geolocation=(), microphone=(), camera=(), interest-cohort=()` |
| `X-Frame-Options` | `DENY` |
| `Content-Security-Policy` | `frame-ancestors 'none'` |

Sólo `frame-ancestors` en la cabecera, **no la política entera**: una segunda
CSP se suma a la del `<meta>` (se aplican las dos, y gana la más estricta), y
tenerla copiada en dos sitios es tenerla desincronizada en uno. El `<meta>`
sigue siendo la fuente.

**3. Rules → Cache Rules**, tres reglas:

| Ruta (`http.request.uri.path`) | Edge TTL | Browser TTL |
|---|---|---|
| `starts_with "/assets/fonts/"` | 1 año | 1 año |
| `starts_with "/assets/img/"` | 1 semana | 1 semana |
| `starts_with "/assets/css/"` o `"/assets/js/"` | respetar el origen | respetar el origen (10 min) |

CSS y JS **no** se alargan: sus URL no llevan versión, y una hoja cacheada un
mes pintaría el HTML nuevo con el estilo viejo durante un mes en vez de
diez minutos. Las fuentes y las imágenes no cambian sin cambiar de nombre o
de dibujo.

**4. Lo que hay que dejar APAGADO en Cloudflare**, porque cada una inyecta un
`<script>` en el HTML y la CSP lo bloquea —o peor, rompe el hash del script
del tema—: **Rocket Loader**, **Auto Minify** (reescribe el script en línea y
el hash deja de coincidir), **Email Address Obfuscation**, **Web Analytics /
Browser Insights** (ya hay GA4) y **Mirage**. **Polish** se puede dejar en
«Lossless»: no toca el HTML.

**5. Redirecciones**: `www` → apex y `http` → `https` ya las hace GitHub. Una
Redirect Rule en Cloudflare las ahorra un salto y no hace falta. Si algún día
cambia una URL del sitio (por ejemplo `/#integraciones` → `/integraciones.html`),
la 301 va acá: Pages no tiene dónde ponerla.

Después de aplicarlo, comprobar con `curl -sI https://vendooapp.com/` que
aparecen `cf-ray`, `strict-transport-security` y las cinco cabeceras, y con
`curl -sI https://vendooapp.com/assets/fonts/poppins-700.woff2` que
`cache-control` dice un año. Y volver a mirar la consola del navegador: si
alguna función de Cloudflare inyectó algo, la CSP lo dice ahí.

**Los bloques JSON-LD no necesitan hash.** Están comprobados contra Chrome:
`<script type="application/ld+json">` no se ejecuta, así que `script-src` no lo
alcanza y no genera violación. El único script que sí necesita su hash es el del
tema, que va en línea en el `<head>`.

---

## Lo que falta, y quién lo decide

| Qué | Dónde | Quién |
|---|---|---|
| Las reglas de Cloudflare de arriba (HSTS, cabeceras, caché) | panel de Cloudflare | Dueño |
| Horario de atención público, si se quiere | `contacto.html` | Dueño |
| 🔴 **Los badges de tienda en INGLÉS.** El arte que hay es el de la campaña en español (Apple `es-MX`, Google `Spanish-LATAM`) y en `/en/` incumple la regla de idioma de las dos guías. Hay que bajarlo de [Apple](https://developer.apple.com/app-store/marketing/guidelines/) y de [Google](https://partnermarketinghub.withgoogle.com/brands/google-play/google-play/lockups-icons-badges/#badges) y servirlo desde `assets/img/tiendas/`. **No se dibuja ni se le edita el texto al que hay**: eso es justo lo que las dos guías prohíben, y un badge retocado es peor que uno en otro idioma | `assets/img/tiendas/` | Dueño |
| **Si el soporte se atiende en inglés.** `/en/contact.html#support` dice hoy «our working language is Spanish», porque que exista la traducción no prueba que haya quien conteste en inglés y eso no está escrito en ningún repositorio. Si se atiende, cambia esa frase y el `availableLanguage` del JSON-LD de esa página pasa a `["es","en"]` | `en/contact.html` | Dueño |
| Que un abogado mire la **nota de prevalencia** de las dos legales en inglés («the Spanish text prevails»), que es lo que evita que la traducción sea un segundo texto vinculante | `en/terms.html`, `en/privacy.html` | Legal |
| Revisión de abogado venezolano de las cláusulas 15 y 17 de los términos | `terminos.html` | Legal |
| Que la ficha de App Store conteste 200 antes de publicar el sitio (el 11-sep-2026 daba 404) | App Store Connect | Dueño |
| `downloadUrl` / `offers` del JSON-LD nombran una sola tienda (admiten un destino) | `index.html` | Dueño |

✅ **El botón compacto de la cabecera ya no lleva sólo a Google Play.** Estaba
en esta tabla como pendiente del dueño, y el dueño lo resolvió el mismo
11-sep-2026 con los dos badges oficiales en la cabecera —y, por debajo de 500 px,
con el botón corto a `/#descargar`—. Está contado arriba, en «Los badges son el
arte OFICIAL».

Nada de eso se inventa: un correo que rebota o un número que no existe es peor
que no poner ninguno. Los datos de contacto publicados son dos:
**hola@vendooapp.com** —que tiene que decir lo mismo en tres sitios: acá, en la
política de privacidad y en el `VENDOO_CORREO_PRIVACIDAD` con el que se compila
la app; si difieren, el vendedor lee uno y escribe al otro— y el **WhatsApp
+58 412-346 9712** (`https://wa.me/584123469712`, dueño, 2-sep-2026), en la
página de contacto y en el pie de las diez páginas. El ícono de WhatsApp es
**propio** (una burbuja con un auricular), no el logotipo: la misma regla del
muro de ERP.

⚠️ **Ese número es además, desde el 12-sep-2026, el TELÉFONO** (`tel:`) del
bloque de soporte. Es el mismo número dicho dos veces, no dos datos: Apple pide
un teléfono en la Support URL, y un número que sólo se puede escribir por un
mensajero no es lo que ese campo promete. Si alguna vez son dos números
distintos hay que separarlos en **seis** sitios: `#soporte` y `#support`, el
pie de las diez páginas, y el JSON-LD de la cabeza de `contacto.html` y de
`en/contact.html`.

Si en el futuro hace falta dejar un dato a la vista sin inventarlo, la clase
`.pendiente` sigue en la hoja de estilo: pinta el marcador en punteado naranja.
⚠️ **Hoy no la usa ninguna página, y ese renglón ya cambió dos veces**: la usó
la «Dirección legal» de `contacto.html#soporte` entre el 12-sep-2026 y el día
en que el dueño entregó el domicilio —que es justamente el caso para el que se
conservó— y volvió a quedar libre cuando ese dato llegó. Sigue en la hoja
porque el caso se va a repetir.

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

  ⚠️ **La segunda revisión grande fue el 11-sep-2026, por iOS**, y ahí Android
  no era una palabra de venta: era la descripción de un mecanismo. Cambiaron
  siete cláusulas, **cada una con su propia «Nota de cambio» fechada**, más una
  nota general al pie de la cláusula 1 que las enumera. Lo que cambió de verdad,
  y lo que no:

  | Cláusula | Qué pasó |
  |---|---|
  | 1 | Se distribuye por las dos tiendas; los permisos los pide «el sistema operativo», no Android. De paso se quitó «acceso a fotografías» de la lista: **ninguna** de las dos versiones pide ese permiso. |
  | 2.e | Una solicitud de pago admite **hasta tres fotografías adicionales** (novedad del 11-sep, no de iOS). |
  | 2.g | *Android Keystore* → «el *Keystore* en Android, el *Llavero* en el iPhone». |
  | 2.i | 🔴 **La que de verdad importaba.** Decía que la aplicación usa ML Kit y que esa biblioteca le manda datos técnicos a Google. **En el iPhone es falso**: lee con *Vision*, de Apple, dentro del aparato y sin enviar nada. La cláusula se partió en dos. |
  | 2.j | En el iPhone el aviso pasa **además por Apple** (APNs) — una transferencia internacional nueva, que hay que declarar—, y el nombre de plataforma que viaja en el registro ya no es siempre `android`. |
  | 4 | La copia en la nube nombra iCloud; se agregó APNs como proveedor; y el mapa **ya no se dibuja en una sola pantalla** (eso venía del 6-sep y estaba sin corregir). |
  | 5 | «Al desinstalar, Android elimina…» → una frase que vale en los dos. |

  **Nada de esto se dedujo del sitio**: cada afirmación se verificó contra
  `../vendoo_app` antes de escribirla. Lo que no se pudo verificar **no se
  escribió**, y está en el reporte del cambio.

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

y pegar el resultado en el `script-src` de **las diez páginas** —las cinco de
cada idioma— y de `_headers` (que sigue siendo la referencia para Cloudflare
aunque Pages lo ignore). El script tiene que ser **idéntico en las diez**, o el
hash sólo servirá para las que lo tengan igual. ⚠️ El de `/en/` es byte a byte
el mismo que el español **a propósito**, comentarios incluidos: no se traduce,
porque traducirlo cambiaría el hash y obligaría a llevar dos en la CSP.
`tool/verificar.py` comprueba justamente eso y te imprime el hash correcto.
