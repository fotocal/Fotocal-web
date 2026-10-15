# Capturas que hay que rehacer — lista única, en español, por orden de importancia

Actualizada el 15 de octubre de 2026. Sustituye a la lista de 25 de
`tools/image-audit/IMAGES.md` y a la de 2026-09-11 de `CAPTURE-BACKLOG.md`.
Solo español: el sitio enseña capturas en español también en /en/ hasta
nueva orden (decisión del propietario, PART 46).

## Reglas, para todas

1. App en **español**, **tema claro**.
2. **Pantalla completa, con la barra de estado**: no recortes nada; el recorte lo hacemos aquí y queda registrado (tools/captures/, tools/frame_screen.py).
3. **Sin datos personales** que no quieras públicos: ni nombre, ni correo, ni foto de perfil, ni una cara en una foto de plato. El peso y el objetivo que se ven en Cuerpo cuentan como personales: si no quieres que salgan, usa la cuenta demo (scripts/demo-account en el repo de la app) o avisa y la pantalla se queda fuera.
4. Envíalas de una en una, como quieras; cada una se cambia en todas las páginas donde se usa y se te dice cuáles.
5. Una captura sirve para varias imágenes del sitio: cada pantalla se pide **una sola vez**.

Cómo leer cada ficha: **dónde** (cómo llegar), **qué tiene que verse**, **estado de la cuenta**, **páginas del sitio** en las que se usa.

## Las cinco primeras (ya elegidas en PART 46)

### 1 · Inicio, arriba del todo
- **Dónde**: abre la app; pestaña Inicio, sin desplazar.
- **Qué tiene que verse**: el anillo de calorías del día con las tres cifras (comidas, restantes, quemadas), los macros del día debajo y la racha arriba.
- **Estado**: un día con dos o tres comidas ya registradas (que el anillo esté a medias, no vacío ni pasado); racha de varios días si la tienes. Gratis o Premium, da igual.
- **Páginas**: portada (cabecera, la imagen más vista del sitio), /features/weight-loss/ (cabecera), /features/lifestyle-mindset/ (cabecera y el recorte de la racha).

### 2 · Cámara de escaneo encuadrando un plato
- **Dónde**: Inicio → botón de registrar → pestaña Escanear; apunta a un plato real antes de disparar.
- **Qué tiene que verse**: el visor con el plato dentro y el botón de disparo; que se entienda qué plato es (uno de verdad, en una mesa, no una foto de pantalla).
- **Estado**: cualquiera.
- **Páginas**: portada (cómo funciona, paso 1; y la tarjeta «Foto»), /features/scan-food/ (cómo funciona), /features/weight-loss/ (cómo funciona).

### 3 · Resultado del escaneo, parte superior
- **Dónde**: después de escanear ese plato, la pantalla de resultado sin desplazar.
- **Qué tiene que verse**: la foto del plato con la puntuación de salud encima, el nombre del plato, las calorías y los macros.
- **Estado**: cualquiera. Mejor si el plato es español y reconocible (una tortilla, unas lentejas, un bocadillo).
- **Páginas**: /features/scan-food/ (cabecera), portada (cómo funciona, paso 2), /features/scan-food/ (cómo funciona, el nombre editable).

### 4 · Hoy, justo después de guardar
- **Dónde**: guarda ese resultado y vuelve a Inicio.
- **Qué tiene que verse**: las calorías, la proteína, los hidratos y la grasa del día frente a los objetivos, con la comida recién añadida en la lista.
- **Estado**: la misma cuenta y el mismo día que la captura 1.
- **Páginas**: portada (cómo funciona, paso 3), /features/scan-food/ (cabecera secundaria y cómo funciona), /features/nutrition-diet/, /features/weight-loss/.

### 5 · Resultado de un código de barras
- **Dónde**: registrar → pestaña Código de barras → escanea un producto envasado; la pantalla de resultado.
- **Qué tiene que verse**: la puntuación sobre 100, las razones debajo (lo bueno y lo malo) y la fila de nutrientes. Un producto con algo que señalar (un refresco, unas galletas) enseña más que uno perfecto.
- **Estado**: si en Mi salud tienes una alergia activada y el producto choca con ella, sale el aviso «No apto para ti»: esa versión vale para dos imágenes a la vez.
- **Páginas**: portada (tarjeta «Código de barras»), /features/ (cómo se registra), /features/scan-barcode/ (cómo funciona y la puntuación), /features/nutrition-diet/.

