# PART 47 — notas técnicas (SEO en español, de la A a la Z)

Fecha: 13 de octubre de 2026. Rama `part47-spanish-seo`, sin fusionar a
`main` hasta que el propietario lo apruebe.

## 1 · Qué se ha construido

| Qué | Dónde | Cómo se mantiene |
|---|---|---|
| Mapa de palabras clave con evidencia | `tools/seo/keyword-map.md` | A mano, tras cada lectura de Search Console |
| Páginas de platos (1 de 20 publicada) | `/calorias/<plato>/` + índice `/calorias/` | `tools/dishes/dishes.json` (texto) + `tools/dishes/app-data.json` (cifras de la app, `sync_from_app.py`) → `python3 tools/gen_dishes.py` |
| Cuatro calculadoras + índice | `/calculadoras/{calorias-diarias,deficit-calorico,imc,macros}/` | `tools/gen_calcs.py` (texto y formularios) + `assets/js/calc.js` (aritmética) |
| Soporte de páginas solo en español | `tools/build_site.py` (`ES_ONLY`) | Prefijos `calorias/` y `calculadoras/`: una sola copia, hreflang es + x-default, una entrada de sitemap |
| `lastmod` por página en el sitemap | `tools/build_site.py` (`page_lastmod`) | Fecha de modificación declarada por la página o, si no, último commit del fuente |
| Enlaces internos | portada (sección solo ES), pie (solo ES), cada artículo del blog (línea «Herramientas», solo ES), páginas de plato ↔ calculadoras ↔ blog | Generadores |
| Árbol del sitio y listado de títulos | `tools/seo/site-tree.md`, `tools/seo/titles-descriptions.md` | `python3 tools/seo/site_tree.py`, `python3 tools/seo/titles.py` tras cada build |
| Merchant listing inválido | `src/subscription/index.html` | Ver §4 |

Orden de regeneración completo:
`gen_blog.py` → `gen_dishes.py` → `gen_calcs.py` → `build_site.py` → `check_site.py` → `seo/site_tree.py` → `seo/titles.py`.

## 2 · Las 21 páginas «no indexadas» de Search Console

No se ha podido abrir Search Console desde aquí, así que esto es lo que la
estructura del sitio predice. El propietario tiene que confirmarlo en
**Páginas → No indexadas → (motivo)** y decir qué motivo lleva cada URL.
Lo normal es que casi todo caiga en estos cubos, y ninguno es un problema:

| Cubo | URLs previstas | Motivo que mostrará Google | Qué hacer |
|---|---|---|---|
| `404.html` en los dos árboles | 2 | «Excluida por la etiqueta noindex» | Nada: es la página de error y está marcada a propósito |
| Las dos redirecciones del blog (`cheat-meals`, `batch-cooking`) ×2 árboles | 4 | «Página con redirección» o «noindex» | Nada: son los antiguos URL que apuntan al artículo fusionado |
| Filtros de categoría del blog `/blog/?cat=…` ×6 ×2 árboles | hasta 12 | «Página duplicada: Google eligió otra canónica» o «Rastreada: actualmente sin indexar» | Nada: la canónica de `/blog/` es `/blog/` y los filtros son la misma página. Si molestan, se cambia el enlace de categoría de las migas a `#` + filtro en JS |
| `/en` sin barra, `/index.html`, `http://` | 2–3 | «Página con redirección» | Nada: GitHub Pages las redirige |
| Hubs de series y FAQ (publicados en septiembre) | 0–4 | «Descubierta: actualmente sin indexar» | Esperar; el sitemap con `lastmod` real y los enlaces nuevos desde portada ayudan |

Si aparece **«Duplicada sin canónica seleccionada por el usuario»** en
páginas `/en/…`, es el par de idiomas: Google ha decidido que la versión
inglesa de una página legal o corta es «la misma» que la española. Es
inofensivo mientras la española esté indexada; si quiere forzarlo, lo que
funciona es más texto distinto en la página, no más etiquetas.

Si aparece algún URL que **no** encaje en la tabla, es el único que
merece una hora de trabajo.

## 3 · Core Web Vitals

Search Console no muestra datos porque CrUX necesita un mínimo de
visitas reales con Chrome y el sitio no lo alcanza (8 clics en 3 meses).
No es un problema de la web: es que no hay muestra. Lo único medible es
en laboratorio. Medido en local, móvil 400 px, red local, tras este
cambio (pesos con fuentes y todo):

