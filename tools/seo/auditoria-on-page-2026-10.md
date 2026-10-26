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
| Imagen principal (LCP) | `s7-home-hero-700-es.webp`, precargada con `fetchpriority="high"`, con `srcset` y tamaño declarado | — |
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
