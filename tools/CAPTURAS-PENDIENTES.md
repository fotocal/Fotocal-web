# Capturas que hay que rehacer — por página del sitio, en el orden de trabajo

Actualizada el 16 de octubre de 2026 (tarde), tras la sesión 7. Sustituye a la versión por pantalla.
**Cada pantalla dos veces: app en español para las páginas en español y app en inglés para /en/.**
Nunca una pantalla en español en /en/ ni al revés.

## Estado tras la sesión 7 (54 capturas recibidas, 17 pantallas publicadas en los dos idiomas)

Publicadas (familia `assets/img/screens/s7-*`): inicio (calorías), inicio tras guardar, actividad semana,
nutrición avanzada, calendario, barra de búsqueda de una comida, resultado del escaneo, detalle
«¿Qué lleva que no ves?», lista completa de nutrientes, código de barras (Aquarius), «Prueba estos en
su lugar», resultado por voz, Coach Kal (plan), Mi progreso, peso mensual, informe semanal, racha.

**Siguen con la captura antigua** (en los dos idiomas) hasta que lleguen estas pantallas, cada una en
español y en inglés, pantalla completa con barra de estado:

1. Cámara de escaneo encuadrando un plato (portada paso 1, escanear comida «cómo», perder peso «cómo»).
2. Editar la ración / los ingredientes del resultado (escanear comida «cómo»).
3. Final del resultado con el consejo Premium (escanear comida «consejo»).
4. Voz escuchando, con el micrófono activo (registro por voz «cómo»).
5. Leer la etiqueta: paso de código de barras (código de barras «cómo», nutrición y dieta «comida»).
6. Coach Kal: una cena que encaje con los macros (nutrición y dieta «pregunta»).
7. Mi salud / perfil con dietas y alergias (Coach Kal «datos», nutrición y dieta «dietas»).
8. Coach Kal recién abierto, respuesta sobre una alergia y la nota «es IA» (página Coach Kal).
9. Meta de peso en Cuerpo (perder peso «cómo»).
10. Agua: la pestaña Día en inglés con barra de estado (la española ya está); nutrición y dieta «comida».
11. Paywall, cuando la app diga que la prueba de 5 días está en los dos planes (suscripción).
12. Escáner de carta: fuera hasta que la IA responda en español.
13. Escáner de código de barras encuadrando el código (código de barras, paso 1).

Opcional: repetir el resultado por voz con una frase clara (la actual lee «Un banana, dos plátano, dos
canarias, dos manzana»). Lo publicado hoy usa esa captura tal cual.

---


## Reglas, para todas

1. App en **español** para las páginas en español y en **inglés** para /en/; **tema claro**. Cada pantalla, dos capturas.
2. **Pantalla completa, con la barra de estado**: sin recortar nada; el recorte lo hacemos aquí y queda registrado (tools/captures/, tools/frame_screen.py).
3. **Sin datos personales** que no quieras públicos: ni nombre, ni correo, ni foto de perfil, ni una cara. Donde salgan tus pesos (Cuerpo, Progreso), la cuenta demo.
4. Una sesión por página: todas las capturas de esa página juntas; aquí se sustituyen todas, se publica y se te enseña la página terminada.
5. **Una captura sirve para varias páginas.** Cada pantalla se pide una sola vez, en la primera página que la necesita; en las siguientes aparece como «ya hecha en la página N».

## El orden de las páginas (diez sesiones, ocho con capturas nuevas)

| Sesión | Página | Capturas nuevas | Ya hechas antes |
|---|---|---|---|
| 1 | Portada — getfotocal.com/ y /en/ | **10** | — |
| 2 | Escanear comida — /features/scan-food/ y /en/features/scan-food/ | **3** | 3 |
| 3 | Funciones (índice) — /features/ y /en/features/ | **1** | 7 |
| 4 | Código de barras — /features/scan-barcode/ y /en/… | **1** | 1 |
| 5 | Registro por voz — /features/voice-logging/ y /en/… | **2** | 1 |
| 6 | Coach Kal — /ai/ y /en/ai/ | **4** | 1 |
| 7 | Nutrición y dieta — /features/nutrition-diet/ y /en/… | **1** | 7 |
| 8 | Perder peso — /features/weight-loss/ y /en/… | **1** | 5 |
| 9 | Hábitos y constancia — /features/lifestyle-mindset/ y /en/… | 0 | 3 |
| 10 | Suscripción — /subscription/ y /en/subscription/ | 0 | 3 |

