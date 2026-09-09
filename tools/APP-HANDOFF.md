# Fotocal app — items found during website work
Source: fotocal/fotocal @ 6c265aa, read 2026-09-09. Hand to the app batch as-is.

1. voice-food.tsx header comment says "FREE feature, never premium-gated".
   Wrong. Product rule (owner, 2026-09-09): 1 voice log/day free, unlimited
   on Premium. Coach Kal's system prompt and the paywall are right; only the
   comment is wrong.

2. paywall.tsx rotator line "No ads · more features" (i18n paywall.rotator.5,
   EN and ES). The app ships no ad SDK — nobody sees ads. Phantom benefit;
   remove the line.

3. supabase/functions/coach-chat/index.ts — the PREMIUM vs FREE line of the
   system prompt (~line 538) still says free scans are "2 AI scans/day
   (photo or recipe)". Recipe mode is off (RECIPE_MODE_ENABLED = false);
   drop "or recipe".

4. coach-chat edge function redeploy. app/coach.tsx notes the server's 5/day
   coach cap "is removed too, but the Edge Function must be REDEPLOYED for
   the change to take effect". Confirm it has been redeployed — the website
   promises unlimited Coach Kal on the free plan.

5. scan-result.tsx ~line 739 comment: "the comment said 3; FREE_DAILY_LIMIT
   in scan-food is 2". The code is right (2); tidy the comment.

6. Number formatting in English: the EN home screen shows "2.499" for two
   thousand four hundred and ninety-nine (capture 2026-09-09). English
   expects "2,499"; the dot reads as a decimal.

7. DEFECT — scan → Coach Kal handoff composes the question in English when
   the app language is Spanish (observed 2026-08-31). Reply language is
   correct, so detection is fine; consistent with an untranslated key on
   the prompt template.

8. DEFECT — Kal's Spanish replies get calorie arithmetic wrong (2026-08-31).
   Same data both languages, 905 kcal bowl vs 663 kcal remaining:
     EN: "it will put you over, leaving you with -242 kcal" — correct.
     ES: "905 kcal … encaja bien con tus 663 kcal restantes" — wrong by 242.
   A second ES sample called the 2 075 kcal daily GOAL "tus calorías
   restantes". 2/2 Spanish wrong, 2/2 English right — suspect the Spanish
   prompt template around numeric context, not the model's maths.