## El resto, por orden

### 6 · Resultado del registro por voz
- **Dónde**: registrar → pestaña Voz → di una frase con dos o tres alimentos («dos huevos y una tostada con aguacate») → la hoja de resultado.
- **Qué tiene que verse**: la frase entendida arriba y cada alimento con calorías y macros, antes de guardar.
- **Estado**: cualquiera. Cuidado: la lista de fondo puede dejar ver registros anteriores; si hay algo raro, mejor otra frase.
- **Páginas**: portada (tarjeta «Voz»), /features/ (cómo se registra), /features/voice-logging/ (cabecera).

### 7 · Progreso, vista Dieta
- **Dónde**: pestaña Progreso → Dieta.
- **Qué tiene que verse**: el anillo de calorías y macros del día y, debajo, las tarjetas de la semana.
- **Estado**: en una cuenta gratis dos tarjetas salen bloqueadas: también vale, porque la página de suscripción enseña justo eso. Si puedes, una de cada (gratis y Premium).
- **Páginas**: /features/ (seguimiento), portada (progreso), /features/nutrition-diet/ (cabecera), /subscription/.

### 8 · Detalle de un alimento guardado
- **Dónde**: Inicio → toca una comida de la lista → la ficha.
- **Qué tiene que verse**: calorías y macros arriba y, debajo, fibra, azúcar, grasa saturada y las filas de vitaminas y minerales.
- **Estado**: Premium, para que el panel de nutrientes salga completo. Si solo tienes gratis, también sirve (dos filas y el resto bajo el candado) y lo decimos así.
- **Páginas**: /features/ (nutrición), /features/weight-loss/ (registro), portada (nutrición).

### 9 · Hoja de ingredientes detectados
- **Dónde**: desde el resultado del escaneo (captura 3) → editar ingredientes.
- **Qué tiene que verse**: cada ingrediente con sus gramos y sus calorías, y que se vea que se pueden cambiar.
- **Estado**: cualquiera.
- **Páginas**: /features/scan-food/ (cómo funciona).

### 10 · Resultado del escaneo, secciones de análisis
- **Dónde**: el mismo resultado de la captura 3, desplazado hasta el desglose.
- **Qué tiene que verse**: desglose nutricional, impacto en la salud y recomendaciones.
- **Estado**: **Premium** (en gratis están bajo el candado).
- **Páginas**: /features/scan-food/ (qué obtienes), /features/nutrition-diet/ (registro), /subscription/ (Premium).

### 11 · Resultado del escaneo, final
- **Dónde**: el mismo resultado, desplazado hasta abajo del todo.
- **Qué tiene que verse**: la confianza de la IA y la recomendación final del plato.
- **Estado**: cualquiera.
- **Páginas**: /features/scan-food/ (consejo).

### 12 · Informe semanal, parte superior
- **Dónde**: pestaña Progreso → Informe semanal (o desde la tarjeta de la semana).
- **Qué tiene que verse**: la media de calorías por día frente al objetivo y las barras de la semana.
- **Estado**: una semana con varios días registrados, para que las barras digan algo. Gratis sirve (abre gratis con dos tarjetas Premium).
- **Páginas**: /features/ (seguimiento), /features/lifestyle-mindset/ (la semana).

### 13 · Coach Kal, una pregunta sobre una comida escaneada
- **Dónde**: desde el resultado de un escaneo → preguntar a Coach Kal («¿me encaja hoy?»), o pestaña Coach Kal escribiendo la pregunta.
- **Qué tiene que verse**: tu pregunta y la respuesta entera en pantalla, con las calorías que quedan.
- **Estado**: un día con comidas registradas, para que la respuesta tenga cifras.
- **Páginas**: /ai/ (cabecera), /features/ (entender), /features/nutrition-diet/ (preguntar), /features/weight-loss/ (constancia), portada (coach), /subscription/ (gratis).

