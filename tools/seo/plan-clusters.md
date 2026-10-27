# Plan de clusters de contenido — propuesta para aprobar (26 de octubre de 2026)

**Estado: APROBADO el 26 de octubre de 2026 («GO»).** Semana 1 publicada
el mismo día: D1 `/blog/calorias-menu-del-dia/` y D2
`/blog/calorias-de-las-tapas/`, sólo en español (slug en español, sin
copia inglesa: los artículos con `"langs": ["es"]` se publican sólo en el
árbol español, con hreflang `es` + `x-default`, y el árbol inglés no los
enlaza). Decisión del propietario: español primero en todos; twin inglés
sólo donde sirva a una consulta inglesa (B1, C2, E1). Desde el 26-10 el ritmo es **un artículo cada lunes, sin fecha de fin**, publicado por una tarea programada que sigue `tools/seo/RUNBOOK-weekly-post.md` (primera ejecución: lunes 2 de noviembre de 2026, 08:38 hora de Madrid). Siguiente: C1 (2-11), luego C2, B1, A1, D3, C3, E1, E2, A2, B2 en ese orden, uno por semana; después, temas nuevos de investigación propia añadidos al mapa.

Reglas que se aplican a todo lo de abajo: cifras reales (las del código
de la app o de etiquetas fotografiadas con fecha; nada inventado);
nunca nombrar competidores si no hay dato público de tienda con fecha;
«gratis» siempre con los límites a la vista (2 escaneos con IA y 1
registro por voz al día, código de barras y Coach Kal sin límite, sin
tarjeta); sin volúmenes de búsqueda; sin «9 apps probadas».

## Las cinco páginas de dinero

| Cluster | Página de dinero | Frase que debe ganar | Por qué esta y no otra |
|---|---|---|---|
| A | `/` (portada) | app para contar calorías gratis | Es donde aterriza quien busca una app. La frase más dura del mapa, y la que convierte. |
| B | `/features/scan-food/` | contar calorías con foto (gratis) | La única consulta de app con primera página floja (mapa §2 y §7). Es el ángulo propio de Fotocal. |
| C | `/calculadoras/deficit-calorico/` | calculadora de déficit calórico (+ mujer, hombre, cómo calcular, 500 kcal) | Las variantes del autocompletar del 16-10 son muchas y concretas; la página ya las responde; le faltan artículos que la enlacen. |
| D | `/calorias/` (+ tabla) | calorías de los platos españoles | Primera página floja (mapa §3), 43 páginas propias ya publicadas y la app con 218 platos: es donde el sitio tiene ventaja de verdad. |
| E | `/features/weight-loss/` | app para perder peso (contando calorías) | Es la intención final de casi todo el blog; hoy el blog enlaza poco a ella. |

Se dejó fuera `/calculadoras/calorias-diarias/` como página de dinero
propia: va dentro de C (la gente llega al déficit después de saber
cuánto gasta) y ya recibe enlaces de la calculadora de déficit.

## Cluster A · «App para contar calorías gratis» (portada)

Apoyo que ya existe: `/features/`, `/subscription/`, `/faq/`, artículos
`how-to-count-calories-accurately`, `common-calorie-counting-mistakes`,
`track-calories-without-weighing`, `choose-photo-calorie-counter`.

| # | Artículo nuevo | Frase / pregunta que responde | Idioma | Qué lleva |
|---|---|---|---|---|
| A1 | **Cómo saber si una app para contar calorías es gratis de verdad: 7 cosas que mirar en la ficha de Play** | «app para contar calorías gratis», «sin pagar», «totalmente gratis»; PAA «¿Qué contador de calorías es gratuito?» | ES (EN no: la ficha de Play es la misma, pero la consulta española es la que tiene «gratis» en el autocompletar) | Criterios, no marcas: límites diarios, prueba con tarjeta, qué pasa el día 6, exportar datos, borrar cuenta. Fotocal como ejemplo con sus límites a la vista. FAQ de 4 preguntas. |
| A2 | **Cómo hacer un conteo de calorías en España sin pesar nada: el método de una semana** | PAA «¿Cómo hacer un conteo de calorías?»; «contar calorías y macros gratis» | ES | Siete días con platos reales de la app (menú del día, tapas, cena en casa) y cifras de `/calorias/`. Enlaza a D y a C. |

## Cluster B · «Contar calorías con foto» (`/features/scan-food/`)

Apoyo que ya existe: `photo-calorie-apps-accuracy`,
`choose-photo-calorie-counter`, `/ai/`, capturas reales de los sittings 7 y 8.

| # | Artículo nuevo | Frase / pregunta | Idioma | Qué lleva |
|---|---|---|---|---|
| B1 | **Cómo hacer la foto para que la app acierte las calorías: seis reglas y tres errores** | «contar calorías con foto», «app calorías foto precisión»; PAA «¿Cuál es la mejor IA para contar calorías?» (se responde con criterios, sin ranking) | ES + EN (es la consulta donde el inglés sí trae gente que puede instalar la app) | Luz, ángulo, un plato por foto, salsas, la ración editable, cuándo usar el código de barras en vez de la foto. Capturas reales ya aprobadas. FAQ. |
| B2 | **Qué acierta y qué falla una foto: tortilla, paella, cocido y un bocadillo, con el resultado real de la app** | «calorías por foto fiable», «app calorías foto funciona» | ES | Cuatro platos con captura del resultado y la cifra de la base de datos al lado. Donde falle, se dice (regla: «wrong calories are worse than missing dishes»). **Necesita 4 capturas nuevas del propietario** en español. |

