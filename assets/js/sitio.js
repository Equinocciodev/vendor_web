/* Vendoo — lo único que este sitio necesita de JavaScript: el interruptor de
   tema. Todo lo demás es HTML y CSS, y la página se lee entera con el script
   apagado.

   El estado tiene TRES valores, no dos: «claro», «oscuro» y —el de fábrica—
   ninguno, que quiere decir «lo que diga el sistema» (`prefers-color-scheme`).
   Por eso el atributo `data-tema` se QUITA en vez de escribirse cuando la
   elección coincide con el sistema: si se escribiera, el visitante que cambia
   su teléfono a oscuro por la noche vería el sitio quedarse en claro.

   La lectura inicial NO vive acá sino en un script en línea dentro del <head>
   de cada página: este archivo se carga con `defer` y para cuando corre el
   primer pintado ya ocurrió, o sea que el sitio parpadearía en blanco. */
(function () {
  'use strict';

  var CLAVE = 'vendoo-tema';
  var raiz = document.documentElement;

  function delSistema() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'oscuro' : 'claro';
  }

  function actual() {
    return raiz.getAttribute('data-tema') || delSistema();
  }

  function aplicar(tema) {
    if (tema === delSistema()) {
      raiz.removeAttribute('data-tema');
      try { localStorage.removeItem(CLAVE); } catch (e) { /* modo privado */ }
    } else {
      raiz.setAttribute('data-tema', tema);
      try { localStorage.setItem(CLAVE, tema); } catch (e) { /* modo privado */ }
    }
    rotular();
  }

  function rotular() {
    var boton = document.querySelector('.tema');
    if (!boton) return;
    var proximo = actual() === 'oscuro' ? 'claro' : 'oscuro';
    boton.setAttribute('aria-label', 'Cambiar a tema ' + proximo);
    boton.setAttribute('title', 'Cambiar a tema ' + proximo);
  }

  document.addEventListener('click', function (ev) {
    var boton = ev.target.closest && ev.target.closest('.tema');
    if (!boton) return;
    aplicar(actual() === 'oscuro' ? 'claro' : 'oscuro');
  });

  // El visitante que no eligió nada sigue al sistema en vivo.
  if (window.matchMedia) {
    var mq = window.matchMedia('(prefers-color-scheme: dark)');
    var alCambiar = function () { if (!raiz.getAttribute('data-tema')) rotular(); };
    if (mq.addEventListener) { mq.addEventListener('change', alCambiar); }
    else if (mq.addListener) { mq.addListener(alCambiar); }
  }

  rotular();
})();


/* ==========================================================================
   Lo que se mueve al hacer scroll (2-sep-2026)

   Tres cosas y ninguna más: las secciones aparecen una vez al entrar en
   pantalla, las cifras cuentan desde cero, y las infografías arrancan su
   animación cuando se las ve (y no antes, corriendo en vano arriba del todo).

   ⚠️ TODO SE VE SIN ESTE ARCHIVO. La regla es que nada quede en `opacity: 0`
   si el JavaScript no corre: el `<head>` de cada página pone `data-anim` y lo
   RETIRA solo a los dos segundos si acá no llegamos a marcar `data-listo`.
   Este archivo es lo primero que hace: reclamar esa marca. Si se bloquea el
   script, la red de seguridad se dispara y la página queda visible, quieta y
   completa — que es exactamente lo que tiene que pasar.

   ⚠️ Y con `prefers-reduced-motion: reduce` no se anima NADA: se quita
   `data-anim` y las cifras se quedan en su valor final, que ya está escrito
   en el HTML. No es una animación más rápida: es ninguna.
   ========================================================================== */
(function () {
  'use strict';

  var raiz = document.documentElement;
  raiz.setAttribute('data-listo', '1');   // el <head> ya no va a quitar data-anim

  var quieto = window.matchMedia &&
               window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (quieto || !('IntersectionObserver' in window)) {
    raiz.removeAttribute('data-anim');    // todo visible, en su estado final
    return;
  }

  /* Las cifras. El valor final ya está escrito en el HTML —es lo que ve
     quien tenga el script apagado y lo que lee un buscador—; acá sólo se
     cuenta hasta él. `data-cifra` es el número y `data-formato` el molde
     («~%d», «%d pasos»), para no tener que adivinar dónde va el símbolo. */
  function contar(nodo) {
    var fin = parseFloat(nodo.getAttribute('data-cifra'));
    var molde = nodo.getAttribute('data-formato') || '%d';
    if (isNaN(fin)) return;
    var arranque = null;
    var duracion = 1100;
    function paso(ahora) {
      if (arranque === null) arranque = ahora;
      var t = Math.min((ahora - arranque) / duracion, 1);
      // desaceleración: llega y se queda, sin rebote
      var v = Math.round(fin * (1 - Math.pow(1 - t, 3)));
      nodo.textContent = molde.replace('%d', v);
      if (t < 1) requestAnimationFrame(paso);
    }
    requestAnimationFrame(paso);
  }

  var mirador = new IntersectionObserver(function (entradas) {
    entradas.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('visible');
      if (e.target.hasAttribute('data-cifra')) contar(e.target);
      mirador.unobserve(e.target);        // una sola vez, nunca al volver
    });
  }, { threshold: 0.18, rootMargin: '0px 0px -6% 0px' });

  var candidatos = document.querySelectorAll('.revelar, [data-cifra]');
  Array.prototype.forEach.call(candidatos, function (n) { mirador.observe(n); });
})();


