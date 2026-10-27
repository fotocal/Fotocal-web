# Auditoría on-page de todo el sitio — 26 de octubre de 2026

Qué es: el repaso de las 216 páginas publicadas (132 en español, 84 en
inglés) contra la lista de la petición: frase objetivo en H1 y primer
párrafo, estructura H2/H3, profundidad, enlaces internos, hreflang,
canonical y datos estructurados. Incluye las señales de desconfianza
(velocidad, alt, enlaces rotos, indexación), la respuesta a «por qué las
páginas en inglés tienen más impresiones», el estado de http→https y un
calendario honesto.

Qué no es: una medición en vivo. Desde este entorno no se puede abrir
getfotocal.com ni Search Console; todo lo de abajo sale del HTML que se
publica (el mismo que sube el workflow) y de la API de GitHub. Donde
hace falta el navegador o Search Console se dice y se da el paso exacto.

## 1 · Resultado global (208 páginas indexables)

| Comprobación | Resultado | Nota |
|---|---|---|
| Un solo H1 | 208/208 | Las 7 páginas restantes son `noindex` (6 redirecciones y la 404). |
| Canonical | 208/208 | Siempre a la propia URL. |
| hreflang | 160 con `es` + `en` + `x-default`; 48 con `es` + `x-default` | Las 48 son las páginas sólo en español (`/calorias/`, `/calculadoras/`): correcto, no tienen twin. |
| Imágenes sin alt | 0 | — |
| BreadcrumbList | 208/208 | Faltaba en las tres páginas de funciones (foto, código, voz) en ambos idiomas: **añadido hoy**. |
| FAQPage | 63 | 41 platos, portada, funciones, foto, código, voz, adelgazar, IA, calculadoras y, desde hoy, suscripción. **0 de 128 artículos del blog** (ver §3). |
| Article / BlogPosting | 108 blog + 41 platos + 18 índices de serie | — |
| HowTo | 0, a propósito | Google dejó de mostrar resultados enriquecidos HowTo en 2023; añadirlo no aporta nada. |
| Organization / WebSite | portada y páginas de app | — |
| Enlaces internos salientes | mínimo 5 por página; blog con «relacionados» (mínimo 1 entrante, 0 huérfanos) | — |
| Enlaces internos rotos | 0 | `check_site.py` recorre todos los enlaces y assets internos en cada build. |
| Profundidad < 400 palabras | 18 | Los 18 índices de serie del blog (160–335 palabras, sin H2). Ver §3. |

## 2 · Las 20 páginas con más impresiones: huecos concretos

La tabla completa está en `keyword-map.md` §7. Las que tienen hueco real:

| Página | Hueco | Qué haría |
|---|---|---|
| `/features/` | El primer párrafo no dice «contar calorías» (dice «todo lo que hace Fotocal»). | Reescribir la primera frase: «Nueve formas de **contar calorías** en una sola app…». Un cambio de copy, 5 minutos. |
| `/ai/` | La consulta con impresiones (IA + calorías) la responde la página de foto, no esta; esta página habla del coach y es correcto que lo haga. | Dejar el H1. Añadir una FAQ «¿Kal es el que cuenta las calorías de la foto?» que enlace a `/features/scan-food/`, para que quien llega por la IA del escáner no se vaya. |
| `/calculadoras/` | El primer párrafo no dice «calculadora de calorías». | Primera frase: «Cuatro **calculadoras de calorías** que responden…». |
| `/blog/best-foods-for-weight-loss/` | H1 «Alimentos que sacian con menos calorías»: no contiene «adelgazar», que es lo que se busca. | H1: «Los mejores alimentos para adelgazar: los que sacian con menos calorías». Cambia el H1 y el headline del Article; el title ya se reescribió. |
| `/blog/how-fast-should-you-lose-weight/` | H1 «¿A qué velocidad deberías perder peso?»; se busca «cuánto peso se puede perder en una semana». | H1: «¿Cuánto peso se puede perder en una semana? El ritmo que no vuelve». |
| `/blog/does-meal-timing-matter-for-weight-loss/` | H1 no dice «cenar tarde». | H1: «¿Cenar tarde engorda? Lo que de verdad importa del horario». |
| `/features/weight-loss/` | H1 en imperativo («Pierde peso…»); está bien como copy, no contiene la frase. | Lo dejaría: el title y el primer párrafo ya la llevan y el H1 es el gancho de la página. |

