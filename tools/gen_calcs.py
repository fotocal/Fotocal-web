#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the four Spanish calculators and their hub, /calculadoras/ (PART 47).

    python3 tools/gen_calcs.py           # writes src/calculadoras/**/index.html
    python3 tools/build_site.py          # then renders the Spanish tree

The arithmetic lives in assets/js/calc.js and runs in the visitor's browser:
no account, nothing sent. This file holds the copy, the forms and the head
of each page, on the same skeleton as the dish pages (tools/gen_dishes.py),
so the two sections look and behave alike. Spanish-only, like /calorias/."""
import os, sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_dishes import head, foot, ld_block, ORG, APP_ASIDE, esc, blog_title, TITLE_MAX, SITE, ROOT  # noqa: E402

SRC = os.path.join(ROOT, "src", "calculadoras")
PUB = "2026-10-13"

CALCS = [
    {"slug": "calorias-diarias", "kind": "tdee", "short": "Calorías diarias",
     "title": "Calculadora de calorías diarias (Mifflin-St Jeor)",
     "desc": "Calcula cuántas calorías necesitas al día para mantener, perder o ganar peso con la fórmula de Mifflin-St Jeor y tu actividad. En la página, sin registro.",
     "h1": "Calculadora de calorías diarias",
     "lead": "Cuántas calorías gastas al día, tu mantenimiento, y cuántas comer para perder o ganar peso despacio. Usa la fórmula de Mifflin-St Jeor, la que recomiendan las guías de dietética, y funciona aquí mismo: sin registro y sin enviar nada.",
     "blog": ["tdee-how-many-calories-you-need", "understanding-your-basal-metabolic-rate", "how-many-calories-does-exercise-burn"],
     "faq": [
         ("¿Cuántas calorías debo comer al día para adelgazar?", "Las de tu mantenimiento menos un recorte moderado: entre 300 y 550 kcal al día para la mayoría de la gente, lo que da entre un cuarto y medio kilo a la semana. La calculadora te muestra las dos cifras. Si tu resultado para perder queda por debajo de 1.200 kcal (mujer) o 1.500 (hombre), no bajes más sin un profesional: baja el ritmo."),
         ("¿Cómo hacer un conteo de calorías?", "Cuatro pasos. Calcula tu mantenimiento aquí y decide el objetivo. Apunta todo lo que comes durante dos semanas, incluidos el aceite, las salsas y las bebidas, que es donde se escapan las calorías; con una app es una foto, una frase por voz o un código de barras por comida. Pesa lo que puedas pesar al principio, sobre todo pan, arroz, pasta y aceite, hasta que calcules a ojo. Y compara la media semanal con la báscula: si en tres semanas no se mueve, recorta 100 o 200 kcal más, no 500."),
         ("¿Es lo mismo que el TDEE?", "Sí. TDEE son las siglas en inglés de gasto energético diario total: lo que gastas en un día contando el metabolismo basal, la digestión y todo lo que te mueves. Aquí lo llamamos mantenimiento, porque es la cifra con la que ni pierdes ni ganas peso."),
         ("¿Por qué me sale distinto que en otra calculadora?", "Porque usan otra fórmula (Harris-Benedict suele dar más) u otros factores de actividad. Ninguna acierta tu cifra exacta: el error típico a nivel individual ronda el 10 %. Toma el resultado como punto de partida y ajústalo con la báscula a las dos o tres semanas."),
     ]},
    {"slug": "deficit-calorico", "kind": "deficit", "short": "Déficit calórico",
     "title": "Calculadora de déficit calórico: mujer y hombre, gratis",
     "desc": "Calcula tu déficit calórico para perder peso: mantenimiento, cuánto recortar según tu sexo y peso, y cuánto tardarías. Gratis, sin registro y con ejemplos.",
     "h1": "Calculadora de déficit calórico: mujer y hombre",
     "lead": "El déficit calórico es comer menos de lo que gastas, y es lo único que hay detrás de toda pérdida de peso que dura. Esta calculadora te da tu mantenimiento según tu sexo, edad, altura, peso y actividad, cuánto recortar para perder entre el 0,5 % y el 1 % de tu peso a la semana y cuánto tardarías con los kilos que te has propuesto. Debajo: cómo se calcula a mano, qué cambia entre mujer y hombre, qué significa un déficit de 500 calorías al día y qué comer mientras tanto.",
     "blog": ["calorie-deficit-for-fat-loss", "how-fast-should-you-lose-weight", "the-truth-about-starvation-mode"],
     "faq": [
         ("¿Cuántas calorías debo quemar para bajar 1 kilo?", "Unas 7.700 kcal de déficit acumulado, entre comer menos y moverte más; no hace falta «quemarlas» en el gimnasio. Con 500 kcal menos al día tardas unas dos semanas; con 250, un mes. La báscula no sigue la regla al pie de la letra: las primeras semanas baja más, por agua, y después menos."),
         ("¿Cuál es el déficit calórico recomendado para bajar de peso?", "El que te hace perder entre el 0,5 % y el 1 % de tu peso a la semana: con 70 kg, de 350 a 700 g, que son unas 385 a 770 kcal al día. Las guías de nutrición deportiva lo recomiendan porque conserva músculo; más rápido se lleva peor y se recupera antes."),
         ("¿Cuánto adelgazo con un déficit de 500 calorías por día?", "Unos 450 g a la semana sobre el papel (3.500 kcal entre 7.700), alrededor de dos kilos al mes. Para una mujer de 55 kg es el ritmo máximo sensato; para un hombre de 100 kg es un ritmo suave. Si 500 kcal menos te dejan por debajo de 1.200 kcal al día siendo mujer o de 1.500 siendo hombre, elige un déficit menor."),
         ("¿Es distinto el déficit calórico para mujer y hombre?", "La regla es la misma, del 0,5 % al 1 % del peso a la semana, pero el punto de partida no: la fórmula de Mifflin-St Jeor da a una mujer unas 166 kcal menos de gasto que a un hombre de la misma edad, altura y peso, y las mujeres suelen pesar menos, así que el mismo porcentaje son menos calorías. Por eso la calculadora pide el sexo y aplica suelos distintos, 1.200 y 1.500 kcal."),
         ("¿De dónde sale lo de 7.700 kcal por kilo?", "De una estimación clásica (Wishnofsky, 1958) de la energía que guarda un kilo de tejido graso. Sirve para dimensionar el recorte, no para predecir la báscula: el cuerpo gasta menos a medida que pesas menos y las primeras semanas se pierde agua además de grasa."),
         ("¿Y si me sale por debajo de mi metabolismo basal?", "Entonces el ritmo elegido es demasiado alto para tu tamaño. Comer por debajo de la tasa metabólica basal de forma mantenida no es una buena idea sin un médico o dietista detrás: baja el ritmo al 0,5 % o reparte el déficit entre comer algo menos y moverte algo más."),
     ]},
    {"slug": "imc", "kind": "bmi", "short": "IMC",
     "title": "Calculadora de IMC (índice de masa corporal)",
     "desc": "Calcula tu índice de masa corporal con tu peso y altura, mira en qué rango de la OMS cae y qué peso corresponde a un IMC normal. Y lo que el IMC no te dice.",
     "h1": "Calculadora de IMC",
     "lead": "El índice de masa corporal relaciona tu peso con tu altura y lo compara con los rangos que usa la Organización Mundial de la Salud para adultos. Es una criba rápida y útil a nivel de población; en una persona concreta hay que leerlo con cuidado, y abajo se explica por qué.",
     "blog": ["why-the-scale-is-not-the-whole-story", "how-to-lose-weight-sustainably", "building-muscle-while-losing-fat"],
     "faq": [
         ("¿Qué IMC es normal?", "Entre 18,5 y 24,9 según la OMS para adultos. Por debajo de 18,5 es bajo peso; de 25 a 29,9, sobrepeso; a partir de 30, obesidad, en tres grados. La calculadora te dice en qué rango estás y qué peso te dejaría dentro del normal con tu altura."),
         ("¿Sirve el IMC si hago mucho deporte?", "Peor que para la media. El IMC no distingue músculo de grasa: una persona musculada puede dar sobrepeso con poca grasa corporal. En ese caso dicen más el perímetro de cintura, cómo te queda la ropa o una medición de composición corporal."),
         ("¿Vale para niños, embarazadas o mayores de 65?", "No con estos rangos. En menores de 18 se usan percentiles por edad y sexo; en el embarazo no aplica; y a partir de los 65 años los puntos de corte se discuten, porque un IMC algo más alto no va asociado a peor salud. En esos casos, el pediatra o el médico."),
     ]},
    {"slug": "macros", "kind": "macros", "short": "Macros",
     "title": "Calculadora de macros: proteínas, grasas e hidratos",
     "desc": "Reparte tus calorías en proteínas, grasas e hidratos según tu peso y tu objetivo: perder grasa, mantener o ganar músculo. Gramos al día, con la regla explicada.",
     "h1": "Calculadora de macros",
     "lead": "Cuántos gramos de proteínas, grasas e hidratos de carbono comer al día a partir de tus calorías y tu peso. La proteína se fija por kilo de peso, la grasa como parte de las calorías y los hidratos se llevan el resto: es la regla que usan los dietistas, y aquí está a la vista.",
     "blog": ["how-to-set-your-macros-for-weight-loss", "macronutrients-101", "how-much-protein-per-day"],
     "faq": [
         ("¿Cuánta proteína necesito al día?", "Entre 1,2 y 2,2 g por kilo de peso según lo que hagas: 1,2 si eres sedentario, 1,6 si entrenas y quieres perder grasa sin perder músculo, hasta 2 o 2,2 si entrenas fuerza en serio o estás en un déficit grande. Con 70 kg, 1,6 g/kg son 112 g de proteína al día."),
         ("¿Por qué la grasa va en porcentaje y no en gramos?", "Porque lo que importa de la grasa es que no baje de un mínimo (hormonas, vitaminas liposolubles) y las guías lo expresan así: entre el 20 % y el 35 % de las calorías. Por debajo del 20 % mantenido mucho tiempo suele dar problemas; por encima del 35 % deja poco sitio para los hidratos."),
         ("¿Los hidratos no deberían ser más bajos para perder grasa?", "No hace falta. Lo que hace perder grasa es el déficit de calorías, no el reparto. Los hidratos son lo que sobra una vez cubiertas la proteína y la grasa, y si entrenas son los que sostienen el rendimiento. Si el resultado te da menos de 50 g, no es que tengas que comer así: es que las calorías son pocas para esa proteína y esa grasa."),
     ]},
]

BODY_FIELDS = """
          <div class="calc-field wide">
            <span class="calc-field" style="display:block"><label>Sexo</label></span>
            <div class="calc-seg" role="radiogroup" aria-label="Sexo">
              <input type="radio" name="sex" id="sex-m" value="m" checked><label for="sex-m">Hombre</label>
              <input type="radio" name="sex" id="sex-f" value="f"><label for="sex-f">Mujer</label>
            </div>
          </div>
          <div class="calc-field"><label for="age">Edad (años)</label><input id="age" name="age" type="number" inputmode="numeric" min="18" max="90" placeholder="35" required></div>
          <div class="calc-field"><label for="height">Altura (cm)</label><input id="height" name="height" type="number" inputmode="numeric" min="130" max="230" placeholder="170" required></div>
          <div class="calc-field"><label for="weight">Peso (kg)</label><input id="weight" name="weight" type="number" inputmode="decimal" step="0.1" min="35" max="250" placeholder="75" required></div>
          <div class="calc-field"><label for="activity">Actividad</label>
            <select id="activity" name="activity">
              <option value="1.2">Sedentario: trabajo sentado, poco ejercicio</option>
              <option value="1.375">Ligera: ejercicio 1–3 días por semana</option>
              <option value="1.55" selected>Moderada: ejercicio 3–5 días por semana</option>
              <option value="1.725">Alta: ejercicio intenso 6–7 días</option>
              <option value="1.9">Muy alta: trabajo físico más entrenamiento</option>
            </select>
          </div>"""

FORMS = {
    "tdee": """
      <form class="calc reveal" data-calc="tdee" novalidate>
        <div class="calc-grid">{BODY}</div>
        <div class="calc-out" id="out" hidden>
          <div class="calc-main"><b id="r-tdee">—</b><span>kcal al día para mantener tu peso</span></div>
          <div class="calc-rows">
            <div class="calc-row"><span>Metabolismo basal (TMB), lo que gastas en reposo</span><b><span id="r-bmr">—</span> kcal</b></div>
            <div class="calc-row is-hl"><span>Para perder unos 250 g a la semana (−275 kcal)</span><b><span id="r-lose25">—</span> kcal</b></div>
            <div class="calc-row is-hl"><span>Para perder unos 500 g a la semana (−550 kcal)</span><b><span id="r-lose50">—</span> kcal</b></div>
            <div class="calc-row"><span>Para ganar unos 250 g a la semana (+275 kcal)</span><b><span id="r-gain">—</span> kcal</b></div>
          </div>
          <p class="calc-warn" id="w-floor" hidden>La cifra para perder medio kilo a la semana queda por debajo de <span id="w-floor-n"></span> kcal. Por debajo de ahí no conviene seguir sin un profesional: elige el ritmo más suave.</p>
          <p class="calc-note">Estimación con la fórmula de Mifflin-St Jeor. El error típico para una persona concreta ronda el 10 %: úsala como punto de partida y ajusta con la báscula a las dos o tres semanas.</p>
        </div>
      </form>""".replace("{BODY}", BODY_FIELDS),
    "deficit": """
      <form class="calc reveal" data-calc="deficit" novalidate>
        <div class="calc-grid">{BODY}
          <div class="calc-field"><label for="goal">Kilos que quieres perder</label><input id="goal" name="goal" type="number" inputmode="decimal" step="0.5" min="0.5" max="100" placeholder="5" required></div>
          <div class="calc-field wide">
            <span class="calc-field" style="display:block"><label>Ritmo semanal</label></span>
            <div class="calc-seg" role="radiogroup" aria-label="Ritmo semanal">
              <input type="radio" name="rate" id="rate-05" value="0.5" checked><label for="rate-05">Suave · 0,5 %</label>
              <input type="radio" name="rate" id="rate-075" value="0.75"><label for="rate-075">Medio · 0,75 %</label>
              <input type="radio" name="rate" id="rate-1" value="1"><label for="rate-1">Rápido · 1 %</label>
            </div>
          </div>
        </div>
        <div class="calc-out" id="out" hidden>
          <div class="calc-main"><b id="r-target">—</b><span>kcal al día para perder al ritmo elegido</span></div>
          <div class="calc-rows">
            <div class="calc-row"><span>Tu mantenimiento (lo que gastas al día)</span><b><span id="r-tdee">—</span> kcal</b></div>
            <div class="calc-row is-hl"><span>Déficit diario</span><b>−<span id="r-deficit">—</span> kcal</b></div>
            <div class="calc-row"><span>Pérdida semanal esperada al principio</span><b><span id="r-weekly">—</span> kg</b></div>
            <div class="calc-row"><span>Tiempo estimado hasta el objetivo</span><b><span id="r-weeks">—</span> semanas (<span id="r-months">—</span> meses)</b></div>
          </div>
          <p class="calc-warn" id="w-bmr" hidden>Ese objetivo queda por debajo de tu metabolismo basal. No lo hagas sin un médico o dietista: elige un ritmo más suave o añade movimiento.</p>
          <p class="calc-warn" id="w-floor" hidden>Por debajo de <span id="w-floor-n"></span> kcal al día no conviene seguir sin supervisión. Elige un ritmo más suave.</p>
          <p class="calc-note">El tiempo es una estimación optimista: parte de 7.700 kcal por kilo y de que el déficit se mantiene constante, y en la práctica la pérdida se frena a medida que pesas menos. Cuenta con algo más.</p>
        </div>
      </form>""".replace("{BODY}", BODY_FIELDS),
    "bmi": """
      <form class="calc reveal" data-calc="bmi" novalidate>
        <div class="calc-grid">
          <div class="calc-field"><label for="height">Altura (cm)</label><input id="height" name="height" type="number" inputmode="numeric" min="130" max="230" placeholder="170" required></div>
          <div class="calc-field"><label for="weight">Peso (kg)</label><input id="weight" name="weight" type="number" inputmode="decimal" step="0.1" min="35" max="250" placeholder="75" required></div>
        </div>
        <div class="calc-out" id="out" hidden>
          <div class="calc-main"><b id="r-bmi">—</b><span>de IMC · <strong id="r-cat">—</strong></span></div>
          <div class="calc-rows">
            <div class="calc-row"><span>Peso que te dejaría en el rango normal (IMC 18,5 a 24,9)</span><b><span id="r-lo">—</span> a <span id="r-hi">—</span> kg</b></div>
          </div>
          <p class="calc-note">Rangos de la OMS para adultos de 18 a 64 años. No sirven tal cual para menores, embarazadas, mayores de 65 ni personas muy musculadas: lee los límites más abajo.</p>
        </div>
      </form>""",
    "macros": """
      <form class="calc reveal" data-calc="macros" novalidate>
        <div class="calc-grid">
          <div class="calc-field"><label for="kcal">Calorías al día</label><input id="kcal" name="kcal" type="number" inputmode="numeric" min="800" max="6000" placeholder="2000" required></div>
          <div class="calc-field"><label for="weight">Peso (kg)</label><input id="weight" name="weight" type="number" inputmode="decimal" step="0.1" min="35" max="250" placeholder="75" required></div>
          <div class="calc-field"><label for="protein">Proteína (g por kg de peso)</label>
            <select id="protein" name="protein">
              <option value="1.2">1,2 · sedentario</option>
              <option value="1.6" selected>1,6 · entrenas, quieres perder grasa</option>
              <option value="2.0">2,0 · fuerza o déficit grande</option>
              <option value="2.2">2,2 · máximo habitual</option>
            </select>
          </div>
          <div class="calc-field"><label for="fat">Grasa (% de las calorías)</label>
            <select id="fat" name="fat">
              <option value="20">20 % · el mínimo razonable</option>
              <option value="25">25 %</option>
              <option value="30" selected>30 % · lo habitual</option>
              <option value="35">35 % · el máximo de las guías</option>
            </select>
          </div>
        </div>
        <p class="calc-note" id="note-prefill" hidden>Las calorías vienen de tu resultado en la calculadora de calorías diarias (tu mantenimiento). Para perder grasa, réstale el déficit antes.</p>
        <div class="calc-out" id="out" hidden>
          <div class="calc-rows">
            <div class="calc-row is-hl"><span>Proteínas</span><b><span id="r-p">—</span> g · <span id="r-pk">—</span> kcal · <span id="r-pp">—</span> %</b></div>
            <div class="calc-row is-hl"><span>Grasas</span><b><span id="r-f">—</span> g · <span id="r-fk">—</span> kcal · <span id="r-fp">—</span> %</b></div>
            <div class="calc-row is-hl"><span>Hidratos de carbono</span><b><span id="r-c">—</span> g · <span id="r-ck">—</span> kcal · <span id="r-cp">—</span> %</b></div>
          </div>
          <p class="calc-warn" id="w-carbs" hidden>Quedan menos de 50 g de hidratos. No es un objetivo: es que las calorías son pocas para esa proteína y esa grasa. Sube las calorías o baja un escalón la proteína o la grasa.</p>
          <p class="calc-note">Redondeado al gramo. 4 kcal por gramo de proteína e hidratos, 9 por gramo de grasa.</p>
        </div>
      </form>""",
}

BODY = {
    "tdee": """
      <h2 id="como">Cómo se calcula</h2>
      <p>Primero la tasa metabólica basal (TMB), lo que gastas tumbado y en ayunas, con la ecuación de Mifflin-St Jeor de 1990, que en las revisiones comparativas es la que menos se desvía de la medición real en adultos:</p>
      <div class="calc-formula"><code>TMB (hombre) = 10 × peso (kg) + 6,25 × altura (cm) − 5 × edad + 5</code><br><code>TMB (mujer) &nbsp;= 10 × peso (kg) + 6,25 × altura (cm) − 5 × edad − 161</code></div>
      <p>Después, el gasto diario total: la TMB multiplicada por un factor de actividad, de 1,2 para una vida sedentaria a 1,9 para trabajo físico más entrenamiento. Ese resultado es tu mantenimiento. Las cifras para perder o ganar restan o suman un recorte fijo: 275 kcal al día equivalen, a 7.700 kcal por kilo, a unos 250 g por semana.</p>
      <h2 id="actividad">Qué nivel de actividad elegir</h2>
      <p>Casi todo el mundo se pone un escalón por encima del real. Si trabajas sentado y entrenas menos de tres veces por semana, eres sedentario a efectos de esta cuenta, aunque camines algo. Moderada es entrenar de verdad tres a cinco días. Alta es casi a diario y con intensidad. Si dudas entre dos, elige la baja: equivocarse por arriba es lo que hace que una dieta bien hecha no funcione.</p>
      <h2 id="limites">Lo que la calculadora no sabe</h2>
      <p>No conoce tu composición corporal, tu historial de dietas ni cuánto te mueves fuera del gimnasio, que es donde más varía el gasto entre dos personas iguales sobre el papel. Por eso el resultado es un punto de partida, no una sentencia: come esa cifra dos o tres semanas, mira la media de la báscula y ajusta 100 o 150 kcal en la dirección que haga falta. El artículo sobre el TDEE explica cómo hacerlo con tus propios datos.</p>""",
    "deficit": """
      <h2 id="que-es">Qué es el déficit calórico</h2>
      <p>Comer menos energía de la que gastas, de forma sostenida, de modo que el cuerpo tire de sus reservas, sobre todo de grasa. No hay dieta que adelgace por otro mecanismo: la cetogénica, el ayuno intermitente o la de puntos funcionan cuando consiguen eso y dejan de funcionar cuando no. Perder peso y perder grasa son la misma cuenta; lo que cambia es cuánto del peso perdido es grasa y cuánto músculo, y eso lo deciden el ritmo, la proteína y el ejercicio de fuerza, no el nombre de la dieta.</p>
      <h2 id="como">Cómo calcular tu déficit calórico, paso a paso</h2>
      <p>Primero, tu mantenimiento: las calorías que gastas en un día normal. Sale igual que en la <a href="../calorias-diarias/">calculadora de calorías diarias</a>, con la fórmula de Mifflin-St Jeor multiplicada por tu factor de actividad. Después, el déficit se dimensiona desde el ritmo que eliges, expresado como porcentaje de tu peso, porque 500 g a la semana son muy distintos para alguien de 60 kg que de 120:</p>
      <div class="calc-formula"><code>kg por semana = peso × ritmo (0,5 % a 1 %)</code><br><code>déficit diario ≈ kg por semana × 7.700 ÷ 7</code><br><code>objetivo diario = mantenimiento − déficit diario</code></div>
      <p>Dos ejemplos con actividad moderada y un ritmo suave del 0,5 %. Una mujer de 35 años, 165 cm y 68 kg gasta unas 2.130 kcal; 340 g a la semana son unas 375 kcal menos al día, objetivo 1.755 kcal. Un hombre de 35 años, 178 cm y 85 kg gasta unas 2.780 kcal; 425 g a la semana son unas 470 kcal menos, objetivo 2.310 kcal. Al 1 % las cifras se doblan, y para mucha gente eso ya es demasiado.</p>
      <h2 id="mujer-hombre">Déficit calórico en la mujer y en el hombre</h2>
      <p>La regla del 0,5 % al 1 % vale igual para los dos. Lo que cambia es el punto de partida: a igual edad, altura, peso y actividad, la fórmula asigna a una mujer unas 166 kcal menos de gasto al día que a un hombre, y como las mujeres suelen pesar menos, el mismo porcentaje se traduce en un recorte menor en calorías. Por eso la calculadora pide el sexo, y por eso aplica dos suelos distintos: no propone objetivos por debajo de 1.200 kcal al día en mujeres ni de 1.500 en hombres. Si tu ritmo te lleva ahí, te lo dice y conviene elegir uno más suave.</p>
      <h2 id="quinientas">Un déficit de 500 calorías al día</h2>
      <p>Es la cifra que más se repite, y sobre el papel son 3.500 kcal a la semana, unos 450 g de grasa. Que sea sensato o no depende de tu tamaño: para una mujer de 55 kg equivale a casi el 0,9 % semanal, el límite alto; para un hombre de 100 kg es un 0,45 %, un ritmo suave que se mantiene bien. Antes de adoptarlo, mira dónde te deja: si 500 kcal menos te sitúan por debajo del suelo de la calculadora, recorta 250 o 300 y pon el resto en moverte más. Y repártelo como prefieras: no tiene por qué salir todo de la comida.</p>
      <h2 id="dieta">Qué comer en déficit calórico</h2>
      <p>No hace falta una dieta con nombre. Lo que funciona dentro del déficit es lo mismo para casi todo el mundo: proteína suficiente, entre 1,6 y 2,2 g por kilo de peso si entrenas, para conservar músculo y llegar con menos hambre; verdura, fruta, legumbre y cereal integral, que llenan por poca energía; y el aceite, el pan y el alcohol medidos, que son donde se esconden las calorías que no se ven. La <a href="../macros/">calculadora de macros</a> reparte tu objetivo en gramos de proteínas, grasas e hidratos, y el <a href="../../blog/calorie-deficit-for-fat-loss/">artículo del blog sobre el déficit</a> entra en el detalle.</p>
      <h2 id="7700">Por qué 7.700 kcal por kilo es una aproximación</h2>
      <p>Es la cifra clásica de la energía que almacena un kilo de grasa corporal. Vale para dimensionar el recorte, pero la báscula no la obedece a la letra: en las primeras semanas se pierde más (agua y glucógeno), después menos (el gasto baja al pesar menos y el cuerpo se adapta), y hay semanas planas aunque todo esté bien hecho. Por eso la estimación de tiempo es optimista a propósito, y por eso conviene mirar medias semanales y no días sueltos.</p>
      <h2 id="sensato">Cuánto déficit es sensato</h2>
      <p>Entre el 0,5 % y el 1 % del peso a la semana es el rango que se recomienda en las guías de nutrición deportiva para perder grasa conservando músculo. Por debajo del 0,5 % también funciona, solo tarda más y se lleva mejor. Por encima del 1 %, o por debajo de tu metabolismo basal, es terreno de supervisión médica: la calculadora te avisa si caes ahí. Y el déficit no tiene por qué salir todo de la comida: moverte más cuenta igual.</p>""",
    "bmi": """
      <h2 id="como">Cómo se calcula</h2>
      <div class="calc-formula"><code>IMC = peso (kg) ÷ altura (m)²</code></div>
      <p>Con 75 kg y 1,70 m: 75 ÷ (1,70 × 1,70) = 26,0. El resultado se compara con los rangos de la Organización Mundial de la Salud para adultos:</p>
      <div class="dp-table-wrap"><table class="dp-table"><thead><tr><th scope="col">IMC</th><th scope="col">Clasificación OMS</th></tr></thead><tbody>
        <tr data-bmi-row="0-18.5"><td>menos de 18,5</td><td>Bajo peso</td></tr>
        <tr data-bmi-row="18.5-25"><td>18,5 a 24,9</td><td>Peso normal</td></tr>
        <tr data-bmi-row="25-30"><td>25,0 a 29,9</td><td>Sobrepeso</td></tr>
        <tr data-bmi-row="30-35"><td>30,0 a 34,9</td><td>Obesidad grado I</td></tr>
        <tr data-bmi-row="35-40"><td>35,0 a 39,9</td><td>Obesidad grado II</td></tr>
        <tr data-bmi-row="40-999"><td>40 o más</td><td>Obesidad grado III</td></tr>
      </tbody></table></div>
      <h2 id="limites">Lo que el IMC no puede decirte</h2>
      <p>Es una relación entre dos números, y no sabe de qué está hecho tu peso. Una persona que entrena fuerza puede dar sobrepeso con muy poca grasa; otra con IMC normal puede llevar demasiada grasa abdominal y poca masa muscular. Tampoco tiene en cuenta la edad (a partir de los 65 los puntos de corte se discuten), el sexo ni el origen étnico, para el que algunas sociedades proponen cortes más bajos.</p>
      <p>Si tu IMC sale alto y no te cuadra, mide la cintura: por encima de 102 cm en hombres y 88 cm en mujeres sí es un dato de riesgo por sí solo, independientemente del IMC. Y si sale normal pero no te encuentras bien, el IMC no es quien tiene que tranquilizarte. En todos los casos, el número útil para actuar no es el IMC sino cuántas calorías comes frente a las que gastas: para eso están las otras dos calculadoras.</p>""",
    "macros": """
      <h2 id="como">Cómo se calcula</h2>
      <p>En este orden, y no en otro, porque el orden es la regla:</p>
      <div class="calc-formula"><code>proteína (g) = peso (kg) × g/kg elegidos &nbsp;→ × 4 kcal</code><br><code>grasa (g) &nbsp;&nbsp;&nbsp;= calorías × % elegido ÷ 9</code><br><code>hidratos (g) = (calorías − kcal de proteína − kcal de grasa) ÷ 4</code></div>
      <p>La proteína se fija primero y por kilo de peso porque es lo que protege el músculo, sobre todo en déficit, y su necesidad depende de cuánto pesas y cuánto entrenas, no de cuántas calorías comes. La grasa va como porcentaje de las calorías porque lo que importa es no bajar de un mínimo: las guías dietéticas la sitúan entre el 20 % y el 35 % de la energía. Los hidratos son lo que queda, y eso está bien: no hay un mínimo fisiológico comparable, y a más entrenamiento, más sitio para ellos.</p>
      <h2 id="rangos">Rangos razonables</h2>
      <p>Proteína: de 1,2 g/kg para alguien sedentario a 2,2 g/kg para quien entrena fuerza en un déficit exigente; 1,6 g/kg es un valor con mucho respaldo para perder grasa entrenando. Grasa: 25 % a 30 % de las calorías es lo habitual; el 20 % es el suelo, no una meta. Si los hidratos te quedan por debajo de 50 g, el reparto no está mal: son las calorías las que no dan para más. Súbelas o baja un escalón la proteína o la grasa.</p>
      <h2 id="calorias">De dónde salen las calorías</h2>
      <p>Si no sabes cuántas calorías comer, calcula primero tu mantenimiento en la <a href="../calorias-diarias/">calculadora de calorías diarias</a> y réstale el déficit con la de <a href="../deficit-calorico/">déficit calórico</a>. Si vienes de ahí, este formulario ya trae tu mantenimiento puesto.</p>""",
}


def page(c):
    title, desc = c["title"], c["desc"]
    if len(title) + len(" — Fotocal") <= TITLE_MAX:
        title += " — Fotocal"
    assert len(title) <= TITLE_MAX and 140 <= len(desc) <= 160, (c["slug"], len(title), len(desc))
    path = "calculadoras/%s/" % c["slug"]
    url = SITE + path
    crumbs = [("Inicio", SITE), ("Calculadoras", SITE + "calculadoras/"), (c["h1"], url)]
    ld = [
        ld_block({"@context": "https://schema.org", "@type": "WebPage", "name": c["h1"], "headline": title.replace(" — Fotocal", ""),
                  "description": desc, "inLanguage": "es", "url": url, "datePublished": PUB, "dateModified": PUB,
                  "publisher": ORG, "isPartOf": {"@type": "WebSite", "@id": SITE + "#site"}}),
        ld_block({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": x[0], "item": x[1]} for i, x in enumerate(crumbs)]}),
        ld_block({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c["faq"]]}),
    ]
    out = [head(2, title, desc, path, "\n".join(ld), "website")]
    o = out.append
    o('\n<main id="main">\n  <article class="post dp">\n    <header class="post-head">\n      <div class="container-narrow">')
    o('        <nav class="post-crumbs reveal" aria-label="Migas de pan"><a href="../../">Inicio</a><span class="sep" aria-hidden="true">/</span><a href="../">Calculadoras</a><span class="sep" aria-hidden="true">/</span><a href="./" aria-current="page">%s</a></nav>' % esc(c["short"]))
    o('        <h1 class="post-title reveal">%s</h1>' % esc(c["h1"]))
    o('        <p class="post-lead reveal">%s</p>' % esc(c["lead"]))
    o('      </div>\n    </header>\n    <div class="container-narrow">')
    o(FORMS[c["kind"]])
    o('      <div class="post-body reveal">')
    o(BODY[c["kind"]])
    o('      <h2 id="preguntas">Preguntas frecuentes</h2>\n      <div class="faq-list">')
    for i, (q, a) in enumerate(c["faq"]):
        o('        <details class="faq-item"%s><summary><span>%s</span><i class="faq-plus" aria-hidden="true"></i></summary><p>%s</p></details>' % (" open" if i == 0 else "", esc(q), esc(a)))
    o('      </div>\n      </div>')
    o(APP_ASIDE.replace("{UP}", "../../").replace("Si quieres las calorías de tu plato, no las de la media", "El siguiente paso: saber cuánto comes de verdad")
      .replace("Fotocal estima la ración a partir de una foto, con los mismos datos de esta página, y te deja corregir cada ingrediente y sus gramos antes de guardar.",
               "Una cifra objetivo solo sirve si sabes cuánto comes. Fotocal estima cada plato a partir de una foto, te deja corregir los gramos antes de guardar y compara el día con tu objetivo."))
    o('      <p class="post-disclaimer reveal">Información general, no consejo médico. Si estás embarazada, tienes una enfermedad, eres menor de 18 años o has tenido un trastorno de la conducta alimentaria, habla antes con un médico o dietista.</p>')
    o('      <nav class="dp-related reveal" aria-label="Páginas relacionadas">\n        <h2>Seguir por aquí</h2>\n        <div class="post-nav">')
    for x in CALCS:
        if x["slug"] != c["slug"]:
            o('          <a class="post-nav-item" href="../%s/"><small>Calculadora</small><strong>%s</strong></a>' % (x["slug"], esc(x["h1"])))
    o('          <a class="post-nav-item" href="../../calorias/"><small>Tabla</small><strong>Calorías de los platos españoles, por ración y por 100 g</strong></a>')
    for b in c["blog"]:
        o('          <a class="post-nav-item" href="../../blog/%s/"><small>Del blog</small><strong>%s</strong></a>' % (b, esc(blog_title(b))))
    o('        </div>\n      </nav>')
    o('    </div>\n  </article>\n</main>')
    o(foot(2).replace('<script src="../../assets/js/main.js"></script>', '<script src="../../assets/js/main.js"></script>\n<script src="../../assets/js/calc.js"></script>'))
    return "\n".join(out)


def hub():
    title = "Calculadoras de calorías gratis: déficit, IMC y macros"
    desc = "Cuatro calculadoras en la página, sin registro: calorías diarias, déficit calórico, IMC y macros, con la fórmula explicada y el resultado en segundos."
    if len(title) + len(" — Fotocal") <= TITLE_MAX:
        title += " — Fotocal"
    assert len(title) <= TITLE_MAX and 140 <= len(desc) <= 160, (len(title), len(desc))
    path = "calculadoras/"
    url = SITE + path
    ld = [
        ld_block({"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "description": desc, "inLanguage": "es", "url": url, "publisher": ORG,
                  "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": c["h1"], "url": SITE + "calculadoras/%s/" % c["slug"]} for i, c in enumerate(CALCS)]}}),
        ld_block({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE}, {"@type": "ListItem", "position": 2, "name": "Calculadoras", "item": url}]}),
    ]
    out = [head(1, title, desc, path, "\n".join(ld), "website")]
    o = out.append
    o('\n<main id="main">\n  <article class="post dp dp-hub">\n    <header class="post-head">\n      <div class="container-narrow">')
    o('        <nav class="post-crumbs reveal" aria-label="Migas de pan"><a href="../">Inicio</a><span class="sep" aria-hidden="true">/</span><a href="./" aria-current="page">Calculadoras</a></nav>')
    o('        <h1 class="post-title reveal">Calculadoras de calorías, déficit calórico, IMC y macros</h1>')
    o('        <p class="post-lead reveal">Cuatro calculadoras de calorías que responden a las cuatro preguntas que llegan antes de cualquier dieta: cuánto gasto, cuánto recortar, dónde estoy y cómo repartirlo. Funcionan aquí, en la página, sin registro y sin enviar tus datos a ningún sitio; cada una explica su fórmula y lo que no puede saber de ti.</p>')
    o('      </div>\n    </header>\n    <div class="container-narrow">')
    o('      <div class="post-nav reveal" style="margin-top:0">')
    blurb = {"calorias-diarias": "Tu mantenimiento con Mifflin-St Jeor y tu actividad, y las cifras para perder o ganar despacio.",
             "deficit-calorico": "Cuánto recortar para perder entre el 0,5 % y el 1 % de tu peso a la semana, y cuánto tardarías.",
             "imc": "Tu índice de masa corporal, el rango de la OMS en el que cae y el peso que te dejaría en el normal.",
             "macros": "Gramos de proteínas, grasas e hidratos a partir de tus calorías y tu peso, con la regla a la vista."}
    for c in CALCS:
        o('        <a class="post-nav-item" href="%s/"><small>Calculadora</small><strong>%s</strong><span class="hub-text"><span>%s</span></span></a>' % (c["slug"], esc(c["h1"]), esc(blurb[c["slug"]])))
    o('      </div>')
    o('      <div class="post-body reveal">')
    o('      <h2>En qué orden usarlas</h2>')
    o('      <p>Primero las <a href="calorias-diarias/">calorías diarias</a>, que es la base de todo lo demás. Si quieres perder grasa, después el <a href="deficit-calorico/">déficit</a>, que toma esa cifra y te dice cuánto recortar y a qué ritmo. Los <a href="macros/">macros</a> van al final: reparten las calorías que ya tienes decididas. El <a href="imc/">IMC</a> va por libre: sitúa tu peso frente a tu altura, y poco más.</p>')
    o('      <h2>De dónde salen estos números</h2>')
    o('      <p>Cada calculadora explica su fórmula, y el blog la desarrolla: <a href="../blog/understanding-your-basal-metabolic-rate/">qué es la tasa metabólica basal</a>, <a href="../blog/tdee-how-many-calories-you-need/">cuántas calorías necesitas al día (TDEE)</a>, <a href="../blog/calorie-deficit-for-fat-loss/">cómo de grande debe ser un déficit</a>, <a href="../blog/how-fast-should-you-lose-weight/">cuánto peso se puede perder en una semana</a> y <a href="../blog/macronutrients-101/">qué hacen la proteína, los hidratos y la grasa</a>.</p>')
    o('      <h2>Lo que ninguna calculadora puede hacer</h2>')
    o('      <p>Saber cuánto comes de verdad. Todas estas cuentas dan una cifra objetivo; la diferencia entre perder peso o no está en compararla cada día con lo que entra, y ahí es donde casi todo el mundo falla por estimar a ojo. Para eso está la app: una foto del plato, los gramos corregidos si hace falta, y el día comparado con tu objetivo. Y para saber cuánto tienen los platos de aquí, la <a href="../calorias/">tabla de calorías de platos españoles</a>.</p>')
    o('      </div>')
    o(APP_ASIDE.replace("{UP}", "../").replace("Si quieres las calorías de tu plato, no las de la media", "El siguiente paso: saber cuánto comes de verdad")
      .replace("Fotocal estima la ración a partir de una foto, con los mismos datos de esta página, y te deja corregir cada ingrediente y sus gramos antes de guardar.",
               "Una cifra objetivo solo sirve si sabes cuánto comes. Fotocal estima cada plato a partir de una foto, te deja corregir los gramos antes de guardar y compara el día con tu objetivo."))
    o('      <p class="post-disclaimer reveal">Información general, no consejo médico.</p>')
    o('    </div>\n  </article>\n</main>')
    o(foot(1))
    return "\n".join(out)


def main():
    if os.path.isdir(SRC):
        for base, dirs, files in os.walk(SRC, topdown=False):
            for f in files:
                os.remove(os.path.join(base, f))
            for d in dirs:
                os.rmdir(os.path.join(base, d))
    for c in CALCS:
        p = os.path.join(SRC, c["slug"])
        os.makedirs(p, exist_ok=True)
        open(os.path.join(p, "index.html"), "w", encoding="utf-8").write(page(c))
        print("  /calculadoras/%s/" % c["slug"])
    open(os.path.join(SRC, "index.html"), "w", encoding="utf-8").write(hub())
    print("4 calculators + hub -> src/calculadoras/")


if __name__ == "__main__":
    main()
