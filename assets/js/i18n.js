/* ═══════════════════════════════════════════════════════════════
   FOTOCAL — translations
   DEFAULT LANGUAGE IS ENGLISH. Spanish is opt-in via the EN/ES toggle
   and is remembered in localStorage ("fotocal-lang").

   RULES FOR ADDING STRINGS
   1. Every key MUST exist in BOTH `en` and `es`. A missing Spanish key
      silently falls back to English (and vice versa) — which is exactly
      the "Spanish leaking into English" bug we are trying to kill, so
      add both at the same time.
   2. Keys ending in nothing special -> injected with textContent.
      Keys used with data-i18n-html -> injected with innerHTML (only
      these may contain markup).
   3. This file must be saved as UTF-8. Spanish accents (á é í ó ú ñ
      ¿ ¡) and the € sign must survive. If you ever see Ã or ð in the
      rendered page, the file was saved with the wrong encoding.
   ═══════════════════════════════════════════════════════════════ */
window.FOTOCAL_I18N = {

  /* ══════════════════════ ENGLISH (default) ══════════════════════ */
  en: {
    /* ── Nav ── */
    "nav.skip": "Skip to content",
    "nav.home": "Home",
    "nav.features": "Features",
    "nav.weightLoss": "Weight Loss",
    "nav.nutrition": "Nutrition & Diet",
    "nav.lifestyle": "Lifestyle & Mindset",
    "nav.blog": "Blog",
    "nav.subscription": "Subscription",
    "nav.about": "About",
    "nav.aboutUs": "About Us",
    "nav.contactUs": "Contact Us",
    "nav.cta": "Get the app",

    /* ── Screenshot placeholders ── */
    "slot.pending": "Screenshot coming soon",

    /* ── Hero ── */
    "hero.eyebrow": "AI nutrition tracking · Android",
    "hero.title": "One photo. All your calories, <em class=\"accent\">instantly</em>.",
    "hero.sub": "Point your camera at any meal and Fotocal works out the calories, the protein, carbs and fat, and how good the meal actually is for you. No weighing. No scrolling through endless food lists.",
    "hero.perk1": "3-day free trial",
    "hero.perk2": "Works offline",
    "hero.perk3": "English & Spanish",
    "cta.badgeTop": "GET IT ON",
    "hero.slot": "Home screen — calorie ring",

    /* ── How it works ── */
    "how.kicker": "How it works",
    "how.title": "Three steps. <em class=\"accent\">Zero friction</em>.",
    "how.sub": "Logging a meal takes about as long as taking a photo — because that is all it is.",
    "how.s1t": "Snap a photo",
    "how.s1b": "Open Fotocal and photograph your plate. Home-cooked, restaurant, or last night's leftovers — it all works.",
    "how.s1slot": "Scan screen — camera pointed at a plate",
    "how.s2t": "The AI analyses it",
    "how.s2b": "In seconds it identifies the food, estimates the portion, and works out calories, macros and a quality score.",
    "how.s2slot": "Scan result — detected food + macros",
    "how.s3t": "It's logged",
    "how.s3b": "The meal drops straight into your diary and your day updates itself. Nothing else for you to do.",
    "how.s3slot": "Meal diary — the day's logged meals",

    /* ── Feature storytelling ── */
    "feat.kicker": "Inside the app",
    "feat.title": "Everything you eat, <em class=\"accent\">understood</em>.",
    "feat.sub": "Fotocal is not just a camera trick. Here is what you actually do inside it, day to day.",

    "f.scan.pill": "The core of Fotocal",
    "f.scan.t": "AI photo scanning",
    "f.scan.b": "Most tracking apps make you find your food in a database and guess the portion. Fotocal looks at the plate instead. You get calories and macros, a quality score from 1 to 10, and a suggestion for what would make the meal better — and you can always adjust anything before you save it.",
    "f.scan.li1": "Recognises whole dishes, not just single ingredients",
    "f.scan.li2": "Quality score with healthier alternatives",
    "f.scan.li3": "Edit the portion or ingredients before saving",
    "f.scan.slot": "Scan result detail — quality score + alternatives",

    "f.coach.pill": "Your pocket coach",
    "f.coach.t": "Coach Kal, your AI nutrition coach",
    "f.coach.b": "Coach Kal can see your diary and your goals, so the advice is about your actual day rather than generic tips. Ask what to cook with what is in the fridge, what to order at a restaurant, or why the scale has not moved this week. Answers are practical and judgement-free.",
    "f.coach.li1": "Ask anything, any time of day",
    "f.coach.li2": "Advice based on what you actually logged",
    "f.coach.li3": "No guilt, no extreme diets",
    "f.coach.slot": "Coach Kal chat",

    "f.report.pill": "Every week",
    "f.report.t": "Your Weekly Report",
    "f.report.b": "One day at a time tells you very little. Once a week Fotocal pulls everything together: how your calories and macros actually landed, which habits held up, where things slipped, and one or two specific things worth changing next week.",
    "f.report.li1": "Trends across the whole week, not just today",
    "f.report.li2": "What went well and what slipped",
    "f.report.li3": "Concrete suggestions for the week ahead",
    "f.report.slot": "Weekly Report",

    "f.progress.pill": "The long game",
    "f.progress.t": "Progress you can actually see",
    "f.progress.b": "Log your weight and your body measurements and watch the line over weeks and months instead of panicking about a single morning. Weight bounces around day to day — the chart is what tells you the truth.",
    "f.progress.li1": "Weight logging with clear charts",
    "f.progress.li2": "Body measurements over time",
    "f.progress.li3": "Trends that ignore the daily noise",
    "f.progress.slot": "Progress — weight + body measurements",

    /* ── Smaller feature cards ── */
    "more.kicker": "And the rest",
    "more.title": "The small things that <em class=\"accent\">keep you going</em>.",
    "more.c1t": "Streaks",
    "more.c1b": "A daily streak that turns logging into a habit worth keeping alive.",
    "more.c2t": "Offline mode",
    "more.c2b": "Log meals, water and weight with no signal. Everything syncs when you are back online.",
    "more.c3t": "Smart reminders",
    "more.c3b": "A nudge at the moment you would normally forget, not at 3pm for no reason.",
    "more.c4t": "Personalised recommendations",
    "more.c4b": "Suggestions that adapt to your goals, your tastes and how your week is actually going.",

    /* ── Pricing teaser ── */
    "price.kicker": "Subscription",
    "price.title": "Start with a <em class=\"accent\">3-day free trial</em>.",
    "price.sub": "One subscription unlocks everything — unlimited AI scans, unlimited Coach Kal, weekly reports and every premium feature. Pick the length that suits you.",
    "price.mName": "Monthly",
    "price.mPer": "/month",
    "price.mNote": "Full flexibility, cancel anytime.",
    "price.qName": "3 months",
    "price.qPer": "/3 months",
    "price.qNote": "A full season to build the habit.",
    "price.yName": "Yearly",
    "price.yPer": "/year",
    "price.yNote": "Works out at about €2.92/month.",
    "price.yFlag": "BEST VALUE",
    "price.cta": "See what's included",
    "price.fine": "Subscriptions are billed through Google Play and renew automatically. You can cancel anytime from the Play Store.",

    /* ── FAQ ── */
    "faq.kicker": "FAQ",
    "faq.title": "Questions, <em class=\"accent\">answered</em>",
    "faq.q1": "How accurate is the photo scanning?",
    "faq.a1": "Fotocal uses current AI vision models to identify food and estimate portions, and it is good enough that the numbers are genuinely useful day to day. It is an estimate, not a laboratory measurement — mixed dishes, stews and anything layered or hidden under sauce are the hardest cases. You can always correct the portion or the ingredients before you save, and a corrected estimate is still far faster than searching a database.",
    "faq.q2": "Do I have to weigh my food?",
    "faq.a2": "No. Estimating the portion from the photo is the whole point. If you want to be precise on a particular meal you can enter the weight by hand, but nothing requires it.",
    "faq.q3": "Does it work offline?",
    "faq.a3": "Mostly, yes. You can log meals, water and weight with no connection and everything syncs once you are back online. The AI photo analysis itself needs a connection, because that is where the recognition happens.",
    "faq.q4": "Is Fotocal free?",
    "faq.a4": "You can download Fotocal and try it free for 3 days. After that a subscription unlocks unlimited AI scans, unlimited Coach Kal and all premium features — €6.99 monthly, €16.99 for 3 months, or €34.99 yearly.",
    "faq.q5": "How do I cancel?",
    "faq.a5": "Subscriptions are handled by Google Play, so you cancel there: Play Store → your profile → Payments and subscriptions → Subscriptions. Cancel before the 3-day trial ends and you are not charged.",
    "faq.q6": "What happens to my data?",
    "faq.a6": "Your data is yours. We never sell it, and you can delete your account and everything in it at any time.",
    "faq.q7": "Which languages does the app support?",
    "faq.a7": "English and Spanish, both in the app and on this site.",

    /* ── Final CTA ── */
    "cta.title": "Your next meal can <em class=\"accent-light\">count itself</em>.",
    "cta.sub": "Download Fotocal and see how easy eating better gets when the hard part is a photo.",

    /* ── Footer ── */
    "footer.tag": "AI nutrition tracking. One photo and you know what you are eating.",
    "footer.product": "Product",
    "footer.company": "Company",
    "footer.privacy": "Privacy Policy",
    "footer.terms": "Terms of Service",
    "footer.deletion": "Account deletion",
    "footer.rights": "All rights reserved.",
    "footer.made": "Made for people who want to eat better.",

    /* ── Coming-soon stubs ── */
    "soon.badge": "Coming soon",
    "soon.title": "This page is <em class=\"accent\">on its way</em>.",
    "soon.body": "We are still writing this one. In the meantime, the app itself is ready — and everything about how Fotocal works is on the home page.",
    "soon.home": "Back to home",
    "soon.play": "Get the app",
    "soon.contactTitle": "Get in <em class=\"accent\">touch</em>.",
    "soon.contactBody": "Questions, bugs, feedback, or anything about your subscription — email us and a real person will read it.",
    "soon.contactCta": "Email support"
  },

  /* ══════════════════════ SPANISH ══════════════════════ */
  es: {
    /* ── Nav ── */
    "nav.skip": "Saltar al contenido",
    "nav.home": "Inicio",
    "nav.features": "Funciones",
    "nav.weightLoss": "Pérdida de peso",
    "nav.nutrition": "Nutrición y dieta",
    "nav.lifestyle": "Hábitos y mentalidad",
    "nav.blog": "Blog",
    "nav.subscription": "Suscripción",
    "nav.about": "Nosotros",
    "nav.aboutUs": "Sobre nosotros",
    "nav.contactUs": "Contacto",
    "nav.cta": "Descargar",

    /* ── Screenshot placeholders ── */
    "slot.pending": "Captura próximamente",

    /* ── Hero ── */
    "hero.eyebrow": "Nutrición con IA · Android",
    "hero.title": "Una foto. Todas tus calorías, <em class=\"accent\">al instante</em>.",
    "hero.sub": "Apunta con la cámara a cualquier comida y Fotocal calcula las calorías, las proteínas, los carbohidratos y las grasas, y lo buena que es esa comida para ti. Sin pesar nada. Sin buscar en listas interminables.",
    "hero.perk1": "Prueba gratis de 3 días",
    "hero.perk2": "Funciona sin conexión",
    "hero.perk3": "En inglés y español",
    "cta.badgeTop": "DISPONIBLE EN",
    "hero.slot": "Pantalla de inicio — anillo de calorías",

    /* ── How it works ── */
    "how.kicker": "Cómo funciona",
    "how.title": "Tres pasos. <em class=\"accent\">Cero fricción</em>.",
    "how.sub": "Registrar una comida cuesta lo mismo que hacer una foto, porque no es nada más que eso.",
    "how.s1t": "Haz la foto",
    "how.s1b": "Abre Fotocal y fotografía tu plato. Casero, de restaurante o las sobras de ayer: funciona igual.",
    "how.s1slot": "Pantalla de escaneo — cámara apuntando a un plato",
    "how.s2t": "La IA lo analiza",
    "how.s2b": "En segundos identifica la comida, estima la ración y calcula calorías, macros y una puntuación de calidad.",
    "how.s2slot": "Resultado del escaneo — comida detectada + macros",
    "how.s3t": "Queda registrado",
    "how.s3b": "La comida entra directa en tu diario y tu día se actualiza solo. No tienes que hacer nada más.",
    "how.s3slot": "Diario de comidas — las comidas del día",

    /* ── Feature storytelling ── */
    "feat.kicker": "Dentro de la app",
    "feat.title": "Todo lo que comes, <em class=\"accent\">entendido</em>.",
    "feat.sub": "Fotocal no es solo un truco de cámara. Esto es lo que haces dentro, día a día.",

    "f.scan.pill": "El núcleo de Fotocal",
    "f.scan.t": "Escaneo de fotos con IA",
    "f.scan.b": "Casi todas las apps te obligan a buscar la comida en una base de datos y adivinar la ración. Fotocal mira el plato. Obtienes calorías y macros, una puntuación de calidad del 1 al 10 y una sugerencia para mejorar la comida, y siempre puedes ajustar lo que quieras antes de guardar.",
    "f.scan.li1": "Reconoce platos enteros, no solo ingredientes sueltos",
    "f.scan.li2": "Puntuación de calidad con alternativas más sanas",
    "f.scan.li3": "Edita la ración o los ingredientes antes de guardar",
    "f.scan.slot": "Detalle del escaneo — puntuación + alternativas",

    "f.coach.pill": "Tu coach de bolsillo",
    "f.coach.t": "Coach Kal, tu entrenador nutricional con IA",
    "f.coach.b": "Coach Kal ve tu diario y tus objetivos, así que sus consejos van sobre tu día real y no sobre generalidades. Pregúntale qué cocinar con lo que hay en la nevera, qué pedir en un restaurante o por qué la báscula no se mueve esta semana. Respuestas prácticas y sin juzgar.",
    "f.coach.li1": "Pregunta lo que quieras, a cualquier hora",
    "f.coach.li2": "Consejos basados en lo que has registrado de verdad",
    "f.coach.li3": "Sin culpa y sin dietas extremas",
    "f.coach.slot": "Chat de Coach Kal",

    "f.report.pill": "Cada semana",
    "f.report.t": "Tu Informe Semanal",
    "f.report.b": "Un día suelto no te dice casi nada. Una vez por semana Fotocal lo junta todo: cómo quedaron de verdad tus calorías y macros, qué hábitos aguantaron, dónde se torció la cosa y una o dos cosas concretas que vale la pena cambiar la semana que viene.",
    "f.report.li1": "Tendencias de toda la semana, no solo de hoy",
    "f.report.li2": "Qué salió bien y qué se torció",
    "f.report.li3": "Sugerencias concretas para la semana siguiente",
    "f.report.slot": "Informe Semanal",

    "f.progress.pill": "El largo plazo",
    "f.progress.t": "Progreso que se ve de verdad",
    "f.progress.b": "Registra tu peso y tus medidas corporales y mira la línea a lo largo de semanas y meses en vez de agobiarte por una mañana concreta. El peso sube y baja cada día: la gráfica es la que te dice la verdad.",
    "f.progress.li1": "Registro de peso con gráficas claras",
    "f.progress.li2": "Medidas corporales a lo largo del tiempo",
    "f.progress.li3": "Tendencias que ignoran el ruido diario",
    "f.progress.slot": "Progreso — peso + medidas corporales",

    /* ── Smaller feature cards ── */
    "more.kicker": "Y lo demás",
    "more.title": "Las cosas pequeñas que <em class=\"accent\">te mantienen</em>.",
    "more.c1t": "Rachas",
    "more.c1b": "Una racha diaria que convierte el registro en un hábito que merece la pena mantener vivo.",
    "more.c2t": "Modo sin conexión",
    "more.c2b": "Registra comidas, agua y peso sin cobertura. Todo se sincroniza cuando vuelves a tener internet.",
    "more.c3t": "Recordatorios inteligentes",
    "more.c3b": "Un aviso justo cuando sueles olvidarte, no a las tres de la tarde porque sí.",
    "more.c4t": "Recomendaciones personalizadas",
    "more.c4b": "Sugerencias que se adaptan a tus objetivos, tus gustos y cómo te está yendo la semana.",

    /* ── Pricing teaser ── */
    "price.kicker": "Suscripción",
    "price.title": "Empieza con <em class=\"accent\">3 días gratis</em>.",
    "price.sub": "Una suscripción lo desbloquea todo: escaneos con IA ilimitados, Coach Kal sin límites, informes semanales y todas las funciones premium. Elige la duración que te encaje.",
    "price.mName": "Mensual",
    "price.mPer": "/mes",
    "price.mNote": "Flexibilidad total, cancela cuando quieras.",
    "price.qName": "3 meses",
    "price.qPer": "/3 meses",
    "price.qNote": "Una temporada entera para crear el hábito.",
    "price.yName": "Anual",
    "price.yPer": "/año",
    "price.yNote": "Sale a unos 2,92 € al mes.",
    "price.yFlag": "MEJOR PRECIO",
    "price.cta": "Ver qué incluye",
    "price.fine": "Las suscripciones se cobran a través de Google Play y se renuevan automáticamente. Puedes cancelar cuando quieras desde la Play Store.",

    /* ── FAQ ── */
    "faq.kicker": "FAQ",
    "faq.title": "Preguntas, <em class=\"accent\">respondidas</em>",
    "faq.q1": "¿Cómo de precisa es la foto?",
    "faq.a1": "Fotocal usa modelos de visión con IA actuales para identificar la comida y estimar la ración, y funciona lo bastante bien como para que los números te sirvan de verdad en el día a día. Es una estimación, no una medición de laboratorio: los platos mezclados, los guisos y todo lo que va en capas o tapado por una salsa son los casos más difíciles. Siempre puedes corregir la ración o los ingredientes antes de guardar, y aun corrigiendo sigue siendo mucho más rápido que buscar en una base de datos.",
    "faq.q2": "¿Tengo que pesar la comida?",
    "faq.a2": "No. Estimar la ración desde la foto es justamente el objetivo. Si en una comida concreta quieres ser preciso puedes meter el peso a mano, pero nada te obliga.",
    "faq.q3": "¿Funciona sin conexión?",
    "faq.a3": "En su mayoría, sí. Puedes registrar comidas, agua y peso sin conexión y todo se sincroniza cuando vuelves a tener internet. El análisis de la foto con IA sí necesita conexión, porque ahí es donde ocurre el reconocimiento.",
    "faq.q4": "¿Fotocal es gratis?",
    "faq.a4": "Puedes descargar Fotocal y probarlo gratis 3 días. Después, una suscripción desbloquea los escaneos con IA ilimitados, Coach Kal sin límites y todas las funciones premium: 6,99 € al mes, 16,99 € por 3 meses o 34,99 € al año.",
    "faq.q5": "¿Cómo cancelo?",
    "faq.a5": "Las suscripciones las gestiona Google Play, así que se cancelan ahí: Play Store → tu perfil → Pagos y suscripciones → Suscripciones. Si cancelas antes de que terminen los 3 días de prueba, no se te cobra nada.",
    "faq.q6": "¿Qué pasa con mis datos?",
    "faq.a6": "Tus datos son tuyos. Nunca los vendemos y puedes eliminar tu cuenta y todo lo que contiene en cualquier momento.",
    "faq.q7": "¿En qué idiomas está la app?",
    "faq.a7": "En inglés y español, tanto en la app como en esta web.",

    /* ── Final CTA ── */
    "cta.title": "Tu próxima comida puede <em class=\"accent-light\">contarse sola</em>.",
    "cta.sub": "Descarga Fotocal y comprueba lo fácil que es comer mejor cuando la parte difícil es una foto.",

    /* ── Footer ── */
    "footer.tag": "Nutrición con IA. Una foto y sabes qué estás comiendo.",
    "footer.product": "Producto",
    "footer.company": "Empresa",
    "footer.privacy": "Política de Privacidad",
    "footer.terms": "Términos de Servicio",
    "footer.deletion": "Eliminación de cuenta",
    "footer.rights": "Todos los derechos reservados.",
    "footer.made": "Hecho para gente que quiere comer mejor.",

    /* ── Coming-soon stubs ── */
    "soon.badge": "Próximamente",
    "soon.title": "Esta página está <em class=\"accent\">en camino</em>.",
    "soon.body": "Todavía la estamos escribiendo. Mientras tanto, la app ya está lista, y todo sobre cómo funciona Fotocal está en la página de inicio.",
    "soon.home": "Volver al inicio",
    "soon.play": "Descargar la app",
    "soon.contactTitle": "Ponte en <em class=\"accent\">contacto</em>.",
    "soon.contactBody": "Dudas, errores, sugerencias o cualquier cosa sobre tu suscripción: escríbenos y te leerá una persona de verdad.",
    "soon.contactCta": "Escribir a soporte"
  }
};
