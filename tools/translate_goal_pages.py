#!/usr/bin/env python3
"""
Translate the three goal pages and wire them to the language toggle.

    python3 tools/extract_goal_pages.py > tools/goal_pages_en.json
    python3 tools/translate_goal_pages.py

Reads the manifest of English strings, rewrites each page so every one of
them carries a data-i18n (or data-i18n-html) attribute, and writes a
paste-ready dictionary block to tools/goal_pages_i18n.js.

WHY KEYS AND NOT data-lang-block
The blog ships both languages in the document because an article body is
far too long to sit in a dictionary. These pages are a different shape:
~35 short strings each, wrapped around images that would otherwise be
duplicated (and the hero carries fetchpriority=high, so a hidden copy
would be fetched twice). Keys keep one DOM, one copy of each image, and
make EN/ES parity something the checker can prove rather than something
you have to eyeball.

The English is taken from the page verbatim — this script never rewrites
it, only attaches an attribute — so translating cannot quietly reword the
original.
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Spanish ─────────────────────────────────────────────────────────
# Written against the exact English in tools/goal_pages_en.json.
# Voice matches the rest of the site's Spanish: informal "tú", plain
# words, em-dashes kept, no exclamation marks. Product nouns that the app
# itself does not translate (Coach Kal, Health Connect, Fotocal) stay put;
# ones it does (Informe Semanal, anillo de calorías) are translated.

ES = {
# ─────────────── WEIGHT LOSS ───────────────
"sp.weight-loss.t01": "Pérdida de peso",
"sp.weight-loss.t02": "Pierde peso sin convertir la comida en <em class=\"accent\">un segundo trabajo</em>.",
"sp.weight-loss.t03": "Perder peso se reduce a una cosa: un déficit calórico suave y constante que puedas mantener de verdad. Fotocal hace que la parte de registrar sea casi gratis — tú haces la foto, él hace las cuentas — para que te concentres en el hábito y no en la hoja de cálculo.",
"sp.weight-loss.t04": "El método",
"sp.weight-loss.t05": "Cuatro pasos para perder peso <em class=\"accent\">de forma sostenible</em>.",
"sp.weight-loss.t06": "Sin dietas milagro y sin alimentos prohibidos. Solo un ciclo repetible que encaja en tu vida real.",
"sp.weight-loss.t07": "Ponte un objetivo realista",
"sp.weight-loss.t08": "Dile a Fotocal tu edad, altura, peso, actividad y objetivo. Te fija un objetivo diario de calorías y macros pensado para un ritmo seguro de ~0,5&ndash;1&nbsp;kg por semana: lo bastante rápido para notar el progreso y lo bastante suave para mantenerlo.",
"sp.weight-loss.t09": "Registra las comidas con una foto",
"sp.weight-loss.t10": "Fotografía tu plato y la IA estima las calorías y los macros en segundos. Cuando registrar es así de rápido, de verdad sigues haciéndolo — y la constancia es lo que hace que se pierda peso.",
"sp.weight-loss.t11": "Mantén un déficit suave",
"sp.weight-loss.t12": "Tu anillo de calorías te enseña cuánto margen te queda en el día. Fotocal te empuja hacia opciones con más proteína y mejor calidad, para que te llenes con menos calorías.",
"sp.weight-loss.t13": "Sigue la tendencia, no la báscula",
"sp.weight-loss.t14": "El peso sube y baja cada día con el agua y la sal. La gráfica de peso de Fotocal suaviza ese ruido para que veas la dirección real — y la ajustes con tu Informe Semanal.",
"sp.weight-loss.t15": "Por qué importa la foto",
"sp.weight-loss.t16": "Que registrar no cueste nada lo es todo",
"sp.weight-loss.t17": "Casi todo el mundo abandona el conteo de calorías en la primera semana; no porque no funcione, sino porque es un rollo. Fotocal quita el rollo. Una foto sustituye a la búsqueda en la base de datos, al pesado y a las suposiciones, así que el hábito sobrevive más allá del tercer día.",
"sp.weight-loss.t18": "Escaneo con IA por foto para comida casera y de restaurante",
"sp.weight-loss.t19": "Lector de códigos de barras para productos envasados",
"sp.weight-loss.t20": "La puntuación de calidad te señala alternativas más saciantes y con menos calorías",
"sp.weight-loss.t21": "El recuento automático de pasos con Health Connect alimenta tu presupuesto diario",
"sp.weight-loss.t22": "Mantener la constancia",
"sp.weight-loss.t23": "Un coach en el bolsillo para los días difíciles",
"sp.weight-loss.t24": "Los estancamientos y las comidas con gente son donde se rompen las dietas. Coach Kal conoce tu diario y tus objetivos, así que puede decirte qué pedir en un restaurante, por qué se ha parado la báscula o cómo gastar las calorías que te quedan — sin culpa y sin normas extremas.",
"sp.weight-loss.t25": "Coach Kal: consejos prácticos y sin juzgar, a cualquier hora",
"sp.weight-loss.t26": "Las rachas convierten el registro diario en un hábito",
"sp.weight-loss.t27": "El Informe Semanal te enseña qué funcionó y qué cambiar",
"sp.weight-loss.t28": "Registra por foto, voz o código de barras — lo que sea más rápido",
"sp.weight-loss.t30": "Los mejores alimentos para perder peso",
"sp.weight-loss.t31": "¿A qué velocidad deberías perder peso?",
"sp.weight-loss.t32": "El déficit calórico, explicado",
"sp.weight-loss.t33": "Empieza a perder peso de forma sostenible.",
"sp.weight-loss.t34": "Descarga Fotocal, fija tu objetivo y deja que una foto haga lo difícil.",

# ─────────────── NUTRITION & DIET ───────────────
"sp.nutrition-diet.t01": "Nutrición y dieta",
"sp.nutrition-diet.t02": "Entiende lo que comes — <em class=\"accent\">no solo cuánto</em>.",
"sp.nutrition-diet.t03": "Las calorías son solo la mitad de la historia. Fotocal te enseña la proteína, los carbohidratos y la grasa que hay detrás de cada comida, puntúa su calidad y te propone alternativas más sanas, para que comas mejor y no solo menos. Y se adapta a tu forma de comer, sea cual sea.",
"sp.nutrition-diet.t04": "Lo que te cuenta cada comida",
"sp.nutrition-diet.t05": "El cuadro nutricional completo, <em class=\"accent\">en una foto</em>.",
"sp.nutrition-diet.t06": "Calorías y macros",
"sp.nutrition-diet.t07": "Cada comida se desglosa en calorías, proteínas, carbohidratos y grasas, con totales diarios que se van sumando frente a tus objetivos.",
"sp.nutrition-diet.t08": "Puntuación de calidad (1&ndash;10)",
"sp.nutrition-diet.t09": "Una puntuación sencilla valora lo nutritiva que es cada comida, así aprendes qué es «bueno» sin necesidad de una carrera en nutrición.",
"sp.nutrition-diet.t10": "Alternativas más sanas",
"sp.nutrition-diet.t11": "Fotocal propone cambios pequeños y realistas — una proteína más magra, más fibra, menos azúcar añadido — para subir la calidad de una comida.",
"sp.nutrition-diet.t12": "Hidratación",
"sp.nutrition-diet.t13": "Registra el agua junto con la comida, porque comer bien no va solo de lo que hay en el plato.",
"sp.nutrition-diet.t14": "Registra lo que sea, rápido",
"sp.nutrition-diet.t15": "Tres formas de capturar una comida",
"sp.nutrition-diet.t16": "Comas como comas, Fotocal tiene una forma rápida de registrarlo — sin recorrer bases de datos infinitas.",
"sp.nutrition-diet.t17": "<strong>Escaneo por foto</strong> — apunta la cámara a cualquier plato, en casa o en un restaurante",
"sp.nutrition-diet.t18": "<strong>Escaneo de código de barras</strong> — nutrición instantánea de productos envasados",
"sp.nutrition-diet.t19": "<strong>Escaneo de carta</strong> — fotografía la carta de un restaurante y te dice qué opción encaja mejor",
"sp.nutrition-diet.t20": "Cualquier forma de comer",
"sp.nutrition-diet.t21": "Pensado alrededor de tu dieta, no en su contra",
"sp.nutrition-diet.t22": "Fotocal lleva los números para que el enfoque que tú elijas sea fácil de seguir — nunca te impone una dieta.",
"sp.nutrition-diet.t23": "Objetivos con más proteína y enfocados a la masa muscular",
"sp.nutrition-diet.t24": "Alimentación baja en carbohidratos y estilo keto",
"sp.nutrition-diet.t25": "Platos vegetarianos y de base vegetal",
"sp.nutrition-diet.t26": "Comer equilibrado y sin normas, pero con más conciencia",
"sp.nutrition-diet.t27": "Orientación hecha a tu medida",
"sp.nutrition-diet.t28": "Pregúntale a Coach Kal <em class=\"accent\">lo que quieras</em> sobre comida.",
"sp.nutrition-diet.t29": "«¿Qué pido esta noche en un italiano?» «¿Cómo tomo más proteína sin más calorías?» Coach Kal ve tu diario y tus objetivos y responde con consejos concretos y realistas — además de recomendaciones personalizadas y un Informe Semanal que enseña hacia dónde va de verdad tu alimentación.",
"sp.nutrition-diet.t31": "Macronutrientes 101",
"sp.nutrition-diet.t32": "Qué aspecto tiene un plato equilibrado",
"sp.nutrition-diet.t33": "La fibra: el nutriente infravalorado",
"sp.nutrition-diet.t34": "Come mejor, una foto cada vez.",
"sp.nutrition-diet.t35": "Descarga Fotocal y descubre toda la historia nutricional que hay detrás de cada comida.",

# ─────────────── LIFESTYLE & MINDSET ───────────────
"sp.lifestyle-mindset.t01": "Hábitos y mentalidad",
"sp.lifestyle-mindset.t02": "Hábitos saludables que <em class=\"accent\">de verdad duran</em>.",
"sp.lifestyle-mindset.t03": "Lo difícil de comer bien no es saber qué hacer: es mantenerlo cuando la vida se complica. Fotocal está construido alrededor de la psicología del hábito — pequeñas victorias, empujones suaves y un coach que nunca te hace sentir culpable.",
"sp.lifestyle-mindset.t04": "Cómo se forman los hábitos",
"sp.lifestyle-mindset.t05": "Pequeñas victorias, <em class=\"accent\">repetidas</em>.",
"sp.lifestyle-mindset.t06": "Fotocal está diseñado para que la opción sana sea también la fácil — y cada día que apareces, se vuelve más fácil.",
"sp.lifestyle-mindset.t07": "Que no cueste nada",
"sp.lifestyle-mindset.t08": "Basta una foto para registrar una comida. Cuando el esfuerzo es mínimo, el hábito sobrevive a los días de locura que normalmente lo rompen.",
"sp.lifestyle-mindset.t09": "Crea una racha",
"sp.lifestyle-mindset.t10": "Tu racha diaria convierte la constancia en un pequeño juego que vale la pena proteger. Lo que te lleva es la inercia, no la motivación.",
"sp.lifestyle-mindset.t11": "Observa, no te castigues",
"sp.lifestyle-mindset.t12": "Una nota rápida de ánimo junto a tus comidas revela cómo se conectan la comida y las emociones — conciencia, nunca culpa.",
"sp.lifestyle-mindset.t13": "Ajusta cada semana",
"sp.lifestyle-mindset.t14": "Tu Informe Semanal celebra lo que ha ido bien y señala una sola cosa pequeña que cambiar: un ritmo de mejora sostenible.",
"sp.lifestyle-mindset.t15": "La mentalidad correcta",
"sp.lifestyle-mindset.t16": "Sin culpa y sin todo o nada",
"sp.lifestyle-mindset.t17": "Una comida generosa no borra tu progreso; abandonar sí. Coach Kal está hecho para que sigas adelante después de un desliz en vez de entrar en barrena, con ánimos que te tratan como a un adulto.",
"sp.lifestyle-mindset.t18": "Coaching sin juicios, disponible a cualquier hora",
"sp.lifestyle-mindset.t19": "Diario de ánimo y hábitos para detectar tus patrones reales",
"sp.lifestyle-mindset.t20": "Fíjate en la tendencia, no en un mal día",
"sp.lifestyle-mindset.t21": "Encaja en la vida real",
"sp.lifestyle-mindset.t22": "Una estructura suave que no se mete en medio",
"sp.lifestyle-mindset.t23": "Fotocal acompaña tu rutina en lugar de gobernarla — los recordatorios llegan cuando ayudan, y registrar lleva segundos lo hagas como lo hagas.",
"sp.lifestyle-mindset.t24": "Recordatorios inteligentes en los momentos en que sueles olvidarte",
"sp.lifestyle-mindset.t25": "Registra por foto, código de barras, carta o voz — en segundos",
"sp.lifestyle-mindset.t26": "Recomendaciones personalizadas que se adaptan a tu semana",
"sp.lifestyle-mindset.t28": "Cómo mantener la constancia con los hábitos saludables",
"sp.lifestyle-mindset.t29": "Alimentación consciente: guía para principiantes",
"sp.lifestyle-mindset.t30": "Comer por emociones, explicado",
"sp.lifestyle-mindset.t31": "Crea hábitos que puedas mantener para siempre.",
"sp.lifestyle-mindset.t32": "Descarga Fotocal y convierte el comer bien en algo que por fin se queda.",
}

# "Guides" already exists in the shared dictionary as feat.guides — reuse it
# rather than minting a third copy of a one-word string per page.
SHARED = {"Guides": "feat.guides"}


def main():
    manifest = json.load(open(os.path.join(ROOT, "tools", "goal_pages_en.json"), encoding="utf-8"))
    en_out, es_out = {}, {}
    missing = []

    for slug, items in manifest.items():
        path = os.path.join(ROOT, "features", slug, "index.html")
        src = open(path, encoding="utf-8").read()
        head, body, tail = src.partition("<main")
        body = body + tail if False else src[src.index("<main"):src.index("</main>")]
        before = src[:src.index("<main")]
        after = src[src.index("</main>"):]

        applied = 0
        for it in items:
            key, inner, tag = it["key"], it["en"], it["tag"]
            shared = SHARED.get(it["text"])
            use_key = shared or key

            if not shared:
                if key not in ES:
                    missing.append(key)
                    continue
                en_out[key] = inner
                es_out[key] = ES[key]

            attr = "data-i18n-html" if it["html"] else "data-i18n"
            # Rewrite the FIRST matching open tag that wraps exactly this
            # inner HTML. Anchoring on the inner content (not on the tag
            # alone) is what keeps this from tagging the wrong element.
            pat = re.compile(r"<%s\b((?:(?!data-i18n)[^>])*?)>%s</%s>"
                             % (tag, re.escape(inner), tag))
            m = pat.search(body)
            if not m:
                missing.append(key + " (no match in HTML)")
                continue
            repl = '<%s%s %s="%s">%s</%s>' % (tag, m.group(1), attr, use_key, inner, tag)
            body = body[:m.start()] + repl + body[m.end():]
            applied += 1

        open(path, "w", encoding="utf-8").write(before + body + after)
        print("%-20s tagged %d/%d" % (slug, applied, len(items)))

    if missing:
        print("\nMISSING:", file=sys.stderr)
        for k in missing:
            print("  " + k, file=sys.stderr)
        sys.exit(1)

    out = os.path.join(ROOT, "tools", "goal_pages_i18n.js")
    with open(out, "w", encoding="utf-8") as f:
        f.write("/* GENERATED by tools/translate_goal_pages.py — paste into assets/js/i18n-pages.js */\n\n")
        for label, d in (("EN", en_out), ("ES", es_out)):
            f.write("/* ===== %s ===== */\n" % label)
            for k in en_out:                      # EN order both times
                f.write('      %s: %s,\n' % (json.dumps(k), json.dumps(d[k], ensure_ascii=False)))
            f.write("\n")
    print("\n%d keys per language -> tools/goal_pages_i18n.js" % len(en_out))


if __name__ == "__main__":
    main()