Los cambios de H1 son editoriales y tocan el texto que el propietario
aprobó; están listados aquí y **no se han aplicado**. Si se aprueban, van
en el mismo commit que los artículos nuevos.

## 3 · Huecos por grupo

**Blog sin FAQPage (128 páginas).** Ningún artículo tiene bloque de
preguntas. No es un error: un FAQPage sin preguntas reales en la página
es spam. Pero las 20 páginas de arriba tienen «Otras preguntas» claras
(mapa §7) y responderlas en un bloque de 3–4 preguntas al final de cada
artículo es la forma más barata de cubrir las variantes sin escribir
artículos nuevos. Propuesta: bloque FAQ en los 11 artículos del top-28,
en español e inglés, con FAQPage generado por `gen_blog.py`. Es
contenido (unas 120 palabras por pregunta) y entra en el plan de
clusters, no se hace a ciegas.

**Índices de serie (18 páginas, 160–335 palabras, sin H2).** Son listas
de lectura: título, intro de dos frases, los artículos en orden. Google
las tiene como indexables y son de las candidatas a aparecer como «no
indexada». Dos opciones: (a) dejarlas y añadir un H2 por artículo con dos
líneas que digan por qué va en ese orden (unas 250 palabras más por
índice, 18 × 2 idiomas), o (b) marcarlas `noindex` y que sólo sirvan
para navegar. Recomiendo (a) sólo para las series que apoyan un cluster
(calorías, perder peso que no vuelve) y (b) para el resto. Decisión del
propietario.

**Páginas sólo en español sin twin.** Correcto por diseño (`/calorias/` y
`/calculadoras/` son para España). El x-default apunta al español.

**Páginas de app.** Portada, funciones, foto, código, voz, adelgazar, IA,
suscripción: todas con FAQPage, breadcrumbs y hreflang correctos desde hoy.

## 4 · Qué se ha arreglado hoy (commit 53a5696)

- Títulos y descripciones de las 8 páginas siguientes por impresiones.
- BreadcrumbList en las tres páginas de funciones (ambos idiomas).
- FAQPage en `/subscription/` y `/en/subscription/` con las seis
  preguntas que ya estaban en la página.
- Red de seguridad http→https en `main.js` (ver §7).
- `docs/` fuera del artefacto publicado; carpeta `js/` obsoleta borrada.

## 5 · Señales de desconfianza

### Velocidad

Lo que carga una página (portada en español, cifras del repositorio;
«gz» es lo que viaja por la red, que es lo que cuenta):

| Recurso | Tamaño | gz |
|---|---|---|
| HTML de la portada | ~70 KB | ~15 KB |
| `site.css` + `home.css` + `fonts.css` | 77 + 23 + 3,5 KB | ~27 KB |
| `i18n.js` + `layout.js` + `main.js` | 47 + 42 + 20 KB | ~36 KB |
| Fuentes (self-hosted, woff2, `font-display: swap`) | 8 archivos, 354 KB en total; una página normal carga 2–4 (de 28 a 78 KB cada uno) | — |
| Imagen principal (LCP) | `app-home-hero-700-es.webp`, precargada con `fetchpriority="high"`, con `srcset` y tamaño declarado | — |
| Resto de capturas | `loading="lazy"`, `decoding="async"`, anchura y altura declaradas | — |
| Terceros | **0** scripts, 0 fuentes externas, 0 iframes | — |

Lo que no se puede medir desde aquí: el LCP real en un móvil de gama
media en España. Paso para el propietario (2 minutos): abrir
pagespeed.web.dev en el móvil y pegar tres URL: `/`,
`/calorias/tortilla-de-patatas/` y `/blog/how-fast-should-you-lose-weight/`.
Lo que yo esperaría: móvil 85–95, con la fuente Fraunces (dos archivos de
64 y 78 KB) como único aviso. Si LCP sale por encima de 2,5 s, lo primero
que recortaría es la Fraunces en cursiva (78 KB) y la precarga del hero a
1080 px en pantallas pequeñas.

Lo que **no** hay que hacer: comprimir más las capturas (ya están en
webp y ya se quejó el propietario de capturas borrosas) ni meter un CDN
de terceros por velocidad.

### Alt

0 imágenes sin alt en 208 páginas. El alt de cada captura está en el
idioma de la página (regla del propietario) y describe la pantalla.

