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
     cada página que la carga tenga en su CSP los hosts que necesita.

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
está publicada en Google Play y el botón de descarga tiene que poder
apuntar ahí. Por eso hay una lista blanca corta —y sigue siendo lista
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
OBLIGATORIAS = ['index.html', 'contacto.html', 'terminos.html', 'privacidad.html']
ADEMAS = ['404.html', 'robots.txt', 'sitemap.xml', 'favicon.svg', 'site.webmanifest']

# Los únicos dominios a los que el sitio puede ENLAZAR (nunca pedirles un
# recurso). Dos, cada uno con su razón: en Play está publicada la aplicación
# y wa.me es el WhatsApp de Vendoo (+58 412-346 9712, decisión del dueño del
# 2-sep-2026), que va en la página de contacto y en el pie de las cinco.
ENLACES_EXTERNOS_PERMITIDOS = {'play.google.com', 'wa.me'}

# La analítica del sitio y los hosts que su SDK necesita en la CSP. Medido
# contra Firebase 12.18.0; si se sube la versión, se vuelve a medir.
ANALITICA = '/assets/js/analitica.js'
HOSTS_ANALITICA = {
    'script-src': ['https://www.gstatic.com', 'https://www.googletagmanager.com'],
    'connect-src': ['https://*.google-analytics.com', 'https://*.analytics.google.com',
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
                pass                      # hreflang: apunta a URLs absolutas propias
            elif a.get('href'):
                self.recursos.append((a['href'], linea))
        elif tag == 'a' and a.get('href'):
            self.enlaces.append((a['href'], linea, a))
        elif tag == 'script':
            self.en_script = (a.get('type') or 'text/javascript').lower()
            self.linea_script = linea
            self.cuerpo_script = ''
            if a.get('src'):
                self.recursos.append((a['src'], linea))
                self.en_script = None
        elif tag == 'img' and a.get('src'):
            self.recursos.append((a['src'], linea))

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
        if self.en_script is not None:
            self.cuerpo_script += datos


def destino(href: str) -> Path | None:
    """Convierte un href interno en la ruta del archivo que debería existir."""
    ruta = href.split('#')[0].split('?')[0]
    if not ruta:
        return None
    if ruta.startswith('/'):
        ruta = ruta[1:]
    if ruta == '' or ruta.endswith('/'):
        ruta += 'index.html'
    return RAIZ / ruta


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

    paginas = sorted(RAIZ.glob('*.html'))
    if not paginas:
        error('(sitio)', 'no hay ninguna página HTML')

    ids_por_pagina: dict[str, set[str]] = {}
    lectores: dict[str, Lector] = {}

    for pagina in paginas:
        texto = pagina.read_text(encoding='utf-8')
        lector = Lector(pagina.name)
        # el <title> se cierra por la vía normal; se recupera con expresión
        # regular porque HTMLParser no distingue el fin del título del resto.
        lector.feed(texto)
        lector.close()
        if lector.pila:
            for tag, ln in lector.pila:
                error(pagina.name, f'<{tag}> abierta en la línea {ln} y nunca cerrada')
        m = re.search(r'<title>(.*?)</title>', texto, re.S)
        lector.titulo = (m.group(1).strip() if m else '')
        lectores[pagina.name] = lector
        ids_por_pagina[pagina.name] = lector.ids

        if not lector.titulo:
            error(pagina.name, 'sin <title>')
        elif len(lector.titulo) > 70:
            aviso(pagina.name, f'<title> de {len(lector.titulo)} caracteres (más de 70)')
        if not lector.descripcion:
            error(pagina.name, 'sin <meta name="description">')
        elif len(lector.descripcion) > 175:
            aviso(pagina.name, f'descripción de {len(lector.descripcion)} caracteres')
        if not lector.lang:
            error(pagina.name, 'el <html> no declara lang')
        if not lector.viewport:
            error(pagina.name, 'sin <meta name="viewport">')
        if not lector.canonica:
            error(pagina.name, 'sin <link rel="canonical">')
        if lector.h1 != 1:
            error(pagina.name, f'tiene {lector.h1} elementos <h1>; debe haber exactamente uno')
        if lector.imagenes_sin_alt:
            error(pagina.name, f'{lector.imagenes_sin_alt} <img> sin alt')

        # Open Graph y Twitter Card: lo que decide cómo se ve el sitio cuando
        # alguien lo pega en un chat. Si falta, no se nota hasta que se pega.
        for etiqueta in ('og:title', 'og:description', 'og:image', 'og:url',
                         'og:type', 'twitter:card', 'twitter:title',
                         'twitter:description', 'twitter:image'):
            if not lector.metas.get(etiqueta):
                error(pagina.name, f'sin <meta> {etiqueta}')

        # Cada <script> en línea tiene que estar declarado en la CSP de SU
        # página, o el navegador lo bloquea en silencio y el tema parpadea.
        # (Los bloques JSON-LD no se ejecutan y no los alcanza la CSP.)
        for tipo, linea, cuerpo in lector.guiones_de_script:
            if tipo == 'application/ld+json':
                try:
                    json.loads(cuerpo)
                except Exception as exc:
                    error(pagina.name, f'línea {linea}: el JSON-LD no es JSON válido ({exc})')
                continue
            h = sha256_b64(cuerpo)
            if h not in lector.csp:
                error(pagina.name,
                      f'línea {linea}: <script> en línea sin su hash en la CSP de esta '
                      f'página. El que corresponde es {h!r} — ver el README.')

    for nombre, lector in lectores.items():
        # La analítica: en todas las páginas, y con sus hosts en la CSP.
        carga_analitica = any(h == ANALITICA for h, _ in lector.recursos)
        if not carga_analitica:
            error(nombre, f'no carga {ANALITICA}: la analítica va en las cinco páginas '
                          'o en ninguna (ver el README).')
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
            archivo = destino(href)
            if archivo is None:
                continue
            if not archivo.exists():
                error(nombre, f'línea {linea}: {href} apunta a un archivo que no está')
                continue
            if '#' in href and archivo.suffix == '.html':
                ancla = href.split('#', 1)[1]
                ids = ids_por_pagina.get(archivo.name)
                if ids is not None and ancla not in ids:
                    error(nombre, f'línea {linea}: {href} apunta a un id que no existe')

        for href, linea in lector.recursos:
            if href.startswith(('http://', 'https://', '//')):
                error(nombre, f'línea {linea}: RECURSO externo ({href}). El sitio se '
                              'sirve entero desde su propio origen.')
                continue
            archivo = destino(href)
            if archivo is not None and not archivo.exists():
                error(nombre, f'línea {linea}: {href} apunta a un archivo que no está')

    # El sitemap tiene que nombrar las cuatro páginas y ninguna que no exista.
    mapa = (RAIZ / 'sitemap.xml')
    if mapa.exists():
        xml = mapa.read_text(encoding='utf-8')
        urls = re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', xml)
        rutas = {u.split('vendooapp.com', 1)[-1] or '/' for u in urls}
        for p in OBLIGATORIAS:
            esperada = '/' if p == 'index.html' else '/' + p
            if esperada not in rutas:
                error('sitemap.xml', f'no incluye {esperada}')
        for r in rutas:
            d = destino(r)
            if d is not None and not d.exists():
                error('sitemap.xml', f'{r} no existe en el sitio')
        if len(re.findall(r'<lastmod>', xml)) != len(urls):
            error('sitemap.xml', 'hay <url> sin <lastmod>')

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
