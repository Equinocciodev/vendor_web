#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificación del sitio de Vendoo — sin dependencias, sin red.

Se corre igual en la máquina de uno (`python3 tool/verificar.py`) que en GitHub
Actions, y por eso no instala nada: usa solo la biblioteca estándar. Es un
chequeo *liviano* a propósito. Lo que comprueba:

  1. que existan las páginas del sitio;
  2. que cada HTML esté bien formado (etiquetas balanceadas);
  3. que cada página tenga lo mínimo de SEO y accesibilidad (title, meta
     description, lang, canonical, viewport, exactamente un <h1>);
  4. que ningún enlace interno ni ningún recurso apunte a un archivo que no
     está, y que ninguna ancla apunte a un id que no existe;
  5. que NO haya recursos externos — nada de CDN: el sitio se sirve entero
     desde su propio origen, que es lo que hace posible la política de
     seguridad de contenido de `_headers`;
  6. que no quede ningún atributo `style=` en el HTML, por lo mismo: cada uno
     obligaría a abrir `style-src` a `unsafe-inline`.

Sale con código 1 si encuentra algo. Los avisos no rompen la publicación.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
OBLIGATORIAS = ['index.html', 'contacto.html', 'terminos.html', 'privacidad.html']
ADEMAS = ['404.html', 'robots.txt', 'sitemap.xml', 'favicon.svg', 'site.webmanifest']

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
        self.enlaces: list[tuple[str, int]] = []
        self.recursos: list[tuple[str, int]] = []
        self.h1 = 0
        self.titulo = ''
        self.en_titulo = False
        self.descripcion = ''
        self.canonica = ''
        self.viewport = ''
        self.lang = ''
        self.imagenes_sin_alt = 0

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
            if a.get('name') == 'description':
                self.descripcion = a.get('content', '')
            if a.get('name') == 'viewport':
                self.viewport = a.get('content', '')
        elif tag == 'link':
            if a.get('rel') == 'canonical':
                self.canonica = a.get('href', '')
            elif a.get('href'):
                self.recursos.append((a['href'], linea))
        elif tag == 'a' and a.get('href'):
            self.enlaces.append((a['href'], linea))
        elif tag in ('script', 'img') and a.get('src'):
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

    def handle_endtag_title(self):
        self.en_titulo = False


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

    for nombre, lector in lectores.items():
        for href, linea in lector.enlaces + lector.recursos:
            if href.startswith(('mailto:', 'tel:')):
                continue
            if href.startswith(('http://', 'https://', '//')):
                error(nombre, f'línea {linea}: recurso o enlace EXTERNO ({href}). '
                              'El sitio se sirve entero desde su propio origen.')
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

    # El sitemap tiene que nombrar las cuatro páginas y ninguna que no exista.
    mapa = (RAIZ / 'sitemap.xml')
    if mapa.exists():
        urls = re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', mapa.read_text(encoding='utf-8'))
        rutas = {u.split('vendooapp.com', 1)[-1] or '/' for u in urls}
        for p in OBLIGATORIAS:
            esperada = '/' if p == 'index.html' else '/' + p
            if esperada not in rutas:
                error('sitemap.xml', f'no incluye {esperada}')
        for r in rutas:
            d = destino(r)
            if d is not None and not d.exists():
                error('sitemap.xml', f'{r} no existe en el sitio')

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