### Enlaces rotos

- Internos: 0 (comprobación en cada build).
- Externos: el sitio sólo enlaza a 4 URL de fuera: la ficha de Play,
  dos páginas de ayuda de Google (suscripciones y reembolsos) y la AEPD
  (en la política de privacidad). Desde este entorno no se pueden abrir;
  el propietario debería tocar las cuatro una vez. Están en
  `/subscription/`, `/privacy-policy/` y el pie.

### Indexación: las 73 páginas «no indexadas»

Sin el export de Search Console no se puede decir página por página; sí
se puede decir qué debería haber en esa lista y qué no:

| Grupo | Páginas | ¿Problema? |
|---|---|---|
| Nuevas del 13–16 de octubre: 41 platos + tabla + índice `/calorias/`, 5 de `/calculadoras/`, 2 artículos nuevos × 2 idiomas | ≈ 52 | **No, todavía.** Tienen 10–13 días. Lo normal son 2–8 semanas. Si el 1 de diciembre siguen fuera, entonces sí. |
| Índices de serie del blog (18) | 18 | **A medias.** Son finos (§3). Si la razón es «Rastreada: actualmente sin indexar», Google las ha visto y no le parecen suficientes: aplicar (a) o (b) de §3. |
| Las 6 redirecciones (`/features/recipe/`, dos artículos retirados, × 2) | 6 | **No.** Son `noindex` y no están en el sitemap. Si aparecen, será como «Página con redirección», que es lo esperado. |
| Cualquier artículo del blog anterior a octubre | debería ser 0 | **Sí, si aparece alguno.** Si un artículo de septiembre sale como «Rastreada: actualmente sin indexar», es señal de calidad o de duplicado y hay que mirarlo uno a uno. |
| «Duplicada: Google eligió otra canónica» | debería ser 0 | **Sí.** Sería que Google junta `/x/` y `/en/x/`. El hreflang y el canonical son correctos; si pasa, hay que ver qué URL eligió. |

Suma de lo esperado: 52 + 18 + 6 = 76, que cuadra con 73. Lo que
necesito del propietario para cerrar esto: en Search Console → Páginas →
«No indexadas», exportar la tabla con la columna **Motivo** (botón
Exportar arriba a la derecha) y pasármela. Con eso digo cuál es cuál.

Mientras tanto, lo que sí se puede hacer y acelera: en Search Console →
Sitemaps, reenviar `https://getfotocal.com/sitemap.xml` (208 URL), y en
Inspección de URL pedir indexación a mano de `/calorias/`,
`/calculadoras/`, `/calorias/tortilla-de-patatas/` y
`/calculadoras/deficit-calorico/`. Son las cuatro que más importan y el
límite diario de peticiones a mano lo permite.

## 6 · Por qué las páginas en inglés tienen más impresiones que las españolas

Las cinco causas, por orden de peso. Ninguna es un fallo técnico.

1. **El blog se escribió en inglés y se tradujo.** Las URL españolas
   llevan el slug inglés (`/blog/does-meal-timing-matter-for-weight-loss/`)
   y los H1 traducidos no siempre coinciden con cómo se busca en España
   («¿A qué velocidad deberías perder peso?» frente a «cuánto peso se
   puede perder en una semana»). Google encuentra la página inglesa con
   más facilidad porque el texto y la consulta encajan palabra por palabra.
2. **Las consultas en inglés son globales.** «calorie deficit for fat
   loss» se busca desde Estados Unidos, Reino Unido, India, Filipinas,
   Nigeria. Las impresiones suman todos los países. «déficit calórico
   para perder grasa» se busca en España y Latinoamérica, y en
   Latinoamérica la primera página son medios locales (semana.com,
   eluniverso, lagaceta: lo que salió hoy en las búsquedas).
3. **Las páginas españolas de dinero son nuevas.** `/calorias/` y
   `/calculadoras/` tienen dos semanas; las inglesas con impresiones son
   artículos de septiembre. No hay diferencia de edad entre los dos
   árboles (los dos se publicaron el 10-09-2026), pero sí entre el tipo
   de página que lleva impresiones en cada idioma.
4. **El x-default apunta al español**, así que para un buscador sin
   idioma claro Google enseña la española. Eso favorece al español, no
   al inglés: no es la causa, y no hay que tocarlo.