## Cluster C · «Déficit calórico» (`/calculadoras/deficit-calorico/`)

Apoyo que ya existe: `calorie-deficit-for-fat-loss`,
`tdee-how-many-calories-you-need`, `understanding-your-basal-metabolic-rate`,
`how-fast-should-you-lose-weight`, `weight-loss-plateaus`,
`the-truth-about-starvation-mode`, `/calculadoras/calorias-diarias/`.

| # | Artículo nuevo | Frase / pregunta | Idioma | Qué lleva |
|---|---|---|---|---|
| C1 | **Déficit calórico de 500 calorías al día: un día de comidas en España, plato por plato** | autocompletar «déficit calórico de 500 calorías por día», «dieta», «para bajar de peso» | ES | Un día real: desayuno, comida, merienda, cena con platos de la app y sus kcal, para una mujer de 2.130 kcal de gasto y un hombre de 2.780 (los ejemplos que ya usa la calculadora). Enlaza a C y D. |
| C2 | **¿Cuántas calorías hay que quemar para perder un kilo? Los 7.700 y lo que significan en días** | PAA «¿Cuántas calorías debo quemar para bajar 1 kilo?» (16-10) | ES + EN | La cifra, de dónde sale, por qué no es exacta, cuánto tarda con 300/500/750 kcal de déficit. Tabla real. Enlaza a C y a `how-fast`. |
| C3 | **Déficit calórico para mujer y para hombre: por qué las cifras cambian y un ejemplo de cada** | autocompletar «déficit calórico mujer», «hombre» | ES | Suelos de 1.200/1.500 kcal (los de la calculadora), masa muscular, ciclo, edad. Sin promesas. |

## Cluster D · «Calorías de los platos españoles» (`/calorias/`)

Apoyo que ya existe: las 41 páginas de plato, la tabla imprimible, los
dos artículos de octubre, `eating-out-without-wrecking-your-diet`,
`portion-control-simple-tricks`.

| # | Artículo nuevo | Frase / pregunta | Idioma | Qué lleva |
|---|---|---|---|---|
| D1 | **Calorías de un menú del día: primero, segundo, pan, bebida y postre, con tres combinaciones reales** | «calorías menú del día», «cuántas calorías tiene un menú del día» | ES | Tres menús montados con platos de la app (lentejas + pollo, ensaladilla + calamares, sopa + albóndigas), barra de pan, caña o vino, arroz con leche o fruta. Cifras de `dishes.json`. |
| D2 | **Cuántas calorías tienen las tapas: caña, bravas, croquetas, pincho de tortilla y jamón, y cómo suman en una tarde** | «calorías tapas», «calorías caña y tapa» | ES | Cada tapa con su cifra de la app, y dos tardes tipo (ligera y de sábado). Enlaza a las páginas de cada plato. |
| D3 | **Calorías del desayuno español: café con leche, tostada con tomate, churros y el zumo** | «calorías desayuno tostada con tomate», «cuántas calorías tiene un café con leche» (autocompletar 16-10) | ES | Cuatro desayunos con cifra, de 180 a 600 kcal, y el cambio que más ahorra. |

## Cluster E · «App para perder peso» (`/features/weight-loss/`)

Apoyo que ya existe: casi todo el blog de peso (`how-to-lose-weight-sustainably`,
`why-crash-diets-fail`, `maintaining-weight-loss`, `why-the-scale-is-not-the-whole-story`).

| # | Artículo nuevo | Frase / pregunta | Idioma | Qué lleva |
|---|---|---|---|---|
| E1 | **Perder 5 kilos: cuánto tarda de verdad con un déficit de 300, 500 o 750 calorías** | «cuánto se tarda en perder 5 kilos», «perder 5 kilos en un mes» | ES + EN | La cuenta honesta (semanas, no días), por qué la primera semana engaña (agua), qué mirar en Progreso. Enlaza a E, C y a `how-fast`. |
| E2 | **Qué hace y qué no hace una app para perder peso** | «app para perder peso gratis»; PAA «¿Cuál es la mejor app para adelgazar?» (criterios, sin ranking) | ES | Lo que una app puede (registrar, enseñar la tendencia, avisar) y lo que no (comer por ti). Fotocal con sus límites. |

## Además de los artículos (mismo commit, menos trabajo)

1. Bloque FAQ (3–4 preguntas, con FAQPage) en los 11 artículos del top-28
   que tienen «Otras preguntas» claras (auditoría §3). ES y EN.
2. Los cinco cambios de H1 de la auditoría §2 (`/features/` y
   `/calculadoras/` primer párrafo; H1 de `best-foods`, `how-fast`,
   `meal-timing`).
