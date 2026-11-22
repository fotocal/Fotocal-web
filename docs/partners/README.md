# Partner and backlink programme: DRAFT, nothing published or sent (22 Nov 2026)

Branch `partners-draft`. Not merged, and nobody has been contacted. Everything below waits for the owner's OK.

## 1. Draft page `/colabora/` (ES) and `/en/colabora/` (EN)
- **Source:** `tools/partners.py`, built by `gen_pages.py`.
- **Not visible to Google:** it is `noindex`, left out of the sitemap and not linked from any page.
- **Pictures:** `shots/colabora-{es,en}-{phone,laptop}.png`.
- **EN URL:** this site puts each English page at the same path under `/en/` (for example `/en/calorias/`). That makes the English page `/en/colabora/` rather than `/en/partners/`. To get `/en/partners/` we would need either a second page or a redirect. My recommendation is to keep `/en/colabora/`.

### What the app really has (checked in the app code, read only, commit 5119c99)
- **«Enviar a mi nutricionista»** ("Compartir informe" on the Progreso tab):
  - The client creates a weekly PDF, Monday to Sunday, on their own phone.
  - It contains a "Resumen semanal" (kcal vs target, days logged, protein, weight change, macros, water/steps/workouts) and a "Detalle diario" with every meal.
  - The client sends it by WhatsApp, email or the share sheet. The nutritionist needs no account.
  - Photos and allergies are only included if the client ticks them.
  - The automatic server email is built but **not live**, so the page does not mention it.
- **Referrals:** the invite screen only shares the Google Play link.
  - The reward programme ended. The server returns `program_ended`, and the invited friend's 14 free days were removed.
  - There are **no codes and nothing to redeem**.
  - So the page promises **no referral code and no reward**, and it says so openly.
