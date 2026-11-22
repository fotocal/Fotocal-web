# -*- coding: utf-8 -*-
"""/colabora/ — «Colabora con Fotocal» (approved by the owner 22-11-2026).

Owner decisions: contact email fotocal.app@gmail.com; no money mentioned;
free Premium only through the app's redeem system, which does not work
(see below), so the page offers none; Google's official badge; footer link.

Facts checked in the app repo (fotocal/fotocal @ 5119c99, read only):
  · «Enviar a mi nutricionista»: a weekly PDF (Monday to Sunday) made on the
    phone, sent by the user over WhatsApp, email or the share sheet; the
    nutritionist needs no account. Page 1 «Resumen semanal» (average kcal vs
    target, days logged, average protein, weight change, kcal per day, macro
    split, water/steps/workouts); page 2+ «Detalle diario» (each meal).
    Photos and allergies only if the user ticks them. (src/lib/nutritionistHtml.ts,
    src/components/NutritionistShareSheet.tsx, es.json «Se crea en tu teléfono…»)
    The automatic email is built but NOT live: not mentioned here.
  · Referrals: the invite screen shares a plain Google Play link; the reward
    programme ended (supabase/functions/referral v9 «program_ended»); there
    are no codes to redeem (app/redeem*.tsx). So this page promises NO
    referral codes and NO rewards. Free Premium for a professional can only
    be granted by hand (RevenueCat dashboard): an owner decision.
  · Android only (no App Store listing).
"""
import gen_dishes as GD
from gen_pages import LANGS, article, crumbs_html, page, write, check, esc

PATH = "colabora/"
UPDATED = "2026-11-22"
PLAY = GD.PLAY

SHOTS = [("app-scan", 700, 1256, 1080, "Pantalla real de la app: un plato escaneado con sus ingredientes, gramos, calorías y macros",
          "Real app screen: a scanned plate with its ingredients, grams, calories and macros"),
         ("app-home-day", 660, 975, 690, "Pantalla real de la app: el inicio con las calorías ingeridas y las que quedan del día",
          "Real app screen: the home screen with the calories eaten and the calories left for the day"),
         ("app-progress", 600, 1124, 900, "Pantalla real de la app: Mi progreso, media de calorías de la semana y meta de peso",
          "Real app screen: My progress, the week's average calories and the weight goal"),
         ("app-barcode", 700, 1201, 1080, "Pantalla real de la app: un producto escaneado con el código de barras y su ficha nutricional",
          "Real app screen: a product scanned by barcode with its nutrition facts")]

META = {"es": {"title": "Colabora con Fotocal: nutricionistas y creadores — Fotocal",
               "desc": "Cómo trabajar con Fotocal si eres nutricionista, dietista o creas contenido sobre alimentación: informe semanal en PDF, kit de prensa y contacto."},
        "en": {"title": "Partner with Fotocal: dietitians and creators — Fotocal",
               "desc": "How to work with Fotocal if you are a dietitian, nutritionist or food and fitness creator: weekly PDF report, press kit and contact details."}}

SHORT = {"es": "Fotocal es una app para Android que cuenta las calorías de un plato a partir de una foto. Está pensada para la comida española: reconoce el cocido, la tortilla o una ración de bravas, y te deja corregir los gramos antes de guardar. También lee códigos de barras y registra por voz. Hecha en Madrid.",
         "en": "Fotocal is an Android app that counts the calories in a plate from a photo. It is built around Spanish food: it recognises a cocido, a tortilla or a plate of patatas bravas, and lets you correct the grams before saving. It also reads barcodes and logs by voice. Made in Madrid."}



BADGE = {"es": "https://play.google.com/intl/en_us/badges/static/images/badges/es_badge_web_generic.png",
         "en": "https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png"}
EMAIL = "fotocal.app@gmail.com"     # owner's decision 22-11-2026: this address on /colabora/ too


def badge(l):
    """Google's official badge, unmodified, served by Google (the embed code
    from Google's badge generator) and linked to the Play listing."""
    alt = "Disponible en Google Play" if l == "es" else "Get it on Google Play"
    return ('<a class="play-badge" href="%s" target="_blank" rel="noopener"><img src="%s" width="646" height="250" alt="%s" loading="lazy"></a>'
            % (esc(PLAY + "&utm_source=web&utm_medium=colabora&utm_campaign=badge"), BADGE[l], alt))