5. **Volumen.** Hay más gente buscando sobre calorías en inglés que en
   español. Es así y no cambia.

Lo que importa de verdad: **las impresiones inglesas valen poco para
Fotocal** si vienen de países donde la app no se vende. Comprobación
(1 minuto): Search Console → Rendimiento → pestaña Países. Si España no
está entre los tres primeros de las impresiones inglesas, esas
impresiones no son clientes y el plan debe seguir siendo español
primero, inglés sólo donde tenga sentido (ya es el criterio del plan de
clusters).

## 7 · http → https

- Lo que hace GitHub Pages: con «Enforce HTTPS» activado en
  Settings → Pages, toda petición `http://getfotocal.com/…` recibe un
  301 a `https://` antes de servir nada. Es la solución buena y la única
  real: una página no puede redirigirse a sí misma antes de cargar.
- Lo que no se ha podido comprobar desde aquí: ni el ajuste (la API de
  Pages está bloqueada para esta sesión) ni la respuesta en vivo (el
  dominio no resuelve desde este entorno).
- Lo que se ha hecho: una red de seguridad en `main.js` (commit 53a5696):
  si una página de getfotocal.com llega a cargar por `http:`, se
  reemplaza por la misma URL en `https:` antes de pintar nada más. Cubre
  el caso de que el ajuste esté apagado, pero el 301 de Pages sigue
  siendo lo que hay que tener.
- Qué debe comprobar el propietario (2 minutos): (1) Settings → Pages →
  «Enforce HTTPS» marcado; (2) en el móvil, escribir
  `http://getfotocal.com/account-deletion/` y ver que la barra pasa a
  `https://` con el candado. Si quiere la prueba exacta, desde un
  ordenador: `curl -I http://getfotocal.com/account-deletion/` debe
  devolver `301` y `Location: https://getfotocal.com/account-deletion/`.
- La impresión en `http://…/account-deletion/` que vio en Search Console
  es de la propiedad de dominio, que recoge ambos esquemas; mientras el
  301 esté, Google acaba consolidando en https. Si en un mes sigue
  habiendo impresiones http, es que el 301 no está.

## 8 · Calendario honesto

Con un dominio de seis semanas de vida real (los dos árboles se
publicaron el 10-09), 655 impresiones y 6 clics en 28 días:

| Qué | Cuándo se puede esperar | Seguridad |
|---|---|---|
| Que las 52 páginas nuevas estén indexadas | 2–8 semanas desde el 16-10, antes si se reenvía el sitemap | Alta |
| Primera página en consultas de marca («fotocal», «fotocal app») | Ya, si no lo está; comprobar «fotokal» (mapa §4) | Alta |
| Primera página en cola larga de platos («calorías tortilla francesa 2 huevos», «un tercio de cerveza calorías») | 2–4 meses para algunas; no todas | Media |
| Primera página en «calculadora de déficit calórico» | 4–8 meses, y sólo si los artículos del cluster enlazan a la calculadora | Baja-media |
| Primera página en «contar calorías con foto» / «app para contar calorías con foto gratis» | 3–6 meses: la primera página es floja (fichas de tienda y un listicle) | Media |
| Primera página en «app para contar calorías gratis» / «contador de calorías» | 12 meses o más, y no está garantizado: Yazio, las tiendas y calculadoras con años de enlaces | Baja |
| Que los clics suban de 6 a decenas al mes | 3 meses si se publica el plan de clusters y se corrigen los H1 de §2 | Media |

Lo que mueve el calendario más que nada de lo de arriba: enlaces desde
fuera (una reseña honesta en un medio español, un foro, una
nutricionista que enlace la tabla) y las búsquedas de marca. Ninguna de
las dos se puede fabricar desde el código.


## 9 · Actualización del 26 de octubre (tarde): decisiones del propietario y lo hecho

**Datos nuevos de Search Console (del propietario).** España es el primer
país con diferencia: 276 de 655 impresiones y 3 de 6 clics; los países de
habla hispana suman cerca del 56 %. Las impresiones inglesas son sobre todo
Estados Unidos (94) y Reino Unido (19): no son clientes. Decisión: español
primero, inglés sólo donde sirva. Se cumple en todo lo de abajo.