Veintitrés pantallas en total. Las sesiones 9 y 10 no necesitan nada nuevo: se publican solas cuando lleguen las anteriores. Una pantalla más, el **escáner de carta**, queda fuera hasta que la app conteste en español en esa pantalla (APP-BUGS, sesión 2, punto 2); la portada y /features/ la enseñan con la captura antigua mientras tanto.

---

## Sesión 1 · PORTADA — https://getfotocal.com/ y https://getfotocal.com/en/

Es la página que más se ve y la que más capturas lleva. Con estas diez cambia entera. Usa el mismo día de la cuenta para la 1, la 2, la 5 y la 9, para que las cifras cuadren entre ellas.

**Capturas que necesita: 10**

1. **Inicio, arriba del todo** — abre la app, pestaña Inicio, sin desplazar — tiene que verse el anillo de calorías con las tres cifras (comidas, restantes, quemadas), los macros del día y la racha en la cabecera — un día con dos o tres comidas ya registradas, para que el anillo esté a medias; gratis o Premium, da igual. *También la usan después: Perder peso (sesión 8) y Hábitos (sesión 9).*

2. **Inicio, la tarjeta de actividad** — la misma pantalla de Inicio, desplazada hasta que la tarjeta de actividad (pasos, vasos de agua, comidas del día) quede entera en pantalla — la tarjeta completa, con algún paso y algún vaso registrados — el mismo día que la 1. *También la usan: Funciones (3), Nutrición y dieta (7), Hábitos (9).*

3. **Cámara de escaneo encuadrando un plato** — Inicio → botón de registrar → pestaña Escanear; apunta a un plato de verdad antes de disparar — el visor con el plato dentro y el botón de disparo; un plato reconocible (tortilla, lentejas, un bocadillo) — cualquiera. *También la usan: Escanear comida (2), Funciones (3), Perder peso (8).*

4. **Resultado del escaneo, arriba** — dispara a ese plato y espera el resultado, sin desplazar — la foto del plato con la puntuación de salud encima, el nombre, las calorías y los macros — cualquiera. *También la usa: Escanear comida (2).*

5. **Hoy, justo después de guardar** — guarda ese resultado y vuelve a Inicio — las calorías, la proteína, los hidratos y la grasa del día frente a los objetivos, con la comida recién añadida — el mismo día que la 1. *También la usan: Escanear comida (2), Nutrición y dieta (7), Perder peso (8).*

6. **Resultado de un código de barras** — registrar → pestaña Código de barras → escanea un producto envasado — la puntuación sobre 100, las razones debajo y la fila de nutrientes; mejor un producto con algo que señalar (refresco, galletas) — **antes, en Perfil → Mi salud, activa una alergia que el producto incumpla** (gluten con unas galletas, lactosa con un yogur): así sale el aviso «No apto para ti» y la misma captura sirve también para la página de código de barras. *También la usan: Funciones (3), Código de barras (4), Nutrición y dieta (7).*

7. **Resultado del registro por voz** — registrar → pestaña Voz → di una frase con dos o tres alimentos («dos huevos y una tostada con aguacate») → la hoja de resultado — la frase entendida arriba y cada alimento con calorías y macros, antes de guardar — cualquiera; si en la lista de fondo asoma algo raro, otra frase. *También la usan: Funciones (3), Registro por voz (5).*

8. **Detalle de un alimento guardado** — Inicio → toca una comida de la lista — calorías y macros arriba y, debajo, fibra, azúcar, grasa saturada y las filas de vitaminas y minerales — Premium para que el panel salga completo (en gratis también vale: dos filas y el candado, y lo decimos así). *También la usan: Funciones (3), Perder peso (8).*

9. **Coach Kal con una pregunta sobre una comida escaneada** — desde el resultado de un escaneo → preguntar a Coach Kal «¿me encaja hoy?» (o escribirlo en la pestaña Coach Kal) — tu pregunta y la respuesta entera, con las calorías que quedan — el mismo día que la 1, con comidas registradas. *También la usan: Funciones (3), Coach Kal (6), Nutrición y dieta (7), Perder peso (8), Suscripción (10).*

10. **Progreso, vista Dieta** — pestaña Progreso → Dieta — el anillo de calorías y macros del día y, debajo, las tarjetas de la semana — **cuenta demo** (aquí salen datos de la cuenta); en gratis dos tarjetas salen bloqueadas y también vale. *También la usan: Funciones (3), Nutrición y dieta (7), Suscripción (10).*

Cuando lleguen las diez: se recortan, se sustituyen las 12 imágenes de la portada (11 pantallas más el recorte de la tarjeta de actividad), se publica, y se te enseña la portada terminada con la lista de archivos cambiados.