3. Enlaces desde cada página de dinero a sus artículos nuevos (sección
   «Para seguir leyendo»), y desde cada artículo a su página de dinero en
   el primer tercio del texto, no sólo al final.
4. Índices de serie: opción (a) o (b) de la auditoría §3, según decida.

## Orden y calendario

| Semana | Artículos | Motivo del orden |
|---|---|---|
| 1 | D1, D2 | Donde hay ventaja real y las cifras ya están en el código. |
| 2 | C1, C2 (+ EN) | Variantes del autocompletar con página de dinero ya lista. |
| 3 | B1 (+ EN), A1 | Consultas con primera página floja. |
| 4 | D3, C3 | Completan D y C. |
| 5 | E1 (+ EN), E2, A2 | Cierran E y A. |
| 6 | B2 (cuando lleguen las 4 capturas) + FAQ de los 11 artículos + H1 | — |

Doce artículos en español, cuatro con twin inglés, 1.200–1.800 palabras
cada uno, FAQ incluida. Efecto medible: no antes de enero de 2027
(auditoría §8). Si hay que recortar, se quitan A2 y E2 primero: son los
que menos se diferencian de lo que ya hay.

## Lo que necesito del propietario

- «Adelante» con el plan tal cual, o con los artículos tachados que no quiera.
- Decisión sobre los índices de serie (a/b).
- Las cuatro capturas de B2, en español, cuando pueda (sin prisa: va en la semana 6).
- El export de Search Console con la columna Motivo (auditoría §5).

## ¿Sigue siendo correcta la estrategia «español primero»? (28 de octubre de 2026, con 90 días de Search Console delante)

Los datos: 1.790 impresiones, 10 clics, 266 consultas. Marca 19 %.
Inglés 78 %. **Español 2,3 %** (41 impresiones en 90 días, nueve
consultas). Y, del 26-10: España es el primer país por impresiones
(276 de 655 en 28 días), es decir, muchas impresiones «españolas» son de
consultas en inglés hechas desde España, no de contenido en español.

**Diagnóstico honesto de por qué el español no aparece.** Las tres
causas, y cuánto pesa cada una:

1. **Edad e indexación (la mayor).** Las páginas españolas que pueden
   ganar algo (`/calorias/`, 41 platos, 4 calculadoras, los dos artículos
   de octubre) tienen entre 12 y 15 días y 80 de ellas siguen
   «descubiertas, sin rastrear». El blog inglés tiene desde septiembre.
   Un periodo de 90 días que termina hoy casi no contiene español
   indexado. Este dato no dice que el español no funcione; dice que aún
   no ha empezado.
2. **El blog español es una traducción (la segunda).** Los 54 artículos
   se escribieron en inglés con sus frases de búsqueda inglesas; la
   versión española lleva slug inglés y H1 traducidos, no las frases que
   se teclean en España. Por eso la única consulta española con volumen
   («pérdida de grasa sostenible», 24) cae en un artículo cuyo H1 no la
   decía. Hoy se han puesto las nueve consultas españolas reales en sus
   páginas, palabra por palabra.
3. **Tiendas y autoridad (la tercera, y la única sin arreglo interno).**
   Para «contador de calorías por foto» la primera página son fichas de
   App Store; para «app contar calorías» Yazio y las tiendas. Ahí el
   español compite contra dominios con años de enlaces, y la web tiene
   cero enlaces externos.

**La respuesta incómoda.** El inglés es donde Google ya confía en el
sitio: tres grupos (contar calorías, alimentos saciantes, estancamiento)
suman más de 150 impresiones con páginas que ni siquiera llevaban la
frase. Costó un día ponerla. El español no ha dado nada todavía y no lo
dará hasta enero por puro calendario. Si la pregunta es «¿dónde está el
tráfico barato ahora?», la respuesta es el inglés, y negarlo sería
contarte lo que quieres oír.

**Lo que haría, en este orden:**

1. **Mantener el español primero en el contenido nuevo**, porque el
   negocio está en España y porque las páginas españolas aún no han
   tenido su oportunidad. Cambiar de rumbo con 15 días de datos sería un
   error mayor que esperar.
2. **No dejar morir el inglés que ya funciona**: lo hecho hoy (frases
   exactas en 14 artículos, el del estancamiento reescrito con FAQ) es
   casi toda la inversión inglesa que hace falta. Una hora al mes para
   revisar qué consultas inglesas nuevas aparecen y ponerlas en su
   página. Nada de artículos nuevos en inglés mientras los españoles no
   estén indexados.
3. **Juzgar el español el 15 de enero de 2027**, no antes: para entonces
   las páginas de octubre llevarán tres meses indexadas y el artículo
   semanal habrá añadido doce. Si en esa fecha «cuántas calorías tiene un
   plato», «calorías tortilla» o «calculadora déficit» no muestran
   impresiones, el problema será de autoridad y la palanca serán los
   enlaces externos, no más contenido.
4. **Lo que no cambia con ninguna estrategia:** las consultas de app
   genéricas las ganan las tiendas. La web gana en preguntas, platos y
   calculadoras, y de ahí manda a la ficha de Play. Ese es el papel de la
   web y conviene asumirlo.