**No indexadas: 99, no 73.** 80 «Descubierta: actualmente sin indexar»,
7 «Rastreada: actualmente sin indexar», 10 «Página alternativa con
etiqueta canónica adecuada», 2 «Página con redirección». No hay ninguna
fila de «Google eligió otra canónica»: lo que preocupaba en §5 no ocurre.
Las 10 «alternativa con canónica adecuada» son normales (son las dos
versiones de idioma que Google agrupa); las 2 redirecciones también.
El problema real son las 80 descubiertas y no rastreadas.

### Qué sube de verdad la prioridad de rastreo (y qué no)

Google rastrea antes lo que más enlaces recibe de páginas que ya rastrea
a menudo, y deja para después lo que sólo cuelga de un sitemap. Lo que
funciona, en orden de efecto, y su estado:

1. **Enlaces desde las páginas más fuertes.** La portada enlaza ahora
   directamente a los 12 platos más buscados con su cifra (tira «Los más
   buscados», commit 1839b58); el pie ya enlazaba a `/calorias/` y
   `/calculadoras/` desde las 132 páginas españolas; los 54 artículos
   llevan la línea de herramientas. Los dos artículos nuevos enlazan a 20
   páginas de plato en el cuerpo del texto. **Hecho.**
2. **Menos URL compitiendo por el mismo presupuesto.** Los 6 índices de
   serie finos pasan a `noindex` y salen del sitemap (de 208 a 198 URL).
   **Hecho.**
3. **Contenido nuevo que enlaza al antiguo, publicado con regularidad.**
   Dos artículos por semana del plan de clusters, cada uno con 10–20
   enlaces a platos, calculadoras y artículos. **Empezado** (semana 1
   publicada).
4. **`lastmod` real en el sitemap.** Ya lo era (fecha del último cambio de
   contenido de cada página, no la de hoy en todas).
5. **Enlaces desde fuera.** Lo único que no se puede hacer desde el código,
   y lo que más pesa.

Lo que **no** funciona y por eso no se ha hecho: `<priority>` y
`<changefreq>` en el sitemap (Google los ignora desde hace años; se dejan
porque no molestan), reenviar el sitemap cada día, IndexNow (sólo Bing),
enlaces internos escondidos o un bloque de 200 enlaces en el pie.

Lo que sí acelera y es tuyo: Inspección de URL → «Solicitar indexación»
para `/calorias/`, `/calculadoras/`, `/calorias/tortilla-de-patatas/` y
`/calculadoras/deficit-calorico/`, una vez. Opcional; no lo pido.

### Lo hecho hoy sobre esta auditoría

| Punto | Estado |
|---|---|
| Los cinco huecos de H1 / primer párrafo (§2) | **Hechos** (commit 1839b58): `/features/` y `/calculadoras/` primer párrafo; H1 de `best-foods`, `how-fast` y `meal-timing`; `/ai/` con la FAQ que manda la consulta de «IA que cuenta calorías» a la página de foto. |
| FAQ en el blog (§3) | **10 artículos** del top-28 con 3 preguntas reales cada uno, en los dos idiomas, con FAQPage: best-foods, how-fast, sustainably, calories-or-quality, added-sugar, meal-timing, calorie-deficit, exercise, night-eating, protein-breakfast. Ninguna pregunta inventada para rellenar: todas salen de «Otras preguntas», del autocompletar o de Search Console. |
| Índices de serie (§3) | Decidido hub por hub, ver abajo. |
| Tira de platos en portada | Hecha. |
| http→https | El propietario activó «Enforce HTTPS» y comprobó el 301; la red de seguridad de `main.js` se retiró. |

### Índices de serie: qué se hizo con cada uno y por qué

Con contenido propio (intro de 150 palabras y una línea por artículo que
dice por qué va en ese orden; siguen indexados):

- **Las calorías, desde cero** (9 artículos): es la serie que sostiene el
  cluster del déficit (C) y enlaza a las dos calculadoras.
- **Perder peso que no vuelve** (5): sostiene el cluster de perder peso (E).
- **Comer bien un día normal** (7 + los dos artículos nuevos): sostiene
  el cluster de los platos (D) y enlaza a `/calorias/`.

Sólo navegación (`noindex, follow`, fuera del sitemap; siguen enlazados y
accesibles): **Las dietas de moda**, **Macros**, **Más allá de los macros**,
**Planificar la semana**, **Apetito, ánimo y hábito**, **Movimiento, sueño
y agua**. Motivo: ninguna apoya una página de dinero, y cada una era una
lista de 160–335 palabras compitiendo por rastreo con los 41 platos. Si
alguna de esas series gana un cluster más adelante, se le da contenido y
se vuelve a indexar: es una línea en `series.json`.

