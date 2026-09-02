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
