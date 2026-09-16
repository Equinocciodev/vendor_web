#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificación del sitio de Vendoo — sin dependencias, sin red.

Se corre igual en la máquina de uno (`python3 tool/verificar.py`) que en GitHub
Actions, y por eso no instala nada: usa solo la biblioteca estándar. Es un
chequeo *liviano* a propósito. Lo que comprueba:

  1. que existan las páginas del sitio;
  2. que cada HTML esté bien formado (etiquetas balanceadas);
  3. que cada página tenga lo mínimo de SEO y accesibilidad (title, meta
     description, lang, canonical, viewport, Open Graph, Twitter Card y
     exactamente un <h1>);
  4. que ningún enlace interno ni ningún recurso apunte a un archivo que no
     está, y que ninguna ancla apunte a un id que no existe;
  5. que NO haya recursos externos — nada de CDN: el sitio se sirve entero
     desde su propio origen, que es lo que hace posible la política de
     seguridad de contenido de `_headers`;
  6. que no quede ningún atributo `style=` en el HTML, por lo mismo: cada uno
     obligaría a abrir `style-src` a `unsafe-inline`;
  7. que cada `<script>` en línea tenga su hash sha256 declarado en la CSP de
     esa misma página, y
  8. que cada bloque JSON-LD sea JSON válido, y
  9. que la analítica (assets/js/analitica.js) esté en TODAS las páginas y que
     cada página que la carga tenga en su CSP los hosts que necesita;
 10. que cada candidato de un `srcset` (de <img> o de <source>) exista, que
     las derivadas WebP de las capturas salgan de la maestra que está hoy en
     el repositorio (huella en assets/img/capturas/derivadas.json, que escribe
     tool/imagenes.py), que la imagen social mida 1200 × 630 y que el
     manifiesto sea JSON válido con íconos que existen; y
 11. que todas las URL de tienda del sitio nombren la MISMA aplicación —un
     solo Apple ID y un solo paquete de Google Play—, y
 12. que las DOS versiones del sitio —español en la raíz, inglés en /en/—
     estén completas y emparejadas: que cada página tenga su gemela, que las
     dos declaren `hreflang` es/en/x-default apuntando la una a la otra, que
     la canónica de cada una sea la suya, que el selector de idioma de la
     cabecera lleve a la GEMELA (y no a la portada del otro idioma), que el
     `lang` del <html> diga la verdad de en qué carpeta está —`sitio.js` lo
     lee para saber en qué idioma escribir— y que el sitemap las nombre a las
     dos con sus alternativas; y
 13. que ningún título, descripción, Open Graph ni JSON-LD diga «app Android»
     o «aplicación Android» (regla del dueño, 2-sep-2026: es «la aplicación»;
     Android queda sólo en `operatingSystem` del JSON-LD, en los botones de
     descarga y en el «Android 7.0 y iOS 15 o superior» del pie).
     ⚠️ Esa regla se escribió PREVIENDO que iba a haber iOS, y el 11-sep-2026
     lo hubo: desde ese día, además de fea, sería falsa. Se conserva tal cual y
     NO se le agregó el espejo «app iOS», que nadie escribió nunca; el día que
     alguien lo escriba, se agrega acá.

⚠️ LA ANALÍTICA ES LA ÚNICA EXCEPCIÓN A «NADA EXTERNO» (decisión del dueño,
2-sep-2026). El <script> que ven estas comprobaciones es propio
(`/assets/js/analitica.js`); lo externo son sus `import` a gstatic y lo que
el SDK carga después, y eso no lo ve un lector de HTML: lo cubre la CSP. Por
eso el chequeo 9 mira que los hosts estén en la política de CADA página —un
script con los hosts a medias falla en silencio, y una página sin el script
cuenta cero visitas.

⚠️ RECURSO y ENLACE no son lo mismo, y desde el 2-sep-2026 el script los
trata distinto. Un *recurso* externo (una hoja de estilo, un script, una
fuente, una imagen de otro dominio) sigue siendo un error: lo carga el
navegador, lo bloquearía la CSP y le contaría a un tercero quién visita el
sitio. Un *enlace* externo es una navegación que el visitante decide, no la
carga: no la toca la CSP y no delata a nadie hasta que se hace clic. La app
está publicada en Google Play y en App Store, y los dos botones de
descarga tienen que poder apuntar ahí. Por eso hay una lista blanca corta —y sigue siendo lista
blanca: cualquier otro dominio es un error, para que nadie meta un pixel de
seguimiento disfrazado de enlace.