---

## Sesión 2 · ESCANEAR COMIDA — /features/scan-food/

Ya hechas en la sesión 1: cámara (3), resultado arriba (4), Hoy tras guardar (5).

**Capturas nuevas: 3**, las tres desde el mismo resultado de la sesión 1 si la comida sigue guardada:

1. **Hoja de ingredientes detectados** — desde el resultado → editar ingredientes — cada ingrediente con sus gramos y calorías — cualquiera.
2. **Resultado, secciones de análisis** — el resultado desplazado hasta el desglose — desglose nutricional, impacto en la salud y recomendaciones — **Premium** (en gratis están bajo el candado). *También la usan: Nutrición y dieta (7), Suscripción (10).*
3. **Resultado, final** — el mismo resultado, abajo del todo — la confianza de la IA y la recomendación final — cualquiera.

## Sesión 3 · FUNCIONES — /features/

Ya hechas: tarjeta de actividad (1.2), cámara (1.3), código de barras (1.6), voz (1.7), detalle (1.8), Coach Kal (1.9), Progreso (1.10).

**Captura nueva: 1**

1. **Informe semanal, arriba** — pestaña Progreso → Informe semanal — la media de calorías por día frente al objetivo y las barras de la semana — **cuenta demo**, con varios días registrados para que las barras digan algo; en gratis abre con dos tarjetas Premium y vale. *También la usa: Hábitos (9).*

## Sesión 4 · CÓDIGO DE BARRAS — /features/scan-barcode/

Ya hecha: resultado con el aviso de alergia (1.6).

**Captura nueva: 1**

1. **Escáner de barras encuadrando** — registrar → Código de barras, antes de que lea — el visor con el código de un producto real dentro — cualquiera.

## Sesión 5 · REGISTRO POR VOZ — /features/voice-logging/

Ya hecha: resultado por voz (1.7).

**Capturas nuevas: 2**

1. **Pantalla de escucha** — registrar → Voz → pulsa el micrófono — «Ya puedes hablar», el micrófono activo y la frase de ejemplo — cualquiera; ojo a los registros anteriores atenuados detrás.
2. **Pantalla de registro con las tres pestañas** — registrar, con Voz seleccionada — Escanear, Código de barras y Voz, Voz marcada, y los últimos registros por voz debajo — cualquiera.

## Sesión 6 · COACH KAL — /ai/

Ya hecha: Coach Kal con la comida escaneada (1.9).

**Capturas nuevas: 4**

1. **Coach Kal recién abierto** — pestaña Coach Kal sin haber escrito nada en esa sesión — las preguntas de inicio que propone — un día con algo registrado.
2. **Coach Kal y una alergia** — Mi salud → alergia activada (gluten) → Coach Kal → «¿puedo comer pan?» — la respuesta diciendo que no, por la alergia — la alergia activada.
3. **El aviso de contenido generado** — el final de cualquier respuesta — la línea «Contenido generado por IA» — cualquiera.
4. **Mi salud** — Perfil → Mi salud — la lista de alergias y, debajo, las formas de comer, con dos o tres activadas — las que quieras, no hace falta que sean las tuyas. *También la usa: Nutrición y dieta (7).*

## Sesión 7 · NUTRICIÓN Y DIETA — /features/nutrition-diet/

Ya hechas: Progreso (1.10), código de barras (1.6), Coach Kal (1.9), análisis Premium (2.2), Hoy (1.5), tarjeta de actividad (1.2), Mi salud (6.4).

**Captura nueva: 1**

1. **Coach Kal, cena que encaje** — Coach Kal → «proponme una cena que encaje en lo que me queda hoy» — la respuesta con los alimentos, sus calorías y el total — un día con comidas registradas.

## Sesión 8 · PERDER PESO — /features/weight-loss/

Ya hechas: Inicio arriba (1.1), Coach Kal (1.9), detalle (1.8), cámara (1.3), Hoy (1.5).

**Captura nueva: 1**

1. **Cuerpo, la tarjeta del objetivo** — pestaña Progreso → Cuerpo — peso inicial, peso actual, meta y lo que llevas — **cuenta demo**.

## Sesión 9 · HÁBITOS Y CONSTANCIA — /features/lifestyle-mindset/

Nada nuevo: Inicio arriba (1.1, también el recorte de la racha), tarjeta de actividad (1.2), informe semanal (3.1). Se publica sola.

## Sesión 10 · SUSCRIPCIÓN — /subscription/

Nada nuevo: Progreso (1.10), Coach Kal (1.9), análisis Premium (2.2). Se publica sola.
