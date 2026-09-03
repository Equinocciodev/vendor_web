#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deriva las imágenes que el sitio sirve a partir de las maestras.

Se corre a mano, desde la raíz del repositorio, cada vez que cambia una
maestra —una captura nueva, o el isotipo— y se versiona lo que produce:

    python3 tool/imagenes.py

No corre en CI a propósito: el sitio se publica tal cual está en el
repositorio, sin build, y lo que se sirve tiene que poder verse en un `git
diff`. Necesita Pillow (`pip install pillow`), con soporte de WebP, que viene
en la rueda oficial.

Qué produce, y por qué:

1. **Las capturas** (`assets/img/capturas/<nombre>.png`, maestras de
   1080 × 2400). La portada las muestra en cajas de 280 a 360 px de ancho, o
   sea que la maestra pesa entre tres y cuatro veces más de lo que hace
   falta en un teléfono de 2×. De cada una salen:

       <nombre>-360.webp   <nombre>-720.webp   <nombre>-1080.webp

   El HTML las nombra con `<picture>`: `<source type="image/webp" srcset>`
   con los tres anchos, y de respaldo un `<img>` con la maestra PNG entera.
   No hay PNG chicos a propósito: al reescalar, un PNG de interfaz pierde su
   paleta y sale MÁS pesado que la maestra (medido: 190 KB a 720 px contra
   64 KB la maestra de 1080), y el respaldo lo ve sólo un navegador sin WebP,
   que hoy es ninguno de los que importan. `tool/verificar.py` comprueba que exista
   cada archivo de cada `srcset`, así que si se cambia una maestra y no se
   vuelve a correr esto, el verificador no se queja —los archivos siguen
   ahí—, así que el script deja la huella SHA-256 de cada maestra en
   `derivadas.json` y el verificador se pone rojo si una maestra cambió sin
   volver a correr esto. **Cambiar una captura es cambiar la maestra Y
   correr este script.**

2. **Los íconos** a partir de `assets/img/isotipo.svg`, que no se rasteriza
   con ninguna librería: el dibujo son tres figuras (la teja redondeada, el
   anillo y el disco) con proporciones fijas, y se pintan acá con esas mismas
   proporciones, sobremuestreadas 4× para que el borde salga limpio.

       favicon-32.png   icono-180.png   icono-192.png   icono-512.png
       icono-512-maskable.png

   El *maskable* es distinto a propósito: Android recorta el ícono del
   manifiesto con la forma que el lanzador quiera (círculo, lágrima…), y
   sólo garantiza el 80 % central. Por eso ese archivo lleva la teja a
   sangre —sin esquinas redondeadas, porque las pone el sistema— y el anillo
   encogido a la zona segura. Servir el `any` como `maskable` deja el anillo
   cortado en los teléfonos con lanzador circular.

Todo se escribe de forma determinista: correrlo dos veces sin cambiar las
maestras no produce ningún diff.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:  # pragma: no cover
    print('Hace falta Pillow: pip install pillow', file=sys.stderr)
    sys.exit(1)

RAIZ = Path(__file__).resolve().parent.parent
CAPTURAS = RAIZ / 'assets' / 'img' / 'capturas'
IMG = RAIZ / 'assets' / 'img'

# Anchos de las derivadas. 360 cubre la caja a 1×, 720 a 2× y la maestra
# (1080) a 3×. Un cuarto escalón no compra nada: nadie ve estas capturas
# más grandes que la caja del teléfono.
ANCHOS = (360, 720, 1080)
ALTO_MAESTRA = 2400
ANCHO_MAESTRA = 1080

# Proporciones del isotipo, sacadas de assets/img/isotipo.svg (viewBox 1024):
# la teja con radio 232, el anillo de radio 265,2 y trazo 149,6, el disco de
# radio 104,7. Todo relativo a 1024 para poder pintarlo a cualquier tamaño.
TEJA = '#0E0E10'
BLANCO = '#FFFFFF'
DISCO = '#9B5DE5'
RADIO_TEJA = 232 / 1024
RADIO_ANILLO = 265.2 / 1024
TRAZO_ANILLO = 149.6 / 1024
RADIO_DISCO = 104.7 / 1024