| Página | Peso | Peticiones | LCP | CLS |
|---|---|---|---|---|
| `/` | 546 kB | 15 | 296 ms | 0 |
| `/calorias/` | 377 kB | 14 | 96 ms | 0 |
| `/calorias/tortilla-de-patatas/` | 414 kB | 15 | 80 ms | 0 |
| `/calculadoras/` | 377 kB | 14 | 60 ms | 0 |
| `/calculadoras/calorias-diarias/` | 421 kB | 16 | 80 ms | 0 |
| `/calculadoras/deficit-calorico/` | 422 kB | 16 | 72 ms | 0 |
| `/calculadoras/imc/` | 419 kB | 16 | 76 ms | 0 |
| `/calculadoras/macros/` | 420 kB | 16 | 60 ms | 0 |
| `/subscription/` | 522 kB | 15 | 404 ms | 0 |

Las páginas nuevas no cargan imágenes propias (solo logo y favicon), no
tienen desplazamiento lateral y su CLS es 0. En una red móvil real el LCP
sube con la latencia, pero nada de aquí lo empeora. El peso fijo de
~370 kB es la base del sitio (fuentes ~200 kB, CSS, JS); si algún día
hay que recortar, el candidato sigue siendo la fuente itálica (77 kB),
como se dijo en PART 46.

Para tener datos de campo sin esperar a CrUX: PageSpeed Insights sobre
`https://getfotocal.com/calorias/tortilla-de-patatas/` da la medición de
laboratorio de Google en móvil; es lo que hay que mirar una vez
desplegado.

## 4 · El «Merchant listing» inválido

Causa: la página de suscripción declaraba un `Product` con tres
`Offer`. Google lee «Product + Offer» como un artículo a la venta en esa
página (un *merchant listing*) y exige imagen, condiciones de envío,
devoluciones, disponibilidad… Una suscripción dentro de una app no es
eso, y los campos que faltan son el error.

Arreglo: el bloque es ahora un `WebPage` que trata *sobre* la entidad de
la app (`SoftwareApplication`, `@id #app`, declarada en la portada con
sus precios como `offers`). La app sigue teniendo precios estructurados
donde corresponde (en la aplicación, no en un producto físico), y la
página de suscripción deja de parecer una tienda. Tras desplegar:
Search Console → Mejoras → Fichas de comerciante → «Validar corrección».

## 5 · `WebSite` con `SearchAction`: no añadido, a propósito

Se pedía un `WebSite` con `SearchAction`. El `WebSite` existe
(`@id #site`, en la portada). El `SearchAction` **no se ha añadido**
porque declara a Google que el sitio tiene un buscador interno al que
enviar `?q=…`, y getfotocal.com no lo tiene: el blog filtra por
categoría, no busca texto. Un `SearchAction` sin buscador detrás es
markup falso y Google lo desactivó como función visible (el *sitelinks
searchbox*) en 2024. Si algún día se añade un buscador real (una página
`/buscar/?q=` con JS sobre el índice del blog y los platos), entonces sí.

## 6 · El lado inglés

Hecho ya en PART 46 y conservado: cada árbol es canónico de sí mismo,
`x-default` apunta al español, el sitemap lista ambos con alternates, y
las secciones nuevas (platos, calculadoras) solo existen en español, con
hreflang es + x-default y sin copia inglesa que compita.

Lo que **no** se puede hacer desde aquí: ver en qué consultas españolas
posiciona una página inglesa. Para verlo, el propietario, en Search
Console → Rendimiento: filtro País = España, pestaña Páginas, y ordenar
por impresiones. Cualquier URL `/en/…` en esa lista con una consulta en
español es un caso de «el inglés gana al español». Con los datos dados
(top queries en inglés; 253 impresiones en España) lo esperable es que
sean artículos del blog con mucho más texto que su par español. La
respuesta no es quitar el inglés sino que la versión española de ese
artículo diga más (el paquete de revisión en castellano de septiembre
va en esa dirección).

## 7 · Marca: «Fotokal»

La búsqueda de la marca devuelve una app de iPhone llamada **Fotokal**
(id 6761237644 en la App Store) que no es la nuestra, y nuestro paquete
de Android se llama `com.fotokal.app`. No se ha tocado nada; está
apuntado en el mapa de palabras clave (§4) con dos medidas baratas.

## 8 · Lo que necesita al propietario

1. Aprobar la primera página de plato y la lista de 20 (o cambiarla).
2. Comprobar en google.es, en incógnito y desde el móvil, las diez
   consultas marcadas ★ en el mapa de palabras clave.
3. Exportar de Search Console las 21 URL no indexadas con su motivo.
4. Tras fusionar y desplegar: reenviar el sitemap en Search Console
   (lleva sin leerse desde el 23 de julio) y validar la corrección del
   Merchant listing.