- **Free Premium for a professional or creator:** the app has no promo-code feature. It can only be granted by hand (RevenueCat dashboard or the account's `promo_premium_until`).
- **Platform:** Android only. There is no App Store listing.

### Owner decisions needed (marked `[OWNER TO DECIDE]` on the page)
1. **Contact email** to show on /colabora/. The site rule is that fotocal.app@gmail.com appears only on Contact and the legal pages. Options:
   - allow it on /colabora/ as well;
   - use a new address (for example colabora@…);
   - link only to the contact form, as the draft does today.

   No phone number and no personal address will be shown either way.
2. **Free Premium for professionals and creators:** yes or no, and for how long (for example 6 or 12 months). It is activated by hand per person.
3. **Creator commission:** the amount and terms, or "none". RevenueCat cannot pay affiliates, so any commission would be agreed in writing and paid by hand.
4. **Referral codes for clients:** the app has none today. Bringing them back would be an app change, not a website change.
5. **Google Play badge:** should we download the official badge and host it on the page? Google allows this if the badge is not modified.
6. **Go-live:** remove `noindex`, add a footer link ("Colabora") and merge.

## 2. Outreach list: 30 Spanish-language sites
Checked on 22 Nov 2026 through live search results. **The pages themselves could not be opened**, because this session's network blocks them. Open each contact page before writing. Every contact is a public business page; there are no personal emails or phones.

| # | Name | Relevant page | Why it fits | Business contact page |
|---|---|---|---|---|
| 1 | Consumer Eroski | consumer.es/alimentacion/aplicaciones-nutricion-usan-inteligencia-artificial-analisis | Reviews AI nutrition apps, including photo recognition | consumer.es/contacto |
| 2 | Infobae Salud | infobae.com/salud/2026/07/28/que-tan-precisas-son-las-aplicaciones-de-calorias-basadas-en-fotos-4-son-puestas-a-prueba/ | Jul 2026 test of photo-calorie apps | infobae.com/contacto/ |
| 3 | Xataka | xataka.com/basics/38-aplicaciones-servicios-para-ayudarte-tus-propositos-ano-nuevo-2026 | New-year app round-up | xataka.com/contacto |
| 4 | Vitónica | vitonica.com (article on an AI app that gives calories from a photo) | Covers the same idea as Fotocal | vitonica.com/contacto |
| 5 | Trendencias | trendencias.com/salud/dieta-9-mejores-apps-para-adelgazar | "Mejores apps para adelgazar" list | trendencias.com/contacto |
| 6 | Andro4all | andro4all.com/aplicaciones/las-mejores-apps-para-contar-calorias-y-medir-lo-que-quemas | Android calorie-app list | andro4all.com/contacto |
| 7 | El Español (Mujer) | elespanol.com/mujer/… (free diet apps) | Writes about free calorie apps | elespanol.com/contactar/ |
| 8 | FitGeneration | fitgeneration.es/top-7-apps-nutricion/ | "7 mejores apps de nutrición (2026)" | fitgeneration.es/contacto/ |
| 9 | Geekflare ES | geekflare.com/es/best-calorie-counting-apps/ | Spanish "best calorie apps" list | geekflare.com/es/contact/ (no guest posts) |
| 10 | Psicología y Mente | psicologiaymente.com/nutricion/mejores-apps-dietas-gratis | "Mejores apps de dietas gratis" | psicologiaymente.com/publicidad |
| 11 | OCU | ocu.org community thread on weight-loss apps | Consumer organisation | ocu.org/organizacion/prensa/nuestros-datos-de-contacto |
| 12 | Sportlife | sportlife.es/nutricion/calcula-calorias-diarias_193100_102.html | Fitness magazine, calorie articles | legal notice only, contact page not confirmed |
| 13 | Myprotein ES (The Zone) | myprotein.es/thezone/nutricion/tabla-de-calorias-de-los-alimentos/ | Calorie tables hub | myprotein.es partnerships page |
| 14 | HSN blog | hsnstore.com/blog/…/como-calcular-las-calorias-necesitas-al-dia/ | Daily-calorie article | hsnstore.com/programa-afiliacion |
| 15 | Nutritienda blog | blog.nutritienda.com/las-5-apps-fitness-mas-usadas-por-las-celebrities/ | Fitness-app round-up | help centre "Contacta con nosotros" (weak channel) |
| 16 | Basic-Fit ES blog | basic-fit.com/es-es/blog/habitos-sencillos-y-saludables-para-adelgazar | Gym blog that recommends food logging | advertising.basic-fit.com/en/contact/ |
| 17 | Mi Dieta Cojea | midietacojea.com | Leading dietitian-run site | midietacojea.com/contacto/consultas-y-propuestas/ |
| 18 | Dime qué comes | dimequecomes.com | Dietitian-run nutrition blog | dimequecomes.com/politica-de-publicidad/ |
| 19 | Nutrición360 | nutricion360.es | Evidence-based portal by professionals | nutricion360.es/sobre-nosotros |
| 20 | Consejo General de Dietistas-Nutricionistas | consejodietistasnutricionistas.com (public register) | National body | press page, notas-de-prensa |
| 21 | CODINMA (Madrid) | codinma.es | Madrid college, local to us | codinma.es/contact/ |
| 22 | CODiNuCoVa (Valencia) | codinucova.es | Regional college | codinucova.es/sala-de-prensa/ |
| 23 | Academia Española de Nutrición y Dietética | academianutricionydietetica.org | Professional association | la-academia page (secretariat) |
| 24 | Fundación Española de la Nutrición | fen.org.es | Public nutrition resources | fen.org.es/conocenos/contacto |
| 25 | SEDCA | nutricion.org | Dietetics society | nutricion.org/inicio/contacto/ |
| 26 | Fundación Española del Corazón | fundaciondelcorazon.com/nutricion/106-calculadoras.html | Calculators page; its old calorie calculator is retired | fundaciondelcorazon.com/prensa/contacto.html |
| 27 | Webconsultas | webconsultas.com | Large health portal with a diet section | webconsultas.com/contacto |
| 28 | Genbeta | genbeta.com | App round-ups (no calorie-app article found) | genbeta.com/contacto |
| 29 | Xataka Android | xatakandroid.com/aplicaciones-android/ocho-apps-para-android-con-las-que-adelgazar-tras-los-excesos-navidenos | Android weight-loss apps | probably xatakandroid.com/contacto (not confirmed) |
| 30 | Diario Extra (Ecuador) | extra.ec/noticia/tecnologia/mejores-apps-nutricion-2027-168353.html | Recent nutrition-app list | weak: no newsroom contact found |

**Notes on the list:**
- **Strongest:** #1–4, 8, 10, 17–21 and 26.
- **Weakest:** #12, 28, 29 and 30.
- **Left out:** "best apps" articles written by competitors (Fitia, Yazio, Noom and others).
- **Not searchable here:** 20minutos, El País, ABC, AS, Men's Health ES and Women's Health ES. They are worth adding by hand.

## 3. Two email templates (Spanish, under 120 words, NOT sent)

**A. To a nutritionist** (89 words)

> Asunto: Una app que te manda el resumen semanal de tus pacientes
>
> Hola, [nombre]:
>
> Soy [nombre], de Fotocal, una app Android hecha en Madrid que cuenta calorías con una foto del plato, pensada para la comida española.
>
> Tiene una función para nutricionistas: cada semana el paciente te envía por WhatsApp o email un PDF con su media de calorías, proteína, peso y el detalle de cada comida. Tú no necesitas cuenta ni app.
>
> Si te apetece probarla, te activo Premium gratis [X meses], sin compromiso. Y si no te convence, me encantaría saber por qué.
>
> Más información: getfotocal.com/colabora/
>
> Un saludo,
> [nombre]

**B. To a blogger or creator** (80 words)

> Asunto: Fotocal, para tu artículo sobre apps de calorías
>
> Hola, [nombre]:
>
> He leído tu artículo «[título]» y creo que Fotocal podría encajar. Es una app Android, hecha en Madrid, que cuenta las calorías con una foto y conoce los platos españoles: cocido, tortilla, bravas…
>
> El plan gratis no pide tarjeta (2 escaneos con IA al día; código de barras sin límite). Si quieres probarla a fondo, te activo Premium gratis [X meses]. Si la mencionas, márcalo como colaboración: no buscamos nada oculto.
>
> Capturas, logo y textos: getfotocal.com/colabora/
>
> Gracias,
> [nombre]

## 4. Free quick wins we can do ourselves (no money, no accounts created)
1. **Google Play listing → website.** In Play Console → Store presence → Store settings → Store listing contact details, set "Website" to `https://getfotocal.com/`. In the long description, add "Más información: getfotocal.com" once, as plain text.
2. **Instagram, TikTok and YouTube bios.** Set the bio link to `https://getfotocal.com/` (with a `?utm_source=instagram` tag if you want to count visits). The site already links to these profiles from its footer.
3. **AlternativeTo** (free).
   - Steps: create an account, then "Suggest new application" (Android, Freemium, description, tags: calorie counter, food photo).
   - Then suggest Fotocal as an alternative on the MyFitnessPal, Yazio and Foodvisor pages.
   - Moderators review every entry.
   - It adds an "official website" link, which may be nofollow.
4. **Product Hunt** (free).
   - Use a personal account; new accounts may have to wait about a week.
   - Go to Post → product URL, tagline (260 characters or fewer) and 2+ images, then schedule for 00:01 PST.
   - Never ask for paid upvotes.
5. **Uptodown** (Spanish Android store, free). Open the developer area, add the app and upload the APK for review. The app page shows the developer website.
6. **Softonic Publishing Centre** (Barcelona). It appears to be free, but this is not confirmed. Create a developer account, verify that you own the app, then publish the listing.
7. **SaaSHub, Uneed, Launching Next, Fazier and Indie Hackers.** Each takes a free submission of URL, description and categories, and the queues can be slow. Uneed's link only becomes dofollow after 20 upvotes on launch day. Fazier's free tier asks for a badge on your site; skip it unless you agree.
8. **Not recommended:** BetaList (all submissions are paid now) and any directory that sells "dofollow" links.