def guardar_png(img: Image.Image, destino: Path) -> None:
    img.save(destino, format='PNG', optimize=True)


def guardar_webp(img: Image.Image, destino: Path) -> None:
    # Calidad 82 es donde una captura de interfaz —texto y superficies
    # planas— deja de mostrar halos alrededor de las letras. Sin `method=6`
    # el archivo sale un 10 % más grande por el mismo dibujo.
    img.save(destino, format='WEBP', quality=82, method=6)


def derivar_capturas() -> int:
    maestras = sorted(p for p in CAPTURAS.glob('*.png')
                      if not any(p.stem.endswith(f'-{a}') for a in ANCHOS))
    if not maestras:
        print(f'no hay maestras en {CAPTURAS}')
        return 0
    n = 0
    huellas: dict[str, str] = {}
    for maestra in maestras:
        huellas[maestra.name] = hashlib.sha256(maestra.read_bytes()).hexdigest()
        with Image.open(maestra) as im:
            if im.size != (ANCHO_MAESTRA, ALTO_MAESTRA):
                print(f'  ⚠ {maestra.name} mide {im.size[0]}×{im.size[1]}; '
                      f'la maestra tiene que ser {ANCHO_MAESTRA}×{ALTO_MAESTRA}')
            rgb = im.convert('RGB')
            for ancho in ANCHOS:
                alto = round(rgb.height * ancho / rgb.width)
                chica = rgb if ancho == rgb.width else rgb.resize((ancho, alto), Image.LANCZOS)
                guardar_webp(chica, maestra.with_name(f'{maestra.stem}-{ancho}.webp'))
                n += 1
        print(f'  {maestra.name} → {len(ANCHOS)} webp')
    # La huella de cada maestra: es lo que le permite a tool/verificar.py
    # decir «esta captura cambió y sus WebP son de la anterior».
    (CAPTURAS / 'derivadas.json').write_text(
        json.dumps(huellas, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    return n + 1


def pintar_isotipo(lado: int, maskable: bool = False) -> Image.Image:
    """Pinta el isotipo a `lado` px, sobremuestreado 4× y reducido al final."""
    s = lado * 4
    img = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if maskable:
        # A sangre y con el dibujo encogido a la zona segura (80 % central).
        d.rectangle((0, 0, s - 1, s - 1), fill=TEJA)
        escala = 0.80
    else:
        d.rounded_rectangle((0, 0, s - 1, s - 1), radius=RADIO_TEJA * s, fill=TEJA)
        escala = 1.0
    c = s / 2
    r_ext = (RADIO_ANILLO + TRAZO_ANILLO / 2) * s * escala
    r_int = (RADIO_ANILLO - TRAZO_ANILLO / 2) * s * escala
    r_disco = RADIO_DISCO * s * escala
    d.ellipse((c - r_ext, c - r_ext, c + r_ext, c + r_ext), fill=BLANCO)
    d.ellipse((c - r_int, c - r_int, c + r_int, c + r_int), fill=TEJA)
    d.ellipse((c - r_disco, c - r_disco, c + r_disco, c + r_disco), fill=DISCO)
    return img.resize((lado, lado), Image.LANCZOS)


def derivar_iconos() -> int:
    salidas = {
        'favicon-32.png': (32, False),
        'icono-180.png': (180, False),
        'icono-192.png': (192, False),
        'icono-512.png': (512, False),
        'icono-512-maskable.png': (512, True),
    }
    for nombre, (lado, maskable) in salidas.items():
        img = pintar_isotipo(lado, maskable)
        if maskable:
            img = img.convert('RGB')      # sin alfa: la teja va a sangre
        guardar_png(img, IMG / nombre)
        print(f'  {nombre} ({lado}×{lado}{", maskable" if maskable else ""})')
    return len(salidas)


def main() -> int:
    print('Capturas:')
    a = derivar_capturas()
    print('Íconos:')
    b = derivar_iconos()
    print(f'\n{a + b} archivo(s) escritos.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
