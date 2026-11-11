# -*- coding: utf-8 -*-
"""Prices and the limited offer, from tools/pricing.json (the single source).

Sources never contain a price. They contain tokens, and tools/build_site.py
resolves them for each language tree on every build, by today's date in
Europe/Madrid:

  {{price:month}}        6,99 €        / €6.99
  {{price:year}}         the yearly price in force today (offer or list)
  {{price:year_list}}    34,99 €       / €34.99   (the price outside any offer)
  {{price:year_month}}   yearly ÷ 12:  1,67 €   / €1.67
  {{price:year_saving}}  % less than 12 monthly payments: 76
  {{price:month_num}} {{price:year_num}}   6.99 / 19.99 (structured data)
  {{offer:note}}         " (oferta hasta el 31 de diciembre de 2026; después, 34,99 € al año)" or ""
  {{offer:badge}}        "Oferta: Premium anual a 19,99 € (antes 34,99 €) · solo hasta el 31 de diciembre" or ""
  {{offer:schema}}       , "priceValidUntil": "2026-12-31"   or ""   (inside an Offer object)
  <!--offer-->…<!--/offer-->   kept while the offer runs, removed with its content afterwards

FOTOCAL_TODAY=YYYY-MM-DD overrides today's date (tests, previews).
"""
import datetime, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = json.load(open(os.path.join(ROOT, "tools", "pricing.json"), encoding="utf-8"))
MONTHS = {"es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
          "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]}


def today():
    env = os.environ.get("FOTOCAL_TODAY")
    if env:
        return datetime.date.fromisoformat(env)
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo("Europe/Madrid")).date()
    except Exception:
        return (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).date()


def offer_active(day=None):
    o = P.get("offer")
    return bool(o and o.get("yearly") and o.get("ends") and (day or today()) <= datetime.date.fromisoformat(o["ends"]))


def yearly(day=None):
    return P["offer"]["yearly"] if offer_active(day) else P["yearly_list"]


def money(v, lang):
    s = "%.2f" % v
    return s.replace(".", ",") + " €" if lang == "es" else "€" + s


def tokens(lang, day=None):
    y, on = yearly(day), offer_active(day)
    t = {"price:month": money(P["monthly"], lang), "price:year": money(y, lang), "price:year_list": money(P["yearly_list"], lang),
         "price:year_month": money(round(y / 12 + 1e-9, 2), lang), "price:year_saving": "%d" % round(100 * (1 - y / (P["monthly"] * 12))),
         "price:month_num": "%.2f" % P["monthly"], "price:year_num": "%.2f" % y,
         "offer:note": "", "offer:badge": "", "offer:schema": "", "offer:until": ""}
    if on:
        e = datetime.date.fromisoformat(P["offer"]["ends"])
        was, now = money(P["yearly_list"], lang), money(y, lang)
        if lang == "es":
            until = "%d de %s" % (e.day, MONTHS["es"][e.month - 1])
            t["offer:until"] = "%s de %d" % (until, e.year)
            t["offer:note"] = " (oferta hasta el %s de %d; después, %s al año)" % (until, e.year, was)
            t["offer:badge"] = "Oferta: Premium anual a %s (antes %s) · solo hasta el %s" % (now, was, until)
        else:
            until = "%d %s" % (e.day, MONTHS["en"][e.month - 1])
            t["offer:until"] = "%s %d" % (until, e.year)
            t["offer:note"] = " (offer until %s %d; after that, %s a year)" % (until, e.year, was)
            t["offer:badge"] = "Offer: yearly Premium %s (was %s) · only until %s" % (now, was, until)
        t["offer:schema"] = ', "priceValidUntil": "%s"' % P["offer"]["ends"]
    return t


TOKEN = re.compile(r"\{\{((?:price|offer):[a-z_]+)\}\}")
BLOCK = re.compile(r"<!--offer-->(.*?)<!--/offer-->", re.S)


def resolve(text, lang, day=None):
    t = tokens(lang, day)
    text = BLOCK.sub((lambda m: m.group(1)) if offer_active(day) else "", text)

    def rep(m):
        if m.group(1) not in t:
            raise SystemExit("unknown price token {{%s}}" % m.group(1))
        return t[m.group(1)]
    return TOKEN.sub(rep, text)


if __name__ == "__main__":
    for lang in ("es", "en"):
        print(lang, tokens(lang))
