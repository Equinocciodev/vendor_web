/* Vendoo — la analítica del sitio: Google Analytics 4 a través de Firebase.

   Decisión del dueño (2-sep-2026), y es la ÚNICA excepción a la regla de que
   el sitio no le pide un byte a un tercero. Hasta ese día la página no
   llamaba a nadie; desde ese día mide visitas. Sólo eso: no hay publicidad,
   no hay remarketing, y los hosts de anuncios que la guía de CSP de Google
   recomienda «por si acaso» (doubleclick, googlesyndication) NO están
   abiertos en la política de contenido, a propósito.

   Es un módulo ES (`<script type="module">`), que es como lo entrega la
   consola de Firebase para un sitio sin empaquetador, con dos diferencias
   sobre el fragmento de la consola:

   1. LOS `import` SON DINÁMICOS Y ESPERAN AL EVENTO `load`. Con `import`
      estáticos el navegador baja los ~100 KB del SDK antes de
      `DOMContentLoaded`, compitiendo con la hoja de estilo y las fuentes que
      pintan el titular. Una visita se cuenta igual medio segundo después;
      el titular no puede esperar. Por lo mismo el `<head>` lleva sólo
      `dns-prefetch` a gstatic y no `preconnect`.

   2. LAS SEÑALES DE GOOGLE VAN APAGADAS (`allow_google_signals` y
      `allow_ad_personalization_signals`). Encendidas, gtag manda además un
      hit a `stats.g.doubleclick.net` y otro a `www.google.com` —los de
      publicidad—, que la CSP bloquea y que dejaban tres errores en la
      consola de cada visita (medido con Lighthouse el 2-sep-2026). Apagarlas
      es decir en el código lo que ya decía la CSP.

   Los dos `import` van directo a gstatic, con la versión FIJADA. Subirla es
   cambiar `VERSION_SDK` y volver a pasar por el navegador sin interfaz
   mirando la consola, porque cada host que el SDK necesite tiene que estar
   en la CSP de las cinco páginas —el `<meta http-equiv="Content-Security-
   Policy">`— y en `_headers`. Lo que hoy pide, medido contra el SDK 12.18.0:

     script-src   www.gstatic.com (estos módulos) y www.googletagmanager.com
                  (el gtag.js que firebase-analytics carga solo)
     connect-src  *.google-analytics.com, analytics.google.com y
                  *.analytics.google.com (los hits: el apex NO lo cubre el
                  comodín, y sin él el hit de la visita se bloqueaba),
                  www.googletagmanager.com, firebase.googleapis.com (la
                  configuración web de la app) y
                  firebaseinstallations.googleapis.com (el registro de la
                  instalación)
     img-src      *.google-analytics.com y www.googletagmanager.com (el
                  píxel de respaldo cuando no hay `sendBeacon`)

   Este archivo se carga en las cinco páginas, o en ninguna:
   `tool/verificar.py` se queja si a alguna le falta. Y la política de
   privacidad lo dice (cláusula 6, «El sitio web»). Si esto se apaga, hay que
   sacar las tres cosas: el script, los hosts de la CSP y la frase. */

const VERSION_SDK = '12.18.0';

const firebaseConfig = {
  apiKey: 'AIzaSyAs0XL0drl89-W9qA18abvCVdsjDVlmubc',
  authDomain: 'guuaoapp.firebaseapp.com',
  projectId: 'guuaoapp',
  storageBucket: 'guuaoapp.firebasestorage.app',
  messagingSenderId: '1001699259851',
  appId: '1:1001699259851:web:e5fc0d5adf707498c0f24e',
  measurementId: 'G-RXQZZXYGJ2'
};

async function medir() {
  const [{ initializeApp }, { initializeAnalytics }] = await Promise.all([
    import(`https://www.gstatic.com/firebasejs/${VERSION_SDK}/firebase-app.js`),
    import(`https://www.gstatic.com/firebasejs/${VERSION_SDK}/firebase-analytics.js`)
  ]);
  const app = initializeApp(firebaseConfig);
  initializeAnalytics(app, {
    config: {
      allow_google_signals: false,
      allow_ad_personalization_signals: false
    }
  });
}

function arrancar() {
  // Un fallo de red hacia Google no es un fallo de la página: se calla.
  medir().catch(function () { /* sin red hacia Google: no se mide y listo */ });
}

if (document.readyState === 'complete') {
  arrancar();
} else {
  window.addEventListener('load', arrancar, { once: true });
}
