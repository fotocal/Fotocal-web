# Plan de publicación en español — 3 meses (octubre 2026 → enero 2027)

Qué es: el orden en que se publican las páginas nuevas y qué se mira
cada semana. Lo que no es: una promesa de tráfico. Con 8 clics en tres
meses, cualquier cifra de visitas sería inventada.

## Tiempos honestos

- Una página nueva en un dominio con esta autoridad tarda **de 2 a 8
  semanas** en indexarse, y **de 2 a 4 meses** en encontrar su posición
  estable. Nada publicado en noviembre dirá nada fiable antes de febrero.
- El sitemap no se lee desde el 23 de julio. Primer paso tras fusionar:
  reenviarlo en Search Console y pedir indexación a mano de `/calorias/`,
  `/calculadoras/` y la portada. Sin eso, el calendario de abajo se
  retrasa un mes entero.
- Publicar 20 platos de golpe no es mejor que 5 por semana: a Google le
  da igual y a quien escribe le permite revisar la cifra y el texto de
  cada uno. Y cada plato son 20–40 minutos de texto bien hecho, no un
  minuto de generador.

## Estado al cierre del 13 de octubre

Los 20 platos, las 4 calculadoras y los dos índices están **publicados en
main**. Lo que queda de este plan es verificación, lectura de datos y la
segunda tanda; no hay nada pendiente de escribir de la primera lista.

## Mes 1 · octubre–noviembre: que Google lo vea

| Semana | Qué | Quién |
|---|---|---|
| 1 | Reenviar el sitemap en Search Console (no se lee desde el 23 de julio). Pedir indexación a mano de la portada, `/calorias/`, `/calculadoras/` y tres platos. Validar la corrección del Merchant listing. | Propietario (20 min) |
| 1 | Comprobar en google.es, en incógnito y desde el móvil, las diez consultas ★ del mapa; anotar «Otras preguntas» para añadirlas a las FAQ de cada plato. | Propietario (30 min) |
| 2 | Añadir a la app los platos con demanda que no tiene (lista en el informe de PART 47 y en el mapa §5.2), con su ración. | App |
| 3 | Revisión del castellano de los 20 platos de una sentada; corregir en `dishes.json` y regenerar. | Lector nativo + Claude |
| 4 | Search Console → Páginas: confirmar que `/calorias/…` y `/calculadoras/…` pasan de «Descubierta» a «Indexada». Si no, volver a pedir indexación. | Propietario |

## Mes 2 · noviembre–diciembre: segunda tanda

| Semana | Qué |
|---|---|
| 5 | Sincronizar `app-data.json` con la app (`sync_from_app.py`) cuando entren los platos nuevos; generar sus páginas: patatas bravas, bocadillo de jamón, calamares a la romana, callos, jamón, cerveza, tinto de verano. |
| 6 | Primera lectura de Search Console con filtro España: qué consultas traen impresiones a `/calorias/` y `/calculadoras/`. Añadir al mapa lo que aparezca. |
| 7 | Siguientes 10 platos de los que la app ya tiene (candidatos en el mapa §5.2), elegidos por lo que Search Console enseñe, no por la lista. |
| 8 | Dulces de temporada si la app los tiene (turrón, roscón): publicar antes de diciembre o no publicar. |

## Mes 3 · diciembre–enero: segunda tanda y ajuste

| Semana | Qué |
|---|---|
| 9–10 | Siguientes 10 platos, elegidos por lo que Search Console enseñe (no por esta lista): los candidatos están en el mapa, §5.2. Las torrijas y los dulces de Navidad (turrón, roscón) solo si la app los tiene. |
| 11 | Calculadoras: mirar qué consultas traen impresiones y si alguna merece una página hermana (por ejemplo «calorías para ganar masa muscular» o «cuánto tardaré en perder X kilos»). No construir nada que no tenga señal. |
| 12 | Informe de cierre: posiciones por página, impresiones España vs resto, qué página inglesa gana a su par española (§6 de las notas técnicas) y la lista de los 20 siguientes. |

## Cada semana, siempre

- Search Console → Páginas → No indexadas: que no entre nada nuevo que no esté en la tabla de las notas técnicas.
- Search Console → Rendimiento → País = España → Consultas: apuntar las nuevas en el mapa.
- Nada de volúmenes inventados: si una cifra no sale de Search Console, no se escribe.

## Lo que haría cambiar el plan

- Si a las 6 semanas `/calorias/` no tiene ni una impresión, el problema es de indexación, no de contenido: revisar sitemap, enlaces desde portada y pedir indexación de nuevo antes de escribir más.
- Si una página de plato entra en la primera página para su consulta, hacer sus hermanas (comparables, misma comida) antes que seguir la lista.
- Si Fotokal (la app de iPhone) empieza a aparecer en las consultas de marca, añadir la línea en la FAQ.
