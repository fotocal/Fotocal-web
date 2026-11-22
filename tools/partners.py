# -*- coding: utf-8 -*-
"""/colabora/ — «Colabora con Fotocal» (DRAFT, branch partners-draft, 22-11-2026).

noindex and linked from nowhere until the owner approves it. Places marked
[OWNER TO DECIDE] are left for the owner on purpose.

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

OWNER = '<span class="owner-todo">[%s]</span>'


def body(l):
    es = l == "es"
    o = []
    T = lambda a, b: a if es else b
    o.append('      <p class="draft-note"><strong>%s</strong> %s</p>' % (
        T("Borrador.", "Draft."), T("Esta página no está publicada en buscadores ni enlazada desde la web hasta que la apruebe el propietario.",
                                   "This page is not indexed or linked from the site until the owner approves it.")))
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
    o.append('      <h3>%s</h3>' % T("Lo que te ofrecemos", "What we offer you"))
    o.append('      <ul><li>%s</li><li>%s</li><li>%s</li></ul>' % (
        T("Premium gratis para que pruebes la app con calma: ", "Free Premium so you can try the app properly: ") + OWNER % T("OWNER TO DECIDE: duración, p. ej. 6 o 12 meses; se activa a mano en tu cuenta", "OWNER TO DECIDE: length, e.g. 6 or 12 months; activated by hand on your account"),
        T("Para tus clientes, el enlace de descarga. El plan gratis no pide tarjeta: 2 escaneos con IA y 1 registro por voz al día; código de barras y Coach Kal sin límite. El informe semanal se puede enviar desde la app.",
          "For your clients, the download link. The free plan needs no card: 2 AI scans and 1 voice log a day; barcode scanner and Coach Kal unlimited. The weekly report can be sent from the app."),
        T("Escuchamos lo que te falte en el informe: si algo te ayudaría a trabajar mejor con tus clientes, nos lo dices.",
          "We listen to what the report is missing: if something would help you work better with your clients, tell us.")))
    o.append('      <p>%s</p>' % T(
        "Para que quede claro: la app no tiene ahora un programa de códigos de invitación ni recompensas por traer clientes. Y Fotocal no da consejo médico ni dietético ni sustituye a un profesional: es una herramienta de registro.",
        "To be clear: the app does not currently have an invite-code programme or rewards for bringing clients. And Fotocal gives no medical or dietary advice and does not replace a professional: it is a logging tool."))
    # creators
    o.append('      <h2 id="%s">%s</h2>' % (T("creadores", "creators"), T("Para creadores de contenido y blogs de nutrición o fitness", "For nutrition and fitness creators and bloggers")))
    o.append('      <p>%s</p>' % T(
        "Si hablas de contar calorías, de comer bien o de apps para hacerlo, puedes probar Fotocal y, si te convence, contarlo a tu manera.",
        "If you talk about counting calories, eating well or the apps that help, you can try Fotocal and, if it convinces you, tell people about it in your own words."))
    o.append('      <ul><li>%s</li><li>%s</li><li>%s</li><li>%s</li></ul>' % (
        T("Premium gratis para probarla: ", "Free Premium to try it: ") + OWNER % T("OWNER TO DECIDE: duración", "OWNER TO DECIDE: length"),
        T("Comisión opcional por suscripciones: ", "Optional commission on subscriptions: ") + OWNER % T("OWNER TO DECIDE: importe y condiciones. No hay pagos automáticos: se acordaría por escrito y se pagaría a mano", "OWNER TO DECIDE: amount and terms. There are no automatic payouts: it would be agreed in writing and paid by hand"),
        T("Las capturas, el logo y los textos del kit de prensa de abajo, para usar libremente al hablar de Fotocal.",
          "The screenshots, logo and texts in the press kit below, free to use when you write about Fotocal."),
        T("Datos propios para tus artículos: las calorías de 218 platos y alimentos españoles con su ración, en la <a href=\"../calorias/tabla-de-calorias/\">tabla de calorías</a>, con la fuente de cada cifra en la <a href=\"../metodologia/\">metodología</a>.",
          "Our own data for your articles: the calories of 218 Spanish dishes and foods with their serving, in the <a href=\"../calorias/tabla-de-calorias/\">calorie table</a>, with the source of every figure in the <a href=\"../metodologia/\">methodology</a>.")))
    o.append('      <h3>%s</h3>' % T("Nuestras reglas", "Our rules"))
    o.append('      <ul><li>%s</li><li>%s</li><li>%s</li></ul>' % (
        T("Si recibes algo a cambio (Premium gratis o comisión), dilo a tu audiencia y marca el enlace como patrocinado (<code>rel=\"sponsored\"</code>), como piden Google y la normativa de publicidad.",
          "If you get something in return (free Premium or a commission), tell your audience and mark the link as sponsored (<code>rel=\"sponsored\"</code>), as Google and advertising rules require."),
        T("No compramos enlaces ocultos ni pedimos reseñas en Google Play a cambio de nada. Nada de reseñas falsas.",
          "We do not buy hidden links or ask for Google Play reviews in exchange for anything. No fake reviews."),
        T("Opina con libertad: si algo no te gusta de la app, también nos sirve saberlo.",
          "Say what you think: if you dislike something in the app, that is useful to us too.")))
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
        "Usa la insignia oficial de Google, sin modificarla, desde su página de insignias (play.google.com/intl/es/badges/), enlazada a nuestra ficha de Google Play. " + OWNER % "OWNER TO DECIDE: ¿la descargamos y la ponemos aquí?",
        "Use Google's official badge, unmodified, from their badge page (play.google.com/intl/en/badges/), linked to our Google Play listing. " + OWNER % "OWNER TO DECIDE: shall we download it and host it here?"))
    # contact
    o.append('      <h2 id="%s">%s</h2>' % (T("contacto", "contact"), T("Contacto", "Contact")))
    o.append('      <p>%s %s</p>' % (
        T("Escríbenos desde el <a href=\"../contact/\">formulario de contacto</a> y cuéntanos quién eres y qué te interesa, o por email:",
          "Write to us through the <a href=\"../contact/\">contact form</a> and tell us who you are and what interests you, or by email:"),
        OWNER % T("OWNER TO DECIDE: qué email poner aquí", "OWNER TO DECIDE: which email to show here")))
    return "\n".join(o)


def colabora():
    check({l: {"title": META[l]["title"].replace(" — Fotocal", ""), "desc": META[l]["desc"]} for l in LANGS})
    blocks = []
    for l in LANGS:
        home, me = ("Inicio", "Colabora") if l == "es" else ("Home", "Partner with us")
        h1 = "Colabora con Fotocal" if l == "es" else "Partner with Fotocal"
        lead = ("Para nutricionistas, dietistas y creadores de contenido sobre alimentación y fitness: qué hace la app por tus clientes y tu audiencia, qué te ofrecemos y cómo escribirnos."
                if l == "es" else "For dietitians, nutritionists and food and fitness creators: what the app does for your clients and audience, what we offer you and how to reach us.")
        blocks.append(article(l, h1, lead, body(l), UPDATED, crumbs_html(l, [(home, "../"), (me, "./")]), "", extra_class="colabora"))
    write(PATH + "index.html", page(1, PATH, META, blocks, "colabora", noindex=True))


if __name__ == "__main__":
    colabora()
    print("draft /colabora/ written (noindex)")
