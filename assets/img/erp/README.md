# Logotipos de los ERP

Acá van los SVG oficiales de los sistemas que aparecen en el muro de
**Integraciones** (`index.html`, `#integraciones`).

## Hoy esta carpeta está vacía, y es a propósito

En el sitio, cada sistema se muestra hoy como **su nombre escrito** con la
tipografía del sitio, monocromo, y con el color de la marca sólo al pasar el
cursor. No hay ni un logotipo dibujado. Las dos razones:

1. **No se dibujan de memoria.** Un logotipo ajeno reconstruido a ojo es un
   logotipo **falso**: proporciones que no son, un tono que no es. Es peor que
   no poner ninguno, y es exactamente lo que las guías de marca prohíben.
2. **No se descargan de su servidor.** Sería un recurso externo, y el sitio
   entero se sirve desde su propio origen (lo comprueba `tool/verificar.py` y
   lo exige la política de seguridad de contenido).

Nombrar una marca por escrito para decir con qué sistemas trabaja el producto
es un **uso nominativo**, que es lo que estamos haciendo. Poner su logotipo ya
es usar su identidad visual, y para eso hace falta su permiso.

## Cómo conseguir cada uno

Cada marca tiene su propio trámite; ninguno lo puede hacer un programador por
su cuenta, los tres primeros menos que ninguno:

| Marca | Dónde se pide |
|---|---|
| **Odoo** | Se lo dan a sus *partners*. Si Vendoo entra al programa, viene con el kit de marca. |
| **SAP** | Exige acuerdo (programa de partners / solicitud de uso de marca). No hay descarga libre. |
| **Oracle NetSuite** | Igual: acuerdo previo con Oracle. |
| **Microsoft** | Tiene guía pública de marca para partners, con condiciones de uso. |
| **Intuit QuickBooks, Sage, Zoho, Salesforce** | Todas publican *brand assets* con sus condiciones; hay que leerlas y respetarlas. |
| **Siigo, Alegra, CONTPAQi** | Se piden a la empresa (prensa o comercial). |

**Pedilos con la guía de marca**, no sólo el archivo: ahí dice el área de
resguardo, el tamaño mínimo, si se puede monocromar y sobre qué fondos.

## Cómo poner uno cuando llegue

Tres pasos, y el tercero es una línea de HTML:

1. Dejá el archivo acá con el nombre del sistema, en minúsculas y sin
   espacios: `odoo.svg`, `sap.svg`, `netsuite.svg`, `dynamics-365.svg`,
   `quickbooks.svg`, `sage.svg`, `zoho.svg`, `salesforce.svg`, `siigo.svg`,
   `alegra.svg`, `contpaqi.svg`.
2. **Comprobá que el SVG no llame a nada de afuera** (ni `<image href="http…">`
   ni una fuente remota): el verificador rechaza cualquier recurso externo, y
   con razón. Un SVG de logotipo debería ser sólo `<path>`.
3. En `index.html`, dentro de la ficha de esa marca, agregá `con-logo` a la
   lista de clases y cambiá el `<span class="erp__marca">` por el `<img>`. De
   `Odoo`, por ejemplo, esto:

```html
<li class="erp erp--nativo erp--odoo">
  <span class="erp__marca">Odoo</span>
  <span class="erp__linea">17, 18 y 19</span>
  <span class="erp__sello">Integración nativa</span>
</li>
```

pasa a esto:

```html
<li class="erp erp--nativo erp--odoo con-logo">
  <img class="erp__logo" src="/assets/img/erp/odoo.svg" alt="Odoo" width="96" height="26">
  <span class="erp__linea">17, 18 y 19</span>
  <span class="erp__sello">Integración nativa</span>
</li>
```

**El estilo ya está escrito** (`.erp__logo`, `.erp.con-logo` en
`assets/css/estilo.css`): el logotipo se dibuja a 26 px de alto, el nombre
escrito se oculta y en tema oscuro se aclara el logotipo para que uno negro no
desaparezca contra el fondo. No hace falta tocar el CSS.

⚠️ **La clase se pone A MANO, no la pone JavaScript.** Se pensó un `<img>` con
`onerror` que cayera al texto si el archivo no está, y se descartó por dos
motivos: la CSP del sitio no admite manejadores en línea, y el sitio se ve
entero sin JavaScript — un logotipo que aparece sólo si el script corre no es
un logotipo, es un adorno. Que el HTML diga la verdad de lo que hay.

⚠️ **El `alt` es el nombre de la marca y nada más.** Ni «logo de», ni el
eslogan: un lector de pantalla ya dice que es una imagen.

## Sobre los colores del muro

Las fichas llevan un color de marca **sólo para el tinte del cursor**
(`--erp-c` / `--erp-c-osc` en la hoja de estilo). Son aproximaciones tomadas
de material público y **no sustituyen a la guía de cada marca**: si al pedir
el logotipo viene el color exacto, corregilo ahí.

Las tres marcas latinoamericanas (Siigo, Alegra, CONTPAQi) **no tienen color
asignado** y usan el violeta del sitio: no confirmamos el suyo, y preferimos
no inventarlo. Mismo criterio que con los datos de contacto.

## Si hay que agregar otro sistema al muro

Quedaron fuera por espacio **Aspel**, **Softland** y **Defontana**. Agregar uno
es copiar una ficha y cambiarle el nombre, pero ojo con la cuenta: el muro son
**doce** fichas y se pinta en 2, 3 o 4 columnas — doce se divide exacto por las
tres, así que ninguna fila queda con una sola ficha. Con trece, sí. Si crece,
que crezca a **quince** o **dieciséis**, o revisá los saltos en el CSS.

Y la regla de fondo, que no se negocia: **una etiqueta «A medida» no se
convierte en «Integración nativa»** hasta que esa integración exista y esté
corriendo en producción. Hoy la única es Odoo.
