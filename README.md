# vendoo_web

Sitio público de **Vendoo**, la aplicación Android de fuerza de ventas de Grupo
Leiros. Cuatro páginas: inicio, contacto, términos de servicio y política de
privacidad.

**HTML, CSS y un poco de JavaScript. No hay framework, no hay build y no hay
dependencias**: ni npm, ni un generador de sitios, ni un CDN. Lo que está en el
repositorio es exactamente lo que se sirve. Eso no es minimalismo por deporte —
es lo que permite que la política de seguridad de contenido de `_headers` sea
tan cerrada como es (todo desde el propio origen) y que cualquiera pueda
corregir una coma de la política de privacidad sin instalar nada.

---

## Estructura

```
.
├── index.html            Inicio: qué es Vendoo, para quién, cómo funciona
├── contacto.html         Canales de contacto  ⚠ tiene marcadores sin completar
├── terminos.html         Términos de servicio  ⚠ borrador para Legal
├── privacidad.html       Política de privacidad  ⚠ borrador para Legal
├── 404.html              Página no encontrada
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
│   └── img/              Isotipo, favicons e imagen de OpenGraph
├── tool/verificar.py     El chequeo que corre en CI y también en tu máquina
└── .github/workflows/publicar.yml
```

### La cabecera y el pie están copiados en cada página

A propósito, y conviene saberlo antes de tocarlos: son unas treinta líneas
idénticas al principio y al final de los cinco HTML. **Si cambiás una, cambiala
en las cinco.** La alternativa era inyectarlas con JavaScript, y eso significa
que el menú y el pie no existen para quien tenga el script bloqueado ni para un
buscador que no ejecute JS. Para cinco páginas, la copia sale más barata que ese
costo.

Lo único que cambia entre página y página dentro de la cabecera es el
`aria-current="page"` del enlace activo.

### De dónde sale la identidad visual

Nada de esto se inventó acá: todo viene de `../vendoo_app`.

| Qué | De dónde |
|---|---|
| Colores | `lib/theme/app_themes.dart`, preset `vendoo` (`kVendooThemeConfig`) |
| Tipografía | `assets/google_fonts/Poppins-*.ttf`, reducidos a un subconjunto latino |
| Isotipo | `assets/logo_vendoo.svg` |
| Logotipo (la palabra) | `assets/logotipo_vendoo.svg`, en línea y con `currentColor` |
| Radios, grosor de borde | el mismo preset: tarjeta 16 px, botón 14 px, borde 1,3 px |

Dos reglas heredadas de la app que **no** hay que "arreglar":

- **El violeta de marca `#9B5DE5` no se usa como color de interfaz.** Da 4,13:1
  sobre blanco y no pasa AA. Vive solo dentro del isotipo, que trae su propio
  fondo oscuro. Para interfaz: `#6D28D9` en claro y `#B57BFF` en oscuro.
- **La tarjeta la define el borde, no el relleno.** Por eso la superficie está
  pegada al fondo y hay un borde de 1,3 px en todas.

---

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

Comprueba que estén las cuatro páginas, que el HTML cierre sus etiquetas, que
cada página tenga `title`, `description`, `lang`, `canonical`, `viewport` y un
solo `h1`, que ningún enlace interno ni ancla apunte a algo que no existe, y que
no haya **ningún** recurso externo. Es el mismo script que corre en CI.

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

## Lo que falta completar antes de publicar

Nada de esto se inventó: un correo que rebota o un número que no existe es peor
que no poner ninguno. Todos los marcadores se ven en la página, en punteado
naranja, con la forma `[[así]]`.

| Marcador | Dónde | Quién lo define |
|---|---|---|
| `[[correo de contacto]]` | `contacto.html`, `terminos.html` | Dueño |
| `[[correo de privacidad]]` | `contacto.html`, `privacidad.html` | Dueño |
| `[[número de WhatsApp de soporte]]` | `contacto.html` | Dueño |
| `[[teléfono de la oficina]]` | `contacto.html` | Dueño |
| `[[horario de atención]]` | `contacto.html` | Dueño |
| `[[razón social completa]]` / `[[razón social]]` | las tres páginas | Dueño |
| `[[domicilio fiscal completo]]` | `contacto.html`, `terminos.html`, `privacidad.html` | Dueño |
| `[[fecha de publicación]]` | `terminos.html`, `privacidad.html` | Dueño |
| `[[plazo de conservación del recorrido, a confirmar]]` | `privacidad.html` §5 | Dueño + Legal |
| `[[acuerdo sobre teléfono y plan de datos, a definir]]` | `terminos.html` §11 | Dueño |
| `[[redacción a revisar por Legal]]` | `terminos.html` §15 | Legal |
| `[[jurisdicción y forma de resolución de controversias, a definir por Legal]]` | `terminos.html` §17 | Legal |

Para encontrarlos todos:

```bash
grep -rn '\[\[' *.html
```

Cuando se reemplace un marcador, hay que **quitar también el
`<span class="pendiente">`** que lo envuelve, o el dato quedará pintado como si
siguiera faltando. Y en `contacto.html` hay comentarios HTML al lado de cada uno
diciendo qué más cambia con él (por ejemplo, el `href` del enlace de WhatsApp).

**El correo de privacidad tiene que decir lo mismo en tres sitios**: acá, en la
política publicada y en el `VENDOO_CORREO_PRIVACIDAD` con el que se compila la
app. Si difieren, el vendedor lee uno y escribe al otro.

---

## Los dos documentos legales son borradores

Están marcados como tales dentro de la propia página, arriba de todo.

- **`privacidad.html`** sale de `../vendoo_app/play/politica-privacidad.html` y
  de `../vendoo_app/docs/app_interna_distribucion_y_privacidad_2026-08-15.md`.
  **Los textos están tomados de ahí, no reescritos**: los redactó ese análisis
  con la norma en la mano. Lo que sí se actualizó, porque el hecho cambió, es la
  cláusula 2.a: hasta el 1-sep-2026 decía que la app no trazaba el recorrido
  entre visitas, y desde ese día el rastro continuo forma parte de la
  aplicación. La cláusula lo dice y lleva su nota de cambio. Se agregó además la
  cláusula 2.f (solicitudes de alta y corrección de clientes, con sus recaudos),
  que no existía cuando se escribió el original.

- **`terminos.html`** se redactó para este sitio, sobre el comportamiento real
  de la app. Las cláusulas 15 y 17 —responsabilidad y ley aplicable— y la
  relación de este documento con el contrato de trabajo ya firmado son las que
  más necesitan un abogado venezolano: el art. 18 de la LOTTT
  (irrenunciabilidad) puede vaciar cláusulas que en otro contexto serían
  rutinarias.

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
  Ese script está cubierto por un hash en la CSP de `_headers` — **si lo tocás,
  hay que recalcular el hash**, o el navegador lo bloqueará y el parpadeo
  volverá.
- Todos los colores vienen medidos de la auditoría de color de la app: los
  textos pasan AA o AAA y los bordes cumplen el 3:1 de WCAG 1.4.11.
- Foco visible en todo lo enfocable, enlace de «saltar al contenido»,
  `prefers-reduced-motion` respetado, y ninguna información transmitida sólo
  por color.

## Licencia

Material propiedad de Grupo Leiros. Todos los derechos reservados.

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

y pegar el resultado en el `script-src` de `_headers`. El script tiene que ser
**idéntico en las cinco páginas**, o el hash sólo servirá para una.