## 10 · Barrido final on-page (27 de octubre de 2026)

Todo lo de abajo está medido, no supuesto. Velocidad: Lighthouse 12.8 en
móvil (4G lenta simulada, CPU ×4) y un segundo paso con Chromium
emulando un Pixel 7 que recorre la página entera para contar lo que de
verdad se descarga. Las dos medidas se hicieron contra el sitio servido en
local **sin compresión**; en GitHub Pages el texto viaja comprimido, así
que los pesos reales son menores en los dos casos y la comparación
antes/después es la que vale.

### Velocidad, antes → después

| Página | Lighthouse | FCP | LCP | TBT | CLS | Peso (LH) | Peticiones |
|---|---|---|---|---|---|---|---|
| `/` | 82 → **88** | 3,0 → 2,5 s | 3,9 → 3,4 s | 96 → 34 ms | 0,005 → 0,001 | 553 → 459 KB | 17 → 13 |
| `/calorias/` | 87 → **95** | 3,2 → 1,8 s | 3,2 → 2,7 s | 0 → 32 ms | 0,001 → 0 | 395 → 301 KB | 15 → 8 |
| `/calculadoras/` | 89 → **95** | 3,0 → 1,8 s | 3,0 → 2,7 s | 0 → 6 ms | 0,019 → 0 | 381 → 288 KB | 15 → 8 |
| `/blog/how-fast-should-you-lose-weight/` | 88 → **96** | 2,7 → 1,7 s | 3,3 → 2,7 s | 6 → 0 ms | 0 → 0 | 411 → 320 KB | 16 → 10 |

Página completa recorrida hasta el final (todas las imágenes perezosas
cargadas), Pixel 7: `/` 1.164 KB y 25 peticiones → **889 KB y 21**;
`/calorias/` 402 KB y 14 → **308 KB y 7**; `/calculadoras/` 388 y 14 →
**294 y 7**; el artículo 418 y 15 → **326 y 9**. INP de laboratorio (un
toque y dos desplazamientos): portada 64–72 ms, el resto 16–32 ms.

Qué se cambió para eso (todo en el build, `tools/build_site.py`):

- **Una hoja de estilos por página en vez de 3 a 6**, minificada
  (`tools/bundle_assets.py` → `assets/dist/`). Un script por página en vez
  de tres, minificado y `defer`. Recursos que bloqueaban el pintado: de 3–9
  a 1.
- **Fuentes:** el `@font-face` va incrustado en el HTML y las dos fuentes
  del primer pantallazo se precargan. Las ocho se quedan: la cursiva se
  usa en los titulares (`<em class="accent">`) y cada archivo solo baja si
  la página usa ese rango.
- **AVIF con WebP de respaldo** (`tools/gen_avif.py`, `<picture>` añadido
  por el build) en las 152 capturas: a calidad 60 el AVIF pesa entre el
  55 % y el 70 % del WebP. Recomprimir el WebP en sí solo ahorraba un
  4–9 % y no se hizo: no compensa el riesgo de perder nitidez en capturas
  que ya costó conseguir.
- **Portada:** el héroe estaba dentro de una animación de aparición que el
  JS primero ocultaba y luego mostraba; Chrome contaba la segunda pintura
  como LCP (1,1 s de retraso medidos). Ahora lo que ya está en pantalla se
  muestra en la misma tarea en que arranca el JS; la animación sigue para
  lo que está por debajo.
- **Navegación y pie pre-renderizados en el HTML** (`tools/render_chrome.mjs`
  → `tools/chrome/`): 47–49 enlaces por página que antes solo existían
  cuando se ejecutaba el JS. El JS ya no vuelve a pintar la navegación.
- Lo que no se puede tocar: GitHub Pages sirve con `max-age=600` y no
  admite cabeceras propias; la versión en la URL (`?v=hash`) es lo único
  que hay.

### Imágenes (236 etiquetas en 217 páginas, los dos idiomas)

