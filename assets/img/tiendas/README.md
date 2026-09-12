# Los badges de las tiendas

⚠️ **Estos dos archivos son ARTE OFICIAL de Apple y de Google, tal como lo
entregan sus guías de marca. No se editan, no se re-tiñen, no se recortan y no
se vuelven a dibujar.** Las dos guías lo prohíben con esas palabras:

- Apple: *«Don't modify, angle, or animate the App Store badge»* y *«Use only
  the badge artwork provided in these guidelines»*.
- Google: *«Don't change the badge color»*, *«Don't remove or rearrange badge
  elements, or otherwise adjust the badge in any way»*.

Hasta el **11-sep-2026** el sitio los **dibujaba a mano** —un triángulo de Play
propio y un ícono nuestro en lugar de la manzana— para no pedirle un byte a un
tercero. Ese día el dueño mandó seguir las guías oficiales y **las dos cosas se
pueden a la vez**: el arte se descarga una vez, se versiona acá y se sirve desde
nuestro propio origen. Cero peticiones a terceros, la CSP intacta (`img-src
'self'`) y el badge es el de verdad.

| Archivo | Qué es | De dónde salió |
|---|---|---|
| `app-store.svg` | «Descárgalo en el App Store», negro, **es-MX** | `https://toolbox.marketingtools.apple.com/api/v2/badges/download-on-the-app-store/black/es-mx` (App Store Marketing Tools). El `<title>` interno lo identifica: `Download_on_the_App_Store_Badge_ESMX_RGB_blk_100217` |
| `google-play.svg` | «DESCARGAR EN Google Play», color, **Spanish-LATAM** | `Google Play Badge guidelines/Get it on Google Play Badges/Digital/svg/GetItOnGooglePlay_Badge_Web_color_Spanish-LATAM.svg`, del paquete que descarga el Partner Marketing Hub (`.../brands/google-play/google-play/lockups-icons-badges/`) |

**El español es el de América Latina, no el de España**, porque el sitio es
`lang="es-VE"`. Apple no publica `es-419`: su variante latinoamericana es
**es-MX** (`es-ES` dice «Consíguelo en el App Store», que acá no se dice). Google
sí tiene `Spanish-LATAM`, y es la que está. Apple además avisa que *«The service
mark App Store always appears in English. Never translate App Store or create
your own localized badge»* — por eso no se toca el texto de adentro.

## Las reglas que aplican al sitio, y dónde se cumplen

Todo esto vive en `.tienda` / `.tiendas` de `assets/css/estilo.css`:

- **Alto mínimo**: Apple pide **40 px** en pantalla; Google, **28 px**. Manda el
  de Apple. El par de la portada va a **48 px** y el de la cabecera a **40 px**,
  que es el mínimo exacto.
- **Zona de respeto**: las dos guías piden **un cuarto del alto del badge** y que
  ahí no entre ni tipografía ni otro gráfico. A 40 px son 10 px y a 48 px, 12; el
  `gap` y los márgenes del contenedor los respetan con holgura.
- **Del mismo tamaño**: Google exige que *«the Google Play badge is the same size
  or larger than the other badges»*. Van **a la misma altura**, y como el de Play
  es más ancho (3,37:1 contra 2,99:1 de Apple) termina siendo el más grande. La
  altura la fija el contenedor y el ancho sale solo: **nunca pongas un `width`
  fijo distinto en uno de los dos.**
- **El App Store va PRIMERO**: Apple lo pide cuando hay badges de otras
  plataformas en la misma composición (*«Place the App Store badge first in the
  lineup of badges»*). Por eso en la portada y en la cabecera el orden es
  App Store → Google Play, y no al revés.
- **Negro los dos, en los dos temas.** Apple: *«Whenever one or more badges for
  other app platforms appear in the layout, use the preferred black badge»*, y el
  badge blanco es sólo una alternativa para cuando el negro pesa de más y **no
  hay otro badge al lado**. Google tiene una sola versión. Los dos traen su
  propio filete gris (`#a6a6a6`), que es lo que los hace legibles sobre el fondo
  oscuro del sitio sin cambiarles un color. **No hay variante para modo oscuro y
  no hay que inventarla.**
- **Van como `<img>`, no en línea.** Un `<svg>` pegado en el HTML invita a que
  alguien le meta `currentColor` o un `fill` del tema, que es exactamente lo que
  las dos guías prohíben. Como `<img>` el arte es intocable desde la hoja de
  estilo.

## Si hay que actualizarlos

Se vuelven a bajar de esas dos fuentes y se reemplazan enteros. **No se editan a
mano**, ni siquiera para sacarles el comentario del generador de Illustrator.