def body(l):
    es = l == "es"
    o = []
    T = lambda a, b: a if es else b
    # nutritionists
    o.append('      <h2 id="%s">%s</h2>' % (T("nutricionistas", "dietitians"), T("Para nutricionistas y dietistas-nutricionistas", "For dietitians and nutritionists")))
    o.append('      <p>%s</p>' % T(
        "Muchos de tus clientes ya apuntan lo que comen. Con Fotocal lo hacen con una foto, y la app tiene una función pensada para ti: <strong>«Enviar a mi nutricionista»</strong>.",
        "Many of your clients already log what they eat. With Fotocal they do it with a photo, and the app has a feature made for you: <strong>“Send to my nutritionist”</strong>."))
    o.append('      <ul>%s</ul>' % "".join("<li>%s</li>" % x for x in (T(
        ["Cada semana, de lunes a domingo, tu cliente genera en su móvil un informe en PDF.",
         "Primera página, «Resumen semanal»: media de calorías frente a su objetivo, días registrados, proteína media, cambio de peso, calorías de cada día, reparto de macros, y agua, pasos y entrenamientos.",
         "Después, «Detalle diario»: cada comida con su ración, calorías y macros.",
         "Te lo envía él mismo por WhatsApp o por email. Tú no necesitas cuenta ni instalar nada.",
         "Las fotos de las comidas y las alergias solo van si tu cliente lo marca, y puede ocultar su nombre. El PDF se crea en su teléfono."],
        ["Every week, Monday to Sunday, your client creates a PDF report on their phone.",
         "Page one, “Weekly summary”: average calories against their target, days logged, average protein, weight change, calories for each day, macro split, and water, steps and workouts.",
         "Then “Daily detail”: each meal with its portion, calories and macros.",
         "They send it to you themselves over WhatsApp or email. You need no account and nothing to install.",
         "Meal photos and allergies are only included if your client ticks them, and they can hide their name. The PDF is created on their phone."]))))
    o.append('      <h3>%s</h3>' % T("Cómo trabajar con nosotros", "How to work with us"))
    o.append('      <ul><li>%s</li><li>%s</li><li>%s</li></ul>' % (
        T("Recomienda la app a tus clientes con el enlace de Google Play. El plan gratis no pide tarjeta: 2 escaneos con IA y 1 registro por voz al día; código de barras y Coach Kal sin límite.",
          "Recommend the app to your clients with the Google Play link. The free plan needs no card: 2 AI scans and 1 voice log a day; barcode scanner and Coach Kal unlimited."),
        T("Cuéntanos qué le falta al informe semanal para que te sea más útil en consulta.",
          "Tell us what the weekly report is missing to make it more useful in your practice."),
        T("Si escribes sobre alimentación, usa con libertad nuestras cifras y el kit de prensa de abajo.",
          "If you write about food, feel free to use our figures and the press kit below.")))
    o.append('      <p>%s</p>' % T(
        "Fotocal no da consejo médico ni dietético ni sustituye a un profesional: es una herramienta de registro.",
        "Fotocal gives no medical or dietary advice and does not replace a professional: it is a logging tool."))
    # creators
    o.append('      <h2 id="%s">%s</h2>' % (T("creadores", "creators"), T("Para creadores de contenido y blogs de nutrición o fitness", "For nutrition and fitness creators and bloggers")))
    o.append('      <p>%s</p>' % T(
        "Si hablas de contar calorías, de comer bien o de apps para hacerlo, prueba Fotocal y, si te convence, cuéntalo a tu manera.",
        "If you talk about counting calories, eating well or the apps that help, try Fotocal and, if it convinces you, tell people about it in your own words."))
    o.append('      <ul><li>%s</li><li>%s</li><li>%s</li></ul>' % (
        T("Las capturas, el logo y los textos del kit de prensa de abajo, para usar libremente al hablar de Fotocal.",
          "The screenshots, logo and texts in the press kit below, free to use when you write about Fotocal."),
        T("Datos propios para tus artículos: las calorías de 218 platos y alimentos españoles con su ración, en la <a href=\"../calorias/tabla-de-calorias/\">tabla de calorías</a>, con la fuente de cada cifra en la <a href=\"../metodologia/\">metodología</a>.",
          "Our own data for your articles: the calories of 218 Spanish dishes and foods with their serving, in the <a href=\"../calorias/tabla-de-calorias/\">calorie table</a>, with the source of every figure in the <a href=\"../metodologia/\">methodology</a>."),
        T("Si tienes una duda sobre la app o quieres una captura concreta, escríbenos.",
          "If you have a question about the app or want a particular screenshot, write to us.")))
    o.append('      <p>%s</p>' % T(
        "No pedimos enlaces ocultos ni reseñas en Google Play, y nunca reseñas falsas. Opina con libertad: si algo no te gusta de la app, también nos sirve saberlo.",
        "We do not ask for hidden links or Google Play reviews, and never fake reviews. Say what you think: if you dislike something in the app, that is useful to us too."))
    # press kit
    o.append('      <h2 id="%s">%s</h2>' % (T("kit-de-prensa", "press-kit"), T("Kit de prensa", "Press kit")))
    o.append('      <h3>%s</h3>\n      <p>%s</p>' % (T("Descripción corta", "Short description"), SHORT[l]))
    o.append('      <p>%s <a href="%s" target="_blank" rel="noopener">%s</a></p>' % (T("Enlace a Google Play:", "Google Play link:"), esc(PLAY), "play.google.com/store/apps/details?id=com.fotokal.app"))
    o.append('      <h3>%s</h3>' % T("Logo", "Logo"))
    o.append('      <p class="kit-logo"><a href="/assets/img/logo.png" download><img src="/assets/img/logo-96.png" width="96" height="96" alt="%s" loading="lazy"></a> <a href="/assets/img/logo.png" download>%s</a></p>'
             % (T("Logo de Fotocal", "Fotocal logo"), T("Descargar el logo (PNG, 512 × 512)", "Download the logo (PNG, 512 × 512)")))
    o.append('      <h3>%s</h3>' % T("Cuatro capturas de la app", "Four app screenshots"))
    o.append('      <div class="kit-shots">%s</div>' % "".join(
        '<a href="/assets/img/screens/%s-%d-%s.webp" download><img src="/assets/img/screens/%s-%d-%s.webp" width="%d" height="%d" alt="%s" loading="lazy"></a>'
        % (stem, big, l, stem, small, l, small, h, (alt_es if es else alt_en)) for stem, small, h, big, alt_es, alt_en in SHOTS))
    o.append('      <p>%s</p>' % T("Toca una captura para descargarla en tamaño grande. Las capturas son de la app real, en español y en inglés según el idioma de esta página.",
                                   "Tap a screenshot to download it full size. They are from the real app, in English or Spanish to match this page."))
    o.append('      <h3>%s</h3>' % T("Insignia «Disponible en Google Play»", "“Get it on Google Play” badge"))
    o.append('      <p>%s</p>' % T(
        "La insignia oficial de Google, enlazada a nuestra ficha. Si la usas, cógela de la página de insignias de Google (play.google.com/intl/es/badges/) y no la modifiques.",
        "Google's official badge, linked to our listing. If you use it, take it from Google's badge page (play.google.com/intl/en/badges/) and do not modify it."))
    o.append('      <p class="kit-badge">%s</p>' % badge(l))
    o.append('      <p class="kit-legal">%s</p>' % T("Google Play y el logotipo de Google Play son marcas de Google LLC.", "Google Play and the Google Play logo are trademarks of Google LLC."))
    # contact
    o.append('      <h2 id="%s">%s</h2>' % (T("contacto", "contact"), T("Contacto", "Contact")))
    o.append('      <p>%s <a href="mailto:%s">%s</a>%s</p>' % (
        T("Escríbenos a", "Write to us at"), EMAIL, EMAIL,
        T(", o desde el <a href=\"../contact/\">formulario de contacto</a>, y cuéntanos quién eres y qué te interesa.",
          ", or through the <a href=\"../contact/\">contact form</a>, and tell us who you are and what interests you.")))
    return "\n".join(o)


def colabora():
    check({l: {"title": META[l]["title"].replace(" — Fotocal", ""), "desc": META[l]["desc"]} for l in LANGS})
    blocks = []
    for l in LANGS:
        home, me = ("Inicio", "Colabora") if l == "es" else ("Home", "Partner with us")
        h1 = "Colabora con Fotocal" if l == "es" else "Partner with Fotocal"
        lead = ("Para nutricionistas, dietistas y creadores de contenido sobre alimentación y fitness: qué hace la app por tus clientes y tu audiencia, cómo trabajar con nosotros y cómo escribirnos."
                if l == "es" else "For dietitians, nutritionists and food and fitness creators: what the app does for your clients and audience, how to work with us and how to reach us.")
        blocks.append(article(l, h1, lead, body(l), UPDATED, crumbs_html(l, [(home, "../"), (me, "./")]), "", extra_class="colabora"))
    write(PATH + "index.html", page(1, PATH, META, blocks, "colabora"))


if __name__ == "__main__":
    colabora()
    print("/colabora/ written")