| Comprobación | Resultado |
|---|---|
| `alt` ausente | 0 |
| `alt=""` deliberado | 112, todas ilustraciones de portada de artículo (SVG decorativo) |
| `alt` en idioma distinto al de la página | 0 (heurística de palabras) |
| `width` y `height` | 236 de 236 |
| Carga | la imagen superior de cada página `fetchpriority="high"` (128), el resto `loading="lazy"` (108) |
| Nombres de archivo | las 256 capturas con código de sesión (`s7-scan-690-es`) renombradas a palabras (`app-scan-690-es`); el resto ya lo eran |
| Imagen servida mayor que la mostrada | 0 (ningún archivo supera el mayor candidato de su `srcset`) |
| Formato moderno | AVIF + WebP en las 20 páginas con capturas; portadas del blog en SVG; `logo.png` de 250 a 41 KB |
| Archivos sin usar | 2 portadas de artículos retirados, borradas |
| `og:image` | antes **2 tarjetas para 198 páginas** (una por idioma); ahora **198 tarjetas, una por página y por idioma** (`tools/gen_og.mjs`, 1.200×630 JPEG, ~41 KB, con el H1 real y, en los platos, las kcal por ración). Solo comparten tarjeta las 6 redirecciones `noindex`. |

### Barrido de las 198 páginas indexables

| Comprobación | Resultado |
|---|---|
| Sitemap | 198 URL, ninguna `noindex` dentro, ninguna indexable fuera, todas construidas |
| Páginas sin ningún enlace HTML entrante | **4 antes** (`/features/` y `/faq/` en los dos idiomas: solo las enlazaba la navegación por JS) → **0** |
| Enlaces internos rotos | 0 |
| Cadenas de redirección | 0 (las 6 redirecciones apuntan a página final) |
| Salto de nivel en encabezados (h2 → h4) | 0 |
| Más o menos de un H1 | 0 |
| Contenido fino (< 350 palabras en `<main>`) | 0 indexables (los 12 índices finos ya son `noindex`) |
| JSON-LD | los 500+ bloques parsean; Article con headline, fecha, imagen y autor; FAQPage con pregunta y respuesta; sin marcadores sin resolver |
| Idioma mezclado | 0 páginas con señal de inglés en español o al revés; `<html lang>` correcto en 218 |
| Canonical / hreflang | sin cambios: correctos (apartado 1) |

### Qué queda, dicho sin adornos

Dentro del sitio queda poco que mueva posiciones. Lo que puede moverlas,
por orden de peso real:

1. **Enlaces desde otras webs.** Es el factor que falta y no se puede
   fabricar desde el código. Dos competidores de «contador de calorías»
   llevan años acumulándolos; Fotocal tiene cero. Sin ellos, lo
   razonable es primera página en cola larga (platos, tapas, menú del día,
   variantes del déficit) y nada garantizado en «app para contar
   calorías gratis». Dónde se consiguen de verdad: dietistas y blogs de
   nutrición españoles que enlacen la tabla o un artículo con cifras
   (hay que pedirlo uno a uno), una reseña honesta en un medio de apps,
   directorios de apps, la ficha de Play (enlace sin autoridad pero con
   tráfico), y que alguien cite el artículo del menú del día en un foro.
2. **Búsquedas de marca y tráfico directo.** Crecen con la app, no con la
   web. Cada usuario que busca «fotocal» enseña a Google que la marca existe.
3. **Tiempo.** Las 52 páginas de octubre tardan de 2 a 8 semanas en
   indexarse y de 2 a 4 meses en asentarse. Nada de lo publicado en
   octubre se puede juzgar antes de enero.
4. **Constancia.** El artículo semanal ya está programado; es lo único
   on-page que sigue sumando solo.

Lo que no va a pasar por mucho on-page que se haga: adelantar a las
tiendas de aplicaciones y a los sitios con miles de enlaces en consultas
de app genéricas. Esa es la parte que necesita enlaces de fuera, y es
honesto decirlo ahora y no en tres meses.

## 11 · Ronda completa de auditoría (28 de octubre de 2026)

Motivo: el propietario encontró en la web publicada un enlace «FAQ» sin
texto, en el desplegable «Nosotros» y en el pie «Empresa», en los dos
idiomas. Tercera vez que un defecto lo encuentra él. Esta ronda busca el
resto, los arregla y **fija cada uno con una comprobación que falla si
vuelve** (`tools/check_pins.py`, ejecutado por `tools/check_site.py`;
`tools/check_mobile.mjs`, `tools/check_calcs.mjs` y
`tools/check_contact.mjs` para lo que necesita navegador).