Sale con código 1 si encuentra algo. Los avisos no rompen la publicación.
"""

from __future__ import annotations

import base64
import hashlib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# El sitio existe en DOS idiomas desde el 15-sep-2026: el espanol en la raiz
# —que es donde estaba y donde se queda, porque esas URL estan registradas en
# App Store Connect y en Google Play y no se mueven— y el ingles en /en/.
#
# `GEMELAS` es la tabla de equivalencias, y es la fuente de casi todo lo que
# comprueba este archivo sobre idiomas: que las dos existan, que cada una
# apunte a la otra con `hreflang`, que el selector de la cabecera lleve a la
# gemela y no a la portada, y que el sitemap las nombre a las dos.
GEMELAS = {
    'index.html':      'en/index.html',
    'contacto.html':   'en/contact.html',
    'terminos.html':   'en/terms.html',
    'privacidad.html': 'en/privacy.html',
}
OBLIGATORIAS = sorted(list(GEMELAS.keys()) + list(GEMELAS.values()))
ADEMAS = ['404.html', 'robots.txt', 'sitemap.xml', 'favicon.svg',
          'site.webmanifest', 'site-en.webmanifest']

# Las URL publicas de cada archivo, para poder comparar lo que dicen los
# `hreflang` contra lo que hay en el disco.
SITIO = 'https://vendooapp.com'


def url_de(rel: str) -> str:
    if rel == 'index.html':
        return SITIO + '/'
    if rel == 'en/index.html':
        return SITIO + '/en/'
    return SITIO + '/' + rel


def rel_de(url: str) -> str:
    """La inversa: de una URL del sitio al archivo que deberia servirla."""
    ruta = url.split(SITIO, 1)[-1] if url.startswith(SITIO) else url
    ruta = ruta.split('#')[0].split('?')[0].lstrip('/')
    if ruta == '' or ruta.endswith('/'):
        ruta += 'index.html'
    return ruta

# Los únicos dominios a los que el sitio puede ENLAZAR (nunca pedirles un
# recurso). Tres, cada uno con su razón: en Play y en App Store está publicada
# la aplicación —`apps.apple.com` entró el 11-sep-2026, el día en que Vendoo
# dejó de ser sólo de Android— y wa.me es el WhatsApp de Vendoo
# (+58 412-346 9712, decisión del dueño del 2-sep-2026), que va en la página de
# contacto y en el pie de las cinco.
#
# ⚠️ Que un dominio esté acá NO dice que la página del otro lado exista: esto
# es una lista blanca de a quién se PUEDE enlazar, no una comprobación de que
# el enlace conteste. El verificador no sale a la red a propósito (corre igual
# sin internet y en CI). Comprobar una ficha de tienda es a mano:
#     curl -o /dev/null -w '%{http_code}' <la url>
# Se hizo el 11-sep-2026: Play contestó 200 y App Store, 404 —la ficha estaba
# creada pero sin publicar—. El enlace se puso igual, por decisión del dueño.
ENLACES_EXTERNOS_PERMITIDOS = {'play.google.com', 'apps.apple.com', 'wa.me'}

# La analítica del sitio y los hosts que su SDK necesita en la CSP. Medido
# contra Firebase 12.18.0; si se sube la versión, se vuelve a medir.
ANALITICA = '/assets/js/analitica.js'
HOSTS_ANALITICA = {
    'script-src': ['https://www.gstatic.com', 'https://www.googletagmanager.com'],
    'connect-src': ['https://*.google-analytics.com', 'https://analytics.google.com',
                    'https://*.analytics.google.com',
                    'https://www.googletagmanager.com', 'https://firebase.googleapis.com',
                    'https://firebaseinstallations.googleapis.com'],
    'img-src': ['https://*.google-analytics.com', 'https://www.googletagmanager.com'],
}

VACIAS = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
          'meta', 'param', 'source', 'track', 'wbr'}

errores: list[str] = []
avisos: list[str] = []


def error(archivo: str, texto: str) -> None:
    errores.append(f'{archivo}: {texto}')


def aviso(archivo: str, texto: str) -> None:
    avisos.append(f'{archivo}: {texto}')


class Lector(HTMLParser):
    """Recorre el documento anotando lo que hace falta comprobar después."""

    def __init__(self, archivo: str):
        super().__init__(convert_charrefs=True)
        self.archivo = archivo
        self.pila: list[tuple[str, int]] = []
        self.ids: set[str] = set()
        self.enlaces: list[tuple[str, int, dict]] = []
        self.recursos: list[tuple[str, int]] = []
        self.pistas: list[tuple[str, int]] = []      # preconnect / dns-prefetch
        self.cabeza = True                            # hasta que se cierre <head>
        self.texto_cabeza: list[str] = []             # title/meta/JSON-LD de la cabeza
        self.h1 = 0
        self.titulo = ''
        self.en_titulo = False
        self.descripcion = ''
        self.canonica = ''
        self.viewport = ''
        self.lang = ''
        self.csp = ''
        self.metas: dict[str, str] = {}
        self.imagenes_sin_alt = 0
        self.alternas: dict[str, str] = {}      # hreflang -> href
        self.idioma_href = ''                   # el <a class="idioma"> de la cabecera
        self.en_script: str | None = None   # el `type` del <script> abierto
        self.guiones_de_script: list[tuple[str, int, str]] = []  # (tipo, linea, cuerpo)
        self.linea_script = 0
        self.cuerpo_script = ''

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        linea = self.getpos()[0]

        if 'id' in a and a['id']:
            self.ids.add(a['id'])
        if 'style' in a:
            error(self.archivo, f'línea {linea}: atributo style= en <{tag}> '
                                '(rompería la política de seguridad de contenido)')

        if tag == 'html':
            self.lang = a.get('lang', '')
        elif tag == 'h1':
            self.h1 += 1
        elif tag == 'title':
            self.en_titulo = True
        elif tag == 'meta':
            nombre = a.get('name') or a.get('property') or ''
            if nombre:
                self.metas[nombre] = a.get('content', '')
            if a.get('name') == 'description':
                self.descripcion = a.get('content', '')
            if a.get('name') == 'viewport':
                self.viewport = a.get('content', '')
            if (a.get('http-equiv') or '').lower() == 'content-security-policy':
                self.csp = a.get('content', '')
        elif tag == 'link':
            if a.get('rel') == 'canonical':
                self.canonica = a.get('href', '')
            elif a.get('rel') == 'alternate':
                # hreflang: apunta a URLs absolutas propias, y desde el
                # 15-sep-2026 se comprueban (ver «los dos idiomas», abajo).
                if a.get('hreflang'):
                    self.alternas[a['hreflang']] = a.get('href', '')
            elif a.get('rel') in ('preconnect', 'dns-prefetch'):
                # Una pista de red no carga nada, pero nombra un host: tiene
                # que ser uno que la CSP ya deje entrar (abajo).
                self.pistas.append((a.get('href', ''), linea))
            elif a.get('href'):
                self.recursos.append((a['href'], linea))
        if tag == 'meta' and self.cabeza:
            self.texto_cabeza.append(a.get('content', ''))
        elif tag == 'a' and a.get('href'):
            self.enlaces.append((a['href'], linea, a))
            if 'idioma' in (a.get('class') or '').split():
                self.idioma_href = a['href']
        elif tag == 'script':
            self.en_script = (a.get('type') or 'text/javascript').lower()
            self.linea_script = linea
            self.cuerpo_script = ''
            if a.get('src'):
                self.recursos.append((a['src'], linea))
                self.en_script = None
        elif tag == 'img' and a.get('src'):
            self.recursos.append((a['src'], linea))
        if tag in ('img', 'source') and a.get('srcset'):
            for candidato in a['srcset'].split(','):
                url = candidato.strip().split()[0] if candidato.strip() else ''
                if url:
                    self.recursos.append((url, linea))

        if tag == 'img' and not a.get('alt') and a.get('alt') != '':
            self.imagenes_sin_alt += 1

        if tag not in VACIAS:
            self.pila.append((tag, linea))

    def handle_startendtag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a and a['id']:
            self.ids.add(a['id'])
        if 'style' in a:
            error(self.archivo, f'línea {self.getpos()[0]}: atributo style= en <{tag}>')

    def handle_endtag(self, tag):
        if tag == 'head':
            self.cabeza = False
        if tag == 'script' and self.en_script is not None:
            self.guiones_de_script.append(
                (self.en_script, self.linea_script, self.cuerpo_script))
            self.en_script = None
        if tag in VACIAS:
            return
        if not self.pila:
            error(self.archivo, f'línea {self.getpos()[0]}: </{tag}> sin apertura')
            return
        if self.pila[-1][0] != tag:
            abierta, ln = self.pila[-1]
            error(self.archivo,
                  f'línea {self.getpos()[0]}: </{tag}> cierra a <{abierta}> '
                  f'(abierta en la línea {ln})')
            # se desapila igual para no encadenar errores falsos
            for i in range(len(self.pila) - 1, -1, -1):
                if self.pila[i][0] == tag:
                    del self.pila[i:]
                    return
            return
        self.pila.pop()

    def handle_data(self, datos):
        if self.en_titulo:
            self.titulo += datos
            if self.cabeza:
                self.texto_cabeza.append(datos)
        if self.en_script is not None:
            self.cuerpo_script += datos
            if self.cabeza and self.en_script == 'application/ld+json':
                self.texto_cabeza.append(datos)


def destino(href: str, desde: str = '') -> Path | None:
    """Convierte un href interno en la ruta del archivo que debería existir.

    `desde` es la página que lo escribió, relativa a la raíz. Hace falta desde
    que hay páginas en subcarpeta: en `/en/` un href relativo NO cuelga de la
    raíz del sitio, y resolverlo como si colgara daba por bueno un enlace roto.
    Todo el sitio escribe rutas absolutas, así que esto es un seguro.
    """
    ruta = href.split('#')[0].split('?')[0]
    if not ruta:
        return None
    if ruta.startswith('/'):
        base = RAIZ
        ruta = ruta[1:]
    else:
        base = (RAIZ / desde).parent if desde else RAIZ
    if ruta == '' or ruta.endswith('/'):
        ruta += 'index.html'
    return base / ruta


def dominio(url: str) -> str:
    sin = re.sub(r'^https?://', '', url)
    sin = sin[2:] if sin.startswith('//') else sin
    return sin.split('/')[0].split(':')[0].lower()


def sha256_b64(texto: str) -> str:
    return 'sha256-' + base64.b64encode(
        hashlib.sha256(texto.encode('utf-8')).digest()).decode()


def main() -> int:
    for nombre in OBLIGATORIAS + ADEMAS:
        if not (RAIZ / nombre).exists():
            error(nombre, 'falta este archivo')

    # Las de la raíz (español) y las de /en/ (inglés). Cada página se nombra
    # por su ruta relativa y NO por su nombre a secas: hay dos `index.html` y
    # dos `contact`/`contacto`, y con el nombre pelado una tapaba a la otra —
    # las anclas de una se habrían comprobado contra los `id` de la otra.
    paginas = sorted(RAIZ.glob('*.html')) + sorted((RAIZ / 'en').glob('*.html'))
    if not paginas:
        error('(sitio)', 'no hay ninguna página HTML')

    def rel(p: Path) -> str:
        return p.relative_to(RAIZ).as_posix()

    ids_por_pagina: dict[str, set[str]] = {}
    lectores: dict[str, Lector] = {}

    for pagina in paginas:
        texto = pagina.read_text(encoding='utf-8')
        lector = Lector(rel(pagina))
        # el <title> se cierra por la vía normal; se recupera con expresión
        # regular porque HTMLParser no distingue el fin del título del resto.
        lector.feed(texto)
        lector.close()
        if lector.pila:
            for tag, ln in lector.pila:
                error(rel(pagina), f'<{tag}> abierta en la línea {ln} y nunca cerrada')
        m = re.search(r'<title>(.*?)</title>', texto, re.S)
        lector.titulo = (m.group(1).strip() if m else '')
        lectores[rel(pagina)] = lector
        ids_por_pagina[rel(pagina)] = lector.ids

        if not lector.titulo:
            error(rel(pagina), 'sin <title>')
        elif len(lector.titulo) > 70:
            aviso(rel(pagina), f'<title> de {len(lector.titulo)} caracteres (más de 70)')
        if not lector.descripcion:
            error(rel(pagina), 'sin <meta name="description">')
        elif len(lector.descripcion) > 175:
            aviso(rel(pagina), f'descripción de {len(lector.descripcion)} caracteres')
        if not lector.lang:
            error(rel(pagina), 'el <html> no declara lang')
        else:
            # El `lang` es la fuente de verdad del idioma: de ahí lo lee
            # `sitio.js` para rotular el interruptor de tema y para armar el
            # correo del formulario. Si una página de /en/ dijera `es-VE`, la
            # traducción estaría ahí pero el script escribiría en español.
            esperado = 'en' if rel(pagina).startswith('en/') else 'es'
            if lector.lang.lower().split('-')[0] != esperado:
                error(rel(pagina), f'el <html> declara lang="{lector.lang}" y está en '
                                   f'la versión «{esperado}». `assets/js/sitio.js` lee ese '
                                   'atributo para saber en qué idioma escribir.')
        if not lector.viewport:
            error(rel(pagina), 'sin <meta name="viewport">')
        if not lector.canonica:
            error(rel(pagina), 'sin <link rel="canonical">')
        if lector.h1 != 1:
            error(rel(pagina), f'tiene {lector.h1} elementos <h1>; debe haber exactamente uno')
        if lector.imagenes_sin_alt:
            error(rel(pagina), f'{lector.imagenes_sin_alt} <img> sin alt')

        # Regla del dueño (2-sep-2026): es «la aplicación», no «la app Android».
        # Se mira title, meta y JSON-LD de la cabeza; `operatingSystem` del
        # JSON-LD es dato técnico y se excluye.
        cabeza = re.sub(r'"operatingSystem"\s*:\s*"[^"]*"', '', '\n'.join(lector.texto_cabeza))
        m_android = re.search(r'\b(app|aplicaci[oó]n)\s+Android\b', cabeza, re.I)
        if m_android:
            error(rel(pagina), f'la cabeza dice «{m_android.group(0)}»: es «la aplicación» '
                               '(regla del dueño, 2-sep-2026; Android sólo en operatingSystem).')

        # Open Graph y Twitter Card: lo que decide cómo se ve el sitio cuando
        # alguien lo pega en un chat. Si falta, no se nota hasta que se pega.
        for etiqueta in ('og:title', 'og:description', 'og:image', 'og:url',
                         'og:type', 'twitter:card', 'twitter:title',
                         'twitter:description', 'twitter:image'):
            if not lector.metas.get(etiqueta):
                error(rel(pagina), f'sin <meta> {etiqueta}')

        # Cada <script> en línea tiene que estar declarado en la CSP de SU
        # página, o el navegador lo bloquea en silencio y el tema parpadea.
        # (Los bloques JSON-LD no se ejecutan y no los alcanza la CSP.)
        for tipo, linea, cuerpo in lector.guiones_de_script:
            if tipo == 'application/ld+json':
                try:
                    json.loads(cuerpo)
                except Exception as exc:
                    error(rel(pagina), f'línea {linea}: el JSON-LD no es JSON válido ({exc})')
                continue
            h = sha256_b64(cuerpo)
            if h not in lector.csp:
                error(rel(pagina),
                      f'línea {linea}: <script> en línea sin su hash en la CSP de esta '
                      f'página. El que corresponde es {h!r} — ver el README.')

    for nombre, lector in lectores.items():
        # La analítica: en todas las páginas, y con sus hosts en la CSP.
        carga_analitica = any(h == ANALITICA for h, _ in lector.recursos)
        if not carga_analitica:
            # ⚠️ «las cinco páginas» es la frase de siempre y se conserva, pero
            # esto recorre TODOS los *.html: desde el 12-sep-2026 son seis, y
            # el sexto —soporte.html— es un desvío a contacto.html#soporte, no
            # una página. Lleva la analítica igual, y así de paso cuenta si
            # alguien llega por esa dirección.
            error(nombre, f'no carga {ANALITICA}: la analítica va en las cinco páginas '
                          '—y en el desvío de soporte.html— o en ninguna (ver el README).')
        else:
            directivas = {}
            for trozo in lector.csp.split(';'):
                partes = trozo.split()
                if partes:
                    directivas[partes[0]] = partes[1:]
            for directiva, hosts in HOSTS_ANALITICA.items():
                faltan = [h for h in hosts if h not in directivas.get(directiva, [])]
                if faltan:
                    error(nombre, f'la CSP no abre {", ".join(faltan)} en {directiva}, y '
                                  f'{ANALITICA} lo necesita.')

        for href, linea in lector.pistas:
            d = dominio(href)
            abiertos = {dominio(h) for hosts in HOSTS_ANALITICA.values() for h in hosts}
            if not href.startswith('https://') or d not in abiertos:
                error(nombre, f'línea {linea}: preconnect/dns-prefetch a {href}, que no es '
                              'un host de la analítica. Una pista de red a un tercero '
                              'le cuenta quién entró aunque no cargue nada.')

        for href, linea, attrs in lector.enlaces:
            if href.startswith(('mailto:', 'tel:')):
                continue
            if href.startswith(('http://', 'https://', '//')):
                d = dominio(href)
                if d not in ENLACES_EXTERNOS_PERMITIDOS:
                    error(nombre, f'línea {linea}: enlace EXTERNO a {d}. Sólo se permite '
                                  f'enlazar a {", ".join(sorted(ENLACES_EXTERNOS_PERMITIDOS))}.')
                    continue
                if not href.startswith('https://'):
                    error(nombre, f'línea {linea}: el enlace externo {href} no es https')
                if 'noopener' not in (attrs.get('rel') or ''):
                    error(nombre, f'línea {linea}: el enlace externo a {d} necesita '
                                  'rel="noopener"')
                continue
            if href.startswith('#'):
                if href[1:] not in lector.ids:
                    error(nombre, f'línea {linea}: el ancla {href} no existe en esta página')
                continue
            archivo = destino(href, nombre)
            if archivo is None:
                continue
            if not archivo.exists():
                error(nombre, f'línea {linea}: {href} apunta a un archivo que no está')
                continue
            if '#' in href and archivo.suffix == '.html':
                ancla = href.split('#', 1)[1]
                try:
                    clave = archivo.resolve().relative_to(RAIZ).as_posix()
                except ValueError:
                    clave = archivo.name
                ids = ids_por_pagina.get(clave)
                if ids is not None and ancla not in ids:
                    error(nombre, f'línea {linea}: {href} apunta a un id que no existe')

        for href, linea in lector.recursos:
            if href.startswith(('http://', 'https://', '//')):
                error(nombre, f'línea {linea}: RECURSO externo ({href}). El sitio se '
                              'sirve entero desde su propio origen.')
                continue
            archivo = destino(href, nombre)
            if archivo is not None and not archivo.exists():
                error(nombre, f'línea {linea}: {href} apunta a un archivo que no está')

    # ======================================================================
    # LOS DOS IDIOMAS (15-sep-2026)
    #
    # Una traducción se rompe siempre por el mismo sitio: alguien agrega una
    # página, o le cambia el nombre a una, y la pareja queda coja. El daño no
    # se ve —la página sigue abriendo— pero Google deja de saber que son la
    # misma cosa en dos lenguas, y el visitante que toca «ES» aterriza en la
    # portada en vez de en la página que estaba leyendo.
    #
    # Es el mismo movimiento que ya se hizo con el hash del script del tema y
    # con los identificadores de tienda: una convención que hay que recordar
    # pasa a ser un chequeo que no se puede olvidar.
    for es, en in sorted(GEMELAS.items()):
        for cual in (es, en):
            if cual not in lectores:
                continue
        l_es, l_en = lectores.get(es), lectores.get(en)
        if l_es is None or l_en is None:
            continue                       # ya se reportó arriba como archivo que falta

        u_es, u_en = url_de(es), url_de(en)

        # 1. Cada una declara las tres alternativas, y apuntan a la pareja.
        for pagina, lector, propia, otra in ((es, l_es, u_es, u_en), (en, l_en, u_en, u_es)):
            esperado = {'es': u_es, 'en': u_en, 'x-default': u_es}
            for etiqueta, url in sorted(esperado.items()):
                hay = lector.alternas.get(etiqueta)
                if not hay:
                    error(pagina, f'no declara <link rel="alternate" hreflang="{etiqueta}">. '
                                  f'El que corresponde apunta a {url}.')
                elif hay != url:
                    error(pagina, f'hreflang="{etiqueta}" apunta a {hay} y tiene que apuntar '
                                  f'a {url}.')
            # 2. Y la canónica es la suya, no la de su gemela.
            if lector.canonica and lector.canonica != propia:
                error(pagina, f'la canónica dice {lector.canonica} y esta página se sirve '
                              f'en {propia}.')

        # 3. El selector de la cabecera lleva a la GEMELA, no a la portada.
        #    Mandar todo a «/en/» es contestarle «esta página no existe en el
        #    otro idioma» a alguien que la está leyendo en el otro idioma.
        for pagina, lector, destino_ok in ((es, l_es, url_de(en)), (en, l_en, url_de(es))):
            ruta_ok = destino_ok.replace(SITIO, '')
            if not lector.idioma_href:
                error(pagina, 'la cabecera no tiene el selector de idioma '
                              f'(<a class="idioma">); el suyo lleva a {ruta_ok}.')
            elif lector.idioma_href != ruta_ok:
                error(pagina, f'el selector de idioma lleva a {lector.idioma_href} y tiene '
                              f'que llevar a la gemela, {ruta_ok}.')

    # Las páginas que NO son de la tabla —404.html y los dos desvíos de
    # soporte— no llevan `hreflang` a propósito: no son contenido, van con
    # `noindex` y no compiten en buscadores. Pero si alguna lo llevara, tendría
    # que apuntar a algo que exista.
    emparejadas = set(GEMELAS.keys()) | set(GEMELAS.values())
    for nombre, lector in sorted(lectores.items()):
        if nombre in emparejadas:
            continue
        for etiqueta, url in sorted(lector.alternas.items()):
            d = RAIZ / rel_de(url)
            if not d.exists():
                error(nombre, f'hreflang="{etiqueta}" apunta a {url}, que no existe.')

    # El asunto del correo de contacto vive en TRES sitios por idioma: el
    # `mailto:` del <noscript>, el del enlace directo de al lado, y la tabla
    # `T` de assets/js/sitio.js que arma el correo cuando el script sí corre.
    # Si difieren, el mismo formulario llega a la bandeja con dos asuntos
    # distintos según si el visitante tenía JavaScript — y ordenar por asunto
    # deja de servir. Es la misma clase de copia que el hash del tema.
    js = (RAIZ / 'assets' / 'js' / 'sitio.js')
    if js.exists():
        fuente = js.read_text(encoding='utf-8')
        for pagina, clave in (('contacto.html', 'es'), ('en/contact.html', 'en')):
            lector = lectores.get(pagina)
            if lector is None:
                continue
            m = re.search(r"%s:\s*\{[^}]*?asunto:\s*'([^']*)'" % clave, fuente, re.S)
            if not m:
                error('assets/js/sitio.js', f'no encuentro el asunto del formulario para '
                                            f'«{clave}» en la tabla T.')
                continue
            del_script = m.group(1).strip().rstrip('\u2014').strip()
            # ⚠️ NO se comparan TODOS los mailto: de la página. El bloque de
            # soporte lleva a propósito su propio asunto («Soporte de Vendoo»),
            # que es lo que hace que una petición de soporte se distinga de una
            # de demo en la bandeja. Lo que se exige es que el asunto del
            # formulario esté en la página AL MENOS UNA VEZ: ése es el que se
            # duplica a mano en el <noscript> y en el enlace de al lado, y el
            # que se queda viejo cuando alguien retoca la tabla `T`.
            from urllib.parse import unquote
            asuntos = [unquote(h.split('subject=')[1].split('&')[0]).strip()
                       for h, _, _ in lector.enlaces
                       if h.startswith('mailto:') and 'subject=' in h]
            if not any(a.startswith(del_script) or del_script.startswith(a) for a in asuntos):
                error(pagina, f'sitio.js arma el asunto «{del_script}…» y ningún mailto: de '
                              f'esta página lo usa (hay {asuntos}). El del <noscript> y el del '
                              'enlace directo tienen que decir lo mismo que el script.')

    # El sitemap tiene que nombrar las cuatro páginas y ninguna que no exista.
    mapa = (RAIZ / 'sitemap.xml')
    if mapa.exists():
        xml = mapa.read_text(encoding='utf-8')
        urls = re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', xml)
        rutas = {u.split('vendooapp.com', 1)[-1] or '/' for u in urls}
        for p in OBLIGATORIAS:
            esperada = url_de(p).replace(SITIO, '') or '/'
            if esperada not in rutas:
                error('sitemap.xml', f'no incluye {esperada}')
        for r in rutas:
            d = destino(r)
            if d is not None and not d.exists():
                error('sitemap.xml', f'{r} no existe en el sitio')
        # Y cada <url> declara sus dos alternativas de idioma, que es lo que
        # le dice a un buscador que son la misma página en dos lenguas.
        for bloque in re.findall(r'<url>(.*?)</url>', xml, re.S):
            loc = re.search(r'<loc>\s*([^<\s]+)\s*</loc>', bloque)
            if not loc:
                continue
            quien = rel_de(loc.group(1))
            if quien not in emparejadas:
                continue
            for etiqueta in ('es', 'en'):
                if f'hreflang="{etiqueta}"' not in bloque:
                    error('sitemap.xml', f'{loc.group(1)} no declara su alternativa '
                                         f'hreflang="{etiqueta}"')
        if len(re.findall(r'<lastmod>', xml)) != len(urls):
            error('sitemap.xml', 'hay <url> sin <lastmod>')

    # Las derivadas WebP de las capturas tienen que salir de la maestra que
    # está hoy en el repo. tool/imagenes.py anota la huella de cada maestra;
    # si alguien cambia una captura y no vuelve a correrlo, la portada
    # serviría la pantalla vieja en WebP y la nueva sólo en el respaldo PNG.
    capturas = RAIZ / 'assets' / 'img' / 'capturas'
    huellas = capturas / 'derivadas.json'
    if huellas.exists():
        try:
            anotadas = json.loads(huellas.read_text(encoding='utf-8'))
        except Exception as exc:
            anotadas = {}
            error('assets/img/capturas/derivadas.json', f'no es JSON válido ({exc})')
        for maestra in sorted(capturas.glob('*.png')):
            if re.search(r'-\d+$', maestra.stem):
                continue
            actual = hashlib.sha256(maestra.read_bytes()).hexdigest()
            if anotadas.get(maestra.name) != actual:
                error(f'assets/img/capturas/{maestra.name}',
                      'cambió y sus derivadas WebP son de la versión anterior: '
                      'corré `python3 tool/imagenes.py` y versioná lo que produce.')
    elif capturas.exists():
        error('assets/img/capturas/derivadas.json', 'falta: corré `python3 tool/imagenes.py`.')

    # Las imágenes sociales: OpenGraph pide 1200 × 630 y se lee del IHDR del
    # PNG. Son DOS desde el 15-sep-2026 —una por idioma, porque el claim que
    # llevan dibujado es texto— y las dos tienen que estar: un `og:image` que
    # contesta 404 no se nota hasta que alguien pega el enlace en un chat y
    # sale una tarjeta gris.
    for nombre_og in ('og.png', 'og-en.png'):
        og = RAIZ / 'assets' / 'img' / nombre_og
        etiqueta = f'assets/img/{nombre_og}'
        if not og.exists():
            error(etiqueta, 'falta: es el `og:image` de una de las dos versiones. '
                            'Se genera con tool/og.html y tool/og-en.html (ver el README).')
            continue
        cab = og.read_bytes()[:24]
        if cab[:8] != b'\x89PNG\r\n\x1a\n':
            error(etiqueta, 'no es un PNG')
        else:
            ancho = int.from_bytes(cab[16:20], 'big')
            alto = int.from_bytes(cab[20:24], 'big')
            if (ancho, alto) != (1200, 630):
                error(etiqueta, f'mide {ancho}×{alto}; tiene que ser 1200×630')

    # Y que cada página apunte a la que le toca: el `og:image` de una página en
    # inglés con el claim en español es el error que nadie ve hasta que el
    # enlace se comparte.
    for nombre, lector in sorted(lectores.items()):
        quiere = 'og-en.png' if nombre.startswith('en/') else 'og.png'
        for etiqueta in ('og:image', 'twitter:image'):
            valor = lector.metas.get(etiqueta, '')
            if valor and not valor.endswith('/' + quiere):
                error(nombre, f'{etiqueta} apunta a {valor} y esta página es '
                              f'«{"en" if quiere == "og-en.png" else "es"}»: le toca {quiere}.')

    # Los manifiestos: JSON válido, y cada ícono que nombran existe. Son DOS
    # desde el 15-sep-2026, uno por idioma, porque `lang`, `name` y
    # `description` son campos de UN idioma y no hay forma de declararlos en
    # dos: con uno solo, quien instalara el sitio desde /en/ se encontraba el
    # nombre y la descripción en castellano.
    for nombre_man, lang_esperado in (('site.webmanifest', 'es'), ('site-en.webmanifest', 'en')):
        manifiesto = RAIZ / nombre_man
        if not manifiesto.exists():
            error(nombre_man, 'falta: hay un manifiesto por idioma (ver el README).')
            continue
        try:
            datos = json.loads(manifiesto.read_text(encoding='utf-8'))
            for icono in datos.get('icons', []):
                d = destino(icono.get('src', ''))
                if d is not None and not d.exists():
                    error(nombre_man, f'el ícono {icono.get("src")} no existe')
            if not any('maskable' in (i.get('purpose') or '') for i in datos.get('icons', [])):
                aviso(nombre_man, 'no hay ícono maskable')
            if (datos.get('lang') or '').lower().split('-')[0] != lang_esperado:
                error(nombre_man, f'declara lang="{datos.get("lang")}" y es el manifiesto '
                                  f'de la versión «{lang_esperado}».')
            partida = datos.get('start_url', '')
            if partida != ('/en/' if lang_esperado == 'en' else '/'):
                error(nombre_man, f'start_url dice {partida!r} y tiene que abrir la portada '
                                  f'de su idioma.')
        except Exception as exc:
            error(nombre_man, f'no es JSON válido ({exc})')

    # Y que cada página enlace el manifiesto de SU idioma.
    for nombre, lector in sorted(lectores.items()):
        quiere = '/site-en.webmanifest' if nombre.startswith('en/') else '/site.webmanifest'
        otro = '/site.webmanifest' if nombre.startswith('en/') else '/site-en.webmanifest'
        enlazados = [h for h, _ in lector.recursos if h.endswith('.webmanifest')]
        if otro in enlazados:
            error(nombre, f'enlaza {otro} y le toca {quiere}: el nombre y la descripción '
                          'que se instalan saldrían en el otro idioma.')

    # Las URL de tienda tienen que nombrar UNA sola aplicación.
    #
    # ⚠️ Hasta el 11-sep-2026 la regla era otra y estaba escrita en el README:
    # «la URL de Apple vive en UN solo sitio del marcado». Ese día los dos
    # badges entraron también a la cabecera de las cinco páginas —encargo del
    # dueño— y la cabecera es, por diseño, cuarenta líneas copiadas en los
    # cinco HTML. O sea que la regla ya no se podía cumplir.
    #
    # Lo que la regla protegía no era la copia: era que una copia se quedara
    # vieja («un identificador de tienda copiado en tres plantillas es el que
    # se queda viejo»). Eso se protege mejor acá que con una convención —es el
    # mismo movimiento que el hash del script del tema, que también vive
    # repetido en las cinco y también lo custodia este archivo—. Si alguien
    # cambia el Apple ID o el paquete en una sola página, esto se pone rojo y
    # dice cuál.
    ids_apple: dict[str, set[str]] = {}
    ids_play: dict[str, set[str]] = {}
    for pagina in paginas:
        texto = pagina.read_text(encoding='utf-8')
        for ident in re.findall(r'apps\.apple\.com/(?:[a-z]{2}/)?app/(?:[^/"\s]+/)?id(\d+)', texto):
            ids_apple.setdefault(ident, set()).add(pagina.name)
        for ident in re.findall(r'play\.google\.com/store/apps/details\?id=([\w.]+)', texto):
            ids_play.setdefault(ident, set()).add(pagina.name)
    for cual, hallados in (('Apple ID', ids_apple), ('paquete de Google Play', ids_play)):
        if len(hallados) > 1:
            detalle = '; '.join(f'{k} en {", ".join(sorted(v))}' for k, v in sorted(hallados.items()))
            error('URL de tienda', f'hay {len(hallados)} {cual} distintos en el sitio '
                                   f'({detalle}). Tienen que nombrar la misma aplicación.')

    # robots.txt tiene que declarar el sitemap, o nadie lo encuentra.
    robots = (RAIZ / 'robots.txt')
    if robots.exists() and 'Sitemap: https://vendooapp.com/sitemap.xml' not in \
            robots.read_text(encoding='utf-8'):
        error('robots.txt', 'no declara el Sitemap')

    for a in avisos:
        print('aviso  ' + a)
    for e in errores:
        print('ERROR  ' + e)

    if errores:
        print(f'\n{len(errores)} error(es). El sitio no se publica así.')
        return 1
    print(f'\nTodo en orden: {len(paginas)} páginas, {len(avisos)} aviso(s).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
