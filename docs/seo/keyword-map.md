# Keyword map: one primary keyword per URL (anti-cannibalisation)

Source: MASTER PROMPT v3 §B.1, applied on 9 November 2026 by `tools/seo/keywords_v3_merge.py` (the same rows are marked `primary_keyword=yes` in `keywords.csv`).

**The rule.** Before writing a title, an H1 or a new page, find its keyword here.
- If the keyword is another URL's primary, don't use it: link to that URL instead, with its primary keyword as the anchor text.
- A secondary may appear on other pages as a natural mention, never in another page's title or H1.

Rows marked *provisional* (blog posts outside §B.1) are a Spanish or English search phrase for the page's topic. The blog rollout PARTs confirm or replace them. English dish names were settled on 11 Nov 2026 (v3 PART 7): they come from `tools/dishes/en.json` → `name`; update this file and the CSV when they do.

| URL (ES; the EN twin mirrors it under /en/) | Primary ES | Secondaries ES | Primary EN |
|---|---|---|---|
| `/` | contador de calorías con foto | contador de calorías gratis · app contar calorías · app contar calorías con foto gratis · contar calorías con ia · calorías y macros · contar calorías sin pesar | photo calorie counter app |
| `/features/scan-food/` | contar calorías con foto | escanear comida calorías · calorías por foto · escáner de calorías con ia · qué aplicación mide calorías con una foto · precisión | ai food scanner |
| `/features/scan-barcode/` | escáner código de barras calorías | escanear código de barras alimentos · app escanear calorías gratis | free barcode scanner calorie counter |
| `/features/voice-logging/` | contar calorías por voz | registrar comidas hablando · dictar comidas · registrar comida por voz | voice calorie tracker |
| `/features/` | funciones app contar calorías | contar calorías con foto, voz y código · coach ia nutrición | calorie counter app features |
| `/features/weight-loss/` | app para adelgazar contando calorías | app para adelgazar gratis · perder peso contando calorías | weight loss calorie counter app |
| `/features/nutrition-diet/` | app de dieta y macros | contador de macros · panel de nutrición | macro tracker app |
| `/features/lifestyle-mindset/` | hábitos para adelgazar | comer mejor sin obsesionarse · hábitos saludables app | healthy eating habits app |
| `/calculadoras/` | calculadoras de nutrición gratis | calculadora de calorías, imc y macros · calculadoras sin registro | free nutrition calculators |
| `/calculadoras/calorias-diarias/` | calculadora de calorías diarias | cuántas calorías debo comer al día · calorías de mantenimiento · calorías que gasto al día · calculadora de calorías harris benedict · calculadora de calorías mifflin st jeor · gasto energético | daily calorie calculator |
| `/calculadoras/deficit-calorico/` | calculadora de déficit calórico | déficit calórico mujer · déficit calórico hombre · cómo calcular el déficit calórico · cuánto déficit calórico para perder 1 kg · calorías para adelgazar · calculadora déficit calórico y macros | calorie deficit calculator |
| `/calculadoras/imc/` | calculadora de imc | calculadora imc mujer · calculadora imc hombre · índice de masa corporal · imc según edad · tabla imc | bmi calculator |
| `/calculadoras/macros/` | calculadora de macros | calculadora de macros y calorías · macros para perder grasa · macros diarios · proteínas grasas carbohidratos | macro calculator |
| `/calculadoras/proteinas/` | calculadora de proteínas | proteínas por kilo de peso · cuántas proteínas hay que tomar al día · proteína para ganar músculo · proteína para perder grasa | protein calculator |
| `/calculadoras/tmb/` | calculadora tmb | metabolismo basal · calculadora tmb y get · tmb mujer · tmb hombre · mifflin st jeor · harris benedict · katch-mcardle | bmr calculator |
| `/calculadoras/agua/` | cuánta agua beber al día | calculadora de agua · cuánta agua beber según tu peso · si peso 70 kilos cuánta agua debo beber · agua para bajar de peso · agua con creatina | how much water to drink a day |
| `/calculadoras/peso-saludable/` | peso ideal según altura | calculadora peso ideal · peso ideal mujer · peso ideal hombre · peso ideal según estatura y edad · tabla de peso ideal | ideal weight by height |
| `/calorias/` | calorías de platos españoles | tabla de calorías de comida española · calorías por ración y por 100 g · calorías de las tapas | calories in spanish food |
| `/calorias/tabla-de-calorias/` | tabla de calorías de alimentos | tabla de calorías por 100 gramos · tabla de calorías por alimentos y porciones · tabla de calorías y proteínas · alimentos con más calorías | food calorie chart |
| `/comparativa/` | mejor app para contar calorías | apps para contar calorías en españa · mejor app para contar calorías con foto · mejor app para contar calorías con ia · mejor app para contar calorías gratis · mejor app para contar calorías y macros · mejor app para contar calorías 2026 | best calorie counter app |
| `/comparativa/fotocal-vs-myfitnesspal/` | fotocal vs myfitnesspal | myfitnesspal o fotocal · es gratuita myfitnesspal · precio myfitnesspal premium | fotocal vs myfitnesspal |
| `/comparativa/fotocal-vs-yazio/` | fotocal vs yazio | es gratis yazio · cuánto vale yazio | fotocal vs yazio |
| `/comparativa/fotocal-vs-cal-ai/` | fotocal vs cal ai | cal ai precio · es gratis cal ai · cal ai android | fotocal vs cal ai |
| `/guias/` | guías para contar calorías | cómo contar calorías · cómo empezar a contar calorías | calorie counting guides |
| **new page:** `/comparativa/alternativas-myfitnesspal/` | alternativa a myfitnesspal | alternativa gratuita a myfitnesspal · alternativa gratis a myfitnesspal · alternativas a myfitnesspal | myfitnesspal alternative |
| **new page:** `/comparativa/cal-ai-opiniones/` | cal ai opiniones | cal ai es gratis · cal ai es de pago · cal ai precio app · es fiable cal ai | cal ai alternative for android |
| **new page:** `/comparativa/yazio-opiniones/` | yazio opiniones | yazio es gratis · yazio es de pago · cuesta dinero yazio | yazio review |
| `/blog/calorias-para-adelgazar-mujer/` (published 14-11-2026) | calorías para adelgazar mujer | cuántas calorías debe comer una mujer para adelgazar · qué pasa si como 1500 calorías al día · calorías para adelgazar 1 kilo por semana | calories to lose weight for women |
| `/blog/app-contar-calorias-gratis/` | app para contar calorías gratis | contador de calorías gratis sin pagar · qué incluye gratis cada app · app calorías sin suscripción | free calorie counter app no subscription |
| `/blog/calorie-deficit-for-fat-loss/` | déficit calórico qué es y cómo hacerlo | cómo hacer un déficit calórico · qué comer en déficit calórico · qué no comer en déficit calórico | calorie deficit explained |
| `/blog/deficit-500-calorias-dia/` | déficit de 500 calorías | cuánto se adelgaza con 500 kcal de déficit · déficit de 500 calorías qué comer | 500 calorie deficit |
| `/blog/calorias-para-perder-un-kilo/` | calorías para perder un kilo | 7700 kcal mito o realidad · perder 1 kilo por semana · cuántas calorías hay que quemar para perder un kilo | calories to lose a kilo |
| `/blog/how-much-protein-per-day/` | cuánta proteína necesito al día | proteína por kilo · proteína para mujeres | how much protein per day |
| `/blog/tdee-how-many-calories-you-need/` | qué es el tdee | get gasto energético total · gasto calórico diario | what is tdee |
| `/blog/understanding-your-basal-metabolic-rate/` | qué es el metabolismo basal | tmb qué es · cómo subir el metabolismo | what is bmr |
| `/blog/photo-calorie-apps-accuracy/` | son precisas las apps de calorías con foto | precisión ia calorías · fiabilidad apps calorías foto | are photo calorie apps accurate |
| `/blog/choose-photo-calorie-counter/` | cómo elegir una app de calorías con foto | qué mirar en una app de calorías · precio y privacidad apps calorías | how to choose a photo calorie app |
| `/blog/added-sugar-vs-natural-sugar/` | azúcar añadido vs natural | — | added sugar vs natural sugar *(provisional)* |
| `/blog/best-foods-for-weight-loss/` | alimentos que sacian con pocas calorías | mejores alimentos para adelgazar | low calorie filling foods *(provisional)* |
| `/blog/building-muscle-while-losing-fat/` | ganar músculo y perder grasa a la vez | recomposición corporal | build muscle while losing fat *(provisional)* |
| `/blog/calorias-bocadillo/` | calorías bocadillo | cuántas calorías tiene un bocadillo | calories in a spanish sandwich bocadillo *(provisional)* |
| `/blog/calorias-de-las-tapas/` | calorías de las tapas | cuántas calorías tiene una tarde de cañas | calories in tapas *(provisional)* |
| `/blog/calorias-desayuno-espanol/` | calorías desayuno español | desayuno de bar calorías | spanish breakfast calories *(provisional)* |
| `/blog/calorias-menu-del-dia/` | calorías menú del día | — | menu del dia calories *(provisional)* |
| `/blog/carbs-are-not-the-enemy/` | los carbohidratos engordan | — | are carbs bad for weight loss *(provisional)* |
| `/blog/cardio-vs-strength-training-for-fat-loss/` | cardio o pesas para perder grasa | — | cardio vs weights for fat loss *(provisional)* |
| `/blog/cena-ligera-menos-de-500-calorias/` | cena ligera menos de 500 calorías | cenas ligeras para adelgazar | light dinner under 500 calories *(provisional)* |
| `/blog/common-calorie-counting-mistakes/` | errores al contar calorías | — | calorie counting mistakes *(provisional)* |
| `/blog/dietary-fat-how-much-and-which-kinds/` | cuánta grasa comer al día | grasas saludables | how much fat per day *(provisional)* |
| `/blog/do-calories-matter-or-food-quality/` | calorías o calidad de la comida | contar calorías funciona | calories vs food quality *(provisional)* |
| `/blog/do-you-need-to-exercise-to-lose-weight/` | adelgazar sin hacer ejercicio | — | lose weight without exercise *(provisional)* |
| `/blog/does-meal-timing-matter-for-weight-loss/` | cenar tarde engorda | horario de las comidas para adelgazar | does meal timing matter for weight loss *(provisional)* |
| `/blog/does-protein-timing-matter/` | cuándo tomar proteína | — | protein timing *(provisional)* |
| `/blog/eating-out-without-wrecking-your-diet/` | comer fuera sin engordar | — | eating out on a diet *(provisional)* |
| `/blog/emotional-eating/` | comer por ansiedad | hambre emocional | emotional eating *(provisional)* |
| `/blog/fiber-the-underrated-nutrient/` | fibra para adelgazar | — | fiber for weight loss *(provisional)* |
| `/blog/healthy-snacks-that-satisfy/` | snacks saludables que sacian | snacks saludables pocas calorías | healthy filling snacks *(provisional)* |
| `/blog/high-protein-breakfast-ideas/` | desayunos altos en proteína | — | high protein breakfast ideas *(provisional)* |
| `/blog/high-protein-diet-benefits-and-how-to-start/` | dieta alta en proteínas | — | high protein diet *(provisional)* |
| `/blog/how-fast-should-you-lose-weight/` | cuánto peso se puede perder en una semana | cuántos kilos se pueden perder en un mes | how fast can you lose weight *(provisional)* |
| `/blog/how-many-calories-does-exercise-burn/` | cuántas calorías quema el ejercicio | calorías quemadas caminando 1 hora | how many calories does exercise burn *(provisional)* |
| `/blog/how-sleep-affects-your-weight/` | dormir poco engorda | — | how sleep affects weight *(provisional)* |
| `/blog/how-to-build-a-healthy-grocery-list/` | lista de la compra saludable | — | healthy grocery list *(provisional)* |
| `/blog/how-to-count-calories-accurately/` | cómo contar calorías para principiantes | — | how to count calories *(provisional)* |
| `/blog/how-to-eat-healthy-on-a-budget/` | comer sano y barato | — | eat healthy on a budget *(provisional)* |
| `/blog/how-to-handle-cravings-without-guilt/` | cómo controlar los antojos | — | how to handle cravings *(provisional)* |
| `/blog/how-to-lose-weight-sustainably/` | cómo adelgazar sin dietas | — | how to lose weight sustainably *(provisional)* |
| `/blog/how-to-read-nutrition-labels/` | cómo leer etiquetas nutricionales | — | how to read nutrition labels *(provisional)* |
| `/blog/how-to-set-your-macros-for-weight-loss/` | cómo calcular macros para perder peso | cómo calcular mis macros | how to set macros for weight loss *(provisional)* |
| `/blog/how-to-stay-consistent-with-healthy-habits/` | cómo ser constante con la dieta | — | how to stay consistent with healthy habits *(provisional)* |
| `/blog/how-to-stop-overeating-at-night/` | cómo dejar de comer por la noche | — | how to stop eating at night *(provisional)* |
| `/blog/hydration-and-weight/` | beber agua adelgaza | — | does drinking water help weight loss *(provisional)* |
| `/blog/intermittent-fasting-what-the-evidence-says/` | ayuno intermitente qué dice la ciencia | ayuno intermitente funciona para adelgazar | intermittent fasting evidence *(provisional)* |
| `/blog/intuitive-eating-vs-calorie-counting/` | alimentación intuitiva o contar calorías | — | intuitive eating vs calorie counting *(provisional)* |
| `/blog/low-carb-vs-low-fat/` | dieta baja en carbohidratos o baja en grasa | — | low carb vs low fat *(provisional)* |
| `/blog/macronutrients-101/` | qué son los macronutrientes | — | what are macronutrients *(provisional)* |
| `/blog/maintaining-weight-loss/` | cómo mantener el peso después de adelgazar | — | how to maintain weight loss *(provisional)* |
| `/blog/meal-prep-for-beginners/` | meal prep para principiantes | — | meal prep for beginners *(provisional)* |
| `/blog/mindful-eating-beginners-guide/` | alimentación consciente | — | mindful eating *(provisional)* |
| `/blog/neat-the-hidden-calorie-burn/` | qué es el neat | — | what is neat *(provisional)* |
| `/blog/plan-a-week-of-meals-in-30-minutes/` | planificar menú semanal | — | plan a week of meals *(provisional)* |
| `/blog/portion-control-simple-tricks/` | controlar las raciones | método de la mano porciones | portion control tips *(provisional)* |
| `/blog/the-truth-about-detox-diets-and-cleanses/` | dietas détox funcionan | — | do detox diets work *(provisional)* |
| `/blog/the-truth-about-starvation-mode/` | modo supervivencia metabolismo | modo ahorro metabolismo mito | starvation mode myth *(provisional)* |
| `/blog/track-calories-without-weighing/` | cómo contar calorías sin pesar | contar calorías sin báscula | how to count calories without weighing food *(provisional)* |
| `/blog/weight-loss-plateaus/` | estancamiento al perder peso | estancamiento perder peso qué hacer | weight loss plateau *(provisional)* |
| `/blog/what-a-balanced-plate-looks-like/` | plato equilibrado | plato de harvard | balanced plate *(provisional)* |
| `/blog/why-crash-diets-fail/` | por qué fallan las dietas | dietas exprés | why crash diets fail *(provisional)* |
| `/blog/why-micronutrients-matter/` | micronutrientes qué son | — | why micronutrients matter *(provisional)* |
| `/blog/why-the-scale-is-not-the-whole-story/` | la báscula no baja pero adelgazo | — | why the scale is not the whole story *(provisional)* |
| `/calorias/tortilla-de-patatas/` | calorías tortilla de patatas | calorías tortilla de patatas por 100 g · calorías tortilla de patatas por ración · engorda tortilla de patatas · proteínas tortilla de patatas | calories in spanish omelette |
| `/calorias/paella-valenciana/` | calorías paella valenciana | calorías paella valenciana por 100 g · calorías paella valenciana por ración · engorda paella valenciana · proteínas paella valenciana | calories in paella |
| `/calorias/croquetas-de-jamon/` | calorías croquetas de jamón | calorías croquetas de jamón por 100 g · calorías croquetas de jamón por ración · engorda croquetas de jamón · proteínas croquetas de jamón | calories in spanish ham croquettes |
| `/calorias/cocido-madrileno/` | calorías cocido madrileño | calorías cocido madrileño por 100 g · calorías cocido madrileño por ración · engorda cocido madrileño · proteínas cocido madrileño | calories in cocido madrileño |
| `/calorias/gazpacho/` | calorías gazpacho | calorías gazpacho por 100 g · calorías gazpacho por ración · engorda gazpacho · proteínas gazpacho | calories in gazpacho |
| `/calorias/salmorejo/` | calorías salmorejo | calorías salmorejo por 100 g · calorías salmorejo por ración · engorda salmorejo · proteínas salmorejo | calories in salmorejo |
| `/calorias/lentejas-estofadas/` | calorías lentejas estofadas | calorías lentejas estofadas por 100 g · calorías lentejas estofadas por ración · engorda lentejas estofadas · proteínas lentejas estofadas | calories in spanish lentil stew |
| `/calorias/fabada-asturiana/` | calorías fabada asturiana | calorías fabada asturiana por 100 g · calorías fabada asturiana por ración · engorda fabada asturiana · proteínas fabada asturiana | calories in fabada asturiana |
| `/calorias/ensaladilla-rusa/` | calorías ensaladilla rusa | calorías ensaladilla rusa por 100 g · calorías ensaladilla rusa por ración · engorda ensaladilla rusa · proteínas ensaladilla rusa | calories in spanish potato salad |
| `/calorias/churros-con-chocolate/` | calorías churros con chocolate | calorías churros con chocolate por 100 g · calorías churros con chocolate por ración · engorda churros con chocolate · proteínas churros con chocolate | calories in churros with chocolate |
| `/calorias/pulpo-a-la-gallega/` | calorías pulpo a la gallega | calorías pulpo a la gallega por 100 g · calorías pulpo a la gallega por ración · engorda pulpo a la gallega · proteínas pulpo a la gallega | calories in galician octopus |
| `/calorias/empanada-gallega/` | calorías empanada gallega | calorías empanada gallega por 100 g · calorías empanada gallega por ración · engorda empanada gallega · proteínas empanada gallega | calories in empanada gallega |
| `/calorias/migas/` | calorías migas | calorías migas por 100 g · calorías migas por ración · engorda migas · proteínas migas | calories in migas |
| `/calorias/torrijas/` | calorías torrijas | calorías torrijas por 100 g · calorías torrijas por ración · engorda torrijas · proteínas torrijas | calories in torrijas |
| `/calorias/tostada-con-tomate-y-aceite/` | calorías tostada con tomate y aceite | calorías tostada con tomate y aceite por 100 g · calorías tostada con tomate y aceite por ración · engorda tostada con tomate y aceite · proteínas tostada con tomate y aceite | calories in tomato toast with olive oil |
| `/calorias/cafe-con-leche/` | calorías café con leche | calorías café con leche por 100 g · calorías café con leche por ración · engorda café con leche · proteínas café con leche | calories in café con leche |
| `/calorias/huevos-fritos-con-patatas/` | calorías huevos fritos con patatas | calorías huevos fritos con patatas por 100 g · calorías huevos fritos con patatas por ración · engorda huevos fritos con patatas · proteínas huevos fritos con patatas | calories in fried eggs and chips |
| `/calorias/arroz-con-leche/` | calorías arroz con leche | calorías arroz con leche por 100 g · calorías arroz con leche por ración · engorda arroz con leche · proteínas arroz con leche | calories in spanish rice pudding |
| `/calorias/albondigas-en-salsa/` | calorías albóndigas en salsa | calorías albóndigas en salsa por 100 g · calorías albóndigas en salsa por ración · engorda albóndigas en salsa · proteínas albóndigas en salsa | calories in spanish meatballs in sauce |
| `/calorias/pincho-de-tortilla/` | calorías pincho de tortilla | calorías pincho de tortilla por 100 g · calorías pincho de tortilla por ración · engorda pincho de tortilla · proteínas pincho de tortilla | calories in spanish omelette slice |
| `/calorias/patatas-bravas/` | calorías patatas bravas | calorías patatas bravas por 100 g · calorías patatas bravas por ración · engorda patatas bravas · proteínas patatas bravas | calories in patatas bravas |
| `/calorias/bocadillo-de-jamon-serrano/` | calorías bocadillo de jamón serrano | calorías bocadillo de jamón serrano por 100 g · calorías bocadillo de jamón serrano por ración · engorda bocadillo de jamón serrano · proteínas bocadillo de jamón serrano | calories in serrano ham sandwich |
| `/calorias/calamares-a-la-romana/` | calorías calamares a la romana | calorías calamares a la romana por 100 g · calorías calamares a la romana por ración · engorda calamares a la romana · proteínas calamares a la romana | calories in fried calamari |
| `/calorias/callos-a-la-madrilena/` | calorías callos a la madrileña | calorías callos a la madrileña por 100 g · calorías callos a la madrileña por ración · engorda callos a la madrileña · proteínas callos a la madrileña | calories in callos a la madrileña |
| `/calorias/jamon-serrano/` | calorías jamón serrano | calorías jamón serrano por 100 g · calorías jamón serrano por ración · engorda jamón serrano · proteínas jamón serrano | calories in serrano ham |
| `/calorias/cana-de-cerveza/` | calorías caña de cerveza | calorías caña de cerveza por 100 g · calorías caña de cerveza por ración · engorda caña de cerveza · proteínas caña de cerveza | calories in small draught beer |
| `/calorias/tinto-de-verano/` | calorías tinto de verano | calorías tinto de verano por 100 g · calorías tinto de verano por ración · engorda tinto de verano · proteínas tinto de verano | calories in tinto de verano |
| `/calorias/pimientos-de-padron/` | calorías pimientos de Padrón | calorías pimientos de Padrón por 100 g · calorías pimientos de Padrón por ración · engorda pimientos de Padrón · proteínas pimientos de Padrón | calories in pimientos de padrón |
| `/calorias/tarta-de-santiago/` | calorías tarta de Santiago | calorías tarta de Santiago por 100 g · calorías tarta de Santiago por ración · engorda tarta de Santiago · proteínas tarta de Santiago | calories in tarta de santiago |
| `/calorias/gambas-al-ajillo/` | calorías gambas al ajillo | calorías gambas al ajillo por 100 g · calorías gambas al ajillo por ración · engorda gambas al ajillo · proteínas gambas al ajillo | calories in garlic prawns |
| `/calorias/bocadillo-de-calamares/` | calorías bocadillo de calamares | calorías bocadillo de calamares por 100 g · calorías bocadillo de calamares por ración · engorda bocadillo de calamares · proteínas bocadillo de calamares | calories in calamari sandwich |
| `/calorias/sopa-castellana/` | calorías sopa castellana | calorías sopa castellana por 100 g · calorías sopa castellana por ración · engorda sopa castellana · proteínas sopa castellana | calories in castilian garlic soup |
| `/calorias/tortilla-francesa/` | calorías tortilla francesa | calorías tortilla francesa por 100 g · calorías tortilla francesa por ración · engorda tortilla francesa · proteínas tortilla francesa | calories in plain omelette |
| `/calorias/sandwich-mixto/` | calorías sándwich mixto de jamón y queso | calorías sándwich mixto de jamón y queso por 100 g · calorías sándwich mixto de jamón y queso por ración · engorda sándwich mixto de jamón y queso · proteínas sándwich mixto de jamón y queso | calories in ham and cheese toastie |
| `/calorias/platano/` | calorías plátano | calorías plátano por 100 g · calorías plátano por ración · engorda plátano · proteínas plátano | calories in banana |
| `/calorias/huevo-cocido/` | calorías huevo cocido | calorías huevo cocido por 100 g · calorías huevo cocido por ración · engorda huevo cocido · proteínas huevo cocido | calories in hard-boiled egg |
| `/calorias/barra-de-pan/` | calorías barra de pan | calorías barra de pan por 100 g · calorías barra de pan por ración · engorda barra de pan · proteínas barra de pan | calories in spanish bread |
| `/calorias/aceite-de-oliva/` | calorías aceite de oliva | calorías aceite de oliva por 100 g · calorías aceite de oliva por ración · engorda aceite de oliva · proteínas aceite de oliva | calories in olive oil |
| `/calorias/coca-cola-zero/` | calorías Coca-Cola Zero | calorías Coca-Cola Zero por 100 g · calorías Coca-Cola Zero por ración · engorda Coca-Cola Zero · proteínas Coca-Cola Zero | calories in coca-cola zero |
| `/calorias/copa-de-vino-tinto/` | calorías copa de vino tinto | calorías copa de vino tinto por 100 g · calorías copa de vino tinto por ración · engorda copa de vino tinto · proteínas copa de vino tinto | calories in red wine |
| `/calorias/tercio-de-cerveza/` | calorías tercio de cerveza | calorías tercio de cerveza por 100 g · calorías tercio de cerveza por ración · engorda tercio de cerveza · proteínas tercio de cerveza | calories in beer |
| `/calorias/croissant/` | calorías cruasán | calorías cruasán por 100 g · calorías cruasán por ración · engorda cruasán · proteínas cruasán | calories in croissant |
| `/calorias/magdalena/` | calorías magdalena | calorías magdalena por 100 g · calorías magdalena por ración · engorda magdalena · proteínas magdalena | calories in spanish muffin |
| `/calorias/salmon-a-la-plancha/` | calorías salmón a la plancha | calorías salmón a la plancha por 100 g · calorías salmón a la plancha por ración · engorda salmón a la plancha · proteínas salmón a la plancha | calories in grilled salmon |
| `/calorias/macarrones-con-tomate/` | calorías macarrones con tomate | calorías macarrones con tomate por 100 g · calorías macarrones con tomate por ración · engorda macarrones con tomate · proteínas macarrones con tomate | calories in macaroni with tomato sauce |
| `/calorias/espaguetis-bolonesa/` | calorías espaguetis a la boloñesa | calorías espaguetis a la boloñesa por 100 g · calorías espaguetis a la boloñesa por ración · engorda espaguetis a la boloñesa · proteínas espaguetis a la boloñesa | calories in spaghetti bolognese |
| `/calorias/pollo-asado/` | calorías pollo asado | calorías pollo asado por 100 g · calorías pollo asado por ración · engorda pollo asado · proteínas pollo asado | calories in roast chicken |
| `/calorias/potaje-de-garbanzos/` | calorías potaje de garbanzos | calorías potaje de garbanzos por 100 g · calorías potaje de garbanzos por ración · engorda potaje de garbanzos · proteínas potaje de garbanzos | calories in spanish chickpea stew |
| `/calorias/ensalada-mixta/` | calorías ensalada mixta | calorías ensalada mixta por 100 g · calorías ensalada mixta por ración · engorda ensalada mixta · proteínas ensalada mixta | calories in spanish mixed salad |
| `/calorias/manzana/` | calorías manzana | calorías manzana por 100 g · calorías manzana por ración · engorda manzana · proteínas manzana | calories in apple |
| `/calorias/almendras/` | calorías almendras | calorías almendras por 100 g · calorías almendras por ración · engorda almendras · proteínas almendras | calories in almonds |
| `/calorias/pizza/` | calorías pizza | calorías pizza por 100 g · calorías pizza por ración · engorda pizza · proteínas pizza | calories in pizza |
| `/calorias/arroz-a-la-cubana/` | calorías arroz a la cubana | calorías arroz a la cubana por 100 g · calorías arroz a la cubana por ración · engorda arroz a la cubana · proteínas arroz a la cubana | calories in cuban-style rice |
| `/calorias/lentejas-con-chorizo/` | calorías lentejas con chorizo | calorías lentejas con chorizo por 100 g · calorías lentejas con chorizo por ración · engorda lentejas con chorizo · proteínas lentejas con chorizo | calories in lentils with chorizo |
| `/calorias/bacalao-al-pil-pil/` | calorías bacalao al pil pil | calorías bacalao al pil pil por 100 g · calorías bacalao al pil pil por ración · engorda bacalao al pil pil · proteínas bacalao al pil pil | calories in cod pil pil |
| `/calorias/fideua/` | calorías fideuá | calorías fideuá por 100 g · calorías fideuá por ración · engorda fideuá · proteínas fideuá | calories in fideuá |
| `/calorias/marmitako/` | calorías marmitako | calorías marmitako por 100 g · calorías marmitako por ración · engorda marmitako · proteínas marmitako | calories in marmitako |
| `/calorias/merluza-en-salsa-verde/` | calorías merluza en salsa verde | calorías merluza en salsa verde por 100 g · calorías merluza en salsa verde por ración · engorda merluza en salsa verde · proteínas merluza en salsa verde | calories in hake in green sauce |

`/metodologia/`, `/about/`, `/contact/`, `/faq/`, `/subscription/`, legal pages and `/widget/` are trust and utility pages: no keyword target, never use a money keyword in their title.

**Dish pages.** The primary is the phrase people type ("calorías paella"). The title and H1 use the natural form ("Calorías de la paella"); it is the same query to Google. Variations (100 g, Mercadona, con cebolla, 3/4/6 huevos, por unidad) are sections of the page, never new URLs.