### Defectos encontrados, gravedad y estado

| # | Defecto | Gravedad | Causa | Estado | Pin |
|---|---|---|---|---|---|
| 1 | Enlace «FAQ» vacío en navegación y pie, 630 enlaces vacíos en 217 páginas | **Alta** (enlace sin texto en todas las páginas, para Google y para lectores de pantalla) | La clave `nav.faq` no existía en el diccionario `i18n.js`; `t()` devuelve «» para una clave que falta. El menú llevaba así desde que se añadió FAQ; el pre-render del 27-10 lo fijó en el HTML en vez de dejarlo sólo en el JS. Además, el script de captura volvió a capturar el nav vacío porque `layout.js` conserva un nav ya pre-renderizado. | Arreglado: clave añadida en los dos idiomas; `render_chrome.mjs` sirve la página sin nav para capturar siempre un render fresco. | Pin 1 (ningún `<a>` sin texto, aria-label o imagen con alt) y pin 9 (toda clave que pida el JS existe en los dos diccionarios). |
| 2 | Selector de idioma pre-renderizado apuntaba a la portada en todas las páginas (capturado desde `/`) | Media (para rastreadores; el JS lo corregía al cargar) | El nav capturado es el de la portada. | Arreglado: el build reescribe los dos `href` con los `hreflang` de cada página; las páginas sólo en español mandan a `/en/`. | Pin 10. |
| 3 | Salto de nivel de encabezado en todas las páginas: `h2` → `h5` | Media | Los títulos de columna del pie eran `<h5>`; antes sólo existían en el DOM renderizado por JS, ahora en el HTML. | Arreglado: son `<p class="footer-h">`. | Pin 5 (un H1, sin saltos). |
| 4 | FAQPage de `/features/voice-logging/` declaraba dos preguntas que no están en la página («¿Qué idiomas entiende?» y otra) | Media (schema que no coincide con el contenido) | Dos de los cuatro acordeones muestran una frase de ejemplo, no la pregunta. | Arreglado: el schema lista sólo las dos preguntas visibles. | Pin 8 (cada pregunta del FAQPage aparece en el texto de la página). |
| 5 | Migas de pan de 22 px de alto en móvil (blog, platos, calculadoras) | Baja (WCAG pide 24 px) | Enlace en línea sin caja. | Arreglado: `inline-block` con relleno. | `check_mobile.mjs`. |
| 6 | Enlaces «Leer →» y «Ver los planes →» de 23 px | Baja | Idem. | Arreglado. | `check_mobile.mjs`. |
| 7 | `pages.css` (7,5 KB) no lo cargaba ninguna página | Baja (archivo muerto; una regla del honeypot que creí activa vivía ahí) | Hoja antigua. | Borrada. La regla real del honeypot está en `features.css` y oculta el señuelo. | Pin 13 (ningún CSS/JS sin cargar). |
| 8 | Páginas huérfanas `/features/` y `/faq/` (ya arreglado el 27-10) | — | — | — | Comprobación de entrantes en el barrido. |

Lo que se buscó y **no** apareció (y queda fijado para que no aparezca):
texto de marcador («TODO», «lorem», `{{`, `undefined`, `NaN`); anchors
«aquí»/«click here»; enlaces del cuerpo a redirecciones; imágenes sin
`alt`, sin dimensiones o sin archivo; `og:image` compartida o ausente;
precios distintos de 6,99 €, 34,99 € y su equivalente 2,92 €/mes; límites
del plan gratis distintos de 2 escaneos y 1 voz al día; otra cifra que no
sea 7.700 kcal por kilo; recuento de platos distinto del de la app
(218); inglés en páginas españolas o al revés (heurística, aviso);
desbordamiento horizontal a 360 px en 25 plantillas. Las cuatro
calculadoras dan la respuesta correcta en 16 valores comprobados contra
Mifflin-St Jeor, 7.700 kcal/kg y 4/4/9 kcal/g; el formulario de contacto
envía el payload correcto a Web3Forms (interceptado, no enviado) en los
dos idiomas y el honeypot bloquea sin enviar.

### Lo que no se puede comprobar desde aquí

El HTML publicado no se puede descargar desde este entorno (el dominio
no resuelve), así que «leer la página desplegada» se hace sobre el HTML
que sube el workflow, que es byte a byte el mismo. La prueba final sigue
siendo el móvil del propietario.
