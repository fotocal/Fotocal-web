/* ═══════════════════════════════════════════════════════════════
   FOTOCAL — translations for the content pages
   /blog/ · /subscription/ · /about/ · /contact/

   WHY THIS IS A SEPARATE FILE FROM assets/js/i18n.js
   i18n.js holds the strings shared by every page (nav, footer, home).
   These four content pages are long-form, so their strings would have
   roughly tripled that file. Keeping them here means:
     · i18n.js stays small and is the one place shared strings live;
     · a change to the Subscription copy cannot break the home page;
     · the two files can be edited independently.
   It merges INTO window.FOTOCAL_I18N rather than replacing it, so
   assets/js/main.js still sees one dictionary and needs no changes.

   LOAD ORDER — this file must sit BETWEEN i18n.js and main.js:
     <script src="../assets/js/i18n.js"></script>
     <script src="../assets/js/i18n-pages.js"></script>   <- this file
     <script src="../assets/js/layout.js" data-page="..."></script>
     <script src="../assets/js/main.js"></script>
   main.js reads window.FOTOCAL_I18N once when it runs, so anything
   merged after main.js would be ignored.

   RULES (same as i18n.js — they are not optional)
   1. Every key MUST exist in BOTH "en" and "es". A missing key silently
      falls back to the other language, which is the "Spanish leaking
      into English" bug. Add both at the same time.
   2. Only keys used with data-i18n-html may contain markup.
   3. This file must be saved as UTF-8. Spanish accents (á é í ó ú ñ
      ¿ ¡) and the € sign must survive. If you see Ã or ð on the page,
      it was saved with the wrong encoding.
   4. CONTENT RULE: everything in here must be TRUE. No invented stats,
      testimonials, user counts, ratings, awards, team or dates. No
      guaranteed-results or medical claims.
   ═══════════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  var PAGES = {

    /* ══════════════════════ ENGLISH ══════════════════════ */
    en: {

      /* ─────────────────────────────────────────────
         SUBSCRIPTION
         ───────────────────────────────────────────── */
      "sub.meta.title": "Subscription & pricing — Fotocal",
      "sub.kicker": "Subscription",
      "sub.title": "Everything Fotocal can do, <em class=\"accent\">unlocked</em>.",
      "sub.lead": "Fotocal is free to download and free to use every day. Premium removes the daily limit on AI photo scans and switches on the deeper analysis — weekly reports, personalised recommendations, sync and an ad-free app.",
      "sub.lead2": "Three lengths, one set of features. The longer you commit, the less it costs per month. That is the whole pricing model — no tiers to decode, no add-ons.",
      "sub.hero.cta": "Get Fotocal on Google Play",
      "sub.hero.compare": "Compare free and Premium ↓",

      /* Coach Kal is free — stated up front because it is the thing
         people most expect to be paywalled. */
      "sub.kal.h": "Coach Kal is free. For everyone, with no limit.",
      "sub.kal.b": "Your AI nutrition coach is not a Premium feature and never has been. Ask Coach Kal as many questions as you like, on the free plan, forever. It is the part of Fotocal most likely to actually change how you eat, so putting it behind a paywall would be backwards.",

      /* Plans */
      "sub.plans.kicker": "The plans",
      "sub.plans.title": "Pick a length. <em class=\"accent\">Same Premium</em> either way.",
      "sub.plans.sub": "Every plan unlocks exactly the same features. The only difference is how long it runs and what that works out to per month.",

      "sub.p.m.name": "Monthly",
      "sub.p.m.per": "/month",
      "sub.p.m.equiv": "Billed every month.",
      "sub.p.m.note": "The flexible one. Good if you want to try Premium properly for a month without thinking further ahead than that.",
      "sub.p.m.trial": "No free trial on this plan — billing starts straight away.",

      "sub.p.y.name": "Yearly",
      "sub.p.y.per": "/year",
      "sub.p.y.equiv": "Works out at <b>about €2.92 a month</b>.",
      "sub.p.y.note": "The cheapest way to use Fotocal, and the only plan with a free trial. Best if you already know you want to build the habit over a full year.",
      "sub.p.y.trial": "Includes a 3-day free trial. Cancel before it ends and you are not charged.",
      "sub.p.y.flag": "MOST POPULAR",
      "sub.p.y.save": "Saves about 58% vs monthly",

      "sub.p.q.name": "3 months",
      "sub.p.q.per": "/3 months",
      "sub.p.q.equiv": "Works out at <b>about €5.66 a month</b>.",
      "sub.p.q.note": "The middle ground. A full season is long enough for a habit to take hold without committing to a year.",
      "sub.p.q.trial": "No free trial on this plan — billing starts straight away.",
      "sub.p.q.save": "Saves about 19% vs monthly",

      "sub.p.cta": "Get it on Google Play",
      "sub.p.ctaY": "Start the 3-day free trial",

      /* The trial caveat, stated plainly rather than buried. */
      "sub.trial.h": "The free trial is on the yearly plan only",
      "sub.trial.b": "This is worth being clear about, because plenty of apps are not. The 3-day free trial comes with the yearly plan. The monthly and 3-month plans do not have a trial — if you pick one of those, billing starts immediately.",
      "sub.trial.b2": "If you want to try Premium at no cost, start the yearly plan and cancel inside 3 days. You will not be charged. If you would rather not deal with a trial at all, the monthly plan is the simplest option.",

      "sub.vat": "All prices are in euros and include Spanish VAT at 21%. What you see here is what you pay — there is nothing added at checkout.",

      /* Comparison table */
      "sub.cmp.kicker": "Free vs Premium",
      "sub.cmp.title": "What you get, <em class=\"accent\">line by line</em>.",
      "sub.cmp.sub": "The free plan is a real product, not a demo — you can log every meal, every day, forever, without paying. Here is exactly where the line sits.",
      "sub.cmp.caption": "Fotocal free plan compared with Fotocal Premium",
      "sub.cmp.colFeature": "Feature",
      "sub.cmp.colFree": "Free",
      "sub.cmp.colPro": "Premium",
      /* Screen-reader text for the ✓ / ✕ marks — the icon alone is
         meaningless without it, and a table of bare icons is unreadable. */
      "sub.cmp.yes": "Included",
      "sub.cmp.no": "Not included",

      "sub.cmp.r1": "AI food scans",
      "sub.cmp.r1s": "Photograph a meal and get calories, macros and a quality score.",
      "sub.cmp.r1free": "3 per day",
      "sub.cmp.r1pro": "Unlimited",

      "sub.cmp.r2": "Coach Kal",
      "sub.cmp.r2s": "Your AI nutrition coach — free for everyone, on every plan.",
      "sub.cmp.r2free": "Unlimited",
      "sub.cmp.r2pro": "Unlimited",

      "sub.cmp.r3": "Meal diary",
      "sub.cmp.r3s": "Log breakfast, lunch, dinner and snacks against your targets.",

      "sub.cmp.r4": "Weight & progress tracking",
      "sub.cmp.r4s": "Log your weight and measurements and watch the trend.",

      "sub.cmp.r5": "Water & steps",
      "sub.cmp.r5s": "Daily hydration, plus steps via Health Connect.",

      "sub.cmp.r6": "Offline mode",
      "sub.cmp.r6s": "Log with no signal. The AI scan itself still needs a connection.",

      "sub.cmp.r7": "Advanced nutrition insights",
      "sub.cmp.r7s": "The deeper read on your macros and patterns, beyond the daily totals.",

      "sub.cmp.r8": "Weekly reports",
      "sub.cmp.r8s": "A weekly pull-together of trends, wins and what slipped.",

      "sub.cmp.r9": "Personalised plans & recommendations",
      "sub.cmp.r9s": "Guidance shaped around your goals and what you actually log.",

      "sub.cmp.r10": "Sync",
      "sub.cmp.r10s": "Your data kept in step and carried to a new phone.",

      "sub.cmp.r11": "Ads",
      "sub.cmp.r11free": "Yes",
      "sub.cmp.r11pro": "None",
      "sub.cmp.r11s": "Premium removes ads from the app entirely.",

      /* Premium storytelling rows */
      "sub.unl.kicker": "What Premium unlocks",
      "sub.unl.title": "Six things that <em class=\"accent\">switch on</em>.",
      "sub.unl.sub": "Not a longer list of the same thing — these are the parts of Fotocal that need Premium, and what each one actually does for you.",

      "sub.u1.pill": "The main one",
      "sub.u1.t": "Unlimited AI food scans",
      "sub.u1.b": "The free plan gives you 3 AI photo scans a day, which covers breakfast, lunch and dinner. It is genuinely enough to use Fotocal properly. What it does not cover is the day with a snack, a coffee, something at a friend's place and dinner out — and that is exactly the day you most want logged, because it is the one you would never reconstruct accurately from memory.",
      "sub.u1.b2": "Premium removes the counter. Scan eleven times in a day if that is what your day looked like. The point of photo logging is that it is cheap enough to do every single time, and a daily limit quietly works against that.",
      "sub.u1.li1": "No daily cap — scan as often as you eat",
      "sub.u1.li2": "The messy days get logged too, not just the tidy ones",
      "sub.u1.li3": "Same scanner, same speed, just no counter",
      "sub.u1.slot": "Scan screen — unlimited scanning",

      "sub.u2.pill": "Deeper analysis",
      "sub.u2.t": "Advanced nutrition insights",
      "sub.u2.b": "Daily totals tell you whether you hit your calories. They do not tell you that your protein is consistently low on the days you eat out, or that your week falls apart on Thursdays rather than at the weekend like you assumed. Advanced insights look across your logged data for the patterns underneath the numbers.",
      "sub.u2.b2": "This is the part that turns tracking into understanding. Anyone can see a number. Knowing which of your habits is actually driving it is the useful bit — and that only becomes visible with enough logged days to look across.",
      "sub.u2.li1": "Patterns across your macros, not just daily totals",
      "sub.u2.li2": "Where your week reliably goes off track",
      "sub.u2.li3": "Built from your own logged data, not averages of other people",
      "sub.u2.slot": "Advanced insights — nutrition breakdown",

      "sub.u3.pill": "Every week",
      "sub.u3.t": "Weekly reports",
      "sub.u3.b": "A single day is noise. One big dinner is not a trend, and one perfect Tuesday is not progress. The weekly report is where a week's worth of logging gets pulled into something you can actually act on: how your calories and macros really landed, which habits held, where things slipped, and one or two specific things worth changing next week.",
      "sub.u3.b2": "It is deliberately not a scoreboard. There is no grade and nothing to fail. It is a summary written to be read on a Sunday evening and to leave you with one clear idea for the week ahead.",
      "sub.u3.li1": "Trends across the whole week, not a single day",
      "sub.u3.li2": "What went well, said as plainly as what did not",
      "sub.u3.li3": "One or two concrete changes, not a lecture",
      "sub.u3.slot": "Weekly report — the week's trends",

      "sub.u4.pill": "Made for you",
      "sub.u4.t": "Personalised plans & recommendations",
      "sub.u4.b": "Generic advice is easy to give and easy to ignore, because it is not about you. Premium recommendations are shaped around your goals, your logged meals and how your week is actually going — so a suggestion arrives when it is relevant rather than as a list of rules you were meant to memorise on day one.",
      "sub.u4.b2": "They adapt as you do. Change your goal, change what you eat, or have a genuinely bad fortnight, and what Fotocal suggests moves with you instead of repeating the same advice at you.",
      "sub.u4.li1": "Built around your goals and your real logged data",
      "sub.u4.li2": "Adapts as your goals and habits change",
      "sub.u4.li3": "Suggestions when they are relevant, not a rulebook",
      "sub.u4.slot": "Personalised plan & recommendations",

      "sub.u5.pill": "Your data, kept",
      "sub.u5.t": "Sync",
      "sub.u5.b": "Months of logging is worth something, and it should not be tied to one handset. Sync keeps your diary, your weight history and your progress in step and carries them over when you change phone. Fotocal is offline-first, so you can always log without a connection — sync is what makes that data safe rather than stranded.",
      "sub.u5.li1": "Your diary and history carried to a new phone",
      "sub.u5.li2": "Works with offline-first logging, not against it",
      "sub.u5.li3": "Months of data that is not stuck on one device",
      "sub.u5.slot": "Sync — data carried across devices",

      "sub.u6.pill": "Quieter",
      "sub.u6.t": "No ads",
      "sub.u6.b": "Premium removes ads from the app completely. Logging a meal takes a few seconds, and an ad in the middle of those few seconds is friction in exactly the wrong place — the whole design goal is that tracking is too quick to talk yourself out of.",
      "sub.u6.li1": "No ads anywhere in the app",
      "sub.u6.li2": "Nothing between you and logging a meal",
      "sub.u6.li3": "Your subscription is what pays for the app instead",
      "sub.u6.slot": "The app with no ads",

      /* Billing */
      "sub.bill.kicker": "Billing & cancelling",
      "sub.bill.title": "Handled by <em class=\"accent\">Google Play</em>.",
      "sub.bill.p1": "Fotocal is an Android app, so every subscription is bought, billed and cancelled through Google Play. We never see or store your card details — Google handles the payment side entirely.",
      "sub.bill.p2": "That has a practical upside: whatever you need to do with your subscription, you do it in one place you already have on your phone, and it works the same way as every other subscription you have there.",
      "sub.bill.h3": "How to cancel",
      "sub.bill.s1": "Open the <b>Play Store</b> app on your phone.",
      "sub.bill.s2": "Tap your <b>profile icon</b> in the top right.",
      "sub.bill.s3": "Go to <b>Payments and subscriptions → Subscriptions</b>.",
      "sub.bill.s4": "Select <b>Fotocal</b> and tap <b>Cancel subscription</b>.",
      "sub.bill.after": "You keep Premium until the end of the period you have already paid for — cancelling does not cut you off on the spot. After that you drop back to the free plan, and your logged data stays exactly where it is.",
      "sub.bill.renew.h": "It renews automatically",
      "sub.bill.renew.b": "Every plan renews on its own until you cancel — that is how Google Play subscriptions work. You can cancel at any time, and if you are on the yearly trial, cancelling within the 3 days means you are not charged at all.",
      "sub.bill.refund.h": "Refunds",
      "sub.bill.refund.b": "Refunds are handled under Google Play's own refund policy, since Google is the seller. If something has gone wrong with a charge, email us and we will help you sort it out — but the refund itself goes through Google Play.",

      /* FAQ */
      "sub.faq.kicker": "FAQ",
      "sub.faq.title": "Subscription <em class=\"accent\">questions</em>",
      "sub.faq.q1": "Can I use Fotocal without paying?",
      "sub.faq.a1": "Yes, indefinitely. The free plan gives you 3 AI photo scans a day, unlimited Coach Kal, the meal diary, weight and progress tracking, water, steps and offline mode. Plenty of people will never need more than that. Premium is for when the daily scan limit starts getting in your way or you want the weekly reports and deeper insights.",
      "sub.faq.q2": "Which plans have a free trial?",
      "sub.faq.a2": "Only the yearly plan. It comes with a 3-day free trial, and if you cancel before the 3 days are up you are not charged. The monthly and 3-month plans start billing immediately.",
      "sub.faq.q3": "Do all three plans unlock the same things?",
      "sub.faq.a3": "Yes. There is one Premium and every plan unlocks all of it. The only thing you are choosing is how long it runs and what it works out to per month.",
      "sub.faq.q4": "Is Coach Kal really free?",
      "sub.faq.a4": "Really. Coach Kal is unlimited on the free plan and always has been. It is not a trial, not a teaser, and there is no message cap.",
      "sub.faq.q5": "Do the prices include tax?",
      "sub.faq.a5": "Yes. Prices are in euros and include Spanish VAT at 21%. Nothing is added on top at checkout.",
      "sub.faq.q6": "What happens to my data if I cancel?",
      "sub.faq.a6": "It stays. You drop back to the free plan and keep your diary, your weight history and everything else you have logged — you just go back to 3 AI scans a day. Nothing is deleted because you stopped paying.",
      "sub.faq.q7": "Can I switch plans?",
      "sub.faq.a7": "Yes, through Google Play, in the same Subscriptions screen where you cancel. Google handles the proration when you change.",
      "sub.faq.q8": "How do I cancel?",
      "sub.faq.a8": "In the Play Store app: your profile icon → Payments and subscriptions → Subscriptions → Fotocal → Cancel subscription. You keep Premium until the period you have paid for runs out.",

      "sub.cta.title": "Start free. <em class=\"accent-light\">Upgrade if it earns it</em>.",
      "sub.cta.sub": "Download Fotocal, use it free for as long as you like, and go Premium only when the daily scan limit is the thing standing in your way.",

      /* ─────────────────────────────────────────────
         BLOG
         ───────────────────────────────────────────── */
      "blog.meta.title": "Blog — Fotocal",
      "blog.kicker": "Blog",
      "blog.title": "Notes on eating, <em class=\"accent\">honestly</em>.",
      "blog.lead": "This is where we will write about nutrition, weight, and the habits that hold the whole thing together — the practical, unglamorous side of eating better that most of the internet skips over on its way to selling you something.",
      "blog.lead2": "Nothing is published yet. Rather than pad this page out with filler, we would rather leave it honest and start it properly.",

      "blog.topics.kicker": "What we will write about",
      "blog.topics.title": "Three things, <em class=\"accent\">covered properly</em>.",
      "blog.topics.sub": "Not a content calendar chasing search traffic. These are the three areas Fotocal is built around, and the ones worth writing something useful about.",

      "blog.t1.t": "Nutrition",
      "blog.t1.b": "What macros actually do, why calorie numbers on a label are estimates too, how to read a portion, and where the popular advice is oversimplified. The aim is that you finish a post understanding something rather than just believing us.",
      "blog.t1.li1": "How estimates work, and their limits",
      "blog.t1.li2": "Protein, carbs and fat without the dogma",
      "blog.t1.li3": "Reading labels and portions in real life",

      "blog.t2.t": "Weight loss",
      "blog.t2.b": "Losing weight in a way that survives contact with an ordinary life — plateaus, water weight, why the scale lies on a daily basis, and why the approaches that work slowly are the ones still working in a year. No before-and-afters, no crash plans.",
      "blog.t2.li1": "Why daily weight bounces, and what to read instead",
      "blog.t2.li2": "Plateaus and what is really happening",
      "blog.t2.li3": "Sustainable beats fast, and why",

      "blog.t3.t": "Habits & mindset",
      "blog.t3.b": "The part that decides everything and gets written about least. How a habit actually forms, why tracking collapses in week three, what to do after a bad week, and how to make eating well take less willpower rather than more.",
      "blog.t3.li1": "Why tracking usually stops in week three",
      "blog.t3.li2": "Getting back on after a bad week, without the guilt",
      "blog.t3.li3": "Making the good option the easy option",

      "blog.empty.h": "No posts yet",
      "blog.empty.b": "The first article has not been written. When posts start going up they will appear here — until then, this page is not going to pretend otherwise.",
      "blog.empty.cta1": "Follow on Instagram",
      "blog.empty.cta2": "Get the app",
      "blog.empty.note": "Instagram is where anything gets posted first, so that is the best place to catch the first article.",

      "blog.demo.kicker": "Design preview",
      "blog.demo.title": "What a post will <em class=\"accent\">look like</em>.",
      "blog.demo.sub": "The card below is a layout example so the design is ready the moment there is something to publish. It is not an article, it is not written, and it does not link anywhere.",
      "blog.demo.ribbon": "Example layout — not a real article",
      "blog.demo.tag": "Example",
      "blog.demo.h": "This is where a post title will sit",
      "blog.demo.b": "And this is the summary line — two or three sentences explaining what the post covers, so you can tell from the card whether it is worth your time. The real thing will have a real title, a real date and a real link.",
      "blog.demo.meta": "Date goes here",
      "blog.demo.read": "5 min read",

      "blog.cta.title": "The app is <em class=\"accent-light\">already written</em>, even if the blog is not.",
      "blog.cta.sub": "Fotocal is on Google Play now. The articles will follow.",

      /* ─────────────────────────────────────────────
         ABOUT
         ───────────────────────────────────────────── */
      "about.meta.title": "About Us — Fotocal",
      "about.kicker": "About us",
      "about.title": "We want you to <em class=\"accent\">see what you eat</em> — as you eat it.",
      "about.lead": "Fotocal is an independent app, built small. No investors, no marketing department, no growth targets. Just a nutrition tracker built the way we thought one should work.",
      "about.lead2": "This page is about why it exists and what we believe. It is deliberately short on biography and long on intent.",

      "about.story.kicker": "Why Fotocal exists",
      "about.story.title": "Most people never actually <em class=\"accent\">see</em> their own eating.",
      "about.story.p1": "Here is the thing that started this. Almost everyone eats three or more times a day, every day, for their whole life — and almost nobody has any real picture of what that adds up to. Not because they do not care. Because looking was always too much work.",
      "about.story.p2": "The traditional way to find out involves waiting for an appointment, then sitting in a room trying to remember what you ate last Tuesday. And you cannot remember. Nobody can. So you reconstruct it, roughly, and you get advice based on a rough reconstruction, and then you wait months and do it again. It is not that the advice is wrong — it is that the picture it is built on is a guess.",
      "about.story.p3": "Meanwhile the thing that would help most is something you could have had all along: seeing what you eat as you eat it. Not remembered. Not estimated weeks later. Just there, in front of you, on the day it happened.",
      "about.story.pull": "We want people to be able to see their own eating in real time — and watch their own transformation happen — instead of it being invisible until someone else points it out.",
      "about.story.p4": "That is the whole idea. Not a diet. Not a plan we invented and want you to follow. Just visibility — the ordinary, day-to-day kind that turns \"I think I eat pretty well\" into something you actually know.",

      "about.mission.kicker": "The mission",
      "about.mission.title": "Make understanding your own eating <em class=\"accent\">effortless</em>.",
      "about.mission.p1": "If tracking is hard, you stop. That is not a character flaw, it is arithmetic — anything you have to do three times a day has to be nearly free or it will not survive the month. Every app that made you search a database, find your food, guess the portion and confirm it was asking for a few minutes a day, and a few minutes a day is more than almost anyone will pay.",
      "about.mission.p2": "So the goal was to make it cost a photo. Point the camera at the plate, and the work happens on our side rather than yours. That is not a gimmick — it is the only version of tracking we have seen that people are still doing in month three, because it is the only one cheap enough to keep doing.",
      "about.mission.p3": "Everything else follows from that. Offline-first, because you eat in places with no signal and a tracker that fails at a restaurant is not a tracker. Coach Kal free and unlimited, because the part most likely to change how you eat should not be the part you have to pay for. Progress shown as trends rather than daily numbers, because a single morning on a scale means nothing and panicking about it helps nobody.",

      "about.empower.kicker": "Your data, your understanding",
      "about.empower.title": "Knowledge in <em class=\"accent\">your own hands</em>, every day.",
      "about.empower.p1": "There is a real difference between being told about your eating and seeing it. Being told is something that happens to you occasionally. Seeing it is something you own, every day, and it changes what you do next without anyone having to tell you anything.",
      "about.empower.p2": "That is what we want Fotocal to give you. Not instructions. Visibility. You log a week and the picture shows up on its own — where the calories actually come from, which days hold together, what your protein really looks like when it is not a guess. Most people find the answer surprising, and surprising is useful. You cannot change a pattern you cannot see.",
      "about.empower.p3": "And the transformation gets visible too, which matters more than it sounds. Progress is slow and mostly invisible from the inside — you do not notice change in a mirror you look at daily. Weight trends, measurements, macros, streaks: they make the slow thing legible. That is the difference between a month that felt pointless and a month you can see worked.",

      "about.comp.h": "Fotocal works with your doctor, not instead of them",
      "about.comp.b": "We want to be very clear about this, because it matters. Fotocal is not a substitute for professional care, and it is not designed to help you avoid it. If anything, the opposite: the most useful thing about having your real eating data is that you can walk into an appointment with it.",
      "about.comp.b2": "Instead of trying to remember last Tuesday, you can show what the last three months actually looked like. A doctor or a dietitian working from real data can give you far better advice than one working from your best guess — that is a better conversation, not a skipped one. If you have a health concern, please go and see someone. Bring your data with you.",

      "about.values.kicker": "What we believe",
      "about.values.title": "The rules we <em class=\"accent\">hold ourselves to</em>.",
      "about.values.sub": "Not a poster in an office. These are the calls that actually decided how the app was built, including the ones that cost us something.",

      "about.v1.t": "Effortless, or it does not count",
      "about.v1.b": "If a feature adds friction to logging a meal, it is wrong, however clever it is. Tracking has to stay cheap enough to do every time or it will not get done at all.",
      "about.v2.t": "Never shaming",
      "about.v2.b": "No red numbers, no guilt, no app disappointed in you. You ate a dessert. It is a dessert. Shame has never made anyone eat better and it makes plenty of people stop logging, which is worse.",
      "about.v3.t": "Honest about the AI",
      "about.v3.b": "Photo analysis gives an estimate, not a lab result. Stews, mixed dishes and anything under a sauce are genuinely hard. We say so, and you can correct any scan before you save it.",
      "about.v4.t": "No promises we cannot keep",
      "about.v4.b": "We will not tell you that you will lose a specific amount in a specific time. Nobody honest can. Fotocal shows you what you are doing — what happens next depends on a lot of things that are not an app.",
      "about.v5.t": "Works anywhere",
      "about.v5.b": "Offline-first, deliberately. You eat in basements, on planes and in places with no bars of signal, and a tracker that only works on good Wi-Fi is not one.",
      "about.v6.t": "Your data is yours",
      "about.v6.b": "We do not sell it. You can delete your account and everything in it whenever you want, and it is a normal option in the app rather than a form you have to beg through.",

      "about.small.kicker": "Who is behind it",
      "about.small.title": "Small, independent, <em class=\"accent\">and honest about it</em>.",
      "about.small.p1": "Fotocal is built and run independently, by a very small team. There is no office, no investors and no growth department. We would rather say that plainly than invent a founding story with a big number in it.",
      "about.small.p2": "That has real trade-offs. We move slower than a company with fifty engineers. Some things you might want are not built yet. But it also means nobody is pushing us to add a dark pattern to make a quarterly number, and when you email support, it reaches the people who made the thing.",
      "about.small.p3": "You will notice this page has no user counts, no ratings, no press quotes and no awards. That is not modesty — it is that we are not going to make any up, and we do not think you should trust a site that does.",

      "about.med.h": "One quick note",
      "about.med.b": "Fotocal is a tracking tool, not medical advice. It does not diagnose anything and it is not a treatment. If you have a health condition, are pregnant, are managing an eating disorder, or you are just not sure whether a change is right for you, please talk to a doctor or a registered dietitian first — and take your Fotocal data along, it will make that conversation a better one.",

      "about.next.contact": "Contact us",
      "about.next.contactB": "Questions, feedback, or anything at all",
      "about.next.privacy": "Privacy Policy",
      "about.next.privacyB": "Exactly what we do with your data",

      "about.cta.title": "See your own eating, <em class=\"accent-light\">starting today</em>.",
      "about.cta.sub": "Fotocal is free to download and free to use. One photo is all it takes to start.",

      /* ─────────────────────────────────────────────
         CONTACT
         ───────────────────────────────────────────── */
      "contact.meta.title": "Contact Us — Fotocal",
      "contact.kicker": "Contact",
      "contact.title": "Talk to <em class=\"accent\">an actual person</em>.",
      "contact.lead": "One email address, read by the people who built the app. No ticket number, no chatbot, no support tier to escalate through.",
      "contact.lead2": "Pick whichever applies below — it just pre-fills the subject line so we can find your email faster.",
      "contact.mailLabel": "Email us at",

      "contact.routes.kicker": "What is it about?",
      "contact.routes.title": "Three ways in. <em class=\"accent\">Same inbox</em>.",
      "contact.routes.sub": "All three go to the same address. The subject line just tells us what we are looking at before we open it.",

      "contact.r1.t": "Support & help",
      "contact.r1.b": "Something is broken, a scan is behaving strangely, you are stuck, or you have a question about your subscription or a charge. This is the one for almost everything.",
      "contact.r1.li1": "Bugs and crashes",
      "contact.r1.li2": "Scans, Coach Kal, syncing",
      "contact.r1.li3": "Subscriptions and billing",
      "contact.r1.cta": "Email support",

      "contact.r2.t": "Privacy & your data",
      "contact.r2.b": "Anything about what we store, how we use it, or getting it deleted. If you want your account and data gone, the app can do it in a couple of taps — but you can also just ask us.",
      "contact.r2.li1": "Data access and deletion",
      "contact.r2.li2": "Questions about the Privacy Policy",
      "contact.r2.li3": "How your information is handled",
      "contact.r2.cta": "Email about privacy",

      "contact.r3.t": "Business & press",
      "contact.r3.b": "Partnerships, press, or anything commercial. We are small and independent, so we read these ourselves — and we will tell you straight if it is not a fit.",
      "contact.r3.li1": "Partnerships and collaborations",
      "contact.r3.li2": "Press and media questions",
      "contact.r3.li3": "Anything commercial",
      "contact.r3.cta": "Email about business",

      "contact.help.kicker": "Getting a good answer faster",
      "contact.help.title": "What to <em class=\"accent\">put in the email</em>.",
      "contact.help.p1": "None of this is required — send a one-line email if that is what you have and we will still reply. But if something is broken, these are the details that usually decide whether we can fix it in one reply or have to spend three emails asking you questions.",
      "contact.help.s1": "<b>Your phone and Android version.</b> Settings → About phone. A surprising number of bugs only happen on one manufacturer's build.",
      "contact.help.s2": "<b>What you were doing.</b> The screen you were on and the last thing you tapped before it went wrong.",
      "contact.help.s3": "<b>A screenshot.</b> Worth roughly a page of description, especially for anything visual or for a scan that came back odd.",
      "contact.help.s4": "<b>The email on your account</b>, if it is a subscription or account question — otherwise we cannot find you.",
      "contact.help.p2": "For a scan that got something wrong, the original photo helps a lot. It is the only way we can tell whether the model misread the food or the portion.",

      "contact.exp.h": "When you will hear back",
      "contact.exp.b": "We aim to reply within a few days. Fotocal is run by a small independent team, so this is a genuine best effort rather than a service guarantee — we would rather tell you that than promise a number we might miss. Every email does get read, and if one has gone unanswered longer than a week, please just send it again. It will be an oversight, not a decision.",

      "contact.quick.kicker": "Before you write",
      "contact.quick.title": "Three things with <em class=\"accent\">instant answers</em>.",
      "contact.quick.sub": "These are the three we get asked most, and all three are faster to do than to email about.",

      "contact.q1.t": "Cancelling your subscription",
      "contact.q1.b": "We cannot cancel it for you — Google Play is the seller, so it has to be done there. Play Store → your profile icon → Payments and subscriptions → Subscriptions → Fotocal → Cancel. You keep Premium until the period you paid for ends.",
      "contact.q1.cta": "More on billing",
      "contact.q2.t": "Deleting your account",
      "contact.q2.b": "You can do it yourself in the app, and it removes your data. The steps are on our account deletion page, and you can email us instead if you would rather.",
      "contact.q2.cta": "Account deletion",
      "contact.q3.t": "What we do with your data",
      "contact.q3.b": "The Privacy Policy covers what is stored, why, and how to get rid of it. If it does not answer your question, that is a gap in the policy and we would like to know.",
      "contact.q3.cta": "Privacy Policy",

      "contact.cta.title": "We would rather hear it <em class=\"accent-light\">than not</em>.",
      "contact.cta.sub": "Bugs, confusion, blunt feedback, or an idea for something Fotocal should do — it all helps, and it all gets read.",
      "contact.cta.btn": "Send us an email"
    },

    /* ══════════════════════ SPANISH ══════════════════════ */
    es: {

      /* ─────────────────────────────────────────────
         SUSCRIPCIÓN
         ───────────────────────────────────────────── */
      "sub.meta.title": "Suscripción y precios — Fotocal",
      "sub.kicker": "Suscripción",
      "sub.title": "Todo lo que Fotocal sabe hacer, <em class=\"accent\">desbloqueado</em>.",
      "sub.lead": "Fotocal se descarga gratis y se usa gratis todos los días. Premium quita el límite diario de escaneos con IA y enciende el análisis profundo: informes semanales, recomendaciones personalizadas, sincronización y una app sin anuncios.",
      "sub.lead2": "Tres duraciones, un mismo conjunto de funciones. Cuanto más largo el plan, menos cuesta al mes. Ese es todo el modelo de precios: sin niveles que descifrar, sin extras.",
      "sub.hero.cta": "Descargar en Google Play",
      "sub.hero.compare": "Comparar gratis y Premium ↓",

      "sub.kal.h": "Coach Kal es gratis. Para todos y sin límite.",
      "sub.kal.b": "Tu entrenador nutricional con IA no es una función Premium y nunca lo ha sido. Pregúntale a Coach Kal todo lo que quieras, en el plan gratuito, para siempre. Es la parte de Fotocal que más probablemente cambie cómo comes, así que ponerla detrás de un muro de pago sería hacerlo al revés.",

      "sub.plans.kicker": "Los planes",
      "sub.plans.title": "Elige duración. <em class=\"accent\">El mismo Premium</em> en todas.",
      "sub.plans.sub": "Todos los planes desbloquean exactamente las mismas funciones. La única diferencia es cuánto duran y a cuánto salen al mes.",

      "sub.p.m.name": "Mensual",
      "sub.p.m.per": "/mes",
      "sub.p.m.equiv": "Se cobra cada mes.",
      "sub.p.m.note": "El flexible. Va bien si quieres probar Premium a fondo durante un mes sin pensar más allá de eso.",
      "sub.p.m.trial": "Este plan no tiene prueba gratis: el cobro empieza directamente.",

      "sub.p.y.name": "Anual",
      "sub.p.y.per": "/año",
      "sub.p.y.equiv": "Sale a <b>unos 2,92 € al mes</b>.",
      "sub.p.y.note": "La forma más barata de usar Fotocal y el único plan con prueba gratis. Ideal si ya sabes que quieres construir el hábito durante todo un año.",
      "sub.p.y.trial": "Incluye 3 días de prueba gratis. Si cancelas antes de que terminen, no se te cobra nada.",
      "sub.p.y.flag": "MÁS POPULAR",
      "sub.p.y.save": "Ahorras un 58% aprox. frente al mensual",

      "sub.p.q.name": "3 meses",
      "sub.p.q.per": "/3 meses",
      "sub.p.q.equiv": "Sale a <b>unos 5,66 € al mes</b>.",
      "sub.p.q.note": "El término medio. Una temporada entera da tiempo a que cuaje el hábito sin comprometerte a un año.",
      "sub.p.q.trial": "Este plan no tiene prueba gratis: el cobro empieza directamente.",
      "sub.p.q.save": "Ahorras un 19% aprox. frente al mensual",

      "sub.p.cta": "Descargar en Google Play",
      "sub.p.ctaY": "Empezar los 3 días gratis",

      "sub.trial.h": "La prueba gratis es solo del plan anual",
      "sub.trial.b": "Merece la pena dejarlo claro, porque muchas apps no lo hacen. Los 3 días de prueba gratis vienen con el plan anual. Los planes mensual y de 3 meses no tienen prueba: si eliges uno de esos, el cobro empieza de inmediato.",
      "sub.trial.b2": "Si quieres probar Premium sin coste, empieza el plan anual y cancela dentro de los 3 días. No se te cobrará nada. Y si prefieres no lidiar con una prueba, el plan mensual es la opción más sencilla.",

      "sub.vat": "Todos los precios están en euros e incluyen el IVA español del 21%. Lo que ves aquí es lo que pagas: no se añade nada al finalizar la compra.",

      "sub.cmp.kicker": "Gratis vs Premium",
      "sub.cmp.title": "Qué incluye cada uno, <em class=\"accent\">línea por línea</em>.",
      "sub.cmp.sub": "El plan gratuito es un producto de verdad, no una demo: puedes registrar todas tus comidas, todos los días, para siempre, sin pagar. Aquí está exactamente dónde está la línea.",
      "sub.cmp.caption": "Plan gratuito de Fotocal comparado con Fotocal Premium",
      "sub.cmp.colFeature": "Función",
      "sub.cmp.colFree": "Gratis",
      "sub.cmp.colPro": "Premium",
      "sub.cmp.yes": "Incluido",
      "sub.cmp.no": "No incluido",

      "sub.cmp.r1": "Escaneos de comida con IA",
      "sub.cmp.r1s": "Fotografía una comida y obtén calorías, macros y una puntuación de calidad.",
      "sub.cmp.r1free": "3 al día",
      "sub.cmp.r1pro": "Ilimitados",

      "sub.cmp.r2": "Coach Kal",
      "sub.cmp.r2s": "Tu entrenador nutricional con IA: gratis para todos, en todos los planes.",
      "sub.cmp.r2free": "Ilimitado",
      "sub.cmp.r2pro": "Ilimitado",

      "sub.cmp.r3": "Diario de comidas",
      "sub.cmp.r3s": "Registra desayuno, comida, cena y snacks frente a tus objetivos.",

      "sub.cmp.r4": "Peso y progreso",
      "sub.cmp.r4s": "Registra tu peso y tus medidas y observa la tendencia.",

      "sub.cmp.r5": "Agua y pasos",
      "sub.cmp.r5s": "Hidratación diaria y pasos a través de Health Connect.",

      "sub.cmp.r6": "Modo sin conexión",
      "sub.cmp.r6s": "Registra sin cobertura. El escaneo con IA sí necesita conexión.",

      "sub.cmp.r7": "Análisis nutricional avanzado",
      "sub.cmp.r7s": "La lectura profunda de tus macros y tus patrones, más allá de los totales del día.",

      "sub.cmp.r8": "Informes semanales",
      "sub.cmp.r8s": "Un resumen semanal de tendencias, aciertos y lo que se torció.",

      "sub.cmp.r9": "Planes y recomendaciones personalizadas",
      "sub.cmp.r9s": "Orientación adaptada a tus objetivos y a lo que registras de verdad.",

      "sub.cmp.r10": "Sincronización",
      "sub.cmp.r10s": "Tus datos al día y trasladados a un móvil nuevo.",

      "sub.cmp.r11": "Anuncios",
      "sub.cmp.r11free": "Sí",
      "sub.cmp.r11pro": "Ninguno",
      "sub.cmp.r11s": "Premium elimina por completo los anuncios de la app.",

      "sub.unl.kicker": "Qué desbloquea Premium",
      "sub.unl.title": "Seis cosas que <em class=\"accent\">se encienden</em>.",
      "sub.unl.sub": "No es una lista más larga de lo mismo: estas son las partes de Fotocal que necesitan Premium, y lo que hace cada una por ti.",

      "sub.u1.pill": "La principal",
      "sub.u1.t": "Escaneos de comida con IA ilimitados",
      "sub.u1.b": "El plan gratuito te da 3 escaneos con IA al día, que cubren desayuno, comida y cena. Es de verdad suficiente para usar Fotocal como toca. Lo que no cubre es el día con un snack, un café, algo en casa de un amigo y cena fuera. Y justo ese es el día que más te interesa registrar, porque es el que nunca reconstruirías bien de memoria.",
      "sub.u1.b2": "Premium quita el contador. Escanea once veces en un día si tu día fue así. La gracia de registrar con fotos es que sale tan barato que lo haces siempre, y un límite diario juega en contra de eso sin hacer ruido.",
      "sub.u1.li1": "Sin tope diario: escanea tantas veces como comas",
      "sub.u1.li2": "Los días caóticos también se registran, no solo los ordenados",
      "sub.u1.li3": "El mismo escáner, la misma velocidad, sin contador",
      "sub.u1.slot": "Pantalla de escaneo — escaneos ilimitados",

      "sub.u2.pill": "Análisis profundo",
      "sub.u2.t": "Análisis nutricional avanzado",
      "sub.u2.b": "Los totales del día te dicen si has llegado a tus calorías. No te dicen que tu proteína está siempre baja los días que comes fuera, ni que tu semana se rompe los jueves y no el fin de semana como tú creías. El análisis avanzado busca en tus datos registrados los patrones que hay debajo de los números.",
      "sub.u2.b2": "Esta es la parte que convierte el registro en comprensión. Un número lo ve cualquiera. Lo útil es saber cuál de tus hábitos lo está provocando, y eso solo se ve cuando hay suficientes días registrados como para mirar el conjunto.",
      "sub.u2.li1": "Patrones en tus macros, no solo totales diarios",
      "sub.u2.li2": "Dónde se te tuerce la semana de forma sistemática",
      "sub.u2.li3": "Construido con tus datos, no con la media de otras personas",
      "sub.u2.slot": "Análisis avanzado — desglose nutricional",

      "sub.u3.pill": "Cada semana",
      "sub.u3.t": "Informes semanales",
      "sub.u3.b": "Un día suelto es ruido. Una cena copiosa no es una tendencia, y un martes perfecto no es progreso. El informe semanal es donde una semana de registro se convierte en algo accionable: cómo quedaron de verdad tus calorías y macros, qué hábitos aguantaron, dónde se torció la cosa y una o dos cosas concretas que cambiar la semana que viene.",
      "sub.u3.b2": "A propósito no es un marcador. No hay nota ni hay nada que suspender. Es un resumen escrito para leerse un domingo por la tarde y dejarte con una idea clara para la semana siguiente.",
      "sub.u3.li1": "Tendencias de toda la semana, no de un solo día",
      "sub.u3.li2": "Lo que salió bien, dicho tan claro como lo que no",
      "sub.u3.li3": "Una o dos cosas concretas, no un sermón",
      "sub.u3.slot": "Informe semanal — las tendencias de la semana",

      "sub.u4.pill": "Hecho para ti",
      "sub.u4.t": "Planes y recomendaciones personalizadas",
      "sub.u4.b": "Los consejos genéricos son fáciles de dar y fáciles de ignorar, porque no van sobre ti. Las recomendaciones Premium se construyen sobre tus objetivos, tus comidas registradas y cómo te está yendo la semana de verdad, así que la sugerencia llega cuando es relevante y no como una lista de normas que tenías que memorizar el primer día.",
      "sub.u4.b2": "Se adaptan según cambias tú. Cambia de objetivo, cambia lo que comes o ten quince días francamente malos: lo que Fotocal te sugiere se mueve contigo en vez de repetirte el mismo consejo.",
      "sub.u4.li1": "Construidas sobre tus objetivos y tus datos reales",
      "sub.u4.li2": "Se adaptan cuando cambian tus objetivos y hábitos",
      "sub.u4.li3": "Sugerencias cuando vienen a cuento, no un reglamento",
      "sub.u4.slot": "Plan y recomendaciones personalizadas",

      "sub.u5.pill": "Tus datos, a salvo",
      "sub.u5.t": "Sincronización",
      "sub.u5.b": "Meses de registro valen algo, y no deberían estar atados a un solo móvil. La sincronización mantiene al día tu diario, tu histórico de peso y tu progreso, y se los lleva contigo cuando cambias de teléfono. Fotocal es offline-first, así que siempre puedes registrar sin conexión: la sincronización es lo que hace que esos datos estén a salvo en vez de atrapados.",
      "sub.u5.li1": "Tu diario y tu histórico se trasladan a un móvil nuevo",
      "sub.u5.li2": "Funciona con el registro sin conexión, no contra él",
      "sub.u5.li3": "Meses de datos que no se quedan en un solo dispositivo",
      "sub.u5.slot": "Sincronización — datos entre dispositivos",

      "sub.u6.pill": "Más tranquilo",
      "sub.u6.t": "Sin anuncios",
      "sub.u6.b": "Premium elimina los anuncios de la app por completo. Registrar una comida cuesta unos segundos, y un anuncio en mitad de esos segundos es fricción justo donde no debe estar: todo el diseño busca que registrar sea demasiado rápido como para que te dé tiempo a echarte atrás.",
      "sub.u6.li1": "Ni un anuncio en ninguna parte de la app",
      "sub.u6.li2": "Nada entre tú y registrar una comida",
      "sub.u6.li3": "Tu suscripción es lo que paga la app en su lugar",
      "sub.u6.slot": "La app sin anuncios",

      "sub.bill.kicker": "Cobros y cancelación",
      "sub.bill.title": "Lo gestiona <em class=\"accent\">Google Play</em>.",
      "sub.bill.p1": "Fotocal es una app de Android, así que todas las suscripciones se compran, se cobran y se cancelan a través de Google Play. Nosotros nunca vemos ni guardamos los datos de tu tarjeta: del pago se encarga Google por completo.",
      "sub.bill.p2": "Eso tiene una ventaja práctica: hagas lo que hagas con tu suscripción, lo haces en un único sitio que ya tienes en el móvil, y funciona igual que cualquier otra suscripción que tengas allí.",
      "sub.bill.h3": "Cómo cancelar",
      "sub.bill.s1": "Abre la app de <b>Play Store</b> en tu móvil.",
      "sub.bill.s2": "Toca tu <b>icono de perfil</b> arriba a la derecha.",
      "sub.bill.s3": "Entra en <b>Pagos y suscripciones → Suscripciones</b>.",
      "sub.bill.s4": "Selecciona <b>Fotocal</b> y toca <b>Cancelar suscripción</b>.",
      "sub.bill.after": "Mantienes Premium hasta el final del periodo que ya has pagado: cancelar no te corta en el acto. Después vuelves al plan gratuito, y tus datos registrados se quedan exactamente donde están.",
      "sub.bill.renew.h": "Se renueva automáticamente",
      "sub.bill.renew.b": "Todos los planes se renuevan solos hasta que canceles: así funcionan las suscripciones de Google Play. Puedes cancelar cuando quieras, y si estás en la prueba del plan anual, cancelar dentro de los 3 días significa que no se te cobra nada.",
      "sub.bill.refund.h": "Reembolsos",
      "sub.bill.refund.b": "Los reembolsos se gestionan según la propia política de Google Play, ya que Google es el vendedor. Si ha habido algún problema con un cobro, escríbenos y te ayudamos a resolverlo, pero el reembolso en sí pasa por Google Play.",

      "sub.faq.kicker": "FAQ",
      "sub.faq.title": "Preguntas sobre la <em class=\"accent\">suscripción</em>",
      "sub.faq.q1": "¿Puedo usar Fotocal sin pagar?",
      "sub.faq.a1": "Sí, indefinidamente. El plan gratuito te da 3 escaneos con IA al día, Coach Kal ilimitado, el diario de comidas, seguimiento de peso y progreso, agua, pasos y modo sin conexión. Mucha gente no necesitará nunca más que eso. Premium es para cuando el límite diario de escaneos empiece a estorbarte o quieras los informes semanales y el análisis profundo.",
      "sub.faq.q2": "¿Qué planes tienen prueba gratis?",
      "sub.faq.a2": "Solo el plan anual. Viene con 3 días de prueba gratis, y si cancelas antes de que terminen no se te cobra nada. Los planes mensual y de 3 meses empiezan a cobrar de inmediato.",
      "sub.faq.q3": "¿Los tres planes desbloquean lo mismo?",
      "sub.faq.a3": "Sí. Hay un único Premium y todos los planes lo desbloquean entero. Lo único que eliges es cuánto dura y a cuánto sale al mes.",
      "sub.faq.q4": "¿Coach Kal es gratis de verdad?",
      "sub.faq.a4": "De verdad. Coach Kal es ilimitado en el plan gratuito y siempre lo ha sido. No es una prueba, no es un anzuelo y no hay tope de mensajes.",
      "sub.faq.q5": "¿Los precios incluyen impuestos?",
      "sub.faq.a5": "Sí. Los precios están en euros e incluyen el IVA español del 21%. No se añade nada al finalizar la compra.",
      "sub.faq.q6": "¿Qué pasa con mis datos si cancelo?",
      "sub.faq.a6": "Se quedan. Vuelves al plan gratuito y conservas tu diario, tu histórico de peso y todo lo que hayas registrado: simplemente vuelves a tener 3 escaneos con IA al día. No se borra nada por dejar de pagar.",
      "sub.faq.q7": "¿Puedo cambiar de plan?",
      "sub.faq.a7": "Sí, desde Google Play, en la misma pantalla de Suscripciones donde se cancela. Google se encarga del prorrateo cuando cambias.",
      "sub.faq.q8": "¿Cómo cancelo?",
      "sub.faq.a8": "En la app de Play Store: tu icono de perfil → Pagos y suscripciones → Suscripciones → Fotocal → Cancelar suscripción. Mantienes Premium hasta que se agote el periodo que has pagado.",

      "sub.cta.title": "Empieza gratis. <em class=\"accent-light\">Paga si se lo gana</em>.",
      "sub.cta.sub": "Descarga Fotocal, úsalo gratis todo el tiempo que quieras y pasa a Premium solo cuando el límite diario de escaneos sea lo que te está estorbando.",

      /* ─────────────────────────────────────────────
         BLOG
         ───────────────────────────────────────────── */
      "blog.meta.title": "Blog — Fotocal",
      "blog.kicker": "Blog",
      "blog.title": "Apuntes sobre comer, <em class=\"accent\">con honestidad</em>.",
      "blog.lead": "Aquí escribiremos sobre nutrición, peso y los hábitos que sostienen todo lo demás: la parte práctica y poco glamurosa de comer mejor que casi todo internet se salta de camino a venderte algo.",
      "blog.lead2": "Todavía no hay nada publicado. Antes que rellenar esta página con paja, preferimos dejarla honesta y empezarla como toca.",

      "blog.topics.kicker": "Sobre qué escribiremos",
      "blog.topics.title": "Tres temas, <em class=\"accent\">bien tratados</em>.",
      "blog.topics.sub": "No es un calendario de contenidos persiguiendo tráfico. Son las tres áreas sobre las que está construido Fotocal, y sobre las que merece la pena escribir algo útil.",

      "blog.t1.t": "Nutrición",
      "blog.t1.b": "Qué hacen realmente los macros, por qué las calorías de una etiqueta también son estimaciones, cómo leer una ración y dónde el consejo popular simplifica de más. La idea es que termines un artículo entendiendo algo, no simplemente creyéndonos.",
      "blog.t1.li1": "Cómo funcionan las estimaciones y dónde están sus límites",
      "blog.t1.li2": "Proteínas, carbohidratos y grasas sin dogmas",
      "blog.t1.li3": "Leer etiquetas y raciones en la vida real",

      "blog.t2.t": "Pérdida de peso",
      "blog.t2.b": "Perder peso de una forma que sobreviva al contacto con una vida normal: estancamientos, retención de líquidos, por qué la báscula miente a diario y por qué los enfoques que funcionan despacio son los que siguen funcionando dentro de un año. Sin antes y después, sin planes exprés.",
      "blog.t2.li1": "Por qué el peso diario oscila y qué mirar en su lugar",
      "blog.t2.li2": "Los estancamientos y qué está pasando de verdad",
      "blog.t2.li3": "Lo sostenible gana a lo rápido, y por qué",

      "blog.t3.t": "Hábitos y mentalidad",
      "blog.t3.b": "La parte que lo decide todo y sobre la que menos se escribe. Cómo se forma de verdad un hábito, por qué el registro se cae en la tercera semana, qué hacer después de una mala semana y cómo lograr que comer bien cueste menos fuerza de voluntad en vez de más.",
      "blog.t3.li1": "Por qué el registro suele parar en la tercera semana",
      "blog.t3.li2": "Volver después de una mala semana, sin culpa",
      "blog.t3.li3": "Que la opción buena sea la opción fácil",

      "blog.empty.h": "Todavía no hay artículos",
      "blog.empty.b": "El primer artículo aún no está escrito. Cuando empiecen a publicarse aparecerán aquí; hasta entonces, esta página no va a fingir lo contrario.",
      "blog.empty.cta1": "Seguir en Instagram",
      "blog.empty.cta2": "Descargar la app",
      "blog.empty.note": "En Instagram es donde se publica todo primero, así que es el mejor sitio para pillar el primer artículo.",

      "blog.demo.kicker": "Vista previa del diseño",
      "blog.demo.title": "Cómo se <em class=\"accent\">verá un artículo</em>.",
      "blog.demo.sub": "La tarjeta de abajo es un ejemplo de maquetación para que el diseño esté listo en cuanto haya algo que publicar. No es un artículo, no está escrito y no lleva a ninguna parte.",
      "blog.demo.ribbon": "Ejemplo de maquetación — no es un artículo real",
      "blog.demo.tag": "Ejemplo",
      "blog.demo.h": "Aquí irá el título del artículo",
      "blog.demo.b": "Y esta es la línea de resumen: dos o tres frases explicando de qué va el artículo, para que puedas decidir desde la tarjeta si merece tu tiempo. El artículo de verdad tendrá un título real, una fecha real y un enlace real.",
      "blog.demo.meta": "Aquí irá la fecha",
      "blog.demo.read": "5 min de lectura",

      "blog.cta.title": "La app <em class=\"accent-light\">ya está escrita</em>, aunque el blog no.",
      "blog.cta.sub": "Fotocal está en Google Play ahora mismo. Los artículos vendrán después.",

      /* ─────────────────────────────────────────────
         SOBRE NOSOTROS
         ───────────────────────────────────────────── */
      "about.meta.title": "Sobre nosotros — Fotocal",
      "about.kicker": "Sobre nosotros",
      "about.title": "Queremos que <em class=\"accent\">veas lo que comes</em>, mientras lo comes.",
      "about.lead": "Fotocal es una app independiente, hecha en pequeño. Sin inversores, sin departamento de marketing, sin objetivos de crecimiento. Solo un registro de nutrición construido como creíamos que debía funcionar.",
      "about.lead2": "Esta página va de por qué existe y de lo que creemos. A propósito tiene poca biografía y mucha intención.",

      "about.story.kicker": "Por qué existe Fotocal",
      "about.story.title": "Casi nadie llega a <em class=\"accent\">ver</em> su propia alimentación.",
      "about.story.p1": "Esto es lo que lo empezó todo. Casi todo el mundo come tres o más veces al día, todos los días, toda su vida, y casi nadie tiene una idea real de a qué suma todo eso. No porque no le importe. Porque mirarlo siempre ha costado demasiado trabajo.",
      "about.story.p2": "La forma tradicional de averiguarlo consiste en esperar a una cita y luego sentarte en una consulta intentando recordar qué comiste el martes pasado. Y no te acuerdas. Nadie se acuerda. Así que lo reconstruyes, más o menos, y recibes consejos basados en una reconstrucción aproximada, y luego esperas meses y lo repites. No es que el consejo esté mal: es que la foto sobre la que se apoya es una suposición.",
      "about.story.p3": "Mientras tanto, lo que más ayudaría es algo que podrías haber tenido desde el principio: ver lo que comes mientras lo comes. Sin recordarlo. Sin estimarlo semanas después. Simplemente ahí, delante de ti, el mismo día que pasó.",
      "about.story.pull": "Queremos que la gente pueda ver su propia alimentación en tiempo real, y ver cómo ocurre su propia transformación, en vez de que sea invisible hasta que otra persona se la señala.",
      "about.story.p4": "Esa es toda la idea. No es una dieta. No es un plan que nos hayamos inventado y queramos que sigas. Es visibilidad: la clase de visibilidad corriente y cotidiana que convierte el \"creo que como bastante bien\" en algo que de verdad sabes.",

      "about.mission.kicker": "La misión",
      "about.mission.title": "Que entender lo que comes <em class=\"accent\">no cueste esfuerzo</em>.",
      "about.mission.p1": "Si registrar cuesta, lo dejas. Eso no es un defecto de carácter, es aritmética: cualquier cosa que tengas que hacer tres veces al día tiene que salir casi gratis o no aguantará el mes. Todas las apps que te obligaban a buscar en una base de datos, encontrar tu comida, adivinar la ración y confirmarla te estaban pidiendo unos minutos al día, y unos minutos al día es más de lo que casi nadie va a pagar.",
      "about.mission.p2": "Así que el objetivo era que costara una foto. Apuntas la cámara al plato y el trabajo pasa a nuestro lado en vez del tuyo. Eso no es un truco: es la única versión del registro que hemos visto que la gente sigue haciendo al tercer mes, porque es la única lo bastante barata como para seguir haciéndola.",
      "about.mission.p3": "Todo lo demás sale de ahí. Offline-first, porque comes en sitios sin cobertura y un registro que falla en un restaurante no es un registro. Coach Kal gratis e ilimitado, porque la parte que más probablemente cambie cómo comes no debería ser la parte por la que hay que pagar. El progreso mostrado como tendencia y no como número diario, porque una mañana suelta en la báscula no significa nada y agobiarse con ella no ayuda a nadie.",

      "about.empower.kicker": "Tus datos, tu comprensión",
      "about.empower.title": "El conocimiento en <em class=\"accent\">tus propias manos</em>, cada día.",
      "about.empower.p1": "Hay una diferencia real entre que te cuenten cómo comes y verlo. Que te lo cuenten es algo que te pasa de vez en cuando. Verlo es algo que es tuyo, cada día, y cambia lo que haces a continuación sin que nadie tenga que decirte nada.",
      "about.empower.p2": "Eso es lo que queremos que te dé Fotocal. No instrucciones. Visibilidad. Registras una semana y la foto aparece sola: de dónde salen las calorías de verdad, qué días se sostienen, qué pinta tiene tu proteína cuando no es una suposición. A casi todo el mundo le sorprende la respuesta, y que sorprenda es útil. No puedes cambiar un patrón que no ves.",
      "about.empower.p3": "Y la transformación también se vuelve visible, que importa más de lo que parece. El progreso es lento y desde dentro es casi invisible: no notas el cambio en un espejo que miras a diario. Las tendencias de peso, las medidas, los macros, las rachas: hacen legible lo lento. Esa es la diferencia entre un mes que pareció inútil y un mes que ves que funcionó.",

      "about.comp.h": "Fotocal trabaja con tu médico, no en su lugar",
      "about.comp.b": "Queremos ser muy claros con esto, porque importa. Fotocal no sustituye la atención profesional y no está diseñado para ayudarte a evitarla. Más bien al contrario: lo más útil de tener tus datos reales de alimentación es que puedes entrar en una consulta con ellos.",
      "about.comp.b2": "En vez de intentar recordar el martes pasado, puedes enseñar cómo han sido de verdad los últimos tres meses. Un médico o un dietista-nutricionista que trabaja con datos reales puede darte consejos muchísimo mejores que uno que trabaja con tu mejor suposición: eso es una conversación mejor, no una consulta que te saltas. Si tienes una preocupación de salud, ve a que te vea alguien. Y llévate tus datos.",

      "about.values.kicker": "Lo que creemos",
      "about.values.title": "Las normas que <em class=\"accent\">nos aplicamos</em>.",
      "about.values.sub": "No es un póster de oficina. Son las decisiones que de verdad han determinado cómo se construyó la app, incluidas las que nos han costado algo.",

      "about.v1.t": "Sin esfuerzo, o no cuenta",
      "about.v1.b": "Si una función añade fricción al registrar una comida, está mal, por muy ingeniosa que sea. Registrar tiene que seguir siendo lo bastante barato como para hacerlo siempre, o no se hará nunca.",
      "about.v2.t": "Nunca culpabilizar",
      "about.v2.b": "Sin números en rojo, sin culpa, sin una app decepcionada contigo. Te has comido un postre. Es un postre. La culpa no ha hecho nunca que nadie coma mejor, y hace que mucha gente deje de registrar, que es peor.",
      "about.v3.t": "Honestos sobre la IA",
      "about.v3.b": "El análisis por foto da una estimación, no un resultado de laboratorio. Los guisos, los platos mezclados y todo lo que va bajo una salsa son difíciles de verdad. Lo decimos, y puedes corregir cualquier escaneo antes de guardarlo.",
      "about.v4.t": "Sin promesas que no podamos cumplir",
      "about.v4.b": "No te vamos a decir que perderás una cantidad concreta en un tiempo concreto. Nadie honesto puede. Fotocal te enseña lo que estás haciendo; lo que pase después depende de muchas cosas que no son una app.",
      "about.v5.t": "Funciona en cualquier sitio",
      "about.v5.b": "Offline-first, a propósito. Comes en sótanos, en aviones y en sitios sin una raya de cobertura, y un registro que solo funciona con buen wifi no es un registro.",
      "about.v6.t": "Tus datos son tuyos",
      "about.v6.b": "No los vendemos. Puedes eliminar tu cuenta y todo lo que contiene cuando quieras, y es una opción normal dentro de la app, no un formulario que hay que suplicar.",

      "about.small.kicker": "Quién está detrás",
      "about.small.title": "Pequeños, independientes <em class=\"accent\">y honestos al decirlo</em>.",
      "about.small.p1": "Fotocal se construye y se mantiene de forma independiente, por un equipo muy pequeño. No hay oficina, no hay inversores y no hay departamento de crecimiento. Preferimos decirlo claro antes que inventarnos una historia fundacional con un número grande dentro.",
      "about.small.p2": "Eso tiene desventajas reales. Vamos más despacio que una empresa con cincuenta ingenieros. Hay cosas que quizá quieras y que todavía no están hechas. Pero también significa que nadie nos está empujando a añadir un patrón oscuro para cuadrar un número trimestral, y que cuando escribes a soporte, llega a la gente que hizo esto.",
      "about.small.p3": "Habrás notado que en esta página no hay número de usuarios, ni valoraciones, ni citas de prensa, ni premios. No es modestia: es que no vamos a inventarnos ninguno, y no creemos que debas fiarte de una web que lo hace.",

      "about.med.h": "Un apunte rápido",
      "about.med.b": "Fotocal es una herramienta de registro, no consejo médico. No diagnostica nada y no es un tratamiento. Si tienes alguna condición de salud, estás embarazada, estás gestionando un trastorno de la conducta alimentaria, o simplemente no sabes si un cambio es adecuado para ti, habla antes con un médico o con un dietista-nutricionista colegiado. Y llévate tus datos de Fotocal: harán que esa conversación sea mejor.",

      "about.next.contact": "Contacto",
      "about.next.contactB": "Dudas, sugerencias o lo que sea",
      "about.next.privacy": "Política de Privacidad",
      "about.next.privacyB": "Exactamente qué hacemos con tus datos",

      "about.cta.title": "Empieza a ver lo que comes, <em class=\"accent-light\">desde hoy</em>.",
      "about.cta.sub": "Fotocal se descarga gratis y se usa gratis. Una foto es todo lo que hace falta para empezar.",

      /* ─────────────────────────────────────────────
         CONTACTO
         ───────────────────────────────────────────── */
      "contact.meta.title": "Contacto — Fotocal",
      "contact.kicker": "Contacto",
      "contact.title": "Habla con <em class=\"accent\">una persona de verdad</em>.",
      "contact.lead": "Una dirección de correo, leída por la gente que hizo la app. Sin número de ticket, sin chatbot, sin niveles de soporte por los que ir escalando.",
      "contact.lead2": "Elige abajo lo que te encaje: lo único que hace es rellenar el asunto para que encontremos tu correo más rápido.",
      "contact.mailLabel": "Escríbenos a",

      "contact.routes.kicker": "¿De qué se trata?",
      "contact.routes.title": "Tres vías. <em class=\"accent\">La misma bandeja</em>.",
      "contact.routes.sub": "Las tres van a la misma dirección. El asunto solo nos dice qué tenemos delante antes de abrirlo.",

      "contact.r1.t": "Soporte y ayuda",
      "contact.r1.b": "Algo no funciona, un escaneo se comporta raro, te has atascado o tienes una duda sobre tu suscripción o un cobro. Esta es la vía para casi todo.",
      "contact.r1.li1": "Errores y cierres inesperados",
      "contact.r1.li2": "Escaneos, Coach Kal, sincronización",
      "contact.r1.li3": "Suscripciones y cobros",
      "contact.r1.cta": "Escribir a soporte",

      "contact.r2.t": "Privacidad y tus datos",
      "contact.r2.b": "Cualquier cosa sobre qué guardamos, cómo lo usamos o cómo borrarlo. Si quieres que tu cuenta y tus datos desaparezcan, la app lo hace en un par de toques, pero también puedes pedírnoslo sin más.",
      "contact.r2.li1": "Acceso y eliminación de datos",
      "contact.r2.li2": "Dudas sobre la Política de Privacidad",
      "contact.r2.li3": "Cómo se trata tu información",
      "contact.r2.cta": "Escribir sobre privacidad",

      "contact.r3.t": "Negocio y prensa",
      "contact.r3.b": "Colaboraciones, prensa o cualquier cosa comercial. Somos pequeños e independientes, así que esto lo leemos nosotros, y te diremos claramente si no encaja.",
      "contact.r3.li1": "Colaboraciones y acuerdos",
      "contact.r3.li2": "Prensa y medios",
      "contact.r3.li3": "Cualquier asunto comercial",
      "contact.r3.cta": "Escribir sobre negocio",

      "contact.help.kicker": "Cómo obtener una buena respuesta antes",
      "contact.help.title": "Qué <em class=\"accent\">poner en el correo</em>.",
      "contact.help.p1": "Nada de esto es obligatorio: mándanos un correo de una línea si es lo que tienes y te responderemos igual. Pero si algo no funciona, estos son los datos que suelen decidir si lo arreglamos en una respuesta o tenemos que gastar tres correos preguntándote cosas.",
      "contact.help.s1": "<b>Tu móvil y tu versión de Android.</b> Ajustes → Información del teléfono. Un número sorprendente de errores solo ocurre en la versión de un fabricante.",
      "contact.help.s2": "<b>Qué estabas haciendo.</b> En qué pantalla estabas y qué fue lo último que tocaste antes de que fallara.",
      "contact.help.s3": "<b>Una captura de pantalla.</b> Vale aproximadamente por una página de explicación, sobre todo si es algo visual o un escaneo que ha salido raro.",
      "contact.help.s4": "<b>El correo de tu cuenta</b>, si es una duda de suscripción o de cuenta; si no, no podemos encontrarte.",
      "contact.help.p2": "Si un escaneo se ha equivocado, la foto original ayuda muchísimo. Es la única forma de saber si el modelo leyó mal la comida o la ración.",

      "contact.exp.h": "Cuándo tendrás respuesta",
      "contact.exp.b": "Intentamos responder en unos pocos días. Fotocal lo lleva un equipo pequeño e independiente, así que esto es un compromiso sincero y no una garantía de servicio: preferimos decírtelo antes que prometer un plazo que quizá no cumplamos. Todos los correos se leen, y si alguno lleva más de una semana sin respuesta, vuelve a mandarlo sin más. Será un despiste, no una decisión.",

      "contact.quick.kicker": "Antes de escribir",
      "contact.quick.title": "Tres cosas con <em class=\"accent\">respuesta inmediata</em>.",
      "contact.quick.sub": "Son las tres que más nos preguntan, y las tres se hacen antes de lo que se tarda en escribir un correo.",

      "contact.q1.t": "Cancelar tu suscripción",
      "contact.q1.b": "No podemos cancelarla por ti: el vendedor es Google Play, así que tiene que hacerse allí. Play Store → tu icono de perfil → Pagos y suscripciones → Suscripciones → Fotocal → Cancelar. Mantienes Premium hasta que acabe el periodo que has pagado.",
      "contact.q1.cta": "Más sobre cobros",
      "contact.q2.t": "Eliminar tu cuenta",
      "contact.q2.b": "Puedes hacerlo tú mismo desde la app, y elimina tus datos. Los pasos están en nuestra página de eliminación de cuenta, y si lo prefieres puedes escribirnos.",
      "contact.q2.cta": "Eliminación de cuenta",
      "contact.q3.t": "Qué hacemos con tus datos",
      "contact.q3.b": "La Política de Privacidad cubre qué se guarda, por qué y cómo deshacerse de ello. Si no responde a tu duda, eso es un hueco en la política y nos gustaría saberlo.",
      "contact.q3.cta": "Política de Privacidad",

      "contact.cta.title": "Preferimos oírlo <em class=\"accent-light\">a no oírlo</em>.",
      "contact.cta.sub": "Errores, confusión, críticas sin filtro o una idea de algo que Fotocal debería hacer: todo ayuda y todo se lee.",
      "contact.cta.btn": "Escríbenos un correo"
    }
  };

  /* ── Merge into the shared dictionary ──
     Additive by design: existing keys from i18n.js are never overwritten
     here, and if i18n.js has not loaded (or a language block is missing)
     we create it rather than throwing. */
  var ROOT = window.FOTOCAL_I18N = window.FOTOCAL_I18N || {};

  Object.keys(PAGES).forEach(function (lang) {
    ROOT[lang] = ROOT[lang] || {};
    var from = PAGES[lang];
    Object.keys(from).forEach(function (key) {
      ROOT[lang][key] = from[key];
    });
  });
})();
