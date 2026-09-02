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