### 14 · Coach Kal, cena que encaje en el día
- **Dónde**: Coach Kal → «proponme una cena que encaje en lo que me queda hoy».
- **Qué tiene que verse**: la respuesta con los alimentos, sus calorías y el total.
- **Estado**: igual que la 13.
- **Páginas**: /features/nutrition-diet/ (preguntar).

### 15 · Coach Kal recién abierto
- **Dónde**: pestaña Coach Kal, sin haber escrito nada en esa sesión.
- **Qué tiene que verse**: las preguntas de inicio que propone, construidas con lo que te queda del día.
- **Estado**: un día con algo registrado.
- **Páginas**: /ai/ (cómo se usa).

### 16 · Coach Kal y una alergia
- **Dónde**: Mi salud → activa una alergia (gluten, por ejemplo) → Coach Kal → «¿puedo comer pan?».
- **Qué tiene que verse**: la respuesta diciendo que no, por la alergia.
- **Estado**: la alergia activada en Mi salud.
- **Páginas**: /ai/ (alergias).

### 17 · Coach Kal, el aviso de contenido generado
- **Dónde**: el final de cualquier respuesta de Coach Kal.
- **Qué tiene que verse**: la línea «Contenido generado por IA» debajo de la respuesta.
- **Estado**: cualquiera.
- **Páginas**: /ai/ (límites).

### 18 · Escáner de código de barras, encuadrando
- **Dónde**: registrar → Código de barras, antes de que lea el código.
- **Qué tiene que verse**: el visor con el código de un producto real dentro.
- **Estado**: cualquiera.
- **Páginas**: /features/scan-barcode/ (cabecera).

### 19 · Voz, pantalla de escucha
- **Dónde**: registrar → Voz → pulsa el micrófono.
- **Qué tiene que verse**: «Ya puedes hablar», el micrófono activo y la frase de ejemplo.
- **Estado**: cualquiera. Cuidado con los registros anteriores que se ven atenuados detrás de la hoja.
- **Páginas**: /features/voice-logging/ (cómo funciona).

### 20 · Pantalla de registro con las tres pestañas
- **Dónde**: registrar, con Voz seleccionada.
- **Qué tiene que verse**: Escanear, Código de barras y Voz, con Voz marcada, y los últimos registros por voz debajo.
- **Estado**: cualquiera.
- **Páginas**: /features/voice-logging/ (cómo funciona).

### 21 · Mi salud
- **Dónde**: Perfil → Mi salud.
- **Qué tiene que verse**: la lista de alergias y, debajo, las formas de comer, con dos o tres activadas.
- **Estado**: las que quieras activadas; no hace falta que sean las tuyas.
- **Páginas**: /ai/ (tus datos), /features/nutrition-diet/ (dietas).

### 22 · Cuerpo, la tarjeta del objetivo
- **Dónde**: pestaña Progreso → Cuerpo.
- **Qué tiene que verse**: peso inicial, peso actual, meta y lo que llevas.
- **Estado**: aquí salen tus cifras: decide si quieres que se publiquen o usa la cuenta demo.
- **Páginas**: /features/weight-loss/ (cómo funciona).

### 23 · Resultado del escáner de carta
- **Dónde**: registrar → carta de restaurante (Premium) → fotografía una carta real.
- **Qué tiene que verse**: la lista de platos leídos con calorías y macros y el plato recomendado resaltado.
- **Estado**: **Premium**. Bloqueada hasta que la app responda en español en esta pantalla (APP-BUGS, sesión 2, punto 2): la captura actual tiene el texto de la IA en inglés dentro de la interfaz española. Pídela la última.
- **Páginas**: /features/ (cómo se registra), portada (tarjeta «Carta»).

## Lo que no hace falta volver a capturar
- El escáner de barras con el **kéfir** y el aviso de alergia: lo cubre la captura 5 si la haces con una alergia activada.
- La **racha** como pantalla aparte: la portada y /features/lifestyle-mindset/ recortan el contador de la captura 1.
- La **tarjeta de actividad** (pasos, agua, comidas) de Inicio: sale en la captura 1 o, si queda abajo, en la 4; se recorta de ahí.
- Fotos de platos y de botellas: no son pantallas de la app y no caducan.

Veintitrés pantallas; con cinco bien hechas (1 a 5) cambian la portada entera y las dos páginas más visitadas.
