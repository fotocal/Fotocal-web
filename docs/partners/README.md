# Partner and backlink programme (22 Nov 2026)

**Status:** the /colabora/ page is published and linked from the footer, with the owner's decisions applied. Nobody has been contacted. The owner sends the emails.


## 1. Page `/colabora/` (ES) and `/en/colabora/` (EN)
- **Source:** `tools/partners.py`, built by `gen_pages.py`.
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

### Owner decisions (22 Nov 2026) and what was done
1. **Contact email:** fotocal.app@gmail.com is on the page, with no phone, no address and no personal name.
2. **Free Premium:** 12 months for nutritionists and 3 for creators, but only through the app's existing redeem/promo-code system. I re-checked that system: it **does not work**. The /redeem and /redeem-code screens send the user to Home, the server's `apply` returns 410 `program_ended`, and the app has no Play offer codes. So the page **offers no free Premium**. To offer it, the app first needs a working code feature (for example Play Console promo codes or a restored redeem screen). That is an app change.
3. **Commission:** none, and nothing about money appears on the page.
4. **Badge:** Google's official "Disponible en Google Play" / "Get it on Google Play" badge is used unmodified, linked to the Play listing, with the trademark line. The image is loaded from Google's own server (the embed code from Google's badge generator), because downloading the file was not allowed from this session.
5. **URL:** /colabora/ and /en/colabora/.
6. **Published:** `noindex` removed, the page is in the sitemap, and there is a footer link («Colabora con Fotocal» / «Partner with us») in the Empresa column.

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

## 3. Two email templates (Spanish, under 120 words, for the owner to send; NOT sent)
Updated 22 Nov after the owner's decisions. There is no free Premium offer, because the app's redeem/promo-code system does not work (see §1), and no money is mentioned.

**A. To a nutritionist**

> Asunto: Una app que te manda el resumen semanal de tus pacientes
>
> Hola, [nombre]:
>
> Soy [nombre], de Fotocal, una app Android hecha en Madrid que cuenta calorías con una foto del plato, pensada para la comida española.
>
> Tiene una función para nutricionistas: cada semana el paciente te envía por WhatsApp o email un PDF con su media de calorías, proteína, peso y el detalle de cada comida. Tú no necesitas cuenta ni app.
>
> Si te parece útil para tu consulta, me encantaría saber qué le añadirías al informe. Y si no te convence, también.
>
> Más información: getfotocal.com/colabora/
>
> Un saludo,
> [nombre]
> fotocal.app@gmail.com

**B. To a blogger or creator**

> Asunto: Fotocal, para tu artículo sobre apps de calorías
>
> Hola, [nombre]:
>
> He leído tu artículo «[título]» y creo que Fotocal podría encajar. Es una app Android, hecha en Madrid, que cuenta las calorías con una foto y conoce los platos españoles: cocido, tortilla, bravas…
>
> El plan gratis no pide tarjeta: 2 escaneos con IA al día y código de barras sin límite. Si la pruebas y te convence, tienes capturas, logo, textos y nuestra tabla de calorías de 218 platos para usar libremente.
>
> Todo está en getfotocal.com/colabora/
>
> Gracias,
> [nombre]
> fotocal.app@gmail.com

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