/* ==========================================================================
   El marcador del menú (2-sep-2026)

   Defecto reportado por el dueño: «el indicador de seleccionado de los links
   del menú principal no funciona, siempre queda Inicio». Y era literal: los
   cuatro del medio —Producto, Cómo funciona, Integraciones, Seguridad— son
   ANCLAS de la portada, así que el `aria-current="page"` escrito a mano en el
   HTML se quedaba pegado en «Inicio» todo el recorrido.

   Lo que hace este bloque es mover esa marca según lo que se está mirando.
   Cuatro cosas que conviene no deshacer:

   1. **El marcado estático del HTML es la verdad sin JavaScript.** Cada
      página trae su `aria-current` escrito (Inicio en la portada, Contacto en
      contacto.html, ninguno en las dos legales, que no están en el menú). Si
      este archivo no corre, esa marca queda y es correcta.
   2. **Se observan TODAS las secciones, no sólo las cuatro del menú.** Cada
      una hereda el ítem de la última ancla que la precede, así que mientras
      se lee «Sin señal» o «Pantalla por pantalla» —que no tienen entrada
      propia— sigue encendido «Cómo funciona». Observar sólo las cuatro dejaba
      encendida la SIGUIENTE, que es peor que no marcar nada.
   3. **La marca nunca retrocede por sorpresa**: la sección activa es la
      primera que sigue cruzando la línea de la cabecera, o sea la que se está
      leyendo. No hay porcentajes de viewport ni umbrales que peleen entre sí.
   4. **Al hacer clic se marca en el acto.** El sitio tiene
      `scroll-behavior: smooth`, y durante ese viaje el observador iría
      encendiendo cada sección intermedia. Por eso el clic fija el ítem y
      calla al observador hasta que el desplazamiento aterriza.
   ========================================================================== */
(function () {
  'use strict';

  var nav = document.querySelector('.nav');
  var cabecera = document.querySelector('.cabecera');
  if (!nav || !('IntersectionObserver' in window)) return;

  var secciones = Array.prototype.slice.call(
    document.querySelectorAll('#principal > section'));
  if (!secciones.length) return;

  var enlaces = Array.prototype.slice.call(nav.querySelectorAll('a'));
  var inicio = null;
  var porAncla = {};
  enlaces.forEach(function (a) {
    var href = a.getAttribute('href') || '';
    var corte = href.indexOf('#');
    if (href === '/' ) { inicio = a; return; }
    // Sólo las anclas de ESTA página: `/#producto`, `#producto`.
    if (corte === -1) return;
    if (corte > 0 && href.slice(0, corte) !== '/') return;
    porAncla[href.slice(corte + 1)] = a;
  });
  if (!inicio) return;

  // Cada sección hereda el ítem de la última ancla que la precede: las que no
  // tienen entrada propia no apagan el menú ni encienden la de más abajo.
  var deLaSeccion = [];
  var actual = inicio;
  var propias = 0;
  secciones.forEach(function (s) {
    var id = s.getAttribute('id');
    if (id && porAncla[id]) { actual = porAncla[id]; propias++; }
    deLaSeccion.push(actual);
  });
  // Las anclas del menú son de la PORTADA. En contacto.html o en las legales
  // ninguna sección responde a ellas, y sin esta salida el marcador les
  // encendería «Inicio» encima del `aria-current` que ya traen escrito.
  if (!propias) return;

  var cruzando = secciones.map(function () { return false; });
  var mudo = 0;

  function marcar(enlace) {
    enlaces.forEach(function (a) {
      if (a === enlace) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
  }

  function calcular() {
    for (var i = 0; i < cruzando.length; i++) {
      if (cruzando[i]) return deLaSeccion[i];
    }
    return deLaSeccion[deLaSeccion.length - 1];
  }

  function repintar() {
    if (Date.now() < mudo) return;
    marcar(calcular());
  }

  var mirador = null;
  function observar() {
    if (mirador) mirador.disconnect();
    // La línea de detección va DEBAJO del `scroll-margin-top` de las secciones
    // (84 px, 104 en pantalla angosta). Si quedara por encima, al saltar a
    // `/#integraciones` la sección de arriba seguiría cruzándola y el menú
    // encendería la ANTERIOR — que es medio arreglo y se ve como el defecto
    // original. Medido: con `+6` fallaba por diez píxeles.
    var alto = (cabecera ? cabecera.offsetHeight : 68) + 28;
    mirador = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        var i = secciones.indexOf(e.target);
        if (i >= 0) cruzando[i] = e.isIntersecting;
      });
      repintar();
    }, { rootMargin: (-alto) + 'px 0px 0px 0px', threshold: 0 });
    secciones.forEach(function (s) { mirador.observe(s); });
  }
  observar();

  // El clic manda mientras dura el desplazamiento suave.
  nav.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a');
    if (!a || enlaces.indexOf(a) === -1) return;
    var href = a.getAttribute('href') || '';
    if (href.indexOf('#') === -1) return;      // Contacto: se va a otra página
    marcar(a);
    mudo = Date.now() + 900;
    setTimeout(function () { mudo = 0; repintar(); }, 950);
  });

  var reloj;
  window.addEventListener('resize', function () {
    clearTimeout(reloj);
    reloj = setTimeout(observar, 200);
  });
})();
